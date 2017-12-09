import scrapy
from scrapy.item import Item, Field

class ProxyItem(Item):
    # define the fields for your item here like:
    ip_id = Field()
    ip_address = Field()
    ip_port = Field()
    
