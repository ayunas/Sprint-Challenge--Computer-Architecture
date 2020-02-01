
from operations import LDI,PRN,TEST1,TEST2,TEST3,TEST4,TEST5,CMP,JEQ,JNE,JMP,HLT,NOT
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
    
    def not_bitwise(self,n):
        binary = f"{n:08b}"
        bin_list = [int(b) for b in iter(binary)]
        # flipped = [1 for b in bin_list if b == 0 else 0 for b in bin_list]
        flipped = ['1' if b == 0 else '0' for b in bin_list]
        notted = "".join(flipped)
        return int(notted,2)

    def ldi(self,r_address,val): #load immediate (into a cpu register)
        self.reg[r_address] = val
        # print('LDI complete.  register:', self.reg)
    
    def alu(self,op,reg_a,reg_b=0):
        if op == 'CMP':
            if self.reg[reg_a] - self.reg[reg_b] < 0: #reg_a < reg_b
                self.fl = 0b00000100  #3
                # print(self.reg[reg_a],' < ', self.reg[reg_b])
            elif self.reg[reg_a] - self.reg[reg_b] > 0: #reg_a > reg_b
                self.fl = 0b00000010 #2
                print(self.reg[reg_a], ' > ', self.reg[reg_b])
            elif self.reg[reg_a] - self.reg[reg_b] == 0:
                self.fl = 0b00000001 #1
                # print(self.reg[reg_a], ' = ', self.reg[reg_b])
            else:
                # print(f'error occured comparing {self.reg[reg_a]} and {self.reg[reg_b]}')
                raise Exception
                sys.exit()
        elif op == 'ADD':
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'AND':
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == 'OR':
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == 'NOT':
            # self.reg[reg_a] = ~self.reg[reg_a]
            self.reg[reg_a] = self.not_bitwise(self.reg[reg_a])
            print(self.reg[reg_a])
            print(self.reg)    

    def push(self,pc):
        self.ram[self.sp] = pc
        self.sp -= 1
        # print('ram after pushing', self.ram)
    
    def pop(self):
        self.sp += 1
        popped = self.ram[self.sp]
        self.ram[self.sp] = 0
        return popped

    def run(self):
        try:
            self.load()
            halted = False
        except Except:
            print('file could not be loaded')
            sys.exit()

        while halted == False:
            instruction = self.ram[self.pc]
            # print(f'instruction', instruction, 'pc:', self.pc)

            if instruction == LDI:
                r_address = self.ram[self.pc + 1]
                val = self.ram[self.pc + 2]
                self.ldi(r_address,val)
                self.pc += 3
        
            elif instruction == PRN:
                r_address = self.ram[self.pc + 1]
                print(self.reg[r_address])
                self.pc += 2
            
            elif instruction == CMP:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu('CMP', reg_a, reg_b)
                self.pc += 3
            
            elif instruction == JEQ: #jump to register if equal
                # print('in JEQ')
                if self.fl == 0b00000001: #equal bit flagged
                    self.push(self.pc)
                    r_address = self.ram[self.pc + 1]
                    self.pc = self.reg[r_address]
                else:
                    # print('fl not equal')
                    self.pc += 2
            elif instruction == NOT:
                reg_a = self.ram[self.pc + 1]
                self.alu('NOT',reg_a)
                self.pc += 2
            
            elif instruction == TEST1:
                # print('in TEST1')
                self.pc += 1 #evaulate the subroutine
            elif instruction == TEST2:
                # print('in TEST2')
                self.pc += 1
            elif instruction == TEST3:
                self.pc += 1
            elif instruction == TEST4:
                self.pc += 1
            elif instruction == TEST5:
                self.pc += 1
            
            elif instruction == JNE: #jump to register if not equal
                # print('in JNE')
                if self.fl != 0b00000001:
                    # print('last comparison values not equal JNE')
                    self.push(self.pc)
                    r_address = self.ram[self.pc + 1]
                    self.pc = self.reg[r_address]
                else:
                    self.pc += 2
            
            elif instruction == JMP:
                # print('in JMP')
                self.push(self.pc)
                r_address = self.ram[self.pc + 1]
                self.pc = self.reg[r_address]
            
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


        