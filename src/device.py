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
from src.commons import *

# Standard libraries
from typing import Tuple          # For fancy function prototype hints
from enum import Enum             # For fancy status using enum
import matplotlib.pyplot as plt   # For plotting
import numpy as np                # For math and 'matlab'-like processing


# =============================================================================
# CONSTANTS
# =============================================================================

# Helper class: STATUS
class Status(Enum) :
  OK = 0
  FAIL = 1

# Helper class: REGION
class Region : 
  def __init__(self, name, domain, model) :
    self.name = name
    self.domain = domain
    self.model = model

  def belongsTo(self, x) :
    """
    Returns True if the input belongs to the definition domain of this
    region.
    """
    return ((self.domain[0] <= x) & (x <= self.domain[1]))
  
  def eval(self, x) :
    """
    Evaluates the model at location 'x'
    """

    return (self.model[0]*x + self.model[1])



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
    
    self.inputName  = "v_BE"
    self.inputUnit  = "V"
    self.outputName = "I_c"
    self.outputUnit = "mA"

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

    # Sort regions
    self.regions.sort(key = lambda R: R.domain[0])

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
    Returns (b, a) if the input interval is given as (a, b) with b < a.
    """

    if (I[0] > I[1]) :
      return (I[1], I[0])
    else :
      return I



  # ---------------------------------------------------------------------------
  # METHOD: Device.testOperatingPoint()
  # ---------------------------------------------------------------------------
  def testOperatingPoint(self, x) :
    """
    Description is TODO.
    """

    print(f"Input = {x} {self.inputUnit}")

    for R in self.regions :
      if R.belongsTo(x) :
        print(R.name)



  # ---------------------------------------------------------------------------
  # METHOD: Device.eval()
  # ---------------------------------------------------------------------------
  def eval(self, x) :
    """
    Evaluates the device's output using the model matching the input.
    """

    assignCount = np.zeros_like(x, dtype = int)
    y = np.full_like(x, None, dtype = object)
    for R in self.regions :
      mask = R.belongsTo(x)
      assignCount += mask.astype(int)
      y[mask] = R.eval(x[mask])
    
    if np.any(assignCount == 0) :
      print("[WARNING] Some inputs are not covered by the model definition.")

    if np.any(assignCount >= 2) :
      print("[WARNING] Some inputs are covered by the model definition more than once.")

    return y
  


  # ---------------------------------------------------------------------------
  # METHOD: Device.plot()
  # ---------------------------------------------------------------------------
  def plot(self, nPts, range) :
    """
    Plots the device's characteristic curve in a given domain.
    """

    if ((NEG_INF in range) or (POS_INF in range)) :
      print("[ERROR] The plotting domain must be finite.")
      return Status.FAIL
    
    x = np.linspace(-0.25, 0.901, nPts)
    y = Q1.eval(x)
    plt.plot(x, 1000*y)
    plt.xlabel(r"$v_{BE}$ (V)")
    plt.ylabel(r"$i_{C}$ (mA)")
    plt.title(r"$Q_1$ device curve")
    plt.grid(True)
    plt.show()

    return Status.OK



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  
  print("[INFO] Class definition 'Device' called as main: running unit tests...")

  iTh   = 0.001   # In A
  vTh   = 0.7     # In V
  gm    = 0.5     # In A/V
  gmOvd = 10      # In A/V
  Q1 = Device("npn")
  Q1.addRegion((NEG_INF, 0.0),  (0.0, 0.0),                             "reverse")
  Q1.addRegion((0.0, vTh),      (iTh/vTh, 0.0),                         "off")
  Q1.addRegion((vTh, 0.9),      (gm, iTh-gm*vTh),                       "forward active")
  Q1.addRegion((0.9, POS_INF),  (gmOvd, 0.9*(gm-gmOvd) + (iTh-gm*vTh)), "forward breakdown")
  Q1.testOperatingPoint(0.4)
  
  # Plot the model for 'Q1'
  Q1.plot(nPts = 100, range = (-0.1, 0.9))
