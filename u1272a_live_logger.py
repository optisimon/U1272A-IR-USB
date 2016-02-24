#!/usr/bin/env python

import serial
import time
from datetime import datetime;

ser = serial.Serial('/dev/ttyUSB0', timeout=0.5)

def send_receive(command):
	ser.write(command + '\n')
	time.sleep(0.02)
	received = ser.read(100)
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
print '# Measurement source: %s\n' %idn
print 'Timestamp\tReading\tRange setting'
while True:
	reading = send_receive('READ?')
	conf = send_receive('CONF?')

	now = datetime.now();
	usecs = now.microsecond
	timestring = now.strftime("%Y-%m-%d %H:%M:%S") + '.%03d' % (usecs/1000)

	print '%s\t%s\t%s' %(timestring, reading, conf)
