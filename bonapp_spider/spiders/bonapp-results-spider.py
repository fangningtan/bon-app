from scrapy import Spider, Request
from bonapp_spider.items import BonappItem
import pandas as pd

class bonapp_spider(Spider):
    name = "bonapp_spider"
    allowed_domains = ['www.bonappetit.com']
    start_urls = ['https://www.bonappetit.com/search/?content=recipe&issueDate=2020-12-01']

    def parse(self, response):
        # Breaks search into urls per month in the specified date range
        timespan = pd.date_range(start='2020-01-01', end='2020-12-01', freq='MS')
        results_monthly = [f'https://www.bonappetit.com/search/?content=recipe&issueDate={date}-01' for date in timespan.strftime('%Y-%m')]
        for url in results_monthly:
            yield Request(url=url, callback=self.parse_gallery_page)


    def parse_gallery_page(self, response):
        # Scrapes results page for recipe links and recipe titles

        recipe_xpaths = response.xpath('//a[@class="photo-link"]')

        # iterates through the recipe_xpaths and obtains title and url values from the scraped data
        for recipe in recipe_xpaths:
            item = BonappItem()
            item['title'] = recipe.xpath('.//@aria-label').get()
            item['url'] = 'https://www.bonappetit.com'+recipe.xpath('.//@href').get()
            yield item

        # the urls obtained can be passed to the recipe-scrapers package



