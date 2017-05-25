import time,sys
class Memory(object):
	"""docstring for Cache"""
	def __init__(self,initialData,blocks,blockSize):
		self.data = initialData #the block size of the memory
		self.iCache=Cache('instruction',blocks,blockSize)
		self.dCache = Cache('data',4,4)#this is the cache location that help find the hit

	#fetch this data from the memory and return the number of cycle to perform this
	#if this time is more than one the other value will need to stall
	def fetch(self,cacheType,startAddress,size):#the size will be in block
		block =-1
		if cacheType=='instruction':
			block =self.iCache.isHit(startAddress,1)
			if  block!= -1:
				return startAddress,size #the address is th eindex 
			else:
				#get the index of the value to write
				index =startAddress//self.iCache.blockSize
				self.iCache.writeToCache(index,index,True)
				return startAddress, size +(self.iCache.blockSize*3)#penalty for cache miss

		elif cacheType=='data':
			block  =self.dCache.isHit(startAddress,size)
			if block!=-1:
				self.dCache.updateCache(block)
				return self.dCache.fetch(block,address,size) ,size
			least = self.dCache.getLeastRecentlyUsed()
			memoryData = self.data[startAddress:startAddress+(size*32)]
			print memoryData
			self.dCache.writeToCache(least,startAddress,memoryData)
		return memoryData, size + (self.dCache.blockSize*3)#penalty for cache miss
	


class Cache(object):
	"""docstring for instructionCache"""
	def __init__(self,cacheType,blocks, blockSize):
		self.blocks = []
		for x in range(0,blocks):
			self.blocks.append({'startAddress':None,'time':None,'data':None}) 
		self.blockSize= blockSize
		self.cacheType = cacheType
		self.hitCount=0
		self.requestCount = 0

	def writeToCache(self,index,address,data):
		block =self.blocks[index]
		block['startAddress']=address
		block['time']=time.time()
		block['data']=data

	def getLeastRecentlyUsed(self):
		min = sys.maxint
		position = -1
		for index,value in enumerate(self.blocks):
			if value['time'] < min:
				position =index
				min = value['time']
		return position

	def isHit(self,address,size):
		# use the information about the strategy to perform this operatio and to get work done here
		block = self.findBlock(address,size)
		self.requestCount+=1
		if block!=-1:
			self.hitCount+=1
			self.blocks[block]['time']= time.time()
			return block
		return -1

	def findBlock(self,address,size):
		for index,block in enumerate(self.blocks):
			if block['startAddress']==None:
				continue
			if self.cacheType =='instruction':
				blockindex = address//self.blockSize
				if blockindex > self.blocks:
					raise Exception('invalid memory location')
				if block['startAddress']==blockindex:
					return index
			else:
				if block['startAddress'] <=address and address <= block['startAddress'] + size:
					return index
		return -1

	def updateCache(self,bl):
		block = self.blocks[0]['time']= time.time()

	def fetch(self,block,address,size):
		data = self.blocks[block]['data']
		return data[address:address+size]
