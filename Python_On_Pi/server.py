import signal
import logging
import sys
import time
import math
import numpy as np
import pika, os, logging
sys.path.append("/home/pi/Adafruit_Python_BNO055")
from Adafruit_BNO055 import BNO055
sys.path.insert(0, "build/lib.linux-armv7l-2.7/")
import VL53L1X
from picamera import PiCamera

def exit_handler(signal, frame):
    global running
    running = False
    tof.stop_ranging()
    connection.close()
    print()
    sys.exit(0)
    
def how_long(start, op):
    print("%s took %.2fs" % (op,time.time()-start))
    return time.time()


""" Connect to PiCamera """
camera = PiCamera()

""" Connect to VL53L1X thru i2c ToF sensor """
tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)


""" Connect to BNO055 thru serial port 9axis gyro """
bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

""" VL53L1X configuration """
tof.open()
tof.start_ranging(0) # Start raning
                     # 0 = Unchanged
                     # 1 = Short 136cm
                     # 2 = Medium 290cm
                     # 3 = Long 360cm
tof.set_timing(200,33)

"""RabbitMQ"""
logging.basicConfig()

url = os.environ.get('CLOUDAMQP_URL','amqp://fnfdxokx:EPwMQFxwqZU4fHV3JY1VgsxXaVBdUsXn@mosquito.rmq.cloudamqp.com/fnfdxokx')
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue = 'sesdata')

# Camera configuration
camera.resolution = (128, 112)
camera.framerate = 90

running = True
signal.signal(signal.SIGINT, exit_handler)

# RGB matrix
output = np.empty((112,128,3),dtype=np.uint8)

# start = time.time()

# sequncing : 1. Gyro reading, 2. Distance, 3. RGB value
while running:
    """Gyro data"""
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = bno.read_euler()
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    sys, gyro, accel, mag = bno.get_calibration_status()
    # Print everything out.
    # print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(heading, roll, pitch, sys, gyro, accel, mag))
    
    """Tof data"""
    distance_mm = tof.get_distance()
    
    """PiCamera RGB value"""
    camera.capture(output,'rgb',use_video_port=True) 
    R = output[56][64][0]
    G = output[56][64][1]
    B = output[56][64][2]
    rgb_value = R<<16 | G<<8 | B
    

    """Transforming to 3D coordinate"""
    x = (- math.sin(math.radians(pitch))) * distance_mm
    z = (math.cos(math.radians(pitch))) * distance_mm
    y = (-math.sin(math.radians(heading))) * x
    x = (math.cos(math.radians(heading))) * x
    
    """Struct the string"""
    msg = ("{0:.2F} {1:.2F} {2:.2F} {3}\n".format(x,y,z,rgb_value))
    channel.basic_publish(exchange='',routing_key='sesdata',body=msg)
    print(msg)
    time.sleep(1)
    
    
    


