from audio_init import pyaudio_init
from ui import build_ui

if __name__=="__main__":
    stream = pyaudio_init()  # Return the stream of Pyaudio
    build_ui(stream)         # Build the ui using tkinter
 

