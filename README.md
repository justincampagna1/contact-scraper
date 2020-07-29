[![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen)]() [![Contributions](https://img.shields.io/badge/Contributions-Welcome-blue)]() [![Release](https://img.shields.io/badge/Release-Stable-green)]() [![Maintained](https://img.shields.io/badge/Maintenance-Active-brightgreen)]() 
# contact-scraper 

contact-scraper gathers and validates all available phone numbers and emails from a given domain by recursively travesing and scraping the entire site-map. Built upon Scrapy.

## **Disclaimer**
This tool is for educational and/or legal scraping purposes only, usage of contact-scraper for scraping targets without prior mutual consent is illegal. Developers of contact-scraper and its dependencies assume no liability and are not responsible for any misuse or damage caused by this program.

## **Installation**
1. `git clone git@github.com:enjoys-sashimi/contact-scraper.git`
2. `cd contact-scraper`
3. `pip install -r requirements.txt`


## **Usage**
***For quick startup edit/run [example.py](https://github.com/enjoys-sashimi/contact-scraper/blob/master/example.py)***


#### Scan a URL

```python
from contactscraper.controller import Controller

instance = Controller(starting_urls=['https://www.python.org/'], 
                       scrape_numbers=True,
                       scrape_emails=True,
                       region="US",
                       max_results=2)

instance.scrape()
```
`starting_urls` is a list of URLs you\'d like to start scraping from. A spider will be deployed on each URL, it won\'t deviate to any links that don\'t contain the root url. For example, passing in `['https://www.python.org/privacy/']` will allow any URL with the root domain of `python.org` to be scraped.

`scrape_emails` & `scrape_numbers` are both booleans depicting if you want to gather emails or numbers, respectively.

`region` is the region you wish to validate numbers against, most of NA uses "US" region validation.

`max_results` is the maximum number of unique URLs that contain either emails or phone numbers you\'d like to receive.

Results get written as a list of JSON objects in output.json

#### Print Results
```python
import json

with open('output.json', 'r') as raw_output:
    data = raw_output.read()
    output = json.loads(data)

print(json.dumps(output, indent=2))
```
Json objects are stored in the following format
```python
[
  {
    "url": "https://www.python.org/privacy/",
    "emails": [
      "psf@python.org"
    ],
    "numbers": []
  },
  {
    "url": "https://status.python.org/",
    "emails": [],
    "numbers": [
      "+16505551234"
    ]
  }
 ]
```
## **Validation**
- Emails are validated against modern specs with the [email_validator library](https://github.com/JoshData/python-email-validator "email_validator library")
- Phone numbers are validated by [region](https://github.com/daviddrysdale/python-phonenumbers/tree/dev/python/phonenumbers/shortdata "region") using the [Python implementation](https://github.com/daviddrysdale/python-phonenumbers "Python implementation") of [Google\'s libphonenumber library](https://github.com/google/libphonenumber "Google\'s libphonenumber library")


## **Custom integration**
If you\'d like contact-scraper implemented into an existing system, please [contact me](https://github.com/enjoys-sashimi "contact me").
