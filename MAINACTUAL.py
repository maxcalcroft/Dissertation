#!/usr/bin/env python
#import necessary modules
import time
import Adafruit_MCP4725
import rospy
#import LiDAR range messages
from sensor_msgs.msg import LaserScan
 
#Defining function for going forward using DAC Address and time
def Y(icAdd, t):
    
	dac = Adafruit_MCP4725.MCP4725(icAdd)
    #maximum DAC voltage
	piV = 5.17
	#set voltage for DAC
    arr = [3.97]
    print "Going forward"
	#conversion of pi voltage to 12 bit DAC voltage
    for x in range(0, len(arr)):
	result = arr[x] / piV
	result = result * 4096
	print int(result)
	dac.set_voltage(int(result))
	time.sleep(0.5)  
#Defining the function for setting the X DAC (left&right) to 2.5V 
#therefore the buggy only goes forwards/backwards

def X(icAdd, t):
    
	dac = Adafruit_MCP4725.MCP4725(icAdd)
    #maximum DAC voltage
	piV = 5.17
	#set voltage for DAC
    arr = [3.97]
    print "Going forward"
	#conversion of pi voltage to 12 bit DAC voltage
    for x in range(0, len(arr)):
	result = arr[x] / piV
	result = result * 4096
	print int(result)
	dac.set_voltage(int(result))
	time.sleep(0.5)    

#Defining stop function
def stop(icAdd, maxV):

    dac = Adafruit_MCP4725.MCP4725(icAdd)
	#2.5V is the voltage at which the buggy stops
    arr = [2.5]

    print "Stopping"

    for x in range(0, len(arr)):
        voltage = (2.5 / maxV) * 4096
        dac.set_voltage(int(voltage))
        time.sleep(0.5)
#Defining the LiDAR range variable 
def scan_callback(msg):
	global g_range_ahead
	#taking the middle value from the Laserscan messages
	g_range_ahead=msg.ranges[len(msg.ranges)/2]

#setting the default range value and initiating the nodes for ROS 
g_range_ahead=1
#subscribing to the laser scan messages (See publishing and subscribing on roswiki)
scan_sub=rospy.Subscriber('scan',LaserScan,scan_callback)
rospy.init_node('wander')
#setting the refresh rate to 10Hz
rate=rospy.Rate(10)

#The while loop for autonomous driving
while not rospy.is_shutdown():

		if(g_range_ahead<1.0):
			#calling the stop function at the X&Y DAC address with their Max voltages
            stop(0x62, 5.17)
			stop(0x63, 4.24)                        
			#stopping the buggy for 3 seconds
			time.sleep(3.0)
			print ("range ahead %0.1f"%g_range_ahead)
		else:
			#calling the forward function at X&Y DAC's for 5 seconds 
     		Y(0x62, 5)
			X(0x63, 5)
			time.sleep(0.5)
			print ("range ahead %0.1f"%g_range_ahead)
				#sleep constantly adjusted by ROS to keep rate at 10Hz based on speed of computer
               	rate.sleep()

































