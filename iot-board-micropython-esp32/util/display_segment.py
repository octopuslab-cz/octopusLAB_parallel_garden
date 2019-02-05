# from util.display_segment import *

aa = 16 # size
y0 = 16 # position
x0 = aa+5

sevenSeg = [      #seven segment display
#0,1,2,3,4,5,6
 [1,1,1,1,1,1,0], #0      +----0----+
 [0,1,1,0,0,0,0], #1      |         |
 [1,1,0,1,1,0,1], #2      5         1
 [1,1,1,1,0,0,1], #3      |         |
 [0,1,1,0,0,1,1], #4      +----6----+
 [1,0,1,1,0,1,1], #5      |         |
 [1,0,1,1,1,1,1], #6      4         2
 [1,1,1,0,0,0,0], #7      |         |
 [1,1,1,1,1,1,1], #8      +----3----+
 [1,1,1,1,0,1,1], #9
 [1,1,0,0,0,1,1], #deg
 [0,0,0,0,0,0,1]  #-
]

def oneDigit(d,seg,x,y,a): #segment /x,y position / a=size
    d.hline(x,y,a,seg[0])
    d.vline(x+a,y,a,seg[1])
    d.vline(x+a,y+a,a,seg[2])
    d.hline(x,y+a+a,a,seg[3])
    d.vline(x,y+a,a,seg[4])
    d.vline(x,y,a,seg[5])
    d.hline(x,y+a,a,seg[6])

def threeDigits(d, dnum,point,deg): #display number 0-999 / point 99.9 / degrees
    d100=int(dnum/100)
    d10=int((dnum-d100*100)/10)
    d1= dnum-d100*100-d10*10
    oneDigit(d,sevenSeg[d100],x0,y0,aa)
    oneDigit(d,sevenSeg[d10],x0+aa+int(aa/2),y0,aa)
    oneDigit(d,sevenSeg[d1],x0+(aa+int(aa/2))*2,y0,aa)
    if point:
       d.fill_rect(x0+(aa+int(aa/2))*2-5,y0+aa+aa,2,3,1) #test poin
    if deg:
       oneDigit(d, sevenSeg[10],x0+(aa+int(aa/2))*3,y0,aa) #test deg
    d.show()
