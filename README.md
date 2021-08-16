# Real-Time-Audio-Filtering-using-Python


Platform for Audio Filtering (Digital Filters) in Real-Time using Convolution Theorem and Fast Fourier Transform.

# Features
* Users to configure the specification of the filter using impulse response of the system h[n], H(z) Transfer fucntion either by H(z) equation or by giving zeros/poles of H(z), LCCDE coefficients, and cut-off frequency.

* It also have in-built Ideal filters like Low Pass Filter, High Pass Filter, Band Pass Filter, and Band Stop filter.

* Users can also Save the Filtered Audio, and Plot the Frequency Response of the ideal as well as custom filters.

# Implementation
* Use Pyaudio to get audio in real time.
* Matpoltlib for visualization.
* Tkinter For UI.

![](https://github.com/deependra227/Real-Time-Audio-Filtering-using-Python/blob/master/images/dsp%20block%20diagram.PNG)</br>

In time domain, filtering is convolution of input x[n] and impulse response of h[n].
<br>
<br>
y[n] = Σ x[k]*h[n-k]
<br>
<br>
where is y[n] is filtered audio.
<br>
<br>
Convolution in time domain is same as product in frequency domain. In frequency domain,
<br>
Y(e<sup>jw</sup>) = X(e<sup>jw</sup>)H(e<sup>jw</sup>)
<br>
<br>
To Convert back into time domain, we have to take inverse dft. Fast and efficient way to take dft is ifft.
<br>
<br>
y[n] = IFFT(Y(e<sup>jw</sup>))
<br>
<br>
# Controls
![](https://github.com/deependra227/Real-Time-Audio-Filtering-using-Python/blob/master/images/controls.PNG)</br>


# Demo
Audio Waveform
![](https://github.com/deependra227/Real-Time-Audio-Filtering-using-Python/blob/master/images/audio%20waveform.PNG)</br>

We have use a low pass filter to filter out high frequency audio.

![](https://github.com/deependra227/Real-Time-Audio-Filtering-using-Python/blob/master/images/H(e%5Ejw).png)</br>
![](https://github.com/deependra227/Real-Time-Audio-Filtering-using-Python/blob/master/images/freq%20response.png)</br>
![](https://github.com/deependra227/Real-Time-Audio-Filtering-using-Python/blob/master/images/zeros%26poles.png)</br>

* When low frequency audio was passed through the filter.Audio was allowed to pass.

![](https://github.com/deependra227/Real-Time-Audio-Filtering-using-Python/blob/master/images/low%20frequency%20for%20low%20pass.png)</br>
<br>
* When High Frequecny audio was passed through the filter. Audio was blocked and was not allowed to pass.

![](https://github.com/deependra227/Real-Time-Audio-Filtering-using-Python/blob/master/images/low%20pass%20filter.PNG)</br>

* When Ideal Low Pass filter was applied. On decreasing the low cut off frequency the higher frequency audio was blocked.

![](https://github.com/deependra227/Real-Time-Audio-Filtering-using-Python/blob/master/images/demo.gif)</br>
