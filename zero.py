import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

left=21
right=22
forward=23
reverse=24

GPIO.setup(left,GPIO.OUT)
GPIO.setup(right,GPIO.OUT)
GPIO.setup(forward,GPIO.OUT)
GPIO.setup(reverse,GPIO.OUT)

GPIO.output(forward,0)
GPIO.output(reverse,0)
GPIO.output(left,0)
GPIO.output(right,0)
	
left=20
right=16
forward=19
reverse=26
conn=13;

GPIO.setup(conn,GPIO.OUT)
GPIO.setup(left,GPIO.OUT)
GPIO.setup(right,GPIO.OUT)
GPIO.setup(forward,GPIO.OUT)
GPIO.setup(reverse,GPIO.OUT)

GPIO.output(conn,0)
GPIO.output(forward,0)
GPIO.output(reverse,0)
GPIO.output(left,0)
GPIO.output(right,0)
	
