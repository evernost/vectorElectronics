# -*- coding: utf-8 -*-
# =============================================================================
# Project       : vectorElectronics
# Module name   : -
# File name     : ring_mod.py
# File type     : Python script (Python 3)
# Purpose       : simulation of a ring modulator
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Saturday, 18 October 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# DESCRIPTION
# =============================================================================
# Simulation of a diode ring (aka 'ring modulator') using a simple piecewise
# linear model.



# =============================================================================
# EXTERNALS
# =============================================================================
# Project libraries
import src.device as device
from src.commons import *

# Standard libraries
import matplotlib.pyplot as plt   # For plotting
import numpy as np                # For math and 'matlab'-like processing



# =============================================================================
# SAMPLE CODE
# =============================================================================

D1 = device.Device("diode")
D1.addRegion((NEG_INF, 0.0),  (0.0, 0.0),                             "reverse")
Q1.addRegion((0.0, vTh),      (iTh/vTh, 0.0),                         "weak forward active")
Q1.addRegion((vTh, 0.9),      (gm, iTh-gm*vTh),                       "forward active")
Q1.addRegion((0.9, POS_INF),  (gmOvd, 0.9*(gm-gmOvd) + (iTh-gm*vTh)), "forward breakdown")

# Polarisation resistors
R = 470

# Input signal: 1Vpp sinewave + 1.2 Volts offset
nPts = 100
v_in = 1.0*np.sin(np.linspace(0, 2*np.pi, nPts)) + 1.4
