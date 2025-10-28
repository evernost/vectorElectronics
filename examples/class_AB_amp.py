# -*- coding: utf-8 -*-
# =============================================================================
# Project       : vectorElectronics
# Module name   : -
# File name     : class_AB_amp.py
# File type     : Python script (Python 3)
# Purpose       : simulation of a BJT final stage amplifier circuit (in class AB)
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Monday, 20 October 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# DESCRIPTION
# =============================================================================
# Simulation of a class AB amplifier.
#
# Please refer to the schematic in '~/resources/ref_schematics.pdf' for the 
# notations, conventions used and the derivations for the equations.



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

# Current source subsystem
Q1 = device.Device("curr_src")
Q1.addRegion((NEG_INF, 0.0), (0.0, 0.0),                             "reverse")


# Current drain subsystem
Q2 = device.Device("curr_drain")
Q2.addRegion((NEG_INF, 0.0),  (0.0, 0.0),                             "reverse")
Q2.addRegion((0.0, vTh),      (iTh/vTh, 0.0),                         "weak forward active")
Q2.addRegion((vTh, 0.9),      (gm, iTh-gm*vTh),                       "forward active")
Q2.addRegion((0.9, POS_INF),  (gmOvd, 0.9*(gm-gmOvd) + (iTh-gm*vTh)), "forward breakdown")

# Emitter resistors
R_e = 4.7

# Biasing voltage
v_B = 1.5

# Output load
R_L = 32

# Input signal: 1Vpp sinewave
nPts = 100
v_in = 1.0*np.sin(np.linspace(0, 2*np.pi, nPts))



# =============================================================================
# STEP 1: EVALUATE OUTPUT FOR ALL REGIONS
# =============================================================================
# Solving for 'v_out' using a linear assumption for Q1/Q2 gives the following 
# expression for the output voltage v_out = f(v_in) :
#
# ** see ref_schematics.pdf ***
#
v_out = np.zeros((nPts, Q1.nRegions*Q2.nRegions))

for (i, regS) in enumerate(Q1.regions) :
  for (j, regD) in enumerate(Q2.regions) :

    # Read the model for that region
    a_S = regS.model[0]
    b_S = regS.model[1]
    a_D = regD.model[0]
    b_D = regD.model[1]

    A_S = a_S/(1 + R_e*a_S)
    B_S = b_S/(1 + R_e*a_S)
    A_D = a_D/(1 + R_e*a_D)
    B_D = b_D/(1 + R_e*a_D)

    # Evaluate the output under that assumption for the model
    idx = j + (Q1.nRegions*i)
    v_out[:, idx] = (R_L / (1 + (A_S+A_D)*R_L)) * ((A_S + A_D)*v_in + (A_S - A_D)*v_B/2 + (B_S - B_D))
    


# =============================================================================
# STEP 2: PICK THE RIGHT SOLUTION FROM EACH REGION
# =============================================================================
# Converse case of the implication: 
# for this 'v_out', does the initial equation still hold?

v_out_valid = np.zeros((nPts, 1))
validRegion = -1

for n in range(nPts) :
  
  print(f"v_in = {v_in[n]:0.4f}V")
  
  validRegion = None
  solCount = 0
  for (i, regS) in enumerate(Q1.regions) :
    for (j, regD) in enumerate(Q2.regions) :

      a_S = regS.model[0]
      b_S = regS.model[1]
      a_D = regD.model[0]
      b_D = regD.model[1]

      A_S = a_S/(1 + R_e*a_S)
      B_S = b_S/(1 + R_e*a_S)
      A_D = a_D/(1 + R_e*a_D)
      B_D = b_D/(1 + R_e*a_D)

      idx = j + (Q1.nRegions*i)
      I_S = A_S*(  v_in[n] - v_out[n, idx]  + v_B/2) + B_S
      I_D = A_D*(-(v_in[n] - v_out[n, idx]) + v_B/2) + B_D
      v_out_th = R_L*(I_S - I_D)

      isValid = abs(v_out_th - v_out[n, idx]) < 0.0001
      if (isValid) :

        print(f"v_out_th = {v_out_th:0.3f} \t\t*v_out[n][{i},{j}] = {v_out[n, idx]:0.3f}")

        if (validRegion is None) :
          validRegion = (i,j)
        
        v_out_valid[n] = v_out[n, idx]
        solCount += 1
      else :
        print(f"v_out_th = {v_out_th:0.3f} \t\t v_out[n][{i},{j}] = {v_out[n, idx]:0.3f}")
    
  if (solCount == 0) :
    print("[WARNING] No solution found in any region!")
  elif (solCount > 1) :
    print("[WARNING] There is a valid solution in at least 2 regions.")

  print()



# =============================================================================
# PLOT OUTPUTS
# =============================================================================
# plt.figure()
# plt.plot(np.linspace(0, 2*np.pi, nPts), v_in        , label = r"$v_{in}$")
# plt.plot(np.linspace(0, 2*np.pi, nPts), v_out_valid , label = r"$v_{out}$")
# plt.xlabel("time (arbitrary)")
# plt.ylabel("voltage")
# plt.title(r"BJT emitter follower: $v_{in}$ vs $v_{out}$ curves")
# plt.legend()
# plt.grid(True)
# plt.show()