#!/usr/bin/env python

from __future__ import print_function

import serial
import sys
import time
from datetime import datetime


def send_receive(command):
    if ser.inWaiting():
        # Providing a way to resynchronize, if we have several outstanding
        # requests. (Only seen this when the user rotates the range switch)
        raise ValueError("ERROR: Unexpected characters read. Throwing away " +
                         "\"" + ser.read(1000) + "\"")

    ser.write(command + '\n')
    time.sleep(0.02)
    received = ser.readline()

    if len(received) and received[0] == '*':
        # Rotation of the range switch sends messages starting with a "*" which
        # destroys our synchronization. (What we read is not the response of
        # the command we sent.)
        raise ValueError("ERROR: Unexpected characters read. Throwing away \""
                         + received + "\"")

    if len(received) == 0:
        raise ValueError("ERROR: No response received for command \"" +
                         command + "\"")

    received = received.replace('\n', '')
    received = received.replace('\r', '')
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


if __name__ == "__main__":

    if len(sys.argv) == 2:
        serial_devname = sys.argv[1]
    else:
        serial_devname = '/dev/ttyUSB0'

    ser = serial.Serial(serial_devname, timeout=0.5)

    try:
        idn = send_receive('*IDN?')
        print('# Measurement source: %s\n' % idn)
    except ValueError as e:
        print(e.args, file=sys.stderr)
        print("ERROR: terminating since meter failed to respond to \"*IDN?\"."
              + "\nIs the meter turned on and connected?", file=sys.stderr)
        exit(1)

    print("Counter\tTimestamp\tReading\tRange setting\tSecondary reading\t" +
          "Secondary range")

    n = 0
    samples_per_second = 4
    while True:
        now = datetime.now()

        try:
            reading1 = send_receive('READ?')
            reading2 = send_receive('FETC? @2')
            conf1 = send_receive('CONF?')
            conf2 = send_receive('CONF? @2')

            msecs = now.microsecond / 1000
            timestring = now.strftime("%Y-%m-%d %H:%M:%S") + '.%03d' % (msecs)

            print('%d\t%s\t%s\t%s\t%s\t%s' % (n, timestring, reading1, conf1,
                  reading2, conf2))
            n += 1

            # Rate limit sampling by sleeping to achieve the samplerate
            # samples_per_second
            now_post_read = datetime.now()
            delta = now_post_read - now

            delta_microseconds = delta.microseconds + 1000000*delta.seconds

            target_delta_microseconds = 1000000.0/samples_per_second

            if target_delta_microseconds > delta_microseconds:
                sleep_usecs = target_delta_microseconds - delta_microseconds
                time.sleep(sleep_usecs*0.000001)

        except ValueError as e:
            print(e.args[0], file=sys.stderr)
