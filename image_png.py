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
        """PNG reader class initialization."""
        # RGB-data from image as a list of rows,
        #   each row contains pixels - triplets of color values
        self.rgb = []
        
        # save the data from the file
        with open(filepath, mode='rb') as f:
            self.binary = f.read()
        
        self._save()
            
    def _check_png(self):
        """Checks, if it is PNG, strip the header."""
        if (self.binary[:8] != b'\x89PNG\r\n\x1a\n'):
            raise PNGWrongHeaderError()
        self.binary = self.binary[8:]
        return self
    
    def _bytes_to_num(self,bytes):
        """Convert several bytes to one number."""
        n = 0
        for b in bytes:
            n = n*256 + b
        return n
    
    def _parse_png(self):
        """From raw binary data, get chunks and save them. Deletes raw data."""
        self._check_png()
        p = 0
        self.data = []
        while p < len(self.binary):
            l = self._bytes_to_num(self.binary[p:p+4])
            p += 4
            
            self.data += [{'head':self.binary[p:p+4], 'data':self.binary[p+4:p+l+4]}]
            
            p += l+8
        del self.binary
        return self
    
    def _get_size(self):
        """Reads image width and height from IHDR. Also checks, if this image is supported."""
        for chunk in self.data:
            if (chunk['head'] == b'IHDR'):
                ihdr = chunk['data']
                break
        self.width = self._bytes_to_num(ihdr[0:4]);
        self.height = self._bytes_to_num(ihdr[4:8]);
        # check if this is the right type of PNG
        if self._bytes_to_num(ihdr[8:9]) != 8 \
        or self._bytes_to_num(ihdr[9:10]) != 2 \
        or self._bytes_to_num(ihdr[10:11]) != 0 \
        or self._bytes_to_num(ihdr[11:12]) != 0 \
        or self._bytes_to_num(ihdr[12:13]) != 0:
            raise PNGNotImplementedError()
        return self;
    
    def _get_idat(self):
        """Gets IDAT and decompresses it."""
        idat = b''
        for chunk in self.data:
            if (chunk['head'] == b'IDAT'):
                idat += chunk['data']
        
        return zlib.decompress(idat)
    
    def _plus(self,a,b):
        """Add two pixels together."""
        return ((a[0]+b[0])%256,(a[1]+b[1])%256,(a[2]+b[2])%256)
    
    def _paeth_predictor(self,a,b,c):
        """Peath predicator from W3C spec."""
        # a = left, b = above, c = upper left
        res = tuple()
        for i in range(0,3):
            p = (a[i]+b[i]-c[i]) # initial estimate
            pa = abs(p-a[i]) # distances to a, b, c
            pb = abs(p-b[i])
            pc = abs(p-c[i])
        
        
            # return nearest of a,b,c,
            # breaking ties in order a,b,c.
            if (pa <= pb and pa <= pc):
                res += (a[i],)
            elif (pb <= pc):
                res += (b[i],)
            else:
                res += (c[i],)
        return res
    
    def _save(self):
        """Main class method. It saves pixels to 2D array."""
        self._parse_png()._get_size()
        idat = self._get_idat()

        self.rgb = []
        p = 0
        for row in range(0,self.height):
            png_filter = idat[p]
            p += 1
            line = []
            left_pixel = (0,0,0) # when no such thing is, this should be used
            upleft_pixel = (0,0,0) # when no such thing is, this should be used
            for column in range(0,self.width):
                pixel = (idat[p],idat[p+1],idat[p+2])
                p += 3
                # http://www.w3.org/TR/PNG-Filters.html
                if (png_filter == 0):
                    # None
                    line += [pixel]
                elif (png_filter == 1):
                    # Sub
                    left_pixel = self._plus(left_pixel,pixel)
                    line += [left_pixel]
                elif (png_filter == 2):
                    # Up
                    line += [self._plus(pixel,self.rgb[len(self.rgb)-1][column])]
                #elif (png_filter == 3):
                    # Average (not used)
                elif (png_filter == 4):
                    # Paeth
                    up_pixel = self.rgb[len(self.rgb)-1][column]
                    current = self._plus(pixel,self._paeth_predictor(left_pixel,up_pixel,upleft_pixel))
                    line += [current]
                    left_pixel = current
                    upleft_pixel = up_pixel
            self.rgb += [line]

        return self

#
# just for testing
#
if __name__ == '__main__':
    PngReader('test_data/sachovnice_paleta.png')
