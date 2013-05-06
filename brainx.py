#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from image_png import PngReader as png

class BrainFuck:
    """Brainfuck interpreter."""
    
    def __init__(self, data, memory=b'\x00', memory_pointer=0):
        """Brainfuck interpreter initialization."""
        
        # variables init
        self.memory = bytearray(memory)
        self.memory_pointer = memory_pointer
        
        # let's see if the given data is code or file, let's hope, it's not both :)
        try:
            with open(data, mode='r') as f:
                self.code = f.read()
        except:
            self.code = data
        
        self.user_input = self._findinput()
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
    
    def _findinput(self):
        """If there is an input after ! save it and cut it out of the code."""
        # find !
        p = 0
        while p < len(self.code) and self.code[p] != '!':
            p += 1
        
        # there was !
        if p+1 < len(self.code):
            # cut it out of the code
            self.code = self.code[:p]
            return self.code[p+1:]
        
        # no input
        return ""

class BrainLoller():
    """BrainLoller preprocessor."""
    
    def __init__(self, filename):
        """BrainLoller preprocessor initialization."""
        
        # self.data contains decoded Brainfuck code..
        self.data = self._getcode(filename)
        # ...to give to the Brainfuck interpreter
        self.program = BrainFuck(self.data)
    
    def _getcode(self,filename):
        """Parse the given image and outputs a BrainFuck code."""
        rgb = png(filename).rgb
        p = 0, 0 # starting point
        m = 0, 1 # movement vector (starts east)
        ret = ''
        while not self._out(rgb,p):
            o, m = self._logic(rgb[p[0]][p[1]],m)
            ret += o
            # move
            p = p[0]+m[0], p[1]+m[1]
        return ret
    
    def _logic(self,color,m):
        """Main logic of color commands."""
        o = ''
        if color == (255,0,0):
            o = '>'
        if color == (128,0,0):
            o = '<'
        if color == (0,255,0):
            o = '+'
        if color == (0,128,0):
            o = '-'
        if color == (0,0,255):
            o = '.'
        if color == (0,0,128):
            o = ','
        if color == (255,255,0):
            o = '['
        if color == (128,128,0):
            o = ']'
        if color == (0,255,255): # turn right
            m = self._turn(m,"right")
        if color == (0,128,128): # turn left
            m = self._turn(m,"left")
        return o, m
    
    def _turn(self,movement_vector,direction):
        """For given direction (left or right) returns turned movement vector."""
        if direction == "right":
            if movement_vector[0] == 0:
                return movement_vector[1], movement_vector[0]
            else:
                return movement_vector[1], -movement_vector[0]
        if direction == "left":
            if movement_vector[0] != 0:
                return movement_vector[1], movement_vector[0]
            else:
                return -movement_vector[1], movement_vector[0]
    
    def _out(self,rgb,p):
        """Is the given coordinate p out of the 2D array rgb?"""
        return p[0] == len(rgb) or p[1] == len(rgb[0]) or p[0] < 0 or p[1] < 0


class BrainCopter(BrainLoller):
    """BrainCopter preprocessor."""
    def _logic(self,color,m):
        """Main logic of color commands."""
        o = ''
        command = (-2*color[0] + 3*color[1] + color[2])%11
        bf = '><+-.,[]'
        if command < 8:
            o = bf[command]
        if command == 8: # turn right
            m = self._turn(m,"right")
        if command == 9: # turn left
            m = self._turn(m,"left")
        return o, m

#
# just for testing
#
if __name__ == '__main__':
    BrainFuck("test_data/hello1.b")
    #BrainLoller("test_data/HelloWorld.png")
    #BrainCopter("test_data/lk.png")
