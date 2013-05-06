#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BrainFuck:
    """Brainfuck interpreter."""
    
    def __init__(self, data, memory=b'\x00', memory_pointer=0):
        """Brainfuck interpreter initialization."""
        
        # program data
        self.data = data
        
        # variables init
        self.memory = memory
        self.memory_pointer = memory_pointer
        
        # DEBUG and tests
        # a) output memory
        self.output = ''
    
    #
    # for tests
    #
    def get_memory(self):
        # Don't forget to change this according to your implementation
        return self.memory
    
    def eval(self,code):
        """Main part of the interpreter, runs the Brainfuck code."""
        p = 0
        while p < len(code):
            # move right
            if code[p] == '>':
                self.memory_pointer += 1
                # not enough space
                if len(self.memory) == self.memory_pointer:
                    self.memory += [0]
            # move left
            if code[p] == '<':
                self.memory_pointer -= 1
            # increase value
            if code[p] == '+':
                self.memory_pointer[p] += 1
                # overflow
                if self.memory_pointer[p] == 256:
                    self.memory_pointer[p] = 0
            # decrease value
            if code[p] == '-':
                self.memory_pointer[p] -= 1
                # overflow
                if self.memory_pointer[p] == -1:
                    self.memory_pointer[p] = 255

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


