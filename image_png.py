#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class PNGWrongHeaderError(Exception):
    """Exception, that says the input file is probably not PNG file."""
    pass


class PNGNotImplementedError(Exception):
    """Exception, that says the PNG image has a structure we cannot process."""
    pass


class PngReader():
    """Class for reading PNG images."""
    
    def __init__(self, filepath):
        
        # RGB-data from image as a list of rows,
        #   each row contains pixels - triplets of color values
        self.rgb = []
        
        # save the data from the file
        self.binary = open(filepath, mode='rb').read()
        
        # check, if it is PNG
        if (self.binary[0:8] != b'\x89PNG\r\n\x1a\n'):
            raise PNGWrongHeaderError()


#
# just for testing
#
if __name__ == '__main__':
    PngReader('test_data/HelloWorld.png')
