import MEDIATOR
import time
#############################################
from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep
import serial
import math
#############################################



Sensor_VaporPressure = float(0)
Sensor_Temperature = float(0)
Sensor_AtmosphericPressure = float(0)
Sensor_Relativehumidity = float(0)
###############################################################################################################
#
#               Sensor_Processor
#
###############################################################################################################
def Sensor_Processor( Sensor_Data ):
        global  Sensor_VaporPressure
        global  Sensor_Temperature
        global  Sensor_AtmosphericPressure
        global  Sensor_Relativehumidity
        step=0
        Sensor_Data1=""
        Sensor_Data2=""
        Sensor_Data3=""
        for n in Sensor_Data:
                if step == 0:
                        if (ord(n))==9:
                                step=1
                elif step == 1:
                        if (ord(n))==32:
                                step=2
                        else:
                                Sensor_Data1=Sensor_Data1+n
                elif step == 2:
                        if (ord(n))==32:
                                step=3
                        else:
                                Sensor_Data2=Sensor_Data2+n
                elif step == 3:
                        if (ord(n))==13:
                                step=4
                        else:
                                Sensor_Data3=Sensor_Data3+n
        #print "SEN1:"+" "+(time.strftime("%d/%m/%Y"))+" "+(time.strftime("%H:%M:%S"))+" "+Sensor_Data1+" "+Sensor_Data2+" "+Sensor_Data3

        Sensor_Relativehumidity = float(0)
        try:
                Sensor_VaporPressure = float(Sensor_Data1)
        except ValueError:
                Sensor_VaporPressure = float(0)
        try:
                Sensor_Temperature = float(Sensor_Data2)
        except ValueError:
                Sensor_Temperature = float(0)
        try:
                Sensor_AtmosphericPressure = float(Sensor_Data3)
        except ValueError:
                Sensor_AtmosphericPressure = float(0)

        Sensor_Relativehumidity = float(Sensor_VaporPressure)/(float(0.611)*math.exp((float(17.502) * float(Sensor_Temperature))/(float(240.97) + float(Sensor_Temperature))))

        return




#############################################
def RUN_INIT():
	print "--> RUN_INIT : "	
	global ser1
	global ser2
	global ser3
	ser1 = serial.Serial(port = "/dev/ttyS1", baudrate=1200,timeout=0.1)
	ser2 = serial.Serial(port = "/dev/ttyS2", baudrate=1200,timeout=0.1)
	ser3 = serial.Serial(port = "/dev/ttyS3", baudrate=1200,timeout=0.1)
	gpio.init()
	gpio.setcfg(port.PA6, gpio.OUTPUT)
	gpio.pullup(port.PA6, gpio.PULLDOWN)
	gpio.output(port.PA6, gpio.LOW)	
	time.sleep(0.1)
	
#############################################	
def RUN_MEM_DATA_PROCESSING(DATA):
	print "--> XXX : " + str(DATA)
	time.sleep(1)
#############################################
def RUN_DATA_PROCESSING(DATA):
	print "--> XXX : " + str(DATA)
	if(DATA=="1"):
		###################################################
		gpio.output(port.PA6, gpio.HIGH)
		time.sleep(1)
		gpio.output(port.PA6, gpio.LOW)
		###################################################
		Sensor_Processor( ser1.read(200) )
		Sensor1_VaporPressure   = Sensor_VaporPressure
		Sensor1_Temperature     = Sensor_Temperature
		Sensor1_AtmosphericPressure     = Sensor_AtmosphericPressure
		Sensor1_Relativehumidity = Sensor_Relativehumidity
		Sensor1_Relativehumidity = "%.2f" % round(Sensor1_Relativehumidity,2)
		print "SEN1:"+" "+(time.strftime("%d/%m/%Y"))+" "+(time.strftime("%H:%M:%S"))+"   VP: "+str(Sensor1_VaporPressure)+"  T: "+str(Sensor1_Temperature)+"  AP: "+str(Sensor1_AtmosphericPressure)+"  RH: "+str(Sensor1_Relativehumidity)
		###################################################
		Sensor_Processor( ser2.read(200) )
		Sensor2_VaporPressure   = Sensor_VaporPressure
		Sensor2_Temperature     = Sensor_Temperature
		Sensor2_AtmosphericPressure     = Sensor_AtmosphericPressure
		Sensor2_Relativehumidity = Sensor_Relativehumidity
		Sensor2_Relativehumidity = "%.2f" % round(Sensor2_Relativehumidity,2)
		print "SEN2:"+" "+(time.strftime("%d/%m/%Y"))+" "+(time.strftime("%H:%M:%S"))+"   VP: "+str(Sensor2_VaporPressure)+"  T: "+str(Sensor2_Temperature)+"  AP: "+str(Sensor2_AtmosphericPressure)+"  RH: "+str(Sensor2_Relativehumidity)
		###################################################
		Sensor_Processor( ser3.read(200) )
		Sensor3_VaporPressure   = Sensor_VaporPressure
		Sensor3_Temperature     = Sensor_Temperature
		Sensor3_AtmosphericPressure     = Sensor_AtmosphericPressure
		Sensor3_Relativehumidity = Sensor_Relativehumidity
		Sensor3_Relativehumidity = "%.2f" % round(Sensor3_Relativehumidity,2)
		print "SEN3:"+" "+(time.strftime("%d/%m/%Y"))+" "+(time.strftime("%H:%M:%S"))+"   VP: "+str(Sensor3_VaporPressure)+"  T: "+str(Sensor3_Temperature)+"  AP: "+str(Sensor3_AtmosphericPressure)+"  RH: "+str(Sensor3_Relativehumidity)
		###################################################
		xx1 = str(Sensor1_Temperature)
		xx2 = str(Sensor1_Relativehumidity)
		xx3 = str(Sensor1_AtmosphericPressure)
		###################################################
		xx4 = str(Sensor2_Temperature)
		xx5 = str(Sensor2_Relativehumidity)
		xx6 = str(Sensor2_AtmosphericPressure)
		###################################################
		xx7 = str(Sensor3_Temperature)
		xx8 = str(Sensor3_Relativehumidity)
		xx9 = str(Sensor3_AtmosphericPressure)
		###################################################
		data = str(xx1+","+xx2+","+xx3+","+xx4+","+xx5+","+xx6+","+xx7+","+xx8+","+xx9)		
		#print data
		
		MEDIATOR.TX(0,str(data))
		
		
		#time.sleep(0.1)
		#MEDIATOR.TX(1,xx1)
		#time.sleep(0.1)
		#MEDIATOR.TX(2,xx2)		
		#time.sleep(0.1)
		#MEDIATOR.TX(9,xx3)		
		#time.sleep(0.1)
		#MEDIATOR.TX(4,xx4)
		#time.sleep(0.1)
		#MEDIATOR.TX(5,xx5)		
		#time.sleep(0.05)
		#MEDIATOR.TX(6,xx6)
		#time.sleep(0.05)
		#MEDIATOR.TX(9,xx7)
		#time.sleep(0.05)
		#MEDIATOR.TX(8,xx8)		
		#time.sleep(0.05)
		#MEDIATOR.TX(9,xx9)		


def RUN_LOOP():
	time.sleep(2)



