import requests
import logging
import threading
import multiprocessing.queues

from multiprocessing import Queue
from lxml import etree

from .BloomFilter.BloomFilter import BloomFilter
from .Tool.Opener import Opener

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

class Fetcher(object):
	def __init__(self, opener, rooturl):
		logging.debug('Fetcher Init...')
		self.opener = opener
		self.bloomfilter = BloomFilter(1000000, 0.001, './Spider/Log/BloomFilter.cache.dat')
		self.rooturl = rooturl
		self.lock1 = threading.Lock()
		self.lock2 = threading.Lock()
		self.URLQueue = Queue()
		self.BufferQueue_1 = Queue()
		self.BufferQueue_2 = Queue()
		self.fillBufferQueue_1()

	def isCompleted(self):
		return self.URLQueue.empty() and self.BufferQueue_2.empty() and self.BufferQueue_1.empty()

	def reset(self, Last_URL_1, Last_URL_2):
		logging.info('Fetcher reset:\nLast_URL_1 : ' + Last_URL_1 + '\nLast_URL_2 : ' + Last_URL_2)
		while True:
			URL_1 = self.BufferQueue_1.get()
			if URL_1 == Last_URL_1:
				break
		self.fillBufferQueue_2(Last_URL_1)
		while True:
			URL_2 = self.BufferQueue_2.get()
			if URL_2 == Last_URL_2:
				break
		self.Current_URL_1 = Last_URL_1
		self.Current_URL_2 = Last_URL_2

	# 一级队列都是标签列表
	def fillBufferQueue_1(self, rooturl=None):		
		if self.lock1.acquire(False):
			logging.debug('fillBufferQueue_1')
			rooturl = self.rooturl if rooturl == None else rooturl
			logging.debug('requests : %s' %rooturl)
			resp = self.opener.openPage(rooturl)
			xmlTree = etree.HTML(resp)
			hrefs = xmlTree.xpath('//div/table/tbody/tr/td/a/@href')
			for href in hrefs:
				self.BufferQueue_1.put('https://movie.douban.com' + str(href))
			self.lock1.release()

	# 二级队列是20部电影的页面
	def fillBufferQueue_2(self, URL_1=None):
		if self.lock2.acquire(False):
			logging.debug('fillBufferQueue_2')
			URL_1 = self.BufferQueue_1.get(timeout=10) if URL_1 == None else URL_1
			self.Current_URL_1 = URL_1
			logging.debug('requests : %s' %URL_1)
			resp = self.opener.openPage(URL_1)	
			xmlTree = etree.HTML(resp)
			nodes = xmlTree.xpath('//div[@class="paginator"]/span[@class="thispage"]/@data-total-page')
			totalPage = int(nodes[0])
			for i in range(0, totalPage):
				URL_2 = URL_1 + '?start=' + str(i * 20) + '&type=T'
				self.BufferQueue_2.put(URL_2)
			self.lock2.release()
			

	# 三级队列是电影的详情页面
	def fillURLQueue(self, URL_2=None):		
		logging.debug('fillURLQueue')
		URL_2 = self.BufferQueue_2.get(timeout=10) if URL_2 == None else URL_2
		self.Current_URL_2 = URL_2
		logging.debug('requests : %s' %URL_2)
		resp = self.opener.openPage(URL_2)
		xmlTree = etree.HTML(resp)
		nodes = xmlTree.xpath('//table/tr[@class="item"]/td/a[@class="nbg"]/@href')
		for node in nodes:
			URL = str(node)
			if self.bloomfilter.addElement(URL) == False:
				print(URL, 'URL已经重复')
			else:
				self.URLQueue.put(URL)

	def keepRunning(self):
		if self.isCompleted():
			return
		if self.URLQueue.qsize() < 100 or self.BufferQueue_2.qsize() < 20:
			if self.BufferQueue_2.empty():
				self.fillBufferQueue_2()
			self.fillURLQueue()

	def getURL(self):
		if self.URLQueue.empty():
			if self.BufferQueue_2.empty():
				if self.BufferQueue_1.empty():
					return None;
				else:
					self.fillBufferQueue_2()
			self.fillURLQueue()
		# self.Current_URL = self.URLQueue.get()
		try:			
			self.Current_URL = self.URLQueue.get(timeout=10)
		except multiprocessing.queues.Empty as e:
			self.Current_URL = self.getURL()
		return self.Current_URL