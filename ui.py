from tkinter import *
from audio_init import *
from filters import update_Hz
from math import pi

def build_ui(stream):
    root = Tk()
    root.grid_columnconfigure((0,1,2),weight = 1)
    root.title('Real Time Audio Processing')

    Button(root, text='Start',command=lambda: start_stream(stream)).grid(row = 0,column = 0)
    Button(root, text='Pause',command=lambda:pause_stream(stream)).grid(row = 0,column = 1)
    Button(root, text='Stop',command=lambda:stop_stream(stream,root)).grid(row = 0,column = 2)
    Button(root, text='Record Start',command=record_start).grid(row = 1,column = 0)
    Button(root, text='Record Stop',command=record_stop).grid(row = 1,column = 1)
    Button(root, text='Record Save',command=record_save).grid(row = 1,column = 2)
    Button(root, text='Show Freq Response of filter',command=plot_filter_response)
  
    Hz_string = StringVar()
    Label(root, text="Enter H(z) Equation").grid(row = 2, column = 0)
    Entry(root,textvariable = Hz_string, font=('calibre',10,'normal')).grid(row = 2,column = 1)
    Button(root,text = 'Submit Hz', command = lambda: update_Hz(Hz_string.get())).grid(row = 2,column = 2)

    zeros_string = StringVar()
    Label(root, text="Enter Zeros of H(z)").grid(row = 3,column = 0)
    Entry(root,textvariable = zeros_string, font=('calibre',10,'normal')).grid(row = 3,column = 1)
    Button(root,text = 'Submit Zeros of H(z)', command = lambda: update_zeros(zeros_string.get())).grid(row = 3,column = 2)

    hn_string = StringVar()
    Label(root, text="Enter Coeffiecient of h[n]").grid(row = 4,column = 0)
    Entry(root,textvariable = hn_string, font=('calibre',10,'normal')).grid(row = 4,column = 1)
    Button(root,text = 'Submit Coeffiecient of h[n]', command = lambda: update_hn(hn_string.get())).grid(row = 4,column = 2)

    b_string = StringVar()
    Label(root, text="Enter Lccde Coeffiecient of numerator").grid(row = 5,column = 0)
    Entry(root,textvariable = b_string, font=('calibre',10,'normal')).grid(row = 5,column = 1)
    Button(root,text = 'Submit Lccde Coeffiecient', command = lambda: update_lccde(b_string.get())).grid(row = 5,column = 2)


    filters = StringVar(root)
    filters.set(OPTIONS[0]) # default value

    OptionMenu(root, filters, *OPTIONS).grid(row = 7,column = 0)
    Button(root, text='Apply Filter',command=lambda:change_filter(filters.get())).grid(row = 7,column = 1)
    Button(root, text='Plot ',command=plot_filter_response).grid(row = 7,column = 2)
    
    Scale(root,orient=HORIZONTAL, from_=1, to=1000,length=1000,resolution=1,command=change_lowcutoff).grid(row = 8,columnspan = 3)
    Scale(root,orient=HORIZONTAL, from_=1, to=1000,length=1000,resolution=1,command=change_highcutoff).grid(row = 9,columnspan = 3)


    root.mainloop()
    stop_stream(stream,root)