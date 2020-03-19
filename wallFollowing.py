# This program demonstrates usage of the servos.
# Keep the robot in a safe location before running this program,
# as it will immediately begin moving.
# See https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/ for more details.
from threading import Thread
import time
import Adafruit_PCA9685
import signal
import math
import RPi.GPIO as GPIO
import json
import math
from random import randint
import sys
sys.path.append('/home/pi/VL53L0X_rasp_python/python')
import VL53L0X

from datetime import datetime
# The servo hat uses its own numbering scheme within the Adafruit library.
# 0 represents the first servo, 1 for the second, and so on.
LSERVO = 0
RSERVO = 1
diameter = 2.6

# Pins that the encoders are connected to
LENCODER = 17
RENCODER = 18

# Pins that the sensors are connected to
LSHDN = 27
FSHDN = 22
RSHDN = 23

DEFAULTADDR = 0x29 # All sensors use this address by default, don't change this
LADDR = 0x2a
RADDR = 0x2b

# Set the pin numbering scheme to the numbering shown on the robot itself.
GPIO.setmode(GPIO.BCM)

# Setup pins
GPIO.setup(LSHDN, GPIO.OUT)
GPIO.setup(FSHDN, GPIO.OUT)
GPIO.setup(RSHDN, GPIO.OUT)

# Shutdown all sensors
GPIO.output(LSHDN, GPIO.LOW)
GPIO.output(FSHDN, GPIO.LOW)
GPIO.output(RSHDN, GPIO.LOW)

time.sleep(0.01)

# Initialize all sensors
lSensor = VL53L0X.VL53L0X(address=LADDR)
fSensor = VL53L0X.VL53L0X(address=DEFAULTADDR)
rSensor = VL53L0X.VL53L0X(address=RADDR)

# Connect the left sensor and start measurement
GPIO.output(LSHDN, GPIO.HIGH)
time.sleep(0.01)
lSensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)

# Connect the right sensor and start measurement
GPIO.output(RSHDN, GPIO.HIGH)
time.sleep(0.01)
rSensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)

# Connect the front sensor and start measurement
GPIO.output(FSHDN, GPIO.HIGH)
time.sleep(0.01)
fSensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)



class Test:
    def __init__(self):
        self.timer_left = 0.0
        self.timer_right = 0.0
        self.count_left = 0
        self.count_right = 0
        self.count = (0,0)
        self.speed = (0,0)
        self.PWM_left = 1.5
        self.PWM_right = 1.5
        
        self.CanDoRight = False
        self.LeftTurns = 0
        self.RightTurns = 0
        self.Uturns = 0
       
    def resetCount(self):
        self.count_left = 0
        self.count_right = 0
        self.count = (0,0)

    def getCounts(self):
        self.count = (self.count_left, self.count_right)
        return self.count
    
    def getSpeeds(self):
        start = [self.count_left, self.count_right]
        time.sleep(1)
        finish = [self.count_left, self.count_right]
        self.speed = ((finish[0]-start[0])/32, (finish[1]-start[1])/32)
        return self.speed
    
    def getInstantSpeeds(self, start_count, time_total):
        finish = list(self.getCounts())
        self.speed = (((finish[0]-start_count[0])/32)/time_total, ((finish[1]-start_count[1])/32)/time_total)
        return self.speed        
    
def printOutput():
        
    print("\nNumber of Left turns: " + str(Test.LeftTurns))
    print("Number of Right turns: " + str(Test.RightTurns))
    print("Number of U-turns: " + str(Test.Uturns))
    print("\n")



# This function is called when Ctrl+C is pressed.
# It's intended for properly exiting the program.
def ctrlC(signum, frame):
    printOutput()
    # Stop the servos
    pwm.set_pwm(LSERVO, 0, 0);
    pwm.set_pwm(RSERVO, 0, 0);
    lSensor.stop_ranging();
    fSensor.stop_ranging();
    rSensor.stop_ranging();
    GPIO.cleanup()
    exit()    

def left_count_thread():
    min_del = 37/((math.fabs(Test.PWM_left-1.5))/0.2)
    currentL = float(time.time()*1000.0)
    delayL = currentL - Test.timer_left 
    if (delayL < min_del ):
        #Test.timer_left = float(time.time()*1000.0)        
        return
    #print(delay)
    Test.timer_left = float(time.time()*1000.0)    

# This function is called when the left encoder detects a rising edge signal.
def onLeftEncode(pin):
    if (Test.PWM_left > 1.5):
        Test.count_left += 1
    elif (Test.PWM_left < 1.5):
        Test.count_left -= 1
        
    #time.sleep((37/((math.fabs(Test.PWM_left-1.5))/0.2))/1000)

        
        
def right_count_thread():
    currentR = float(time.time()*1000.0)
    min_del = 37/((math.fabs(Test.PWM_right-1.5))/0.2)
    delayR = currentR - Test.timer_right
    if (delayR < min_del ):
        return

    Test.timer_right = float(time.time()*1000.0)   

# This function is called when the right encoder detects a rising edge signal.
def onRightEncode(pin):
    #print(delayR)
    if (Test.PWM_right > 1.5):
        Test.count_right -= 1
    elif (Test.PWM_right < 1.5):
        Test.count_right += 1
    #time.sleep((37/((math.fabs(Test.PWM_right-1.5))/0.2))/1000)

Test = Test()

def calibrateSpeeds():
    Test.PWM = 1.3
    data = {}

    while Test.PWM<1.71:
        Test.PWM_left = Test.PWM
        Test.PWM_right = Test.PWM
        # Write a maximum value of 1.7 for each servo.
        # Since the servos are oriented in opposite directions,
        # the robot will end up spinning in one direction.
        # Values between 1.3 and 1.7 should be used.
        pwm.set_pwm(LSERVO, 0, math.floor(Test.PWM / 20 * 4096));
        pwm.set_pwm(RSERVO, 0, math.floor(Test.PWM / 20 * 4096));
        time.sleep(1)
        print("PWM:" + str(Test.PWM))
        data[Test.PWM] = Test.getSpeeds()
        print('\n')
        print(Test.speed)
        Test.PWM = round((Test.PWM + 0.01), 2)
    pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096));
    pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096));
    print(data)
    with open('./data.txt', 'w') as outfile:
        json.dump(data, outfile)






def findClosest(rpsLeft, rpsRight):
    lPWM = 0.0
    rPWM = 0.0   
    with open('data.txt') as json_file:
        data = json.load(json_file)
        bestDifference = 999
        #FOR left PWM
        for key, value in data.items():
            difference = math.fabs(value[0]- rpsLeft)
            if (difference < bestDifference):
                bestDifference = difference
                lPWM = key
            
        bestDifference = 999     
        #FOR right PWM
        for key, value in data.items():
            difference = math.fabs(value[1] - rpsRight)
            if (difference < bestDifference):
                bestDifference = difference
                rPWM = key
            
    return([float(lPWM), float(rPWM)])


def setSpeedsPWM(pwmLeft, pwmRight):
    Test.PWM_right = pwmRight
    Test.PWM_left = pwmLeft
    pwm.set_pwm(LSERVO, 0, math.floor(Test.PWM_left / 20 * 4096));
    pwm.set_pwm(RSERVO, 0, math.floor(Test.PWM_right / 20 * 4096));

def setSpeedsRPS(rpsLeft, rpsRight):
    close_PWM = findClosest(rpsLeft, rpsRight)
    setSpeedsPWM(close_PWM[0], close_PWM[1])
    
def setSpeedsIPS(ipsLeft, ipsRight):
    circumference = diameter * math.pi
    setSpeedsRPS(ipsLeft/circumference, ipsRight/circumference)

def setSpeedsVW(v,w):
    d =4.7
    if w >= 0: 
        ipsLeft = v - (w * d/2)
        ipsRight = v + (w * d/2)
        setSpeedsIPS(ipsLeft,ipsRight)
    else:
        rads = w * -1
        ipsLeft2 = v - (rads * d/2)
        ipsRight2 = v + (rads * d/2)
        setSpeedsIPS(ipsRight2,ipsLeft2)
# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)
    
# Set the pin numbering scheme to the numbering shown on the robot itself.
GPIO.setmode(GPIO.BCM)

# Set encoder pins as input
# Also enable pull-up resistors on the encoder pins
# This ensures a clean 0V and 3.3V is always outputted from the encoders.
GPIO.setup(LENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Attach a rising edge interrupt to the encoder pins
GPIO.add_event_detect(LENCODER, GPIO.RISING, onLeftEncode)
GPIO.add_event_detect(RENCODER, GPIO.RISING, onRightEncode)

# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)
    
# Initialize the servo hat library.
pwm = Adafruit_PCA9685.PCA9685()

# 50Hz is used for the frequency of the servos.
pwm.set_pwm_freq(50)

# Write an initial value of 1.5, which keeps the servos stopped.
# Due to how servos work, and the design of the Adafruit library, 
# the value must be divided by 20 and multiplied by 4096.


def loadMeasure():
    setSpeedsPWM(1.6,1.6)
    time.sleep(1)
    start = datetime.now()
    counts = Test.getCounts()
    timer = 0.0
    while True:
        timer += 0.3
        speed = list(Test.getInstantSpeeds(counts, timer))
        dt = datetime.now()
        print(str(dt-start) + '\t\t' + str(speed[0])+ '\t\t' + str(speed[1]))
        if str(dt-start)>('0:00:10.00'):
            break

    
    
#loadMeasure()
        


def mesurments():
    timer = 0.0
    start_count = Test.getCounts()     
    start = datetime.now()
    while Test.Running:
        timer += 0.3
        time.sleep(0.3)
        speed = list(Test.getInstantSpeeds(start_count, timer))
        dt = datetime.now()
        print(str(dt-start) + '\t\t' + str(speed[0])+ '\t\t' + str(speed[1]))
        
def distance(distance, sec):
    speed = distance/sec
    if speed>6.55:
        print("Cant do this distance within seconds")
        return
    circumference = diameter * math.pi
    needToTravel = int((distance/circumference)*32)
    #print(needToTravel)
    setSpeedsIPS(speed, speed)
    while (Test.getCounts()<(needToTravel, -needToTravel)):
            time.sleep(0.01)
    setSpeedsPWM(1.5, 1.5)
    Test.resetCount()
            
def orientation(degrees, sec):
    
    circumference = diameter * math.pi
    part = degrees/360
    distance = (math.pi*4.55*part)
    speed = distance/sec
    if speed>7:
        print("Cant do this turn within seconds")
        return
    needToTravel = int(distance/circumference*32)
    #print(needToTravel)
   
    setSpeedsIPS(speed, -speed)

    if degrees>0:
        while (Test.getCounts()<(needToTravel, -needToTravel)):
            time.sleep(0.01)


    else:
        while ((list(Test.getCounts())[1],list(Test.getCounts())[0]) <(-needToTravel, needToTravel)):
            time.sleep(0.01)


    setSpeedsPWM(1.5, 1.5)
    Test.resetCount()
    return True


    
def saturation(control_signal):
    circumference = diameter * math.pi
    C_min = -0.8*circumference    
    C_max = 0.8*circumference
    control_signal_out = 0.0
    
    if control_signal > C_max:
        control_signal_out = C_max
    elif control_signal < C_min:
        control_signal_out = C_min
    else:
        control_signal_out = control_signal
    return round(control_signal_out, 2)

K = 0.75
start = datetime.now()

def goStraight():
    print("Going Straight")
    while True:
        time.sleep(0.1)

        lDistance = lSensor.get_distance()/25.4
        rDistance = rSensor.get_distance()/25.4
        fDistance = fSensor.get_distance()/25.4
        
        if int(rDistance) > 20 and int(fDistance) > 25 and Test.CanDoRight and int(lDistance) < 14:
            time.sleep(1)
            break
        
        if lDistance > 15:
            lDistance = 7
        
        if rDistance > 15:
            rDistance = 7
        else:
            Test.CanDoRight = True
        
        if (int(fDistance) == int(6)):
            Test.CanDoRight = False
            break
        
        dt = datetime.now()
        print(str(dt-start) + '\t\t' + str(round(fDistance,2))+ '\t\t' + str(round(rDistance,2))+ '\t\t' + str(round(lDistance,2)))

        
        center = (lDistance + rDistance)/2;
        
        desired_dist_left = center
        desired_dist_right = center
        desired_disr_front = 6
                
        dist_err_left = desired_dist_left - lDistance
        dist_err_right = desired_dist_right - rDistance
        dist_err_front = fDistance - desired_disr_front
        
        control_signal_left = K * dist_err_left
        control_signal_right = K * dist_err_right
        control_signal_front = dist_err_front
        
        
        speed_left = saturation(control_signal_left)
        speed_right = saturation(control_signal_right)
        speed_front = saturation(control_signal_front)
       
        setSpeedsIPS(speed_front+speed_left,speed_front+speed_right)

def goLeft():
    print("Turning Left")
    Test.LeftTurns += 1
    orientation(-90, 0.75)

def goRight():
    Test.RightTurns +=1
    print("Turning right")
    orientation(90, 0.75)


def make_Uturn():
    Test.Uturns += 1
    print("Making a U-turn")
    orientation(180,1.5)
    
while True:
    goStraight()
    time.sleep(0.1)
    
    lDistance = lSensor.get_distance()/25.4
    rDistance = rSensor.get_distance()/25.4
    fDistance = fSensor.get_distance()/25.4
    if lDistance > 14 and rDistance<14:
        goLeft()
    elif rDistance > 14 and lDistance<14:
        goRight()
    elif int(lDistance+rDistance) < 20:
        make_Uturn()
    else:
        RANDOM = randint(0,1)
        if RANDOM:
            goLeft()
        else:
            goRight()

# Stop measurement for all sensors
lSensor.stop_ranging()
fSensor.stop_ranging()
rSensor.stop_ranging()


#calibrateSpeeds()
    
#setSpeedsVW(4,1)
#setSpeedsPWM(1.7,1.7)
#setSpeedsRPS(1, -1)      
#setSpeedsIPS(8,8)

#Test.Running =True
#Thread(target=(mesurments)).start()
#circle(float(R), float(Y))
#orientation(float(X), float(Y))
#Test.Running =False

#print(Test.getCounts())
#rectangle (float(H),float(W),float(Y))
     
pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096));
pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096));