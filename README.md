## **contact-scraper**

contact-scraper gathers and validates all available phone numbers and emails from a given domain by recursively travesing and scraping the entire site-map. Built upon Scrapy.

## **Installation**
1. `git clone git@github.com:enjoys-sashimi/contact-scraper.git`
2. `cd contact-scraper`
3. `pip install -r requirements.txt`

## **Usage**
For quick startup edit/run example.py


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
Reults get written as a list of JSON objects in output.json

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
- Phone numbers are validated by [region](https://github.com/daviddrysdale/python-phonenumbers/tree/dev/python/phonenumbers/shortdata "region") using the [Python implementation](https://github.com/daviddrysdale/python-phonenumbers "Python implementation") of [Google\'s libphonenumber library](https://github.com/google/libphonenumber)

## **Custom integration**
If you\'d like contact-scraper implemented into an existing system, please contact me.
