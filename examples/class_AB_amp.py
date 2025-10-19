# -*- coding: utf-8 -*-
# =============================================================================
# Project       : vectorElectronics
# Module name   : -
# File name     : class_AB_amp.py
# File type     : Python script (Python 3)
# Purpose       : simulation of a BJT amplifier circuit (in class AB)
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Tuesday, 07 October 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# DESCRIPTION
# =============================================================================
# Description is TODO



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
iTh   = 0.001   # In A
vTh   = 0.7     # In V
gm    = 0.5     # In A/V
gmOvd = 10      # In A/V (overload transconductance)
Q1 = device.Device("npn")
Q1.addRegion((NEG_INF, 0.0),  (0.0, 0.0),                             "reverse")
Q1.addRegion((0.0, vTh),      (iTh/vTh, 0.0),                         "weak forward active")
Q1.addRegion((vTh, 0.9),      (gm, iTh-gm*vTh),                       "forward active")
Q1.addRegion((0.9, POS_INF),  (gmOvd, 0.9*(gm-gmOvd) + (iTh-gm*vTh)), "forward breakdown")

# Emitter resistor
R_e = 100

# Input signal: 1Vpp sinewave + 1.2 Volts offset
nPts = 100
v_in = 1.0*np.sin(np.linspace(0, 2*np.pi, nPts)) + 1.4

# Solving for v_out using a linear assumption gives the following 
# expression for the output voltage v_out = f(v_in) :
#
# v_out = v_in * (R_e*a / (1 + R_e*a)) + R_e*b/(1 + R_e*a)
#
# We now study the values of 'v_out' as we browse through the different values
# of the model.
# Only one will make physical sense.
v_out = np.zeros((nPts, Q1.nRegions))
v_out_valid = np.zeros((nPts, 1))

for n in range(nPts) :
  
  print(f"v_in = {v_in[n]:0.4f}V")
  
  validRegion = -1
  for (i, R) in enumerate(Q1.regions) :
    
    # Read the model for that region
    a = R.model[0]
    b = R.model[1]

    # Evaluate output with that model assumption
    v_out[:, i] = v_in * (R_e*a / (1 + R_e*a)) + R_e*b/(1 + R_e*a)
    
    # Converse case of the implication: 
    # for this 'v_out', does the initial equation still hold?
    v_out_th = R_e*Q1.eval(v_in[n]-v_out[n][i])
    isValid = abs(v_out_th - v_out[n][i]) < 0.0001
    
    # Log the result
    if (isValid) :
      print(f"v_out = {v_out[n][i]:0.4f}V\t\tR_e*f(v_in-v_out) = {v_out_th:0.4f}V\t\t*REGION {i} ({R.name})")
      if (validRegion != -1) :
        print("[WARNING] There is a valid solution in at least 2 regions.")
      else :
        validRegion = i
      v_out_valid[n] = v_out[n, i]
    else :
      print(f"v_out = {v_out[n][i]:0.4f}V\t\tR_e*f(v_in-v_out) = {v_out_th:0.4f}V\t\t REGION {i} ({R.name})")
  
  if (validRegion == -1) :
    print("[WARNING] No solution found in any region!")

  print()

plt.figure()
plt.plot(np.linspace(0, 2*np.pi, nPts), v_in, "k--", label = r"$v_{in}$")

# Plot each column of v_out
for i in range(v_out.shape[1]):
  plt.plot(np.linspace(0, 2*np.pi, nPts), v_out[:, i], label = r"$v_{out}$" + f" ({Q1.regions[i].name})")

plt.xlabel("time (arbitrary)")
plt.ylabel("voltage")
plt.title(r"$v_{in}$ vs $v_{out}$")
plt.legend()
plt.grid(True)
plt.show()


plt.figure()
plt.plot(np.linspace(0, 2*np.pi, nPts), v_in, "k--", label = r"$v_{in}$")
plt.plot(np.linspace(0, 2*np.pi, nPts), v_out_valid, label = r"$v_{out}$")
plt.show()