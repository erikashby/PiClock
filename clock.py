#################################################################
## The amazing clock program
## This program was written by Esther Ashby and her father
## This program has no rights or restrictions and can be copied by anyone
## who whishes to have a cool clock.

## This program is designed to work with a 7 segment display board
## that was created for this program, and will run on a Raspberry Pi #2
## using retro pi. (Becasue we also like to play games)  ;-)

## Running this program:
## This program must run as root (Eg: sudo python clock.py)

##################################################################
#Initiate CLOCK section

#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
#import pygame

#Global GPIO Serial Ports
SDI   = 4
RCLK  = 20
SRCLK = 21

#Global Alarm
alarm='07:00'

#Digits
one=[0,0,0,0,0,1,1,0]
two=[0,0,1,1,1,0,1,1]
three=[0,0,1,0,1,1,1,1]
four=[0,1,1,0,0,1,1,0]
five=[0,1,1,0,1,1,0,1]
six=[0,1,1,1,1,1,0,1]
seven=[0,0,0,0,0,1,1,1]
eight=[0,1,1,1,1,1,1,1]
nine=[0,1,1,0,0,1,1,1]
zero=[0,1,0,1,1,1,1,1]
error=[1,0,1,0,0,0,0,0]

##################################################################
#Functions section

#GPIO Setup
def GPIO_setup():
    GPIO.setmode(GPIO.BCM)    # Number GPIOs by its physical location
    GPIO.setup(SDI, GPIO.OUT)
    GPIO.setup(RCLK, GPIO.OUT)
    GPIO.setup(SRCLK, GPIO.OUT)
    GPIO.output(SDI, GPIO.LOW)
    GPIO.output(RCLK, GPIO.LOW)
    GPIO.output(SRCLK, GPIO.LOW)


#set_digit :
# This will push a digit into the 7 segment display;  The way
#this is wired each digit added will push all other digets to the left
    
def clear():
    GPIO.output(SDI, GPIO.LOW)
    for x in range(0,32):
        GPIO.output(SRCLK, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(SRCLK, GPIO.LOW)
        time.sleep(0.001)
    GPIO.output(RCLK, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(RCLK, GPIO.LOW)
    time.sleep(0.001)

def erase() :
    GPIO.output(SDI , GPIO.LOW)
    for x in range(0,8):
        GPIO.output(SRCLK, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(SRCLK, GPIO.LOW)

    

def set_digit(n):

    if n == 1:
        display = one
    elif n == 2:
        display = two
    elif n == 3:
        display = three
    elif n == 4:
        display = four
    elif n == 5:
        display = five
    elif n == 6:
        display = six
    elif n == 7:
        display = seven
    elif n == 8:
        display = eight
    elif n == 9:
        display = nine
    elif n == 0:
        display = zero
    else:
        display = error

    for d in display:
        GPIO.output(SDI, d)
        GPIO.output(SRCLK, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(SRCLK, GPIO.LOW)
        time.sleep(0.001)

def update_clock():
    GPIO.output(RCLK, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(RCLK, GPIO.LOW)
    

##################################################################
# Main section

print "Press control-C to quit"

### Initilize clock
GPIO_setup()
clear()

#Test Digits
for x in range(0,11):
    print x
    set_digit(x)
    update_clock()
    time.sleep(.5)
clear()

#change old-time to ZERO
old_time = "0000"
#challange
#for x in range(0,2) :
#    set_digit(3)
#    update_clock()
#    time.sleep(5)
#erase()
#time.sleep(5)

while True:
    #change current-time to real time
    current_time = time.strftime("%I%M", time.localtime())
    alarm_time = time.strftime("%R", time.localtime())
    

    #if current-time is different from old-time then update clock
    if not(current_time == old_time):
        #Set new time on clock memory
        pos = 0
        for d in current_time:
            if pos == 0 and int(d) == 0:
                erase()
            else:
                set_digit(int(d))
            pos = pos + 1

        #Update the clock display
        update_clock()

        print current_time
        #print alarm_time

    #if alarm_time == alarm:
    #    pygame.mixer.init()
    #    pygame.mixer.music.load('01-02- The Apology Song.mp3')
    #    pygame.mixer.music.set_volume(1)
    #    pygame.mixer.music.play()

        #Update old_tme
        old_time = current_time

    #wait 1 second
    time.sleep(.01)
