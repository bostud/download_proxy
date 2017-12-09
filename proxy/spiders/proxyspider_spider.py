import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.loader import ItemLoader
from proxy.items import ProxyItem


class ProxyLoaer(ItemLoader):
	default_output_processor = Identity()

class ProxyListSpider(scrapy.Spider):
	
	name = "proxyspider"
	allowed_domain = ['spys.one']

	def start_requests(self):
		headers = {
			'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
			'cookie':'_ga=GA1.2.1334516637.1512809840; _gid=GA1.2.1181586788.1512809840'
		}
		pages = [1, 2, 3, 0, 4]
		using_urls = ['http://spys.one/proxies/']
		
		for page in pages:

			for url in using_urls:
				url_ = ''
				url_ = url + str(page) + '/'
				
				yield scrapy.Request(url=url_, headers=headers, callback=self.parse)

	def parse(self, response):
		page_info = Selector(response)
		
		all_ip_address = page_info.xpath('//tr[@onmouseover]/td[1]/font[@class="spy14"]/text()[1]').extract()
		try:
			all_ip_port = page_info.xpath('//tr[@onmouseover]/td[1]/font[@class="spy14"]/text()[2]').extract()
		except Exception as e:
			all_ip_port = []

		for ip_address in all_ip_address:
			item_index = 0
			item_index = all_ip_address.index(ip_address)
			Item = ProxyItem()
			Item['ip_address'] = ip_address.strip()
			try:
				ip_port = all_ip_port[item_index]
			except Exception as e:
				ip_port = ''
			Item['ip_port'] = ip_port.strip()
			yield Item
		print('Test')
			



