import RPi.GPIO as GPIO
import time
from client import *

device_id = 1
pulse_duration = 0
distance = 0
park_thresh = 15
dist = ''
occupied = False
prev_occupied = False
stat_change = False

try:
    GPIO.setmode(GPIO.BOARD)

    PIN_TRIGGER = 7
    PIN_ECHO = 11

    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    while True:
        prev_occupied = occupied
        #print("Waiting for sensor to settle")

        time.sleep(.1)

        #print("Calculating distance")

        GPIO.output(PIN_TRIGGER, GPIO.HIGH)

        time.sleep(0.00001)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        #print("Distance:",distance,"cm")

        if (distance < park_thresh):
            occupied = True
        else:
            occupied = False
        
        if occupied != prev_occupied:
            #print(f'Parking status change to {occupied}')
            post_status(device_id, occupied)
        

except:
    print('fail')

finally:
    GPIO.cleanup()