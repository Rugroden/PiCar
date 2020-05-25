import bluetooth as BT
import RPi.GPIO as GPIO
import traceback as TRACE
import sys as SYS
'''
Setup GPIO things.
Diagram:Car:Truck:Wire:Target
   in1:21:20:RED   :LEFT
   in2:22:16:YELLOW:RIGHT
   in3:23:19:GREEN :REVERSE
   in4:24:26:BLUE  :FORWARD

LISTENING: 13:RED 
CONNECTED: 21:GREEN
'''
vehicle="car"
GPIO.setmode(GPIO.BCM)
lightList=13
lightConn=6
left=21
right=22
reverse=23
forward=24
client_sock=None
server_sock=None

GPIO.setup(left,GPIO.OUT)
GPIO.setup(right,GPIO.OUT)
GPIO.setup(reverse,GPIO.OUT)
GPIO.setup(forward,GPIO.OUT)
GPIO.setup(lightList,GPIO.OUT)
GPIO.setup(lightConn,GPIO.OUT)

def FORWARD():
    GPIO.output(reverse,0)
    GPIO.output(forward,1)
def FRN():
    GPIO.output(reverse,0)
    GPIO.output(forward,0)
def REVERSE():
    GPIO.output(forward,0)
    GPIO.output(reverse,1)
def LEFT():
    GPIO.output(right,0)
    GPIO.output(left,1)
def LRN():
    GPIO.output(right,0)
    GPIO.output(left,0)
def RIGHT():
    GPIO.output(left,0)
    GPIO.output(right,1)
def zero():
    GPIO.output(lightList,0)
    GPIO.output(lightConn,0)
    FRN()
    LRN()
def dieDamnit(cSock,sSock):
    try:
        zero()
        cSock.close()
        sSock.close()
    except:
        print("Exception in die()")
    SYS.exit(0)

'''Set up bluetooth things'''
superDone=False
while not superDone:
    try:
        connected=False
        zero()
        server_sock=BT.BluetoothSocket(BT.RFCOMM)
        server_sock.bind(("",BT.PORT_ANY))
        server_sock.listen(1)
        GPIO.output(lightConn,0)
        GPIO.output(lightList,1)
        uuid="89cdc54c-9dcb-11ea-b26b-2baa1b4a399b"
        BT.advertise_service(server_sock,
                "Pi-Car",
                service_id=uuid,
                service_classes=[uuid,BT.SERIAL_PORT_CLASS],
                profiles=[BT.SERIAL_PORT_PROFILE]
                )
        try:
            client_sock,address=server_sock.accept()
            connected = True
            GPIO.output(lightList,0)
            GPIO.output(lightConn,1)
            while connected:
                data=client_sock.recv(1024).decode()
                print("recieved '{}'".format(data))
                if data=="wa":
                    FORWARD()
                    LEFT()
                elif data=="w":
                    FORWARD()
                    LRN()
                elif data=="wd":
                    FORWARD()
                    RIGHT()
                elif data=="a":
                    FRN()
                    LEFT()
                elif data=="d":
                    FRN()
                    RIGHT()
                elif data=="sa":
                    REVERSE()
                    LEFT()
                elif data=="s":
                    REVERSE()
                    LRN()
                elif data=="sd":
                    REVERSE()
                    RIGHT()
                elif data=='q':
                    FRN()
                    LRN()
                elif data=="l":
                    client_sock.close()
                    connected = False
                else:
                    print("unexpected data recieved")
        except KeyboardInterrupt:
            client_sock.close()
            connected = False
            superDone = True

    except:
        TRACE.print_exc()
        dieDamnit(client_sock,server_sock)
dieDamnit(client_sock,server_sock)
GPIO.cleanup()
