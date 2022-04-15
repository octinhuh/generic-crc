"""
bit_array_utils.py - A collection of two functions that convert integer lists
    containing 1's or 0's to integers and vice versa
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

def to_bit_array(num, length=None):
  """
  Converts an integer into a bit array (LSB on right)
  :param num: The number to convert
  :param length: Optional length of bit vector to produce
  :return: numpy array of bits
  """

  # first find order of the number (highest power of 2)
  power = 0
  if length:
    power = length
  else:
    while num // (2 ** power):
      power += 1

    if power == 0:
      power = 1 # prevent an empty list

  arr = []

  # fill arr with values
  for i in range(power):

    arr.append((num // 2 ** (power - i - 1)) % 2)

  return np.array(arr, dtype = int)

def from_bit_array(arr):
  """
  Converts a bit array to an integer
  :param arr: The array (or list) with LSB on the right
  :return: The integer
  """

  integer = 0

  for power in range(len(arr)):
    integer += (arr[len(arr) - power - 1] % 2) * (2 ** power)

  return integer