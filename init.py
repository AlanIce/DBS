import multiprocessing.queues
import time
import threading
import traceback

from multiprocessing import Queue

from Spider import *
from Spider.Tool.config import database_config

# 不停地生产SQL语句，关系到Fetcher和Parser
class Spider(object):
	def __init__(self, URL_1=None, URL_2=None):
		rooturl = 'https://movie.douban.com/tag/?view=cloud'
		self.opener  = Opener()
		self.fetcher = Fetcher(self.opener, rooturl)
		if URL_1 is not None and URL_2 is not None:
			print('reset fetcher')
			self.fetcher.reset(URL_1, URL_2)
		self.parser  = Parser(self.opener, self.fetcher)
		self.saver   = Saver(self.parser.ModelQueue, **database_config)
		self.running = True

	def initThreads(self):
		try:
			threads = []
			for i in range(0, 3):
				thread = threading.Thread(target=self.produce)
				threads.append(thread)	
			threads.append(threading.Thread(target=self.consume))
			for t in threads:
				t.setDaemon(True)
				t.start()
			while  True:
				time.sleep(100)
		except KeyboardInterrupt as e:
			self.running = False
			print('捕捉到KeyboardInterrupt')
			with open('./Spider/Log/interrupt.log', 'a+') as file:
				file.writelines('Current_URL_1 : ' + self.fetcher.Current_URL_1 + '\n')
				file.writelines('Current_URL_2 : ' + self.fetcher.Current_URL_2 + '\n')
				file.writelines('Current_URL   : ' + self.fetcher.Current_URL   + '\n\n')
			self.fetcher.bloomfilter.write_to_file()
			time.sleep(10)
		finally:
			print('所有线程即将结束...')

	def produce(self):
		# while self.running:
		while self.running:
			try:
				print('%s : produce 运行' %threading.current_thread().name)
				self.parser.parse()
			except multiprocessing.queues.Empty as e:
				pass
				self.running = not self.fetcher.isCompleted()
			except KeyboardInterrupt as e:
				self.running = False
			finally:
				time.sleep(6)
		print('%s : produce 退出' %threading.current_thread().name)

	def consume(self):
		while self.running:
			print('%s : consume 运行' %threading.current_thread().name)
			try:
				self.saver.save()
			except multiprocessing.queues.Empty as e:
				if self.fetcher.isCompleted():
					self.running = False
					print('已经完成')
				else:
					print('尚未完成')
			except Exception as e:
				with open('./Spider/Log/exception.log', 'a+', encoding='utf8') as file:
					file.write('%s\n' %time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
					file.write('%s\n\n' %traceback.format_exc())
		print('%s : consume 退出' %threading.current_thread().name)

if __name__ == '__main__':
	URL_1 = 'https://movie.douban.com/tag/日本'
	URL_2 = 'https://movie.douban.com/tag/日本?start=60&type=T'
	spider = Spider(URL_1, URL_2)
	spider.initThreads()