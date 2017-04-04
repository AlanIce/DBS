from Spider.BloomFilter import *

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