"""
Extracting all URLs and domains from google search result pages. It is appropriate for gathering data.
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
    max_depth=3 #### Number of next pages

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
            """
            If you want parse each pages, comment part 2. 
            Write your function in page_parser method.
            """
            ##################### Part 1 #########################
            # yield scrapy.Request(url[0], callback=self.page_parser)
            ######################################################
            
            """
            If you want collect all pages's url, without parsing pages, comment part 1.
            """
            ##################### Part 2 #########################
            if url.startswith("/url?"):
                url = parse_qs(urlparse(url).query)['q']
            # print(url[0])
            if validators.url(url[0]):
                domain = (urlparse(url[0]).netloc)
                if domain.startswith("www."):  ## It must be checked because the string may contain "www.".
                    domain = domain.split("www.")[1]
                yield {"url":url[0],
                       "domain":domain
                       }
            ######################################################


    def page_parser(self, response):
        """
        In this fuction, you can write your code for parsing each pages.     
        """
   
