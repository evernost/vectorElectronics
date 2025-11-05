# -*- coding: utf-8 -*-
# =============================================================================
# Project       : vectorElectronics
# Module name   : -
# File name     : emitter_follower.py
# File type     : Python script (Python 3)
# Purpose       : simulation of a 'rubber diode' circuit
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Sunday, 02 November 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# DESCRIPTION
# =============================================================================
# Piecewise linear model used to simulate the 'rubber diode' circuit.



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
# SETTINGS
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

R1 = 1000
R2 = 2200

# Input signal: linear sweep from 0 to 2V
nPts = 100
v_in = np.linspace(0, 2.0, nPts)



# =============================================================================
# STEP 1: EVALUATE OUTPUT FOR ALL REGIONS
# =============================================================================
# Solving for 'i_out' using a linear assumption gives the following 
# expression for the current i = f(v) :
#
# i_out = v_in*(1 + a*R2)/(R1 + R2) + b
#
i_out = np.zeros((nPts, Q1.nRegions))

for (i, reg) in enumerate(Q1.regions) :
  
  # Read the model for that region
  a = reg.model[0]
  b = reg.model[1]

  # Evaluate the output under that assumption
  i_out[:, i] = v_in * (1 + a*R2)/(R1 + R2) + b



# =============================================================================
# STEP 2: PICK THE RIGHT SOLUTION FROM EACH REGION
# =============================================================================
# Converse case of the implication: 
# for this 'v_out', does the initial equation still hold?
i_out_valid = np.zeros((nPts, 1))
validRegion = -1

# Check point by point
for n in range(nPts) :

  print(f"v_in = {v_in[n]:0.4f}V")
  
  validRegion = -1
  for (i, reg) in enumerate(Q1.regions) :

    # Evaluate 'v_out' from its original equation
    i_out_th = v_in[n]/(R1+R2) + Q1.eval(v_in[n]*R2/(R1+R2))
    
    # Does that solution make sense?
    # Reminder: 'i_out' is solution iff i_out = R_e*f(v_in-v_out)
    isValid = abs(i_out_th - i_out[n][i]) < 0.0001
    
    # Log the result
    if (isValid) :
      print(f"v_out = {i_out[n][i]:0.4f}V\t\tR_e*f(v_in-v_out) = {i_out_th:0.4f}V\t\t*REGION {i} ({reg.name})")
      if (validRegion != -1) :
        print("[WARNING] There is a valid solution in at least 2 regions.")
      else :
        validRegion = i
      i_out_valid[n] = i_out[n, i]
    else :
      print(f"v_out = {i_out[n][i]:0.4f}V\t\tR_e*f(v_in-v_out) = {i_out_th:0.4f}V\t\t REGION {i} ({reg.name})")
  
  if (validRegion == -1) :
    print("[WARNING] No solution found in any region!")

  print()



# =============================================================================
# PLOT OUTPUTS
# =============================================================================
plt.figure()
plt.plot(v_in, i_out_valid , label = r"$v_{out}$")
plt.xlabel("time (arbitrary)")
plt.ylabel("voltage")
plt.title(r"BJT emitter follower: $v_{in}$ vs $v_{out}$ curves")
plt.legend()
plt.grid(True)
plt.show()


plt.figure()
plt.plot(np.linspace(0, 2*np.pi, nPts), v_in, "k--", label = r"$v_{in}$")
for i in range(v_out.shape[1]):
  plt.plot(np.linspace(0, 2*np.pi, nPts), v_out[:, i], label = r"$v_{out}$" + f" ({Q1.regions[i].name})")
plt.xlabel("time (arbitrary)")
plt.ylabel("voltage")
plt.title(r"$v_{in}$ vs $v_{out}$")
plt.legend()
plt.grid(True)
plt.show()


