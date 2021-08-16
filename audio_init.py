from filters import *
from tkinter import *
import pyaudio
import wave
import matplotlib.pyplot as plt
from tkinter import messagebox

## Configuation ###
Fs = 5000                   #Sampling Rate
low_cutoff_freq = 100      #Low Cut off Freq
high_cutoff_freq = 200     #Low Cut off Freq
order = 5
###################

## Change h[n] ######
hn = [0.5,0.5,0.5,0.5,0.5,0.5,0.5]

def update_hn(input):
    global hn
    hn = np.fromstring(input,dtype = np.float32,sep=' ')
#################

####### Filiter using Poles and Zeros #####
poles = []
zeros = [1]
gain = 0.5

def update_zeros(input):
    global zeros
    zeros = np.fromstring(input,dtype = np.float32,sep=' ')
#####################

####### Filiter using Coffiecnet of LCCDE Eq #####
num = [1,1] ## Can't be empty
den = [1]
def update_lccde(b):
    global num,den
    num = np.fromstring(b,dtype = np.float32,sep=' ')
    # den = np.fromstring(a,dtype = np.float32,sep=' ')
#####################

WIDTH = 2
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"
CHUNK = 2048
FORMAT = pyaudio.paInt16

isRecording = False
isSteamOpen = False
isSteamPause = True
    

OPTIONS = [
"No Filiter",
"Low Pass Filter",
"High Pass Filter",
"Band Pass Filter",
"Band Stop Filter",
"h[n] Filter",
"Poles and Zeors Filter",
"LCCDE",
"H(z)"
] 


p = pyaudio.PyAudio()
frames = []

filter_type = OPTIONS[0]



def plot_filter_response():
    '''
    Plot the response of the filter
    '''
    print(filter_type)
    plt.figure()
    H = 1
    if filter_type == OPTIONS[0]:
        messagebox.showinfo("Title", "No Filter Applied")
        return
    elif filter_type == OPTIONS[1]:
        H = np.abs(lowpass(low_cutoff_freq,CHUNK))
    elif filter_type == OPTIONS[2]:
        H =np.abs(highpass(high_cutoff_freq,CHUNK))
    elif filter_type == OPTIONS[3]:
        H = np.abs(bandpass(low_cutoff_freq,high_cutoff_freq,CHUNK))
    elif filter_type == OPTIONS[4]:
        H = np.abs(bandstop(low_cutoff_freq,high_cutoff_freq,CHUNK))
    elif filter_type == OPTIONS[5]:
        H = np.abs(hn_filter(hn,CHUNK))
    elif filter_type == OPTIONS[6]:
        H = np.abs(zeros_filter(zeros,CHUNK))
    elif filter_type == OPTIONS[7]:
        H = np.abs(lccde_filter(num,CHUNK))
    elif filter_type == OPTIONS[8]:
        H = np.abs(evalHz(CHUNK))
    freqs = np.fft.fftfreq(len(H))
    plt.plot(freqs,H)
    plt.show()

def change_lowcutoff(value=5):
    '''
    Change the value of Low Cut off Freq
    '''
    global low_cutoff_freq
    low_cutoff_freq = float(value)
def change_highcutoff(value=5):
    '''
    Change the value of High Cut off Freq
    '''
    global high_cutoff_freq
    high_cutoff_freq = float(value)



def pyaudio_init():
    '''
    Return : Stream of pyaudio
    '''
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK
    )
    global isSteamOpen
    isSteamOpen = True
    return stream

def record_start():
    '''
    Start Recording
    '''
    global isRecording
    isRecording = True
    print('recording started')

def record_stop():
    '''
    Pause Recording
    '''
    global isRecording
    isRecording = False
    print('recording stopped')
    

def record_save():
    '''
    Save Recording
    '''
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print('recording saved')


def plot():
    '''
    Plots the Waveform (input Audio) and Filterd Audio Plot
    '''
    x = np.arange(0, 2 * CHUNK, 2)
    fig, (ax1,ax2) = plt.subplots(2)
    # create a line object with random data
    ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)
    ax2.plot(x, np.random.rand(CHUNK), '-', lw=2)
    plt.ion()
    # basic formatting for the axes
    ax1.set_title('FFT of input')
    # ax1.set_xlabel('samples')
    # ax1.set_ylabel('volume')
    ax1.set_ylim(0,2000)
    ax1.set_xlim(0, CHUNK)
    plt.setp(ax1, xticks=[0, CHUNK], yticks=[ 0, 2000])

    ax2.set_title(filter_type)
    # ax2.set_xlabel('samples')
    # ax2.set_ylabel('volume')
    ax2.set_ylim(0,2000)
    # freqs = np.fft.fftfreq(CHUNK)
    ax2.set_xlim(0, CHUNK)
    plt.setp(ax2, xticks=[0,CHUNK], yticks=[0,2000])

    # show the plot
    fig.tight_layout()

    plt.show(block=False)
    return fig,ax1,ax2

def dft(s):
    N = len(s)  # N show the length of signal

    # (S show the DFT points)
    S = [0 for _ in range(N)]   # Initialization the S with 0

    # DFT calculation
    for i in range(N):
        for j in range(N):
            tmp = [((0-1j)*(2*np.pi*i*j)) / N]
            S[i] += s[j] * np.exp(tmp)
    return s

def apply_filter(X):
    '''
    Apply the selected Filiter
    '''
    if filter_type == OPTIONS[0]:
        # messagebox.showinfo("Title", "No Filter Applied")
        return X
    elif filter_type == OPTIONS[1]:
        return  X*lowpass(low_cutoff_freq,CHUNK)
    elif filter_type == OPTIONS[2]:
        return X*highpass(high_cutoff_freq,CHUNK)
    elif filter_type == OPTIONS[3]:
        return X*bandpass(low_cutoff_freq,high_cutoff_freq,CHUNK)
    elif filter_type == OPTIONS[4]:
        return X*bandstop(low_cutoff_freq,high_cutoff_freq,CHUNK)
    elif filter_type == OPTIONS[5]:
        return X*hn_filter(hn,CHUNK)
    elif filter_type == OPTIONS[6]:
        return X*zeros_filter(zeros,CHUNK)
    elif filter_type == OPTIONS[7]:
        return X*lccde_filter(num,CHUNK)
    elif filter_type == OPTIONS[8]:
        return X*evalHz(CHUNK)


    

def start_stream(stream):
    '''
    Start Listerning 
    '''
    if isSteamOpen is True: stream.start_stream()
    else: 
        print("Can't start Session ended")
        return
    global isSteamPause
    isSteamPause = False
    print('started',isSteamPause,isSteamOpen)

    if plt.fignum_exists(1):
        fig = plt.figure(1)
        ax1 = fig.axes[0]
        ax2 = fig.axes[1]
    else :
        fig,ax1,ax2 = plot()

    line1 = ax1.lines[0]
    line2 = ax2.lines[0]
    

    while isSteamOpen is True and isSteamPause is False :
        # Get audio in bytes
        data = stream.read(CHUNK) 

        # convert byte data to ndarray
        data_np = np.frombuffer(data,dtype=np.int16)
        input = data_np.astype(np.float32)

        # update Y axis of input plot
        X = np.fft.fft(input,CHUNK)
        line1.set_ydata(np.abs(X[0:CHUNK])/(CHUNK))

        # apply filter with given input
        Y = apply_filter(X)

        y = np.fft.ifft(Y)
        y = np.real(y)
        # Update Y-axis of filter plot
        line2.set_ydata(np.abs(Y[0:CHUNK])/(CHUNK))


        y = y.astype(np.int16)
         # Convert ndarray back to bytes and play back immediately 
        stream.write(y.tobytes())

         #If recording is on, store the filtered audio.
        if isRecording is True:
            global frames
            frames.append(y.tobytes())
        #Update the plot
        try:
            fig.canvas.draw()
            fig.canvas.flush_events()
        
        except : 
            print('stream stopped')
            break
        

def pause_stream(stream):
    '''
    Pause Stream
    '''
    global isSteamPause
    isSteamPause = True
    stream.stop_stream()
    print('paused')

def stop_stream(stream,root):
    '''
    Stop Stream
    '''
    global isSteamOpen
    isSteamOpen = False
    print('stream stopped')
    stream.close()
    p.terminate()
    try:
        root.destroy()
    except :
        print('Root already destroyed')
        

def change_filter(filter):
    '''
    Change the Filter
    '''
    global filter_type
    filter_type = filter
    fig = plt.gcf()
    ax2 = fig.axes[1]
    ax2.set_title(filter)

    print(filter_type)
    return


    
        