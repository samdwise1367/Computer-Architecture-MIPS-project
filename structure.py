import time
class Memory(object):
	"""docstring for Cache"""
	def __init__(self,initialData, blocks,blockSize):
		self.data = initialData #the block size of the memory
		self.iCache=Cache('instruction',blocks,blockSize)
		self.dCache = Cache('data',4,4)#this is the cache location that help find the hit

	#fetch this data from the memory and return the number of cycle to perform this
	#if this time is more than one the other value will need to stall
	def fetch(self,fetchType,startAddress,size,wait=0):#the size will be in block
		if  self.iCache.isHit(address):
			return size;
		return wait+(size*3)#penalty for cache miss
	


class Cache(object):
	"""docstring for instructionCache"""
	def __init__(self,cacheType,blocks, blockSize):
		self.blocks = blocks
		self.blockSize= blockSize
		self.cacheType = cacheType
		self.buffer ={}#use a dictinary of dictionary to represent the cache information 
	def isHit(self,fetchType,address):
		# use the information about the strategy to perform this operatio and to get work done here
		if self.checkAddress(fetchType,address):
			self.buffer[address]['time']= time.time()
			return true;
	def checkAddress(self,cacheType,address):
		if fetchType=='instruction':
			index = address%self.blocks

	def update(self,fetchType,address,data):
		pass			