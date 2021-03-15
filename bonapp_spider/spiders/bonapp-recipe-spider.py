from scrapy import Spider, Request
from bonapp_spider.items import BonappItem
import re
import time
import pandas as pd
from math import ceil
import re


class BonappSpider(Spider):
    name = "bonapp_recipe_spider"
    allowed_domains = ['www.bonappetit.com']
    start_urls = ['https://www.bonappetit.com/search/?content=recipe&issueDate=2014-01-01']

    def parse(self, response):

        ## Breaks starting search page into urls per month in date range

        timespan = pd.date_range(start='2014-01-01', end='2021-02-01', freq='MS') # change this if i want more years
        urls_bymonth = [f'https://www.bonappetit.com/search/?content=recipe&issueDate={date}-01' for date in
                        timespan.strftime('%Y-%m')]
        for url in urls_bymonth:
            yield Request(url=url, callback=self.parse_monthly_urls)

    def parse_monthly_urls(self, response):

        ## Gathers number of recipe results to parse into total number of search pages

        results_num = response.xpath('//span[@class="matching-count"]/text()').extract_first()
        urls_pagecount = ceil(int(results_num) / 18)
        addt_gallery_pages = [f'{response.url}&page={i}' for i in range(1, urls_pagecount + 1)]

        for url in addt_gallery_pages:
            yield Request(url=url, callback=self.parse_gallery_page)

    def parse_gallery_page(self, response):

        ## Scrapes result page for recipe links

        recipe_xpaths = response.xpath('//a[@class="photo-link"]')
        recipe_links = [f'https://www.bonappetit.com{lnk}' for lnk in recipe_xpaths.xpath('.//@href').extract()]
        for url in recipe_links:
            yield Request(url=url, callback=self.parse_recipe_page)

    def parse_recipe_page(self, response):

        title = response.xpath('//head//title/text()').get().split(' Recipe', 1)[0]

        author = response.xpath('//head//meta[@name="author"]//@content').get()

        date = response.xpath(
            '//div//time/text()').get()  # this is not present in all types of recipes so add if else statement

        ## Some recipe pages (e.g. from Basically) have a different format
        if response.xpath('//div[@data-testid="IngredientList"]'):
            ingredients = response.xpath(
                '//div[@data-testid="IngredientList"]//div/descendant-or-self::*/text()').extract()
        else:
            ## Some ingredients have hyperlinked words for brands, the following navigates that possibility
            ingredients = []
            ingred_bin = response.xpath('//div[@class="ingredients__text"]')
            for ingred in ingred_bin:
                if ingred.xpath('./a'):
                    ingredients.append(''.join(ingred.xpath('.//descendant-or-self::*/text()').extract()))
                else:
                    ingredients.append(ingred.xpath('./text()').extract()[0])

        ## Some recipes have no reviews/ratings so the following code accounts for it
        # identifies recipe pages with reviews by looking for the div class with id=reviews
        if response.xpath('//div[@id="reviews"]'):
            review_header = response.xpath('//div[@id="reviews"]//p/text()').get()  # review_count is is x in Reviews (x)
            review_count = re.findall(r'(\d+)', review_header)[0]  # extract digits from the string as a string (otherwise re returns it as a list)
        else: review_count = 0

        # identifies recipe pages with ratings by seeing if the following div class has a p element
        if response.xpath('//div[@data-testid="RatingWrapper"]//p'):
            rating = response.xpath('//div[@data-testid="RatingWrapper"]//p/text()')[0].get()
            ratings_count = response.xpath('//div[@data-testid="RatingWrapper"]//p/text()')[2].get()  # the ratings count is sandwiched between two parantheses
        else:
            rating = 'NA'
            ratings_count = 0

        # obtain tags from tagcloudwrapper
        tags = response.xpath('//div[@data-testid="TagCloudWrapper"]//a//span/text()').getall()


        item = BonappItem()
        item["title"] = title
        item["author"] = author
        item["date"] = date
        item["ingredients"] = ingredients
        item["rating"] = rating
        item["ratings_count"] = ratings_count
        item["review_count"] = review_count
        item["tags"] = tags
        item["url"] = response.url

        yield item