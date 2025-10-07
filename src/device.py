# -*- coding: utf-8 -*-
# =============================================================================
# Project       : vectorElectronics
# Module name   : device
# File name     : device.py
# File type     : Python script (Python 3)
# Purpose       : generic model for electronic parts
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Monday, 29 September 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# DESCRIPTION
# =============================================================================
# A 'Device' object is a generic model for any electronic part.
# It models it as a bunch of piecewise linear functions.
# 
# The idea is to assume that the component has a linear characteristic.
# In the most general case, that characteristic is not linear and the key part
# is to try to find what part of the piecewise linear model is active depending
# on the current operating conditions of the circuit.



# =============================================================================
# EXTERNALS
# =============================================================================
# Project libraries
# None.

# Standard libraries
from typing import Tuple          # For fancy function prototype hints
from enum import Enum             # For fancy status using enum
import matplotlib.pyplot as plt   # For plotting
import numpy as np                # For math and 'matlab'-like processing


# =============================================================================
# CONSTANTS
# =============================================================================
POS_INF = float("inf")
NEG_INF = float("-inf")

class Status(Enum) :
  OK = 0
  FAIL = 1

class Region : 
  def __init__(self, name, domain, model) :
    self.name = name
    self.domain = domain
    self.model = model

  def belongsTo(self, x) :
    return ((self.domain[0] <= x) and (x <= self.domain[1]))


# =============================================================================
# CLASS DEFINITION
# =============================================================================
class Device :

  """
  DEVICE object
  
  Description is TODO.
  """

  def __init__(self, name) :
    
    # Name of your device
    self.name = name
    self.inUnits  = ""
    self.outUnits = ""

    # Internal parameters
    self.regions = []
    self.nRegions = 0



  # ---------------------------------------------------------------------------
  # METHOD: Device.addRegion()
  # ---------------------------------------------------------------------------
  def addRegion(self, domain : Tuple[float, float], model : Tuple[float, float], name : str = "") -> None :
    """
    Adds a new operating region to the device.

    The function looks for overlaps and prevents adding a new region if there 
    is a conflict in the domain definition.

    Arguments:
    - domain  = (xMin, xMax)  : domain definition
    - model   = (a, b)        : parameters for the model y = a*x + b
    - name                    : name of the region (optional)
    """

    # Swap the bounds in case they are inverted
    domain = self._normalise(domain)

    # Compare the domain definition against what already exists
    for R in self.regions :
      if self._hasOverlap(R.domain, domain) :
        print("[WARNING] Detected conflict in definitions domains")
        return Status.FAIL

    # Add the region
    self.regions.append(Region(name, domain , model))
    self.nRegions += 1
    print(f"[NOTE] Added model definition: {domain[0]} -> {domain[1]}")
    return Status.OK



  # ---------------------------------------------------------------------------
  # METHOD: Device._hasOverlap()                                      [PRIVATE]
  # ---------------------------------------------------------------------------
  def _hasOverlap(self, I, J) -> bool :
    """
    Returns True if the intervals I = [Ia, Ib] and J = [Ja, Jb] have a 
    non-empty intersection.
    Returns False otherwise.
    """
    
    I = self._normalise(I)
    J = self._normalise(J)

    if (I[1] <= J[0]) :
      return False
    elif (J[1] <= I[0]) :
      return False
    else :
      return True
      


  # ---------------------------------------------------------------------------
  # METHOD: Device._normalise()                                       [PRIVATE]
  # ---------------------------------------------------------------------------
  def _normalise(self, I : Tuple[float, float]) -> Tuple[float, float] :
    """
    Returns a normalised version of an interval.
    """

    if (I[0] > I[1]) :
      return (I[1], I[0])
    else :
      return I



  # ---------------------------------------------------------------------------
  # METHOD: Device.getOperatingPoint()
  # ---------------------------------------------------------------------------
  def getOperatingPoint(self, x) :
    """
    Description is TODO.
    """

    for R in self.regions :
      if ((R.domain[0] <= x) and (x <= R.domain[1])) :
        print(R.name)



  # ---------------------------------------------------------------------------
  # METHOD: Device.eval()
  # ---------------------------------------------------------------------------
  def eval(self, x) :
    """
    Evaluates the device's output using the model matching the input.
    """

    return 0.0
  


  # ---------------------------------------------------------------------------
  # METHOD: Device.plot()
  # ---------------------------------------------------------------------------
  def plot(self, domain) :
    """
    Plots the device's characteristic curve in a given domain.
    """

    if ((NEG_INF in domain) or (POS_INF in domain)) :
      print("[ERROR] The plotting domain must be finite.")
      return Status.FAIL  
    
    return Status.OK



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  
  print("[INFO] Class definition 'Device' called as main: running unit tests...")

  iTh = 0.001   # In A
  vTh = 0.7     # In V
  gm = 0.5      # In A/V
  Q1 = Device("npn")
  Q1.addRegion((NEG_INF, 0.0),  (0.0, 0.0),       "reverse")
  Q1.addRegion((0.0, vTh),      (iTh/vTh, 0.0),   "off")
  Q1.addRegion((vTh, 0.9),      (gm, iTh-gm*vTh), "forward active")
  Q1.addRegion((0.9, POS_INF),  (0.0, 0.0),       "forward breakdown")
  Q1.getOperatingPoint(0.4)
  


  # ---------------------------------------------------------------------------
  # Example 1: emitter follower
  # ---------------------------------------------------------------------------

  # Emitter resistor
  R_e = 100

  # Input signal: 1Vpp sinewave + 2 Volts offset
  nPts = 20
  v_in = 1.0*np.sin(np.linspace(0, 2*np.pi, nPts)) + 2.0

  # Solving using the linear assumption gives the output voltage:
  # v_out = v_in * (R_e*a / (1 + R_e*a)) + R_e*b/(1 + R_e*a)
  #
  # We now study the values of 'v_out' as we browse through the different values
  # of the model.
  # Only one will make physical sense.
  v_out = np.zeros((nPts, Q1.nRegions))

  for n in range(nPts) :
    
    print(f"v_in = {v_in[n]:0.4f}V")
    
    for (i, R) in enumerate(Q1.regions) :
      a = R.model[0]
      b = R.model[1]
      v_out_reg = v_in * (R_e*a / (1 + R_e*a)) + R_e*b/(1 + R_e*a)

      v_out[:, i] = v_out_reg

      #print(f"*** REGION {i}: y = {a:0.5f}x + {b:0.5f} ***")
      consCheck = R.belongsTo(v_in[n]-v_out[n][i])
      print(f"v_out = {v_out[n][i]:0.4f}V\t\tv_in-v_out = {v_in[n]-v_out[n][i]:0.4f}V\t\tConsistent? {consCheck}\t\tREGION {i} ({R.name})")
    
    print()


plt.plot(np.linspace(0, 2*np.pi, nPts), v_in, 'k--', label="v_in")

# Plot each column of v_out
for i in range(v_out.shape[1]):
  plt.plot(np.linspace(0, 2*np.pi, nPts), v_out[:, i], label = f"v_out ({Q1.regions[i].name})")

plt.xlabel("time (arbitrary)")
plt.ylabel("voltage")
plt.title("v_in vs v_out")
plt.legend()
plt.grid(True)
plt.show()