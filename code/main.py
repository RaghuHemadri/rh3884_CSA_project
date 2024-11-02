import os
import argparse
import math
from utils import Utils
from SingleStageExecution import SingleStageExecution
from SingleStageDecode import SingleStageDecode


MemSize = 1000 # memory size, in reality, the memory size should be 2^32, but for this lab, for the space resaon, we keep it as this large number, but the memory is still 32-bit addressable.

class InsMem(object):
    def __init__(self, name, ioDir):
        self.id = name
        
        with open(os.path.join(ioDir, "imem.txt")) as im:
            self.IMem = [data.replace("\n", "") for data in im.readlines()]
        

    def readInstr(self, ReadAddress):
        #read instruction memory
        #return 32 bit hex val
        instruction = ''.join(self.IMem[ReadAddress : ReadAddress+4])
        return instruction
          
class DataMem(object):
    def __init__(self, name, ioDir):
        self.id = name
        self.ioDir = ioDir
        with open(os.path.join(ioDir, "dmem.txt")) as dm:
            self.DMem = [data.replace("\n", "") for data in dm.readlines()]
            self.DMem.extend(["00000000"]*(1000-len(self.DMem)))
        

    def readDataMem(self, ReadAddress):
        #read data memory
        #return 32 bit hex val
        data = ''.join(self.DMem[ReadAddress : ReadAddress+4])
        
        return Utils.twos_complement(data)
        
    def writeDataMem(self, Address, WriteData):
        # write data into byte addressable memory
        WriteData = Utils.decimal_to_binary(WriteData)
        arr = [WriteData[i:i+8] for i in range(0, len(WriteData), 8)]
        
        for i in range(len(arr)):
            self.DMem[Address+i] = arr[i]
                     
    def outputDataMem(self):
        resPath = self.ioDir + os.sep + self.id + "_DMEMResult.txt"
        with open(resPath, "w") as rp:
            rp.writelines([str(data) + "\n" for data in self.DMem])

class RegisterFile(object):
    def __init__(self, ioDir):
        self.outputFile = ioDir + "RFResult.txt"
        self.Registers = [0x0 for i in range(32)]
    
    def readRF(self, Reg_addr):
        return self.Registers[Reg_addr]
    
    def writeRF(self, Reg_addr, Wrt_reg_data):
        if Reg_addr !=0:
            self.Registers[Reg_addr] = Wrt_reg_data
         
    def outputRF(self, cycle):
        op = ["-"*70+"\n", "State of RF after executing cycle:" + str(cycle) + "\n"]
        op.extend([Utils.decimal_to_binary(val)+"\n" for val in self.Registers])
        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.outputFile, perm) as file:
            file.writelines(op)

class State(object):
    def __init__(self):
        self.IF = {"nop": False, "PC": 0}
        self.ID = {"nop": True, "Instr": 0, "is_hazard":False}
        self.EX = {"nop": True, "Read_data1": 0, "Read_data2": 0, "Imm": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "is_I_type": False, "rd_mem": 0, 
                   "wrt_mem": 0, "alu_op": 0, "wrt_enable": 0}
        self.MEM = {"nop": True, "ALUresult": 0, "Store_data": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "rd_mem": 0, 
                   "wrt_mem": 0, "wrt_enable": 0}
        self.WB = {"nop": True, "Wrt_data": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "wrt_enable": 0}

class Core(object):
    def __init__(self, ioDir, imem, dmem):
        self.myRF = RegisterFile(ioDir)
        self.cycle = 0
        self.halted = False
        self.ioDir = ioDir
        self.state = State()
        self.nextState = State()
        self.ext_imem = imem
        self.ext_dmem = dmem
        self.takeBranch = False

class SingleStageCore(Core):
    def __init__(self, ioDir, imem, dmem):
        super(SingleStageCore, self).__init__(ioDir + os.sep + "SS_", imem, dmem)
        self.opFilePath = ioDir + os.sep + "StateResult_SS.txt"
        self.SingleStageExecution = SingleStageExecution()

    def step(self):
        # Your implementation
        if self.state.IF["nop"]:
            self.halted = True

        instr = imem.readInstr(self.state.IF["PC"])
        decodedInst = SingleStageDecode.decode(instr) #dict of all operands
        if decodedInst is None: 
            self.halted = True
        else: 
            self.SingleStageExecution.perform_operation(decodedInst,self.myRF,self.ext_dmem,self.takeBranch,self.state)
            
        self.myRF.outputRF(self.cycle) # dump RF
        self.printState(self.state, self.cycle) # print states after executing cycle 0, cycle 1, cycle 2 ... 
            
        # self.state = self.nextState #The end of the cycle and updates the current state with the values calculated in this cycle
        self.cycle += 1


    def printState(self, state, cycle):
        printstate = ["-"*70+"\n", "State after executing cycle: " + str(cycle) + "\n"]
        printstate.append("IF.PC: " + str(state.IF["PC"]) + "\n")
        printstate.append("IF.nop: " + str(state.IF["nop"]) + "\n")
        
        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.opFilePath, perm) as wf:
            wf.writelines(printstate)

class FiveStageCore(Core):
    def __init__(self, ioDir, imem, dmem):
        super(FiveStageCore, self).__init__(ioDir + "/FS_", imem, dmem)
        self.opFilePath = os.path.join(ioDir, "StateResult_FS.txt")

    def step(self):
        # Your implementation
        # --------------------- WB stage ---------------------
        
        
        
        # --------------------- MEM stage --------------------
        
        
        
        # --------------------- EX stage ---------------------
        
        
        
        # --------------------- ID stage ---------------------
        
        
        
        # --------------------- IF stage ---------------------
        
        self.halted = True
        if self.state.IF["nop"] and self.state.ID["nop"] and self.state.EX["nop"] and self.state.MEM["nop"] and self.state.WB["nop"]:
            self.halted = True
        
        self.myRF.outputRF(self.cycle) # dump RF
        self.printState(self.nextState, self.cycle) # print states after executing cycle 0, cycle 1, cycle 2 ... 
        
        self.state = self.nextState #The end of the cycle and updates the current state with the values calculated in this cycle
        self.cycle += 1

    def printState(self, state, cycle):
        printstate = ["-"*70+"\n", "State after executing cycle: " + str(cycle) + "\n"]
        printstate.extend(["IF." + key + ": " + str(val) + "\n" for key, val in state.IF.items()])
        printstate.extend(["ID." + key + ": " + str(val) + "\n" for key, val in state.ID.items()])
        printstate.extend(["EX." + key + ": " + str(val) + "\n" for key, val in state.EX.items()])
        printstate.extend(["MEM." + key + ": " + str(val) + "\n" for key, val in state.MEM.items()])
        printstate.extend(["WB." + key + ": " + str(val) + "\n" for key, val in state.WB.items()])

        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.opFilePath, perm) as wf:
            wf.writelines(printstate)

def printPerformanceMetrics(ioDir,CPI_SS, IPC_SS, cycles_SS):

    

    opFilePath = ioDir + os.sep + "PerformanceMetrics_Result.txt"
    printstate_SS = ["-----------------------------Single Stage Core Performance Metrics-----------------------------\n"]
    printstate_SS.append("Number of cycles taken: " + str(cycles_SS) + "\n")
    printstate_SS.append("Total Number of Instructions: " + str(math.ceil(cycles_SS/CPI_SS)) + "\n")
    printstate_SS.append("Cycles per instruction: " + str(CPI_SS) + "\n")
    printstate_SS.append("Instructions per cycle: " + str(IPC_SS) + "\n")

    # for line in printstate_SS:
    #     print(line)

    with open(opFilePath, 'w') as wf:
        wf.writelines(printstate_SS)

if __name__ == "__main__":
     
    #parse arguments for input file location
    parser = argparse.ArgumentParser(description='RV32I processor')
    parser.add_argument('--iodir', default="", type=str, help='Directory containing the input files.')
    args = parser.parse_args()

    ioDir = os.path.abspath(args.iodir)
    print("IO Directory:", ioDir)

    imem = InsMem("Imem", ioDir)
    dmem_ss = DataMem("SS", ioDir)
    # dmem_fs = DataMem("FS", ioDir)
    
    ssCore = SingleStageCore(ioDir, imem, dmem_ss)
    # fsCore = FiveStageCore(ioDir, imem, dmem_fs)

    while True:
        if not ssCore.halted:
            ssCore.step()
        if ssCore.halted:
            break

    # while True:
    #     if not fsCore.halted:
    #         fsCore.step()

    #     if fsCore.halted:
    #         break
    
    # dump SS and FS data mem.
    dmem_ss.outputDataMem()

    IPC_SS = round((ssCore.cycle - 1) / ssCore.cycle,6)
    CPI_SS = round(1/IPC_SS,5)
    printPerformanceMetrics(ioDir,CPI_SS,IPC_SS,ssCore.cycle)
