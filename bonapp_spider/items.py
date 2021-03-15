# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class BonappItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    author = Field()
    url = Field()
    date = Field()
    ingredients = Field()
    rating = Field()
    ratings_count = Field()
    review_text = Field()
    review_count = Field()
    tags = Field()
