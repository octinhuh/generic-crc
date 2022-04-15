"""
BinLFSR.py - A generic binary linear feedback shift register (LFSR) that accepts
    any connection polynomial.
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
from bit_array_utils import *

class BinLFSR:

  def __init__(self, g, n, initstate=1):
    """
    Constructor
    :param g: The connection polynomial
    :param n: The degree of the connection polynomial
    :param initstate: The initial state (seed) of the LFSR
    """

    self.g = g
    self.n = n
    if initstate < 0:
    
      raise Exception("Cannot seed negative numbers in LFSR")  
    self.state = initstate

  def setstate(self, state):
    """
    Set the initial state of the LFSR
    :param state: the state to set the LFSR to
    :return: None
    """

    self.state = state

  def step(self, state=False):
    """
    Step the LFSR by one step
    :param state: If true, return the state in a tuple
    :return: 1-bit output (int), and state (as a tuple, python does not pass
      reference.)
    """

    g_vec = to_bit_array(self.g, self.n + 1)
    state_vec = to_bit_array(self.state, self.n)
    new_state = to_bit_array(self.state * 2, self.n)

    new_state[self.n-1] = state_vec[0]

    # flip the bits with a term in g(x) of this order and 1 below if necessary
    for i in range(0,self.n - 1):
      if g_vec[i+1]:
        new_state[i] = state_vec[i+1] ^ state_vec[0]
    
    # turn the bit array back into a number
    self.state = from_bit_array(new_state)

    if state:
      return new_state[0], self.state
    else:
      return new_state[0]

  def steps(self, nstep, outputs):
    """
    Step the LFSR nstep times
    :param nstep: number of steps to cycle through
    :param outputs: The array to output to
    :return: The list of 1-bit outputs
    """

    for _ in range(nstep):
      outputs.append(self.step())


if __name__ == "__main__":
  # The following is a test of the BinLFSR class

  GENERATOR = [1,0,1,1,1]
  
  lfsr = BinLFSR(from_bit_array(GENERATOR),len(GENERATOR)-1)

  num_steps = 20

  print("Testing LFSR with generator", GENERATOR, "for", num_steps, "steps")
  outputs1 = []
  lfsr.steps(num_steps, outputs1)

  print(outputs1)

  print("Resetting LFSR and displaying its states through each step:")
  lfsr.setstate(1)
  seed = 1
  count = 0
  started = False
  lfsr.setstate(seed)
  print("State at step", count, to_bit_array(lfsr.state,len(GENERATOR)-1))
  while lfsr.state != seed or not started:
    count += 1
    started = True
    print("State at step", count, \
      to_bit_array(lfsr.step(True)[1],len(GENERATOR)-1))
  
  print("The LFSR with a generator", GENERATOR, "has a period of", count)