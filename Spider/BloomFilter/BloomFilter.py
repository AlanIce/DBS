from math import e, log, ceil
from BitVector import BitVector
from ..Tool.Decorator import logTime
import time, os, hashlib

class BloomFilter:
	@logTime
	def __init__(self, N, E, filename = None):
		self.N = N
		self.E = E
		self.Size = N * log(e / E, 2)
		Bit = ceil(log(self.Size, 2))
		self.Size = 1 << Bit
		self.Basic = self.Size - 1
		self.Hash_num = log(2) * self.Size / N
		self.Hash_num = ceil(self.Hash_num)
		self.filename = filename
		if self.Hash_num > 20:
			Hash_num = 20
		if filename != None and os.path.exists(filename):
			self.bitvector = BitVector(filename = filename)
			self.bitvector = self.bitvector.read_bits_from_file(self.Size)
		else:
			self.bitvector = BitVector(size = self.Size)
		self.Seed = (101, 191, 223, 271, 353, 419, 613, 691, 757, 883, 911, 977, 2339, 3119, 3733, 5939, 7193, 7331, 11411, 29989)

	def hash(self, s, seed):
		hash_val = 1
		s = hashlib.md5(s.encode('utf-8')).hexdigest()
		for ch in s:
			ch_val = ord(ch);
			hash_val += hash_val * seed + ch_val
			hash_val &= self.Basic
		return hash_val;

	# 返回真表示添加成功， 返回假表示已存在
	def addElement(self, element):
		tag = False
		for i in range(0, self.Hash_num):
			hash_val = self.hash(str(element), self.Seed[i])
			if self.bitvector[hash_val] == 0:
				self.bitvector[hash_val] = 1
				tag = True
		return tag

	# 返回真表示已经存在
	def is_exsit(self, element):
		tag = True
		for i in range(0, self.Hash_num):
			hash_val = self.hash(str(element), self.Seed[i])
			if self.bitvector[hash_val] == 0:
				tag = False
		return tag

	@logTime
	def write_to_file(self, filename = None):
		if filename == None and self.filename == None:
			raise Exception('保存文件请指定文件名！')
		filename = filename if filename != None else self.filename
		with open(filename, 'wb') as file:
			self.bitvector.write_to_file(file)
		with open(filename + '.log', 'w') as logfile:
			logfile.write('N : %d\nE : %.4f\n' %(self.N, self.E))
			logfile.write('Size : %d\nHash_num : %d' %(self.Size, self.Hash_num))


if __name__ == '__main__':
	bloomfilter = BloomFilter(1000000, 0.001, 'bloomfilter.dat')

	print(bloomfilter.addElement('12'))
	print(bloomfilter.addElement('1'))
	print(bloomfilter.addElement('1'))
	print(bloomfilter.addElement('2'))
	print(bloomfilter.addElement('asdasdwrw'))
	print(bloomfilter.addElement('asdasdas'))
	print(bloomfilter.addElement('aczxca'))
	print(bloomfilter.addElement('zxczxcz'))
	print(bloomfilter.addElement('zxczxc'))
	print(bloomfilter.addElement('asdqawre'))
	print(bloomfilter.addElement('fdsafzczx'))
	print(bloomfilter.addElement('fdsafzczx'))
	print(bloomfilter.addElement('wotamayeshizuile'))

	bloomfilter.write_to_file()