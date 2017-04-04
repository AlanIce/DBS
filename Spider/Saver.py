import pymysql
import multiprocessing.queues

from multiprocessing import Queue

from .ORM import *

class Saver:
	def __init__(self, ModelQueue, host, db, user, passwd):
		self.ModelQueue = ModelQueue
		self.conn = pymysql.connect(host=host, db=db, user=user, passwd=passwd, charset='utf8')
		self.cur = self.conn.cursor()

	def save(self):
		sql = self.ModelQueue.get(timeout=10)
		self.cur.execute(sql)
		self.conn.commit()

		
	def close(self):
		self.cur.close()
		self.conn.close()
		print('MySQL 连接已经关闭')
		pass

if __name__ == '__main__':
	saver = Saver()