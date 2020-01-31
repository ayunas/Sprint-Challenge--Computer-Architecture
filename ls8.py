
from operations import LDI,PRN,TEST1,TEST2,TEST3,TEST4,TEST5,CMP,JEQ,JNE,JMP,HLT
import sys

class LS8:
    def __init__(self):
        self.pc = 0
        self.ram = [0]*256 #ls8 is a 8 bit processor, at most, it can process a total of 2^8 = 256 bytes in memory
        self.reg = [0]*8  #ls8 has 8 registers for usege
        self.sp = -1 #initial stack pointer at the end of the ram
        self.fl = 0b00000000 #00000LGE L = Less, G = Greater E = Equal

    def load(self):
        if len(sys.argv) != 2:
            raise IOError("cannot load file or file not specified")
            sys.exit()
        try:
            filename = sys.argv[1]
            program = open(filename, 'r')
            address = 0
        except IOError:
            print('Could not open/read file', filename)
            raise IOError
            sys.exit()

        for i in range(7): #skip the 1st 7 lines of the program
            program.readline()
        
        instructions = []
        for line in program:
            byte = line.split(' #')[0]
            byte = byte.strip()
            if '#' in byte:
                continue
            instructions.append(byte)
        
        for byte in instructions:
            self.ram[address] = int(byte,2)
            address += 1
        
        print(self.ram)

    def ldi(self,r_address,val): #load immediate (into a cpu register)
        self.reg[r_address] = val
        print('register:', self.reg)
    
    def alu(self,op,reg_a,reg_b):
        if op == 'CMP':
            if reg_a - reg_b > 0: #reg_a > reg_b
                self.fl = 0b00000010
                print(self.reg[reg_a], ' > ', self.reg[reg_b])
            elif reg_a - reg_b < 0: #reg_a < reg_b
                self.fl = 0b00000100
                print(self.reg[reg_a],' < ', self.reg[reg_b])
            elif reg_a - reg_b == 0:
                self.fl = 0b00000001
                print(self.reg[reg_a], ' = ', self.reg[reg_b])
            else:
                print(f'error occured comparing {self.reg[reg_a]} and {self.reg[reg_b]}')
                raise Exception
                sys.exit()
        
    def run(self):
        try:
            self.load()
            halted = False
        except Except:
            print('file could not be loaded')
            sys.exit()

        while halted == False:
            instruction = self.ram[self.pc]

            if instruction == LDI:
                r_address = self.ram[self.pc + 1]
                val = self.ram[self.pc + 2]
                self.ldi(r_address,val)
                self.pc += 3
            
            elif instruction == CMP:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu('CMP', reg_a, reg_b)
                self.pc += 2

            elif instruction == HLT:
                self.pc += 1
                halted = True
                sys.exit()
            
            else:
                print(f"error occured at program counter index: {self.pc}")
                raise IndexError
                sys.exit()

ls8 = LS8()
ls8.run()


        