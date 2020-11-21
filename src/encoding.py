#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/encoding.py

# Author : Irreq

"""
    Encoding for data
    some code has been borrowed, see below
"""


# =============== Start Borrowed Code ======================
#
# Author : Ian Cotter-Llewellyn
# Source : https://github.com/ian-llewellyn/manchester-coding
#
# Code is untouched and just placed in
# this file for ease of readability

class Manchester(object):

    """

    Manchester(differential=True).encode(data)

    # -*- coding: utf-8 -*-

    G. E. Thomas: 0 = 01, 1 = 10
    ISO 802.4: 0 = 10, 1 = 01

    """
    _bit_symbol_map = {
        # bit: symbol
        '0': '01',
        '1': '10',
        'invert': {
            # bit: symbol
            '0': '10',
            '1': '01'},
        'differential': {
            # (init_level, bit): symbol
            ('1', '0'): '01',
            ('0', '0'): '10',
            ('0', '1'): '11',
            ('1', '1'): '00'
        }
    }

    def __init__(self, differential=False, invert=False):
        self._invert = invert
        self._differential = differential
        self._init_level = '0'

    def invert(self):
        self._invert = not self._invert

    def differential(self):
        self._differential = not self._differential

    def decode(self, symbols):
        bits = ''
        while len(symbols):
            symbol = symbols[0:2]
            symbols = symbols[2:]

            if self._differential:
                for ib, s in self._bit_symbol_map['differential'].items():
                    if symbol == s:
                        bits += ib[1]
                continue

            if self._invert:
                for b, s in self._bit_symbol_map['invert'].items():
                    if symbol == s:
                        bits += b
                continue

            for b, s in self._bit_symbol_map.items():
                if symbol == s:
                    bits += b

        return bits

    def encode(self, bits, init_level=None):
        if init_level:
            self._init_level = init_level

        symbols = ''
        for bit in bits:
            # Differential Manchester Coding
            if self._differential:
                symbols += self._bit_symbol_map['differential'][(self._init_level, bit)]
                self._init_level = symbols[-1]
                continue

            # IEEE 802.4 (Inverted Manchester Coding)
            if self._invert:
                symbols += self._bit_symbol_map['invert'][bit]
                continue

            # Manchester Coding
            symbols += self._bit_symbol_map[bit]

        return symbols

# =============== End Borrowed Code ======================

def str_to_bin(data_string, encoding=False):

    """
    String to Binary String Converter Function

     data_string : str()
        encoding : Boolean

         returns : str()
    """

    binary = "".join(f"{ord(i):08b}" for i in data_string) # String to binary conversion

    if encoding:

        binary = Manchester(differential=True).encode(binary) # returns Manchester encoded data

    return binary

def bin_to_str(data_string, encoding=False):

    """
    Binary String to String Converter Function

     data_string : str()
        encoding : Boolean

         returns : str()
    """

    if encoding:

        data = Manchester(differential=True).decode(data_string)

    return ''.join(chr(int(data[i*8:i*8+8],2)) for i in range(len(data)//8))
