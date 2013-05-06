#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zlib

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
        
        self._parse_png()
            
    def _check_png(self):
        """Checks, if it is PNG, strip theheader."""
        if (self.binary[:8] != b'\x89PNG\r\n\x1a\n'):
            raise PNGWrongHeaderError()
            self.binary = self.binary[8:]
        return self
    
    def _bytes_to_num(self,bytes):
        n = 0
        for b in bytes:
            n = n*256 + b
        return n
    
    def _parse_png(self):
        self._check_png()
        p = 0
        self.data = []
        while p < len(self.binary):
            l = self._bytes_to_num(self.binary[p:p+4])
            p += 4
            
            self.data += [{'head':self.binary[p:p+4],
                           'length':l,
                           'data':self.binary[p+4:p+l+4],
                           'crc':self.binary[p+l+4:p+l+8]}]
            
            p += l+8
        return self
    
    def _get_size(self):
        for chunk in self.data:
            if (chunk['head'] == b'IHDR'):
                ihdr = chunk['data']
                break
        self.width = self._bytes_to_num(ihdr[0:4]);
        self.height = self._bytes_to_num(ihdr[4:8]);
        return self;


#
# just for testing
#
if __name__ == '__main__':
    PngReader('test_data/HelloWorld.png')
