# -*- coding: utf-8 -*-
# =============================================================================
# Project       : vectorElectronics
# Module name   : -
# File name     : class_AB_subsystem_source.py
# File type     : Python script (Python 3)
# Purpose       : subsystem simulation: current source in the class AB amp
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Friday, 24 October 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# DESCRIPTION
# =============================================================================
# Simulation of a class AB amplifier: the current source/drain subsystem.
#
# Please refer to the schematic in '~/resources/article.pdf' for the 
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

# Current source BJT
Q1 = device.Device("npn")
Q1.addRegion((NEG_INF, 0.0),  (0.0, 0.0),                             "reverse")
Q1.addRegion((0.0, vTh),      (iTh/vTh, 0.0),                         "weak forward active")
Q1.addRegion((vTh, 0.9),      (gm, iTh-gm*vTh),                       "forward active")
Q1.addRegion((0.9, POS_INF),  (gmOvd, 0.9*(gm-gmOvd) + (iTh-gm*vTh)), "forward breakdown")

# Current drain BJT
Q2 = device.Device("pnp")
Q2.addRegion((NEG_INF, 0.0),  (0.0, 0.0),                             "reverse")
Q2.addRegion((0.0, vTh),      (iTh/vTh, 0.0),                         "weak forward active")
Q2.addRegion((vTh, 0.9),      (gm, iTh-gm*vTh),                       "forward active")
Q2.addRegion((0.9, POS_INF),  (gmOvd, 0.9*(gm-gmOvd) + (iTh-gm*vTh)), "forward breakdown")

# Emitter resistors
R_e = 4.7

# Biasing voltage
v_B = 1.5

# Input signal: linear sweep from -0.5V to 0.5V
nPts = 500
delta_v = np.linspace(-0.5, 0.5, nPts)



# =============================================================================
# STEP 1: EVALUATE OUTPUT FOR ALL REGIONS
# =============================================================================
# Solving for 'delta_v' using a linear assumption for Q1 gives the following 
# expression for the collector current I_S = f(delta_v + ...) :
#
# ** see ref_schematics.pdf ***
#
i_S = np.zeros((nPts, Q1.nRegions))
i_D = np.zeros((nPts, Q2.nRegions))

# Current source
for (i, reg) in enumerate(Q1.regions) :
  a = reg.model[0]
  b = reg.model[1]
  i_S[:, i] = delta_v*((-a) / (1 + a*R_e)) + ((a*v_B/2)+b)/((1 + a*R_e))
  print(f"REGION {i} ({reg.name}): {a*R_e / (1 + a*R_e):.3f}")

# Current drain
for (i, reg) in enumerate(Q2.regions) :
  a = reg.model[0]
  b = reg.model[1]
  i_D[:, i] = delta_v*(a / (1 + a*R_e)) + ((a*v_B/2)+b)/((1 + a*R_e))



# =============================================================================
# STEP 2: PICK THE RIGHT SOLUTION FROM EACH REGION
# =============================================================================
# Converse case of the implication: 
# for this 'v_out', does the initial equation still hold?

i_S_valid = np.zeros((nPts, 1))
validRegion = -1

for n in range(nPts) :

  print(f"delta_v = {delta_v[n]:0.4f}V")
  
  validRegion = -1
  for (i, reg) in enumerate(Q1.regions) :

    # Evaluate 'i_S' from its original equation
    i_S_th = Q1.eval(-delta_v[n] + v_B/2 - R_e*i_S[n, i])
    
    # Does that solution make sense?
    # Reminder: 'i_S' is solution iff i_S = f(-delta_v + v_B/2 - R_e*i_S)
    isValid = abs(i_S_th - i_S[n, i]) < 0.0001
    
    # Log the result
    if (isValid) :
      print(f"i_S = {i_S[n, i]:0.4f}V\t\tf(-delta_v + v_B/2 - R_e*i_S) = {i_S_th:0.4f}A\t\t*REGION {i} ({reg.name})")
      if (validRegion != -1) :
        print("[WARNING] There is a valid solution in at least 2 regions.")
      else :
        validRegion = i
      i_S_valid[n] = i_S[n, i]
    else :
      print(f"i_S = {i_S[n, i]:0.4f}V\t\tf(-delta_v + v_B/2 - R_e*i_S) = {i_S_th:0.4f}A\t\t REGION {i} ({reg.name})")
  
  if (validRegion == -1) :
    print("[WARNING] No solution found in any region!")

  print()


i_D_valid = np.zeros((nPts, 1))
validRegion = -1

for n in range(nPts) :  
  validRegion = -1
  for (i, reg) in enumerate(Q2.regions) :

    # Evaluate 'i_D' from its original equation
    i_D_th = Q1.eval(delta_v[n] + v_B/2 - R_e*i_D[n, i])
    
    # Does that solution make sense?
    # Reminder: 'i_D' is solution iff i_D = f(delta_v + v_B/2 - R_e*i_D)
    isValid = abs(i_D_th - i_D[n, i]) < 0.0001
    
    # Log the result
    if (isValid) :
      print(f"i_D = {i_D[n, i]:0.4f}V\t\tf(delta_v + V_B/2 - R_e*i_D) = {i_S_th:0.4f}A\t\t*REGION {i} ({reg.name})")
      if (validRegion != -1) :
        print("[WARNING] There is a valid solution in at least 2 regions.")
      else :
        validRegion = i
      i_D_valid[n] = i_D[n, i]
    else :
      print(f"i_D = {i_D[n, i]:0.4f}V\t\tf(delta_v + V_B/2 - R_e*i_D) = {i_S_th:0.4f}A\t\t REGION {i} ({reg.name})")
  
  if (validRegion == -1) :
    print("[WARNING] No solution found in any region!")

  print()


# =============================================================================
# PLOT OUTPUTS
# =============================================================================
plt.figure()
plt.plot(delta_v, i_S_valid, label = r"$I_S$")
plt.plot(delta_v, i_D_valid, label = r"$I_D$")
plt.xlabel(r"$\Delta V$")
plt.ylabel(r"Collector current $I_C$")
plt.title(r"Class AB subsystem: $I_S$ and $I_D$ vs. input voltage $\Delta V$")
plt.legend()
plt.grid(True)
plt.show()