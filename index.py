import sys
import tkinter
import classes.myUrl as myUrl
import classes.myBrowser as myBrowser

urlString = "http://example.org/index.html"
fileString = "file://"


# how to run the code = python3 index.py <urlstring>

if __name__ == "__main__":
    #myUrl.load(sys.argv[1])
    _browser = myBrowser.Browser()
    tkinter.mainloop()