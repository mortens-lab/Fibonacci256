import codecs
import pcbnew
import math 
import sys
import csv

print '---------------------------------------------------------------'
print '-                                                             -'
print '-                                                             -'
print '- INIT                                                        -'
print '-                                                             -'
print '-                                                             -'
print '---------------------------------------------------------------'

pcb = pcbnew.GetBoard()
Radius = 20

Mat = [None]*(256+1) #Index 0 stays empty to align LEDs number with index
x_posi=[]
y_posi=[]
angle=[]

MatC = [None]*(256+1)
cx_posi=[]
cy_posi=[]

NetsInner = [1,3,4]
NetsOuter = [2,5,6,7]

mods = pcb.GetModules()
print type(mods)

#Get All LEDs
print '---------------------------------------------------------------'
print '-                                                             -'
print '-                                                             -'
print '- LEDS                                                        -'
print '-                                                             -'
print '-                                                             -'
print '---------------------------------------------------------------'

for modu in pcb.GetModules():
	ref = modu.GetReference().encode('utf-8')
	if(ref.startswith('D')):
		pos = int(ref.split('D')[-1])
		#rot = 2*math.pi/(len(Mat)-1)*(pos-1)
		rot = 0
		padA = None
		padB = None
		netA = None
		netB = None
		for pad in modu.Pads():
			if int(pad.GetPadName()) == 1:
				padA = pad
				netA = pad.GetNetCode()
			else:
				padB = pad
				netB = pad.GetNetCode()
		Mat[pos] = [modu,rot,padA,netA,padB,netB,ref]
		print 'Read: %s,  Rotation %f, NetA %d, NetB %d' % (ref,rot,netA,netB)

print '---------------------------------------------------------------'
print '- Delete-Nets                                                 -'
print '---------------------------------------------------------------'

tracks = pcb.GetTracks()
for t in tracks:
	pcb.Delete(t)

print '---------------------------------------------------------------'
print '- Open and read LEDs x,y,rotation                             -'
print '---------------------------------------------------------------'

with open("c:\\Users\\Morten\\coors2.csv","rb") as csvfile:
    p=0; 
    # get number of columns
    for line in csvfile.readlines():
        p=p+1
        array = line.split('_')
        first_item = array[0]
        second_item = array[1]
        third_item = array[2]
        tmp1 = first_item.replace(",",".")
        tmp2 = second_item.replace(",",".")  
        test1 = float(tmp1) 
        test2 = float(tmp2)
        test3 = float(third_item)
        #print("%.2f" % float(tmp1))
     	#print("%.2f" % float(tmp2))
    	#print("%.2f" % float(third_item))
    	#print(" %d " % p)
        print("CSV.file D%d %6.2f %6.2f %6.2f" % (p, float(tmp1), float(tmp2), float(third_item)))
        x_posi.insert(p,test1)
        y_posi.insert(p,test2)   
        angle.insert(p,test3)
    	#num_columns = len(array)
    	#print(num_columns)
	csvfile.seek(0)

r=0

for mat in Mat[1:]:
	deg = angle[r]
	mat[0].SetOrientation(1800+(deg*10))
	posX = x_posi[r]
	posY = y_posi[r]
	mat[0].SetPosition(pcbnew.wxPointMM(posX,posY))
	print 'Placed: LED %s at %6.2f, %6.2f with rot %6.2f' % (mat[6], posX, posY, deg)
	r=r+1


#Get All CAPACITORs

print '---------------------------------------------------------------'
print '-                                                             -'
print '-                                                             -'
print '- CAPACITORS                                                  -'
print '-                                                             -'
print '-                                                             -'
print '---------------------------------------------------------------'

for modu in pcb.GetModules():
	ref = modu.GetReference().encode('utf-8')
	if(ref.startswith('C')):
		pos = int(ref.split('C')[-1])
		#rot = 2*math.pi/(len(MatC)-1)*(pos-1)
		rot = 0
		padA = None
		padB = None
		netA = None
		netB = None
		for pad in modu.Pads():
			if int(pad.GetPadName()) == 1:
				padA = pad
				netA = pad.GetNetCode()
			else:
				padB = pad
				netB = pad.GetNetCode()
		MatC[pos] = [modu,rot,padA,netA,padB,netB,ref]
		print 'Read: %s,  Rotation %f, NetA %d, NetB %d' % (ref,rot,netA,netB)


print '---------------------------------------------------------------'
print '- Open and read CAPACITORs x,y,rotation                       -'
print '---------------------------------------------------------------'


with open("c:\\Users\\Morten\\coors3.csv","rb") as csvfile:
    p=0; 
    # get number of columns
    for line in csvfile.readlines():
        p=p+1
        array = line.split('_')
        first_item = array[0]
        second_item = array[1]
	#third_item = array[2]
        tmp1 = first_item.replace(",",".")
        tmp2 = second_item.replace(",",".")  
        test1 = float(tmp1) 
        test2 = float(tmp2)
	#test3 = float(third_item)
        #print("%.2f" % float(tmp1))
        #print("%.2f" % float(tmp2))
	#print("%.2f" % float(third_item))
        #print(" %d " % p)
	print("CSV.file C%d %6.2f %6.2f" % (p, float(tmp1), float(tmp2)))
        cx_posi.insert(p,test1)
        cy_posi.insert(p,test2)   
	#angle.insert(p,test3)
    	#num_columns = len(array)
    	#print(num_columns)
    	csvfile.seek(0)

w=0

for mat in MatC[1:]:
	deg = angle[w]
	mat[0].SetOrientation(deg*10)
	cposX = cx_posi[w]
	cposY = cy_posi[w]
	mat[0].SetPosition(pcbnew.wxPointMM(cposX,cposY))
	print 'Placed: CAPACITOR %s at %6.2f, %6.2f with rot %6.2f' % (mat[6], cposX, cposY, deg)
	w=w+1


pcbnew.Refresh();

print '---------------------------------------------------------------'
print '- Done!                                                       -'
print '---------------------------------------------------------------'
