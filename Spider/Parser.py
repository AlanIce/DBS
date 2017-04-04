import logging
import traceback
import time
import multiprocessing.queues

from multiprocessing import Queue
from lxml import etree

from .Tool.Opener import Opener
from .ORM import *

class Parser(object):
	def __init__(self, opener, fetcher):
		self.opener = opener
		self.fetcher = fetcher
		self.ModelQueue = Queue()

	def isComplete(self):
		return self.fetcher.isComplete()

	def parse(self, url=None):
		try:
			url = self.fetcher.getURL() if url == None else url
			if url == None:
				raise multiprocessing.queues.Empty
			resp = self.opener.openPage(url)
			xmlTree = etree.HTML(resp)
			contentNode = xmlTree.xpath('/html/body/div[@id="wrapper"]/div[@id="content"]')[0]
			articleNode = contentNode.xpath('div/div[@class="article"]')[0]
			subjectNode = articleNode.xpath('div[@class="indent clearfix"]/div/div[@class="subject clearfix"]')[0]
			m_dic = dict()
			# 获取影片 名称(title)
			titleNode = contentNode.xpath('h1/span')
			title = titleNode[0].text + titleNode[1].text
			m_dic['title'] = title

			# 获取影片信息
			### 导演(directors)、编剧(writers)、主演(casts)
			infoNodes = subjectNode.xpath('div[@id="info"]/span')
			directors = ' / '.join([child.text for child in infoNodes[0].xpath('span[@class="attrs"]/a')]	)
			writers	= ' / '.join([child.text for child in infoNodes[1].xpath('span[@class="attrs"]/a')])
			casts = ' / '.join([child.text for child in infoNodes[2].xpath('span[@class="attrs"]/a')])
			m_dic['directors'] = directors
			m_dic['writers'] = writers
			m_dic['casts'] = casts
			### 类型(genres)
			genres = ' / '.join([child.text for child in subjectNode.xpath('div[@id="info"]/span[@property="v:genre"]')])
			m_dic['genres'] = genres
			### 制片国家/地区(countries)、语言(languages)
			countries = subjectNode.xpath('div[@id="info"]/span[text()="制片国家/地区:"]')[0].tail.strip()
			languages = subjectNode.xpath('div[@id="info"]/span[text()="语言:"]')[0].tail.strip()
			m_dic['countries'] = countries
			m_dic['languages'] = languages
			### 又名(aka)
			akaNode = subjectNode.xpath('div[@id="info"]/span[text()="又名:"]')
			aka = '' if len(akaNode) == 0 else akaNode[0].tail.strip()
			m_dic['aka'] = aka			
			### 上映日期(pubdates)
			pubdates = ' / '.join([child.text for child in subjectNode.xpath('div[@id="info"]/span[@property="v:initialReleaseDate"]')])
			m_dic['pubdates'] = pubdates
			### 片长(durations)
			durationsNode = subjectNode.xpath('div[@id="info"]/span[@property="v:runtime"]')
			durations = ' / '.join([child.text for child in durationsNode])
			if len(durationsNode) > 0 and durationsNode[0].tail:
				durations += subjectNode.xpath('div[@id="info"]/span[@property="v:runtime"]')[0].tail
			if durations == '': durations = '未知'
			m_dic['durations'] = durations


			# 获取影片简介(summary)
			summaryBaseNode = articleNode.xpath('div[@class="related-info"]/div[@id="link-report"]')[0]
			summaryNode = summaryBaseNode.xpath('span[@class="all hidden"] | span[@property="v:summary"]')[0]
			# property="v:summary"
			summary = ('    %s\n    %s' %(summaryNode.text.strip(), '\n  '.join([child.tail.strip() for child in summaryNode])))
			m_dic['summary'] = summary

			# 获取影片评分(rating)和评分人数(rating_count)
			ratingNode = articleNode.xpath('div[@class="indent clearfix"]/div/div[@id="interest_sectl"]/div[@rel="v:rating"]/div[@typeof="v:Rating"]')[0]
			if ratingNode.xpath('strong')[0].text == None:
				rating = -1
				rating_count = -1
			else:
				rating = float(ratingNode.xpath('strong')[0].text)
				rating_count = ratingNode.xpath('div/div[@class="rating_sum"]/a/span[@property="v:votes"]')[0].text
			m_dic['rating'] = rating
			m_dic['rating_count'] = rating_count

			# 获取影片海报链接(image_url)
			imageNode = subjectNode.xpath('div[@id="mainpic"]/a/img')[0]
			image_url = str(imageNode.xpath('@src')[0])
			m_dic['image_url'] = image_url

			# 组装movie
			movie = Movie(**m_dic)
			self.ModelQueue.put(movie.getSaveSQL())
		except multiprocessing.queues.Empty as e:
			raise e
		except Exception as e:
			with open('./Spider/Log/exception.log', 'a+', encoding='utf8') as file:
				file.write('%s\n' %time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
				file.write('url : %s\n' %url)
				file.write('%s\n\n' %traceback.format_exc())