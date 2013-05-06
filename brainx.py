#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

class BrainFuck:
    """Brainfuck interpreter."""
    
    def __init__(self, data, memory=b'\x00', memory_pointer=0):
        """Brainfuck interpreter initialization."""
        
        # variables init
        self.memory = bytearray(memory)
        self.memory_pointer = memory_pointer
        self.code = data
        self.user_input = self._findinput(self.code)
        self.output = ""
        
        # DEBUG and tests
        # a) output memory
        self.output = ''
        self._eval(self.code)
    
    #
    # for tests
    #
    def get_memory(self):
        # Don't forget to change this according to your implementation
        return self.memory
    
    def _eval(self,code):
        """Main part of the interpreter, runs the Brainfuck code."""
        p = 0
        while p < len(code):
            # move right
            if code[p] == '>':
                self.memory_pointer += 1
                # not enough space
                if len(self.memory) == self.memory_pointer:
                    self.memory += bytearray([0])
            # move left
            if code[p] == '<':
                if self.memory_pointer > 0:
                    self.memory_pointer -= 1
            # increase value
            if code[p] == '+':
                self.memory[self.memory_pointer] += 1
                # overflow
                if self.memory[self.memory_pointer] == 256:
                    self.memory[self.memory_pointer] = 0
            # decrease value
            if code[p] == '-':
                self.memory[self.memory_pointer] -= 1
                # overflow
                if self.memory[self.memory_pointer] == -1:
                    self.memory[self.memory_pointer] = 255
            # print value
            if code[p] == '.':
                print(chr(self.memory[self.memory_pointer]),end=r'')
                self.output += chr(self.memory[self.memory_pointer])
            # read value
            if code[p] == ',':
                self.memory[self.memory_pointer] = ord(self._readchar())
            # start loop
            if code[p] == '[':
                # get the code inside loop
                loopcode = self._getloopcode(code[p:])
                # run it until zero
                while self.memory[self.memory_pointer] != 0:
                    self._eval(loopcode)
                # move the code pointer (closing ] is +1)
                p += len(loopcode) + 1
            
            # move the code pointer
            p += 1
    
    def _getloopcode(self,code):
        # count [ and ] until thay match
        end = 1
        while (code[0:end].count('[') != code[0:end].count(']')):
            end += 1
        
        # return the code without oepening and closing []
        return code[1:end-1]
    
    def _readchar(self):
        """Read from previously saved input or from stdin if there is no such thing."""
        # no input defined or left
        if len(self.user_input) == 0:
            return sys.stdin.read(1)
        # still some input
        else:
            ret = self.user_input[0]
            self.user_input = self.user_input[1:]
            return ret
    
    def _findinput(self,code):
        """If there is an input after ! save it and cut it out of the code."""
        # find !
        p = 0
        while p < len(code) and code[p] != '!':
            p += 1
        
        # there was !
        if p+1 < len(code):
            # cut it out of the code
            self.code = code[:p]
            return code[p+1:]
        
        # no input
        return ""

class BrainLoller():
    """BrainLoller preprocessor."""
    
    def __init__(self, filename):
        """BrainLoller preprocessor initialization."""
        
        # self.data contains decoded Brainfuck code..
        self.data = ''
        # ...to give to the Brainfuck interpreter
        self.program = BrainFuck(self.data)


class BrainCopter():
    """BrainCopter preprocessor."""
    
    def __init__(self, filename):
        """BrainCopter preprocessor initialization."""
        
        # self.data contains decoded Brainfuck code..
        self.data = ''
        # ...to give to the Brainfuck interpreter
        self.program = BrainFuck(self.data)

#
# just for testing
#
if __name__ == '__main__':
    r"""HelloWorld without \n"""
    with open( 'test_data/hello2.b', encoding='ascii' ) as stream:
        data = stream.read()
    program = BrainFuck(data)
    print("a")
    print(program.output)
