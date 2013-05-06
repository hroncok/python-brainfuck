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
        
        # RGB-data obrázku jako seznam seznamů řádek,
        #   v každé řádce co pixel, to trojce (R, G, B)
        self.rgb = []
