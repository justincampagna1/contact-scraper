from scrapy.utils.project import get_project_settings
import scrapy
import re
import logging

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from scrapy.exceptions import CloseSpider
from contactscraper.spiders.contactspider import ContactSpider
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
import os
from datetime import datetime, timezone, timedelta
import sys
import tldextract

class Controller:
    def __init__(self, starting_urls, scrape_numbers=True, scrape_emails=True, region="US", max_results=False):
        
        #Init logging
        start_time = datetime.now().timestamp()
        logging.basicConfig(filename=f'.\logs\{start_time}.log',level=logging.INFO)
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

        #Init project with scrapy settings
        self.settings = Settings()
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'contactscraper.settings'
        settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
        self.settings.setmodule(settings_module_path, priority='project')

        #Init instance variables
        self.starting_urls = starting_urls
        self.scrape_numbers = scrape_numbers
        self.scrape_emails = scrape_emails
        self.region = region
        self.max_results = max_results
    
        logging.info("Controller initilized...")
        

    def scrape(self):
        '''
        * * * * *
        * Linearly spins up instances of MailSpider for each tld in tld_documents
        * This function ensures atomicity between MailSpiders by spinning up a Twisted Reactor and using deferred callbacks.
        *
        * see: https://twistedmatrix.com/documents/current/api/twisted.internet.reactor.html
        * and: https://twistedmatrix.com/documents/current/api/twisted.internet.defer.inlineCallbacks.html
        * * * * *
        * @param List<Tld> tld_documents : a list of Tld documents
        * @param Bool call_controller : used to indicate the call was made by the controller, and after we've finished scanning all the tlds we should go back to the controller
        * @return void
        * * * * *
        '''
        # #Instiate an instance of the CrawlerRunner class from scrapy
        runner = CrawlerRunner(self.settings)

        # #Relinquish ContentCops control of stdout | log files will continue to write
        configure_logging()



        @defer.inlineCallbacks
        def crawl(starting_urls):
            #using our CrawlerRunner, instiate a new mail_spider for each tld
            #see MailSpider.py for the actual spider that's running inside CrawlerRunner
            for starting_url in starting_urls:
                ext = tldextract.extract(starting_url)
                root = '.'.join(ext[2:])
                try:
                    
                    yield runner.crawl(ContactSpider, 
                                        root=root, 
                                        region=self.region,
                                        scrape_emails=self.scrape_emails,
                                        scrape_numbers=self.scrape_numbers,
                                        start_urls=[starting_url], 
                                        allowed_domains=[root],
                                        max_results=self.max_results
                                        )                   
                except Exception as e:
                    logging.warning(f"FATAL: NEW MAIL-SPIDER FAILED TO LAUNCH\n\t{str(e)}")
            reactor.stop()
        
        #Start recursively spinning up spiders
        crawl(self.starting_urls)
        
        # Start a Twisted Reactor, 
        # this will lock all threads until the last call to crawl is finished
        reactor.run() 
