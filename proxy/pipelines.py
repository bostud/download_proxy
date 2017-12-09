# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String
from sqlalchemy.orm import Session
import os
from scrapy.exceptions import DropItem
from proxy.items import ProxyItem


Base = declarative_base()

class ProxyItem(Base):

	__tablename__ = "proxyitem"
	id = Column(Integer, primary_key=True)
	ip_address = Column(String)
	ip_port = Column(String)

	def __init__(self, ip_address, ip_port):
		self.ip_address = ip_address
		self.ip_port = ip_port

class ProxyPipeline(object):

	def __init__(self):
		basename = "data_proxy"
		self.engine = create_engine("sqlite:///%s" % basename, echo=False)
		if not os.path.exists(basename):
			Base.metadata.create_all(self.engine)
		self.dt = set()

	def process_item(self, item, spider):
		if isinstance(item, ProxyItem):
			dt = DataTable(item['ip_address'], item['ip_port'])
			self.session.add(dt)
		return item

	def close_spider(self, spider):
		self.session.commit()
		self.session.close()

	def open_spider(self, spider):
		self.session = Session(bind=self.engine)	