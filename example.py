from contactscraper.controller import Controller


instance = Controller(starting_urls=['https://losangeles.craigslist.org/d/apts-housing-for-rent/search/apa'], 
                       scrape_numbers=True,
                       scrape_emails=True,
                       region="US",
                       max_results=10)

instance.scrape()




import json
import pprint as pprint



with open('output.json', 'r') as raw_output:
    data = raw_output.read()
    output = json.loads(data)

print(json.dumps(output, indent=2))
