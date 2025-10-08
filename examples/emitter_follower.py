# -*- coding: utf-8 -*-
# =============================================================================
# Project       : vectorElectronics
# Module name   : -
# File name     : emitter_follower.py
# File type     : Python script (Python 3)
# Purpose       : 
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Tuesday, 07 October 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# DESCRIPTION
# =============================================================================




# =============================================================================
# EXTERNALS
# =============================================================================
# Project libraries
import src.device as device
from commons import *

# Standard libraries
import matplotlib.pyplot as plt   # For plotting
import numpy as np                # For math and 'matlab'-like processing



# =============================================================================
# SAMPLE CODE
# =============================================================================
iTh = 0.001   # In A
vTh = 0.7     # In V
gm = 0.5      # In A/V
Q1 = device.Device("npn")
Q1.addRegion((NEG_INF, 0.0),  (0.0, 0.0),       "reverse")
Q1.addRegion((0.0, vTh),      (iTh/vTh, 0.0),   "off")
Q1.addRegion((vTh, 0.9),      (gm, iTh-gm*vTh), "forward active")
Q1.addRegion((0.9, POS_INF),  (0.0, 0.0),       "forward breakdown")

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