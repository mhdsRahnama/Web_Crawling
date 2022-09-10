"""
Extracting all urls and domains from google search result pages
"""

import scrapy
import re
import pandas
import csv
from urllib.parse import urlparse, parse_qs
import validators

###### Running ##########
#scrapy runspider web_scraping.py -o output.csv
################

class QuotesSpider(scrapy.Spider):
    
    name = "quotes"
    query="پایتون" 
    start_urls = ["https://www.google.com/search?q="+query]
    next_depth=0 ### Counter of next page
    max_depth=3 #### Number of next page

    def parse(self, response):
        
        #### You can save the html content #############
        # filename = response.url.split("/")[-2] + '.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        #################################################

        if self.next_depth<self.max_depth:

            next=response.css("a[aria-label='Next page']::attr(href)").extract_first()
            nextpage = "https://www.google.com/search?q="+next.split("/search?q=")[-1]
            yield scrapy.Request(nextpage)
            self.next_depth+=1
    
        links=response.xpath('//a/@href').extract()

        for url in links:
            if url.startswith("/url?"):
                url = parse_qs(urlparse(url).query)['q']
           
            if validators.url(url[0]):
                domain = (urlparse(url[0]).netloc)
                if domain.startswith("www."):  ## It must be checked because the string may contain "www.".
                    domain = domain.split("www.")[1]
                    
                yield {"url":url[0],
                       "domain":domain
                       }
   
