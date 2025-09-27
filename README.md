# vectorElectronics

## The issue

Electronic circuits made of:
- resistors
- capacitors
- inductors
- voltage sources
- current sources

are linear and can be solved analytically in the general case using various theorems (Thevenin, Norton, superposition etc.)

However, non-linear devices like diodes, transistors, MOSFETs, etc. require the solutions to equation that can't be solved explicitely.

Even a simple diode in series with a resistor requires approximations in order to understand the transfer function:

<img width="481" height="383" alt="image" src="https://github.com/user-attachments/assets/b1fbdb13-7a38-4019-8a4f-10933642b604" />



## The idea
Piecewise linear functions are dense in the set of continuous real-valued functions.<br>
In other words, any continuous real function can be approximated by a piecewise linear function and the approximation can be made as good as desired.<br>

In this study, we consider a theoretical device with a linear (I,V) transfer curve. We put it in various basic circuits configurations and study how the transfer curve is modified.

