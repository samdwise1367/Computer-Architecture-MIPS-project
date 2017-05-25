# contains functionalities for parsing the instruction and the configuration file
import instruction,functionalunit
class functionalParser(object):
	"""docstring for functionalParser"""
	def __init__(self,instructionFile,configFile,data):
		self.instructionFile = instructionFile
		self.configFile = configFile
		self.dataFile = data
		self.labels=[]
		
	def loadInstructions(self):
		# this function parses instruction in the file and report in case or error
		content = self.loadFile(self.instructionFile)
		result=[]
		instr = content.split('\n');
		for index,ins in enumerate(instr):
			label=None
			col =ins.strip()
			col = ins.split(' ',1)
			if len(col) ==1:
				#make this instruction to be a one operand instruction
				command = col[0].strip()
				operands =[]
			else:
				com = col[0].strip().split(':') # process label
				if len(com) > 1:
					label =com[0]
					self.labels.append({label:index})
					command = com[1]
				else:
					command = com[0]
				operands = col[1].strip().split(',')
			if not self.isValidInstruction(command,operands):
				raise Exception('syntax error on line '+str(index+1))
			tempInstruction = instruction.Instruction(command,operands,label)
			result.append(tempInstruction)
		return result


	def icacheInfo(self):
		try:
			return self.icacheBlock,self.icacheSize
		except Exception as e:
			self.loadFunctionalFileInfo()
			return self.icacheBlock,self.icacheSize
		

	def loadFunctionalFileInfo(self):
		content = self.loadFile(self.configFile);
		items = content.strip().split("\n")
		for item in items:
			startpos = item.index(':')
			startpos+=1
			if item.find("adder")!= -1:
				temp = item[startpos:].strip().split(',')
				self.adderCycle = int(temp[1])
				self.adderSize = int(temp[0])
			elif item.find("Multiplier")!= -1:
				temp = item[startpos:].strip().split(',')
				self.multiplierCycle = int(temp[1])
				self.multiplierSize = int(temp[0])
			elif item.find("divider") != -1:
				temp = item[startpos:].strip().split(',')
				self.dividerCycle = int(temp[1])
				self.dividerSize = int(temp[0])
			elif item.find("I-Cache")!= -1:
				temp = item[startpos:].strip().split(',')
				self.icacheBlock = int(temp[0])
				self.icacheSize = int(temp[1])

	def isValidInstruction(self,command,operands):
		# need a  list of all the valid istruction and the number of operands
		instruction = self.findInstruction(command)
		if instruction==None:
			return False
		return instruction['operand']==len(operands) 
		
		# loads the configuration needed for the cpu,this function return the starting memory state for the cpu also		
	def getCPUParam(self,filename):
		'return a tuple that contains the information needed by the cpu object'
		content = self.loadFile(filename)
		config = content.split('\n')
		for index,con in enumerate(config):
			result = con.split(' ')
			return tuple(result)

	def loadFile(self,filename):
		file = open(filename,'r')
		content = file.read()
		file.close()
		return content

	def getInstructionSet(self):
		try:
			return self.instructionSet
		except Exception as e:
			self.instructionSet = self.buildInstructionSet()
			return self.instructionSet

	def findInstruction(self,instructionName):
		instruction = self.getInstructionSet()
		for inst in instruction:
			if inst['name']==instructionName:
				return inst
		return None

	def buildInstructionSet(self):
		#create a list of dictionaries containing the instruction set and the properties
		dict = [{'name':'HLT','execute':0,'completionStage':'Issue','operand':0,'type':'Special'}]
		dict.append({'name':'J','execute':0,'completionStage':'Issue','operand':3,'type':'Control'})
		dict.append({'name':'BEQ','execute':0,'completionStage':'Read','operand':3,'type':'Arithmetic'})
		dict.append({'name':'BNE','execute':0,'completionStage':'Read','operand':3,'type':'Arithmetic'})
		dict.append({'name':'DADD','execute':1,'completionStage':'Execute','operand':3,'type':'Arithmetic'})
		dict.append({'name':'DADDI','execute':1,'completionStage':'Execute','operand':3,'type':'Arithmetic'})
		dict.append({'name':'DSUB','execute':1,'completionStage':'Execute','operand':3,'type':'Arithmetic'})
		dict.append({'name':'DSUBI','execute':1,'completionStage':'Execute','operand':3,'type':'Arithmetic'})
		dict.append({'name':'AND','execute':1,'completionStage':'Execute','operand':3,'type':'Arithmetic'})
		dict.append({'name':'ANDI','execute':1,'completionStage':'Execute','operand':3,'type':'Arithmetic'})
		dict.append({'name':'OR','execute':1,'completionStage':'Execute','operand':3,'type':'Logical'})
		dict.append({'name':'ORI','execute':1,'completionStage':'Execute','operand':3,'type':'Arithmetic'})
		dict.append({'name':'LI','execute':1,'completionStage':'Execute','operand':2,'type':'Data'})
		dict.append({'name':'LUI','execute':1,'completionStage':'Execute','operand':2,'type':'Data'})
		dict.append({'name':'LW','execute':1,'completionStage':'Execute','operand':2,'type':'Data'})
		dict.append({'name':'SW','execute':1,'completionStage':'Execute','operand':2,'type':'Data'})
		dict.append({'name':'L.D','execute':2,'completionStage':'Execute','operand':2,'type':'Data'})
		dict.append({'name':'S.D','execute':2,'completionStage':'Execute','operand':2,'type':'Data'})
		add,mul,div= self.loadConfigFromFile();
		dict.append({'name':'ADD.D','execute':add,'completionStage':'Execute','operand':3,'type':'Arithmetic'})
		dict.append({'name':'SUB.D','execute':add,'completionStage':'Execute','operand':3,'type':'Arithmetic'})
		dict.append({'name':'MUL.D','execute':mul,'completionStage':'Execute','operand':3,'type':'Arithmetic'})
		dict.append({'name':'DIV.D','execute':div,'completionStage':'Execute','operand':3,'type':'Arithmetic'})
		return dict

	def loadConfigFromFile(self):
		return self.adderCycle,self.multiplierCycle,self.dividerCycle
	#function to load the memory information in a way that it can be easily accessed
	def loadInitialMemoryData(self):
		content = self.loadFile(self.dataFile)
		content = content.replace("\n",'')
		return content