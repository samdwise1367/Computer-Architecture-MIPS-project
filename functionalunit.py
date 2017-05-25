class FunctionalUnit(object):
	"""The class that represent functional unit of the simulator

	"""
	def __init__(self, name,count):
		self.count = count
		self.name = name
		self.used = 0
	def occupy(self):
		if self.used < self.count:
			self.used+=1
			return True
		else:
			return False
	def free(self):
		if used > 0:
			used-=1
		