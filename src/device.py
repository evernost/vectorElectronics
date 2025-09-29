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
# None.



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
    
    self.name = name



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
