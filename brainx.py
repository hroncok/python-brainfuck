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


