import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bonapp_spider.items import BonappItem
import re


class BonappBasicallySpider(CrawlSpider):
    # using crawl spider because i want to generalise the solution to keep clicking if there's a next page
    name = "bonapp_basically_crawler"
    allowed_domains = ['www.bonappetit.com']
    start_urls = ['https://www.bonappetit.com/healthyish/recipes/'] # change basically to healthyish if scraping for that

    # using CrawlSpider so rules need to be set
    # first rule checks if there's a next page available and follows it
    # second rule requests for all the links on the page that are in the specified format: /recipes/name
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[contains(@class, 'pager__link--next')]"), follow=True),
        Rule(LinkExtractor(restrict_xpaths="//h1[@class='feature-item-hed']//a"), callback='parse_recipe_page')

    )

    def parse_recipe_page(self, response):

        title = response.xpath('//head//title/text()').get().split(' Recipe', 1)[0]

        author = response.xpath('//head//meta[@name="author"]//@content').get()

        date = response.xpath('//div//time/text()').get()  # this is not present in all types of recipes so add if else statement

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

        # identifies recipe pages with ratings by seeing if the following div class has a p element (because the p element contains the rating and rating count)
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