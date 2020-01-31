LDI = 0b10000010
CMP = 0b10100111
HLT = 0b00000001

import sys

class LS8:
    def __init__(self):
        self.pc = 0
        self.ram = [0]*256 #ls8 is a 8 bit processor, at most, it can process a total of 2^8 = 256 bytes in memory
        self.reg = [0]*8  #ls8 has 8 registers for usege
        self.sp = -1 #initial stack pointer at the end of the ram

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

    def ldi(self,r_address,val): #load immediate
        self.reg[r_address] = val

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
                self.pc += 2

            elif instruction == HLT:
                self.pc += 1
                halted = True
                sys.exit()
            
            else:
                print(f"error occured at index: {self.pc}")
                raise IndexError
                sys.exit()

ls8 = LS8()
ls8.run()


        