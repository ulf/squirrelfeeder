import RPi.GPIO as GPIO
import time
import subprocess
 
#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
 
# Setup PINs for distance measuring
GPIO_TRIGGER = 11
GPIO_ECHO = 12 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Define pins for the stepper motor
StepPins = [18,22,24,26]

# Set all pins as output
for pin in StepPins:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)
  
# Contains the number of cycles to rotate
rotate = 0
# Delay between to rotate cycles
WaitTime = 0.005

# Define simple sequence for rotating the motor
StepCounter = 0
StepCount = 4
Seq = []
Seq = range(0, StepCount)
Seq[3] = [1,0,0,0]
Seq[2] = [0,1,0,0]
Seq[1] = [0,0,1,0]
Seq[0] = [0,0,0,1]

# returns distance in cm  
def distance():
  GPIO.output(GPIO_TRIGGER, True)
 
  # trigger signal
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
 
  StartTime = time.time()
  StopTime = time.time()
 
  # Save start time
  while GPIO.input(GPIO_ECHO) == 0:
    StartTime = time.time()
    if StartTime - StopTime > 1:
      return 999
 
  # save time when echo arrives
  while GPIO.input(GPIO_ECHO) == 1:
    StopTime = time.time()
    if (StopTime - StartTime) > 1:
      return 999
 
  # Calculate distance based on speed of sound
  TimeElapsed = StopTime - StartTime
  distance = (TimeElapsed * 34300) / 2
  return distance

rotation = False
 
if __name__ == '__main__':
  try:
    while True:
      if rotate > 0:
        rotate -= 1
        for pin in range(0, 4):
          xpin = StepPins[pin]
          if Seq[StepCounter][pin]!=0:
            GPIO.output(xpin, True)
          else:
            GPIO.output(xpin, False)      
        StepCounter += 1
        if (StepCounter==StepCount):
          StepCounter = 0
        if (StepCounter<0):
          StepCounter = StepCount
        time.sleep(WaitTime)
        rotation = True
      else:
        if rotation:
          rotation = False
          with open('/tmp/rotate','w') as f:
            f.write(str(time.time()))
        dist = distance()
        # Rotate for 1020 cycles ( ~180 degrees)
        if dist > 0 and dist < 10:
          rotate = 1020
        time.sleep(0.2)
 
  except KeyboardInterrupt:
    GPIO.cleanup()
