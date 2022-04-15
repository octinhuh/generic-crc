"""
CRC.py - A generic cyclic redundancy check (CRC) script that accepts any valid 
    CRC generator polynomial or payload length (in bytes).
    Copyright (C) 2022  Austin Grieve

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from BinLFSR import BinLFSR
from bit_array_utils import *
from BinPolyDiv import BinPolyDiv
import numpy as np

ITEM_SIZE = 8 # size of a byte

class CRC:

  def __init__(self, g, n):
    """
    Constructor
    :param g: The generator polynomial (integer)
    :param n: Length of a payload (bytes)
    """

    self.g = g
    self.n = n
    self.crc_len = len(to_bit_array(g))
    self.divider = BinPolyDiv(g,self.crc_len - 1)

  def encode_bytes(self, m, size=ITEM_SIZE):
    """
    Encode a given message byte (integer)
    :param m: The message vector (array of integers, length n)
    :param size: The size of each byte (default 8)
    :return: The codeword (array of bits)
    """

    # c(x) = x^12m(x) + d(x)

    # turn message bytes into a list of bits
    c_list = []
    for i in range(self.n):
      for j in range(ITEM_SIZE-1,-1,-1):
        c_list.append((m[i] // (2**j)) % 2)

    # append 0's to the end of this vector (multiplying by x^crc_len)
    for i in range(self.crc_len-1):
      c_list.append(0)

    # get remainder from the divider circuit
    r = to_bit_array(self.divider.remainder(c_list),self.crc_len-1)

    # add the remainder to the codeword
    for i in range(self.n * ITEM_SIZE, len(c_list)):
      c_list[i] = r[i - (self.n * ITEM_SIZE)]

    return c_list

  def decode(self, received):
    """
    Decode a given bitstream, and pass back the original list of bytes
    :param r: The received stream (list or array of bits)
    :return: list of integers representing decoded items and remainder (int)
      as a (tuple)
    """

    # find if an error was transmitted
    remainder = self.divider.remainder(received)
    
    m_list = []
    for i in range(self.n):
      m_list.append(from_bit_array(\
        received[i*ITEM_SIZE:i*ITEM_SIZE + ITEM_SIZE]))

    return m_list, remainder

# A demonstration of the CRC class using CRC_ANSI
if __name__ == "__main__":

  CRC_GEN =  0x18005 # CRC-ANSI generator

  payload = [0x6d,0x27]
  bigger_payload = [0,1,2,3,4,5,6,7,8,9,0xA,0xB,0xC,0xD,0xE,0xF,0xA1,0xB2,0xC3,\
    0xD4,0xE5,0xF6,0xA7,0xB8,0xC9,0xDA,0xEB,0xFC]
  
  crc = CRC(CRC_GEN, len(payload))
  bigger_crc = CRC(CRC_GEN, len(bigger_payload))

  print("Testing the encoding and decoding of CRC-{} with payload {}"\
    .format(len(to_bit_array(CRC_GEN)) - 1, payload))

  encoded = crc.encode_bytes(payload)

  print("Encoded payload as:\t", encoded)
  decoded = crc.decode(encoded)
  print("Decoded payload as:\t", decoded[0], end=" ")
  if decoded[1]:
    print("(Error detected) Remainder: %d\n" % decoded[1])
  else:
    print("(No error detected)\n")

  print("Testing error detection by introducing errors in positions:")
  errors = [13,20] # positions to introduce errors
  print(errors)
  
  for pos in errors:
    encoded[pos] = (encoded[pos] ^ 1) % 2

  decoded = crc.decode(encoded)
  print("Encoded with errors as:\t", encoded)
  decoded = crc.decode(encoded)
  print("Decoded payload as:\t", decoded[0], end=" ")
  if decoded[1]:
    print("(Error detected) Remainder: %d\n" % decoded[1])
  else:
    print("(No error detected)\n")

  print("Testing with payload:\t", bigger_payload)
  encoded = bigger_crc.encode_bytes(bigger_payload)
  print("Encoded payload as:", encoded)
  decoded = bigger_crc.decode(encoded)
  print("Decoded payload as:\t", decoded[0], end=" ")
  if decoded[1]:
    print("(Error detected) Remainder: %d\n" % decoded[1])
  else:
    print("(No error detected)\n")
