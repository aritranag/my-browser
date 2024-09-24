import os
import tkinter


os.environ['TK_SILENCE_DEPRECATION'] = '1' #suppressing the deprecation warning for Tkinter
WIDTH, HEIGHT = 1800, 1600 # Constants for the canvas

class Browser:
    """
    Browser class to render the webpage

    Method List:
    constructor := Creates a canvas with WIDTH, HEIGHT via Tkinter package
    """
    def __init__(self):
        """
        Constructor to create a canvas in a Tkinter window

        Object properties:
        window - defines a 
        """
        self.window = tkinter.Tk()

        # Creates a canvas to display the contents of the webpage
        self.canvas = tkinter.Canvas(self.window,width=WIDTH,height=HEIGHT)
        self.canvas.pack()
