import time

def logTime(func):
	def wrapper(*args, **kwargs):
		start = time.clock()
		ret = func(*args, **kwargs)
		end = time.clock()
		print('%s spend %.6f seconds' %(func.__name__, end - start))
		return ret
	return wrapper