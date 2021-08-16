import matplotlib.pyplot as plt
import numpy as np
from math import pi
import sympy
from sympy import symbols,sympify
from sympy.functions import arg
from sympy.utilities.lambdify import lambdify
z = symbols('z')

Hz = (z**7+ z**6 +z**5 + z**4 + z**3 +z**2 + z+1)/(2*(z**7))

def update_Hz(input):
    global Hz
    Hz = sympify(input)


def evalHz(N):
    k = np.linspace(0,N-2,N)
    func = lambdify(z,Hz,'numpy')
    H = func(np.exp(1j*((2*np.pi*k)/N)))
    H = H/np.amax(np.abs(H))
    return H 

def plot_Hz(N, funcname ='H', plotMag = True, plotPhase = True):
    k = np.linspace(0,N-2,N)
    H = evalHz(N)
    magH = np.abs(H)
    phaseH = np.angle(H)
    hn = np.real(np.fft.ifft(H))
    if plotMag:
        plt.figure()
        plt.plot(k,magH)
        plt.ylabel('$|%s(e*{j\omega})|$'%funcname)
        plt.xlabel('$\omega/\pi$')
        plt.grid()
    if plotPhase:
        plt.figure()
        plt.plot(hn)
        plt.ylabel('$\measuredangle %s(e*{j\omega})$'%funcname)
        plt.xlabel('$\omega/\pi$')
        plt.grid()
    plt.show()


def lowpass(cutoff,CHUNK):
    w = np.linspace(0,CHUNK-2,CHUNK)
    return 1*(w <= cutoff)

def highpass(cutoff,CHUNK):
    w = np.linspace(0,CHUNK-2,CHUNK)
    return 1*(w >= cutoff)

def bandpass(lowcut,highcut,CHUNK):
    w = np.linspace(0,CHUNK-2,CHUNK)
    return 1*((w >= lowcut) & (w<=highcut))

def bandstop(lowcut,highcut,CHUNK):
    w = np.linspace(0,CHUNK-2,CHUNK)
    return 1*((w <= lowcut) | (w >=highcut))
       
# #***********If h[n] is given************
def hn_filter(hn,CHUNK):
    '''
    xn: (np.array 1D)
    hn: (np.array 1D)
    yn: (np.array 1D)
    '''
    H_z = np.fft.fft(hn,CHUNK)
    H_z = H_z/np.amax(H_z)
    return H_z

def zeros_filter(zeors,CHUNK):
    global Hz
    Hz = 1
    for zero in zeors:
        Hz = Hz*(z - zero)
    return evalHz(CHUNK)

def lccde_filter(b,CHUNK):
    num = np.poly1d(b)
    global Hz
    Hz = 1.0
    zeros = num.roots
    for zero in zeros:
        Hz = Hz*(z - zero)
    return evalHz(CHUNK)

