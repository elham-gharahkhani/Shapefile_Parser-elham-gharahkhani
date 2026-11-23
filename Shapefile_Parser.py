
import matplotlib.pyplot as plt  
import numpy as np  
import struct 

def readshape(shapefile):  
    binaryshapefile=open(shapefile, 'rb')  
    r28=binaryshapefile.read(28) 
    r28unpack=struct.unpack('>lllllll',r28) 
    r99=binaryshapefile.read(72) 
    structbyte=struct.unpack('<lldddddddd', r99) 
    #point
    if structbyte[1]==1: 

        binaryshapefile.seek(24) 
        r4=binaryshapefile.read(4)  
        r4unpack=struct.unpack('>l',r4) 
        numberpoint=(r4unpack[0]*2-100)/(8+20) 

        coordinatexy=[]  
        for i in range(int(numberpoint)):
            binaryshapefile.seek(100 + i * 28 + 4 + 8)
            r16=binaryshapefile.read(16) 
            x,y=struct.unpack('<dd',r16) 
            coordinatexy.append((x,y))   
            plt.plot(x,y,'o')            
    plt.show() 
#polyline
    if structbyte[1] == 5:
        aline = 100
        coordinatexy = []
        a = 0         
        while aline != r28unpack[6] * 2:

            a = 1 + a
            binaryshapefile.seek(aline + 48) 
            r4 = binaryshapefile.read(4)  
            r4unpack = struct.unpack('<l', r4)  
            binaryshapefile.seek(aline + 56)  
            r4=binaryshapefile.read(r4unpack[0] * 2 * 8) 

            coorxy=struct.unpack('<'+'d'*r4unpack[0]*2,r4) 
            X=[] 
            Y=[]
            for i in range(0,len(coorxy)):


                if (i%2)==0:
                    X.append(coorxy[i])
                elif (i%2)!=0:
                    Y.append(coorxy[i])
            plt.plot(X,Y)

            coordinatexy.append(coorxy)
            aline=aline+56+r4unpack[0]*16


    plt.show()
#polygon
    if structbyte[1]==3: 
        aline=100 
        coordinatexy=[]
        a=0
        while aline!=r28unpack[6]*2:
            a=1+a
            binaryshapefile.seek(aline + 48)
            r4=binaryshapefile.read(4)
            r4unpack=struct.unpack('<l',r4)
            binaryshapefile.seek(aline + 56)
            r4=binaryshapefile.read(r4unpack[0] * 2 * 8)
            coorxy=struct.unpack('<'+'d'*r4unpack[0]*2,r4)
            X=[]
            Y=[]
            for i in range(0,len(coorxy)):
                if (i%2)==0:
                    X.append(coorxy[i])
                elif (i%2)!=0:
                    Y.append(coorxy[i])
            plt.plot(X,Y)
            coordinatexy.append(coorxy)
            aline=aline+56+r4unpack[0]*16
    plt.show()
from tkinter import *
from tkinter import filedialog

import matplotlib.pyplot as plt
import numpy as np
root=Tk()
root.title("shapfile")
root.geometry("300x100")
color="blue"
def getTextInput():
    global result
    result=0
    print(result)

def getfile():
    global fname
    fname=filedialog.askopenfile(mode="r")
    print(fname.name)
firstbutton=Button(root, height=2, width=45, bg="red", text="click",
                   command=getfile)

firstbutton.pack()

def graph():
    readshape(fname.name)
    plt.show()

secondbutton=Button(root, height=2, width=35, bg="blue", text='figure', command=graph)
secondbutton.pack()

root.mainloop()