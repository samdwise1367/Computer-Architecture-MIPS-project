# this class does the loading of all the functioall unit of the computer organisation
# function to load the cpu
import sys,parser,argparse,memory,cpu



prs = argparse.ArgumentParser(description='MIPS Sub-Instruction set simulator..')
prs.add_argument('instruction',help='the path to the instruction to be loaded')
prs.add_argument('config',help='the configuration file for the simulator')
prs.add_argument('memory',help='the initial memory value')
prs.add_argument('output',help='the file to save the result to')
argum = prs.parse_args()
instr = argum.instruction
config = argum.config
data = argum.memory
out = argum.output
myParser = parser.functionalParser(instr,config,data)
icacheBlocks,icacheBlockSize = myParser.icacheInfo()
memoryData =myParser.loadInitialMemoryData()
memory =memory.Memory(memoryData,icacheBlocks,icacheBlockSize);
instructions = myParser.loadInstructions();
instructionSet = myParser.getInstructionSet();
processor = cpu.CPU(memory,instructions,instructionSet,myParser.adderSize,myParser.multiplierSize,myParser.dividerSize,out)
processor.start()