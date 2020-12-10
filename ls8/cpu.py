"""CPU functionality."""

import sys

class methods:
    LDI = 0b10000010
    PRN = 0b1000111
    HLT = 0b1
    MUL = 0b10100010
    PUSH = 0b01000101 
    POP = 0b01000110
    
class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.ir = 0
        self.mar = 0
        self.fl = 0
        self.stack_pointer = 7
        self.memory = []
        self.running = True
    
    def ram_read(self,address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        program = []
        file = open(f'./examples/{filename}.ls8', 'r')
        lines = file.readlines()

        for line in lines:
            if line == '':
                pass
            else:
                split = line.split('#',1)
                if split[0] == '' or split[0] == '\n':
                    pass
                else:
                    final = split[0].split('\n')
                    binary = int('0b' + final[0], 2)
                    program.append(binary)

        file.close()
        stack_space = 256 - len(program)
        mem = program + [0] * stack_space
        self.reg[self.stack_pointer] = len(mem) - 1
        print(mem)
        for instruction in program:
            self.ram[address] = instruction
            address += 1
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        while self.running:
            command = self.ram_read(self.pc)
            if command == methods.LDI:
                op_1 = self.ram_read(self.pc + 1)
                op_2 = self.ram_read(self.pc + 2)

                self.reg[op_1] = op_2
                self.pc += 3
            elif command == methods.PRN:
                op_1 = self.ram_read(self.pc + 1)
                print(self.reg[op_1])
                self.pc += 2
            elif command == methods.MUL:
                op_1 = self.ram_read(self.pc + 1)
                op_2 = self.ram_read(self.pc + 2)
                self.reg[op_1] = op_1 * op_2
                self.pc += 3
            elif command == methods.HLT:
                self.running = False
                self.pc += 1
            elif command == methods.PUSH:
                self.reg[self.stack_pointer] -= 1
                op_1 = self.ram_read(self.pc+1)
                val_in_reg = self.reg[op_1]
                self.ram[self.reg[self.stack_pointer]] = val_in_reg
                self.pc += 2
            elif command == methods.POP:
                op_1 = self.ram_read(self.pc + 1)

                self.reg[op_1] = self.ram[self.reg[self.stack_pointer]]
                
                self.reg[self.stack_pointer] += 1
                self.pc += 2


