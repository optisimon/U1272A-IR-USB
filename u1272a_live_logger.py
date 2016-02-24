#!/usr/bin/env python

import serial
import time

ser = serial.Serial('/dev/ttyUSB0', timeout=0.5)

def send_receive(command):
	print(command)
	ser.write(command + '\n')
	time.sleep(0.02)
	received = ser.read(100)
	received = received.replace('\n','')
	print received
	return received

send_receive('*IDN?')
send_receive('SYST:BATT?')
send_receive('CONF?')
send_receive('STAT?')
send_receive('FETC?')
#send_receive('*RST')
send_receive('SYST:VERS?')
send_receive('SYST:ERR?')
send_receive('READ?')
