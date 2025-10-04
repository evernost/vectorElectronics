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
from typing import Tuple



# =============================================================================
# CONSTANTS
# =============================================================================
# None.



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

    # Internal parameters
    self.regions = []



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

    domain = self._normalise(domain)

    if (len(self.regions) == 0) :
      self.regions.append({
            "domain": domain
          }
        )
    else :
      for R in self.regions :
        if self._hasOverlap(R["domain"], domain) :
          print("[NOTE] Detected conflict in definitions domains")
        else :
          self.regions.append({
              "domain": domain
            }
          )



  # ---------------------------------------------------------------------------
  # METHOD: Device._hasOverlap()                                      [PRIVATE]
  # ---------------------------------------------------------------------------
  def _hasOverlap(self, I : Tuple[float, float], J : Tuple[float, float]) -> bool :
    """
    Returns True if the intervals I = [Ia, Ib] and J = [Ja, Jb] overlap
    False otherwise.
    """
    
    I = self._normalise(I)
    J = self._normalise(J)

    if (I[1] < J[0]) :
      return False
    elif (J[1] < I[0]) :
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
  # METHOD: Device._getOperatingPoint()                               [PRIVATE]
  # ---------------------------------------------------------------------------
  def _getOperatingPoint(self) :
    """
    Description is TODO.
    """

    print("TODO")



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  
  print("[INFO] Class definition 'Device' called as main: running unit tests...")

  Q1 = Device("npn")
  Q1.addRegion((0.0, 0.7), (0.0, 0.0), "off")
  Q1.addRegion((0.7, 100), (0.0, 0.0), "forward active")
  
