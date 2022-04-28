from tabnanny import check
import RPi.GPIO as GPIO
import time
from client import *

device_id = 1
pulse_duration = 0
distance = 0
park_thresh = 25
dist = ''
occupied = False
prev_occupied = False
stat_change = False

class sensor():
    def __init__(self, device_id, trig_pin, echo_pin, sensor_thresh):
        self.device_id = device_id
        self.PIN_TRIGGER = trig_pin
        self.PIN_ECHO = echo_pin
        self.pulse_duration = 0
        self.distance = 0
        self.park_thresh = sensor_thresh
        self.occupied = False
        self.prev_occupied = False
        self.stat_change = False

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(self.PIN_ECHO, GPIO.IN)
        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)
    
    def check_status(self):
        while True:
            self.prev_occupied = self.occupied
            #print("Waiting for sensor to settle")

            time.sleep(.1)

            #print("Calculating distance")

            GPIO.output(self.PIN_TRIGGER, GPIO.HIGH)

            time.sleep(0.00001)

            GPIO.output(self.PIN_TRIGGER, GPIO.LOW)

            while GPIO.input(self.PIN_ECHO)==0:
                pulse_start_time = time.time()
            while GPIO.input(self.PIN_ECHO)==1:
                pulse_end_time = time.time()

            pulse_duration = pulse_end_time - pulse_start_time
            self.distance = round(pulse_duration * 17150, 2)
            #print("Distance:",distance,"cm")

            if (self.distance < self.park_thresh):
                self.occupied = True
            else:
                self.occupied = False
            
            if self.occupied != self.prev_occupied:
                #print(f'Parking status change to {occupied}')
                post_status(self.device_id, self.occupied)
    
    def start(self):
        from threading import Thread
        sensor_thread = Thread(target=self.check_status)
        try:
            sensor_thread.start()
        except:
            sensor_thread.join()
            print('Thread closed')
            GPIO.cleanup()

if __name__ == '__main__':
    sensor1 = sensor(1,7,11,25)
    sensor1.start()

# try:
#     GPIO.setmode(GPIO.BOARD)

#     PIN_TRIGGER = 7
#     PIN_ECHO = 11

#     GPIO.setup(PIN_TRIGGER, GPIO.OUT)
#     GPIO.setup(PIN_ECHO, GPIO.IN)

#     GPIO.output(PIN_TRIGGER, GPIO.LOW)
#     while True:
#         prev_occupied = occupied
#         #print("Waiting for sensor to settle")

#         time.sleep(.1)

#         #print("Calculating distance")

#         GPIO.output(PIN_TRIGGER, GPIO.HIGH)

#         time.sleep(0.00001)

#         GPIO.output(PIN_TRIGGER, GPIO.LOW)

#         while GPIO.input(PIN_ECHO)==0:
#             pulse_start_time = time.time()
#         while GPIO.input(PIN_ECHO)==1:
#             pulse_end_time = time.time()

#         pulse_duration = pulse_end_time - pulse_start_time
#         distance = round(pulse_duration * 17150, 2)
#         #print("Distance:",distance,"cm")

#         if (distance < park_thresh):
#             occupied = True
#         else:
#             occupied = False
        
#         if occupied != prev_occupied:
#             #print(f'Parking status change to {occupied}')
#             post_status(device_id, occupied)
        

# except:
#     print('fail')

# finally:
#     GPIO.cleanup()
