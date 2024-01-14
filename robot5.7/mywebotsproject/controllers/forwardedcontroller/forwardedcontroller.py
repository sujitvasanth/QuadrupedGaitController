#Tkinter gui to control 4 limbs of a robot with graph for x-y plane, slider for z plane servoposition file i/o and editing, 
import thread, Tkinter, tkFileDialog, pickle, os, time;from math import *;from controller import Supervisor, Motor #using supervisor insteasd of robot
def findangles(x,y,z, d1=0.3, d2=0.3):
    ydsq=y*y+z*z
    test=(x*x+ydsq-d1*d1-d2*d2)/(2*d1*d2)
    if test <-1 or test >1: return(0,0,0,0) #solutions=0
    a1=a2=a3=0.0;yd=sqrt(ydsq);a2=acos(test)
    if y<0: yd=-yd
    if x==0: temp=pi/2
    else: temp=atan(yd/x)    
    a1=temp-asin(d2*sin(a2)/sqrt(x*x+y*y+z*z))
    if x>0: a1=a1+pi# i.e. use the second item in the solution set
    if y==0: a3=pi/2
    else: a3=asin(z/yd)
    return(a1-0.43,a3,-a2,1)
def leaving():
    for g in range(0,4): canv[g].coords(line1[g], 0, 50, 200, 50); canv[g].coords(line2[g], 100, 0, 100, 200)
    label2.config(text="")
def motion(ex,ey):
    for g in range(0,4): label2.config(text=str([ex-100, 50-ey]));canv[g].coords(line1[g], 0, ey, 200, ey);canv[g].coords(line2[g], ex, 0, ex, 200)
def common(ex=0, ey=0,code=0, b=0, Mot=0):
    global vector
    me=checkval[b].get();e=yslider[b].get()
    if code=="zmovement": c=vector[b][0];d=vector[b][1]
    elif code=="textentry":
        vector[b]=eval(label[b].get())
        c=vector[b][0];d=vector[b][1];e=vector[b][2];
        yslider[b].set(e)
    else: c=(ex)-100;d=(50-ey)
    a=findangles(c/200.00,d/200.00,e/600.00)
    if a[3]==0: return    
    for g in range(0,4):
        canv[g].coords(line1[g], 0, 50-d, 200, 50-d);canv[g].coords(line2[g], c+100, 0, c+100, 200)
        if b==g or (checkval[g].get()==1 and me==1):
            case=[[0,0,0],[1,1,-1],[4,2,4],[5,3,3]];h,i,j=case[g]
            Mot[1+h].setPosition(a[0]);Mot[9+i].setPosition(a[1]);Mot[4+j].setPosition(a[2]);vector[g]=(c,d,e)
            if code=="zmovement": yslider[g].set(e)
            canv[g].coords(foot[g],c+90,40-d,c+110,60-d)
            vector[g]=[c,d,e];label[g].delete(0, "end");label[g].insert(0,str(vector[g]))
def play():
    global flag, timer,p; timer=time.time()+n[p][0]*0.001
    if flag==2: flag=1;p=0
    else: flag=2
def nextpos():
    global p, flag; p=p+1; flag=1
    if p > n[0][0]: p=1
def previouspos():
    global p, flag; p=p-1;flag=1
    if p < 1: p=n[0][0]
    if n[p][7]==1: p=p-1 
def update(): global n; a=n[p][13];n[p]=[eval(label3.get())];n[p].extend(vector[0]+vector[1]+vector[2]+vector[3]);n[p].append(a)
def delete(): global n; n[0][0]=n[0][0]-1;del(n[p]);previouspos()    
def insert(): global n; n[0][0]=n[0][0]+1;n.insert(p+1, n[p]);nextpos()
def copy():
    global clip; clip=n[p]
    if p==0: clip=[200];clip.extend(n[0][1:13])
def paste(): global n;n[0][0]=n[0][0]+1;n.insert(p+1, clip);nextpos()
def reset(): global p, flag; robot.simulationSetMode(2);robot.simulationReset();robot.simulationSetMode(1);p=0;flag=1
def open2():
    global n; directory = os.getcwd()
    try:
        filename=tkFileDialog.askopenfilename(initialdir = directory,title = "Select file")
        fileObject = open(filename,"r"); n=pickle.load(fileObject);fileObject.close(); print "load succeeded"
    except: print "didnt load"
def save():
    try: fileObject = open("C:\Users\SOMEUSER\Desktop\servoppos","wb");pickle.dump(n,fileObject);fileObject.close();print "successful save"
    except: print "failed save"
def saveas():
    global n; directory = os.getcwd(); filename=tkFileDialog.asksaveasfilename(initialdir = directory,title = "Select file")
    try: fileObject = open(filename,"wb");pickle.dump(n,fileObject);fileObject.close();print "successful save"
    except: print "failed save"

def oval(event):
    global gtrans
    gtrans[0]=[0,-gslider[0].get()];gtrans[2]=[gslider[1].get(),0];gtrans[4]=[0,gslider[2].get()];gtrans[6]=[-gslider[3].get(),0]
    gait.coords(ovalline,100+gtrans[0][0],80+gtrans[0][1],100+gtrans[1][0],80+gtrans[1][1],100+gtrans[2][0],80+gtrans[2][1],100+gtrans[3][0],80+gtrans[3][1],
                100+gtrans[4][0],80+gtrans[4][1],100+gtrans[5][0],80+gtrans[5][1],100+gtrans[6][0],80+gtrans[6][1],100+gtrans[7][0],80+gtrans[7][1])
def skew2(event):
    global gtrans;x=event.x;y=event.y 
    if x>100:
        if y<80: gtrans[1]=[x-100,y-80]   #quadrant1 
        else: gtrans[3]=[x-100,y-80]  #quadrant2
    else:
        if y>80: gtrans[5]=[x-100,y-80] #quadrant3 
        else: gtrans[7]=[x-100,y-80] #quadrant 4
    gait.coords(ovalline,100+gtrans[0][0],80+gtrans[0][1],100+gtrans[1][0],80+gtrans[1][1],100+gtrans[2][0],80+gtrans[2][1],100+gtrans[3][0],80+gtrans[3][1],
                100+gtrans[4][0],80+gtrans[4][1],100+gtrans[5][0],80+gtrans[5][1],100+gtrans[6][0],80+gtrans[6][1],100+gtrans[7][0],80+gtrans[7][1])
def stance():
    global M,vector
    for g in range(0,4):
        c=gorigin[g][0];d=gorigin[g][1];e=gorigin[g][2];
        yslider[g].set(e);canv[g].coords(foot[g],c+90,40-d,c+110,60-d)
        a=findangles(c/200.00,d/200.00,e/600.00)
        case=[[0,0,0],[1,1,-1],[4,2,4],[5,3,3]];h,i,j=case[g]
        M[1+h].setPosition(a[0]);M[9+i].setPosition(a[1]);M[4+j].setPosition(a[2])
        vector[g]=[c,d,e];label[g].delete(0, "end");label[g].insert(0,str(vector[g]))

def gupdate(event):
    global gorigin
    gorigin[0]=eval(glabel[0].get());gorigin[1]=eval(glabel[1].get());gorigin[2]=eval(glabel[2].get());gorigin[3]=eval(glabel[3].get())
def gnext():
    global gp, flag; gp=gp+1; flag=3
    if gp > 7: gp=0
def gprev():
    global gp, flag; gp=gp-1;flag=3
    if gp < 0: gp=7

try:
    fileObject = open("C:\Users\SOMEUSER\Desktop\servoppos",mode="r"); n=pickle.load(fileObject);fileObject.close()
except:
    n = [[6, 0,-65,0,0,-65,0,0,-65,0,0,-65,0, 0]] #list of lists n[0][0] denotes the number of positions =1, x1,y1,z1 etc 
    n.append([210,   0,-65,0,   0,-50,0,    0,-50,0,     0,-65,0,    0])
    n.append([210,   0,-50,0,   0,-65,0,    0,-65,0,     0,-50,0,    0]) #n[1][0] ms wait time, n[1][13] denotes 0=wait, 1 move on
    n.append([210,   0,-65,0,   0,-50,0,    0,-50,0,     0,-65,0,    0])
    n.append([210,   0,-50,0,   0,-65,0,    0,-65,0,     0,-50,0,    0])
    n.append([210,   0,-65,0,   0,-50,0,    0,-50,0,     0,-65,0,    0])
    n.append([210,   0,-50,0,   0,-65,0,    0,-65,0,     0,-50,0,    0])
timer=time.time(); p=0;flag=1;clip=0;gp=0
M=[0]*13;bbutton=[0]*12;gtrans=[0]*8
robot = Supervisor()
for a in range(1,13): M[a]=robot.getMotor("motor"+str(a))

mGui=Tkinter.Tk();mGui.title('Robot Controller');mGui.geometry("670x585+520+30");mGui.attributes("-topmost", True)
mGui.wait_visibility(mGui);#mGui.wm_attributes('-alpha', 0.62)
label1 = Tkinter.Label(mGui, text=str(p));label2 = Tkinter.Label(mGui, text="", fg="red");label1.place(x=500, y=10);label2.place(x=595, y=40)
label3=Tkinter.Entry(mGui,text="", width=5);label3.place(x=500, y=40)

case=["canv","line2","line1","foot","yslider","check","checkval","label","vector","gslider","glabel","gorigin"]
for i in case: exec("%s = [0]*4" %i)
case=[["Play","play",500,100],["<<<","previouspos",550,10],[">>>","nextpos",595,10],["Reset","reset",550,40,0],["Open","open2",500,130],
      ["Save","save",550,130],["Save As","saveas",595,130],["Update","update",500,70],["Delete","delete",550,70],["Insert","insert",595,70],
      ["Copy","copy",550,100],["Paste","paste",595,100]]
for g in range(0,12): bbutton[g]=Tkinter.Button(mGui,text=case[g][0],width=5,command=eval(case[g][1]));bbutton[g].place(x=case[g][2],y=case[g][3])
for a in range(0,4):
    vector[a]=(n[0][1+3*a],n[0][2+3*a],n[0][3+3*a])
    yslider[a]=Tkinter.Scale(mGui, width=20, length=160, from_=80, to_=-80)
    canv[a]=Tkinter.Canvas(mGui,bg="red", width=200,height=160)
    canv[a].create_line(100, 0, 100, 200, fill='white');canv[a].create_line(0, 50, 200, 50, fill='white');canv[a].create_oval(90,40,110,60, fill="", outline="white")
    line2[a]=canv[a].create_line(100, 0, 100, 200, fill='white'); line1[a]=canv[a].create_line(0, 50, 200, 50, fill='white')
    foot[a]=canv[a].create_oval(90,105,110,125, fill="white", outline="white")
    checkval[a]=Tkinter.IntVar(); check[a]=Tkinter.Checkbutton(mGui, text="Leg "+str(a), variable=checkval[a])
    label[a]=Tkinter.Entry(mGui,text="",width=14)
    canv[a].bind("<Leave>", lambda event: leaving())
    canv[a].bind("<Motion>", lambda event, copy=a: motion(event.x, event.y))
    canv[a].bind('<ButtonPress-1>',lambda event, copy=a, code="press", motors=M: common(event.x, event.y, code, copy, motors))
    canv[a].bind("<B1-Motion>", lambda event, copy=a, code="dragpress", motors=M: common(event.x, event.y, code, copy, motors))
    yslider[a].bind("<B1-Motion>", lambda event, copy=a, code="zmovement", motors=M: common(None,None,code, copy, motors))
    label[a].bind('<Return>', lambda event, copy=a, code="textentry", motors=M: common(None,None,code, copy, motors))
    case=[[290,10], [40,10], [290,210], [40,210]];ax,ay=case[a]
    canv[a].place(x=ax,y=ay);yslider[a].place(x=ax-50,y=ay);check[a].place(x=ax-25,y=ay+170);label[a].place(x=ax+30,y=ay+170)
    case=[[80,80,0,"vertical",0,440],[100,0,100,"horizontal",140,400],[80,0,80,"vertical",0,520],[100,100,0,"horizontal",40,400]]
    gslider[a]=Tkinter.Scale(mGui, width=20, length=case[a][0],from_=case[a][1],to_=case[a][2],orient=case[a][3])
    gslider[a].place(x=case[a][4],y=case[a][5]);gslider[a].set(50);gslider[a].bind("<B1-Motion>",oval)
    case=[[0,-75,80,0],[0,-75,-80,4],[0,-75,80,4],[0,-75,-80,0]]
    gorigin[a]=[case[a][0],case[a][1],case[a][2],case[a][3]]    
    glabel[a]=Tkinter.Entry(mGui,width=14);glabel[a].place(x=290,y=440+a*30);glabel[a].insert(0,gorigin[a]);glabel[a].bind('<Return>',gupdate)
gait=Tkinter.Canvas(mGui,bg="green", width=200,height=160);gait.place(x=40,y=440)
gait.create_line(100, 0, 100, 200, fill='white');gait.create_line(0, 80, 200, 80, fill='white')
gait.create_oval(90,70,110,90, fill="", outline="white");gait.bind('<Button-1>',skew2)
gtrans=[[0,-gslider[0].get()],[25,-25],[gslider[1].get(),0],[25,25],[0,gslider[2].get()],[-25,25],[-gslider[3].get(),0],[-25,-25]]
ovalline=gait.create_polygon(100+gtrans[0][0],80+gtrans[0][1],100+gtrans[1][0],80+gtrans[1][1],100+gtrans[2][0],80+gtrans[2][1],100+gtrans[3][0],80+gtrans[3][1],
                100+gtrans[4][0],80+gtrans[4][1],100+gtrans[5][0],80+gtrans[5][1],100+gtrans[6][0],80+gtrans[6][1],100+gtrans[7][0],80+gtrans[7][1],fill="", outline="white", smooth=0)
tslider=Tkinter.Scale(mGui, width=20, length=200,from_=0,to_=300,orient="horizontal");tslider.place(x=290,y=580)
case=[["Stance","stance",500,430],["<<<","gprev",500,460],[">>>","gnext",550,460]]
for g in range(0,3): bbutton[g]=Tkinter.Button(mGui,text=case[g][0],width=5,command=eval(case[g][1]));bbutton[g].place(x=case[g][2],y=case[g][3])
robot.simulationSetMode(1)

while True:
    try:
        mGui.update()#
        if robot.simulationGetMode()!=0: robot.step(32)#update the robot controller
    except: pass
    if flag==0:
        pass
    elif flag==3:
        flag=0
        for g in range(0,4):
            phase=gp+gorigin[g][3]
            if phase>7: phase=phase-8
            c=gorigin[g][0]+(0.5*gtrans[phase][0]);d=gorigin[g][1]-(0.5*gtrans[phase][1]);e=gorigin[g][2]
            vector[g]=[c,d,e];label[g].delete(0, "end");label[g].insert(0,str(vector[g]))
            yslider[g].set(e);canv[g].coords(foot[g],c+90,40-d,c+110,60-d)
            a=findangles(c/200.00,d/200.00,e/600.00)
            case=[[0,0,0],[1,1,-1],[4,2,4],[5,3,3]];h,i,j=case[g]
            M[1+h].setPosition(a[0]);M[9+i].setPosition(a[1]);M[4+j].setPosition(a[2])
    else:
        if flag==2 and timer<time.time(): #update playmode
            p=p+1
            if p>n[0][0]:p=1
            timer=time.time()+n[p][0]*0.001
        if flag==1: flag=0 #update position mode
        label1.config(text=str(p)+" of "+str(n[0][0]))
        label3.delete(0,"end");label3.insert(0,str(n[p][0]))       
        for g in range(0,4):
            c=n[p][1+3*g];d=n[p][2+3*g];e=n[p][3+3*g]
            a=findangles(c/200.00,d/200.00,e/600.00)
            vector[g]=[c,d,e];label[g].delete(0, "end");label[g].insert(0,str(vector[g]))
            yslider[g].set(e);canv[g].coords(foot[g],c+90,40-d,c+110,60-d)
            case=[[0,0,0],[1,1,-1],[4,2,4],[5,3,3]];h,i,j=case[g]
            M[1+h].setPosition(a[0]);M[9+i].setPosition(a[1]);M[4+j].setPosition(a[2])

