#!/usr/bin/env python

from __future__ import print_function

import serial
import sys
import time
from datetime import datetime;

ser = serial.Serial('/dev/ttyUSB0', timeout=0.5)

def send_receive(command):
	if ser.inWaiting():
		#Providing a way to resynchronize, if we have several outstanding requests
		#(only seen this kick in when the user rotates the range switch)
		print("WARNING: Throwing away \"" + ser.read(1000) + "\"", file=sys.stderr)

	ser.write(command + '\n')
	time.sleep(0.02)
	received = ser.readline()
	received = received.replace('\n','')
	received = received.replace('\r','')
	return received

#send_receive('*IDN?')
#send_receive('SYST:BATT?')
#send_receive('CONF?')
#send_receive('STAT?')
#send_receive('FETC?')
#send_receive('FETC? @2')
#send_receive('*RST')
#send_receive('SYST:VERS?')
#send_receive('SYST:ERR?')
#send_receive('READ?')

idn = send_receive('*IDN?')
print('# Measurement source: %s\n'% idn)
print('Counter\tTimestamp\tReading\tRange setting\tSecondary reading\tSecondary range')

n=0
while True:
	reading1 = send_receive('READ?')
	reading2 = send_receive('FETC? @2')
	conf1 = send_receive('CONF?')
	conf2 = send_receive('CONF? @2')

	now = datetime.now();
	usecs = now.microsecond
	timestring = now.strftime("%Y-%m-%d %H:%M:%S") + '.%03d' % (usecs/1000)

	print('%d\t%s\t%s\t%s\t%s\t%s'% (n, timestring, reading1, conf1, reading2, conf2))
	n += 1
