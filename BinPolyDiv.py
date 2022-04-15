"""
BinPolyDiv.py - An implementation of the BinPolyDiv class, which can divide two
    polynomials, calcualting the remainder. Note, this is NOT the same as 
    np.convolve/deconvolve
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


import numpy as np

from BinLFSR import BinLFSR
from bit_array_utils import *

class BinPolyDiv:

  def __init__(self,g, p):
    """
    Constructor for BinPolyDiv
    :param g: The divisor polynomial (integer)
    :param p: The degree of the divisor
    """
    self.g = to_bit_array(g, p + 1)
    self.p = p
    self.lfsr = BinLFSR(g, self.p, initstate=0)

  def _div(self, d):
    """
    Divide a dividend d by the divisor g
    :param d: The dividend (numpy array or list) whose degree is its length-1
    :return: The quotient and remainder in a tuple
    """

    d_vec = d
    self.lfsr.setstate(0)
    state = to_bit_array(self.lfsr.state, self.p)
    remainder = state
    quotient = []

    for j in range(len(d_vec)):

      # shift this bit into the state
      if (remainder[0] % 2) ^ d_vec[j]:
        state[len(state)-1] = 1
      else:
        state[len(state)-1] = 0
      self.lfsr.setstate(from_bit_array(state))
      remainder = state

      result = self.lfsr.step(state=True)
      state = to_bit_array(result[1], self.p)

      # push this bit into the quotient vector
      if j != len(d_vec) - 1:
        quotient.append(remainder[0])

    return np.array(quotient, dtype=int), remainder


  def div(self, d):
    """
    Divide a dividend d by the divisor g, and return the quotient
    :param d: The dividend (numpy array or list) whose degree is its length-1
    :return: The quotient (integer)
    """

    return int(from_bit_array(self._div(d)[0]))

  def remainder(self, d):
    """
    Divide a dividend by the divisor g, and return the remainder
    :param d: The dividend (numpy array or list) whose degree is its length-1
    :return: The quotient (integer)
    """

    return int(from_bit_array(self._div(d)[1]))

if __name__ == "__main__":
  # The following is a test of the BinPolyDiv class
  # An example problem from Moon's "Error Correction Codes" is used as a
  # demonstration

  generator = [1,0,0,0,1,1]
  bin_div = BinPolyDiv(from_bit_array(generator), len(generator) - 1)
  dividend = [1,1,0,1,0,0,0,1,1]
  print("Divider from Moon Example 4.15")
  print("{} / {} = {} R: {}".format(dividend,generator,\
    to_bit_array(bin_div.div(dividend)),\
    to_bit_array(bin_div.remainder(dividend))))
  
  
  generator = 5
  gen_vec = to_bit_array(generator)
  bin_div = BinPolyDiv(generator,len(gen_vec) - 1)
  print("\nCreated a divider with a divisor:",gen_vec)

  for i in range(0,16):
    i_vec = to_bit_array(i,5)
    print(i_vec,"/",gen_vec,"=",to_bit_array(bin_div.div(i_vec),3), \
      "R:",to_bit_array(bin_div.remainder(i_vec),2))

