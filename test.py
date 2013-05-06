#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

# tested modules
import brainx
import image_png



#
# Class with temporary fake output
#

import sys

class FakeStdOut:
    def write(self, *args, **kwargs):
        pass
    def flush(self):
        pass



#
# Classes with tests
#

class TestBrainfuck(unittest.TestCase):
    """Tests the Brainfuck interpreter."""
    
    def setUp(self):
        self.BF = brainx.BrainFuck
        # skrytí výstupu
        self.out = sys.stdout
        sys.stdout = FakeStdOut()
    
    def tearDown(self):
        sys.stdout = self.out
   
    def test_bf_01(self):
        """zero current cell"""
        program = self.BF('[-]', memory=b'\x03\x02', memory_pointer=1)
        self.assertEqual(program.get_memory(), b'\x03\x00')
    
    def test_bf_02(self):
        """zero all non-zero cells to left"""
        program = self.BF('[[-]<]', memory=b'\x03\x03\x00\x02\x02', memory_pointer=4)
        self.assertEqual(program.get_memory(), b'\x03\x03\x00\x00\x00')
    
    def test_bf_03(self):
        """move to the first non-zero cell to left"""
        program = self.BF('[<]', memory=b'\x03\x03\x00\x02\x02', memory_pointer=4)
        self.assertEqual(program.memory_pointer, 2)
    
    def test_bf_04(self):
        """move to the first non-zero cell to right"""
        program = self.BF('[>]', memory=b'\x03\x03\x00\x02\x02')
        self.assertEqual(program.memory_pointer, 2)
    
    def test_bf_05(self):
        """destructive addition of the current cell to the next one"""
        program = self.BF('[>+<-]', memory=b'\x03\x03')
        self.assertEqual(program.get_memory(), b'\x00\x06')
    
    def test_bf_06(self):
        """non-destructive addition of the current cell to the next one"""
        program = self.BF('[>+>+<<-]>>[<<+>>-]', memory=b'\x03\x03')
        self.assertEqual(program.get_memory(), b'\x03\x06\x00')
    
    def test_bf_07(self):
        """destructive removeal of the current cell from the next one"""
        program = self.BF('[>-<-]', memory=b'\x03\x05')
        self.assertEqual(program.get_memory(), b'\x00\x02')
    
    def test_bf_11(self):
        r"""HelloWorld with \n"""
        with open( 'test_data/hello1.b', encoding='ascii' ) as stream:
            data = stream.read()
        program = self.BF(data)
        self.assertEqual(program.output, 'Hello World!\n')
    
    def test_bf_12(self):
        r"""HelloWorld without \n"""
        with open( 'test_data/hello2.b', encoding='ascii' ) as stream:
            data = stream.read()
        program = self.BF(data)
        self.assertEqual(program.output, 'Hello World!')


class TestBrainfuckWithInput(unittest.TestCase):
    """Tests the Brainfuck interpreter using programs with defined input."""
    
    def setUp(self):
        self.BF = brainx.BrainFuck
        # skrytí výstupu
        self.out = sys.stdout
        sys.stdout = FakeStdOut()
    
    def tearDown(self):
        sys.stdout = self.out
    
    def test_bf_input_2(self):
        """numwarp.b with '123' input"""
        with open( 'test_data/numwarp_input.b', encoding='ascii' ) as stream:
            data = stream.read()
        program = self.BF(data)
        self.assertEqual(program.output, '    /\\\n     /\\\n  /\\  /\n   / \n \\ \\/\n  \\\n   \n')


class TestPNG(unittest.TestCase):
    """Tests correct load of PNG images."""
    
    def setUp(self):
        self.png = image_png.PngReader
        # skrytí výstupu
        self.out = sys.stdout
        sys.stdout = FakeStdOut()
    
    def tearDown(self):
        sys.stdout = self.out
    
    def test_png_01(self):
        """only support PNGs"""
        self.assertRaises( image_png.PNGWrongHeaderError, self.png, 'test_data/sachovnice.jpg' )
    
    def test_png_02(self):
        """only support some PNGs"""
        self.assertRaises( image_png.PNGNotImplementedError, self.png, 'test_data/sachovnice_paleta.png' )
    
    def test_png_03(self):
        """simple PNG load"""
        image = self.png('test_data/sachovnice.png')
        self.assertEqual( image.rgb, [[(255, 0, 0), (0, 255, 0), (0, 0, 255)], [(255, 255, 255), (127, 127, 127), (0, 0, 0)], [(255, 255, 0), (255, 0, 255), (0, 255, 255)]] )


class TestBrainloller(unittest.TestCase):
    """Tests the BrainLoller interpreter."""
    
    def setUp(self):
        self.BF = brainx.BrainFuck
        self.BL = brainx.BrainLoller
        # hide output
        self.out = sys.stdout
        sys.stdout = FakeStdOut()
    
    def tearDown(self):
        sys.stdout = self.out
    
    def test_bl_1a(self):
        """load data from HelloWorld.png image"""
        obj = self.BL('test_data/HelloWorld.png')
        self.assertEqual(obj.data, '>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+.')
    
    def test_bl_1b(self):
        """run the program from HelloWorld.png image"""
        obj = self.BL('test_data/HelloWorld.png')
        self.assertEqual(obj.program.output, 'Hello World!')


#
# Run the tests when this script is run
#
if __name__ == '__main__':
    unittest.main()
