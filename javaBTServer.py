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
vehicle="truck"
GPIO.setmode(GPIO.BCM)
lightList=21
lightConn=13
left=20
right=16
reverse=19
forward=26
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
        sSock.close()
        cSock.close()
    except:
        print("")
    SYS.exit(0)

'''Set up bluetooth things'''
superDone=False
while not superDone:
    try:
        done=False
        zero()
        server_sock=BT.BluetoothSocket(BT.RFCOMM)
        server_sock.bind(("",BT.PORT_ANY))
        server_sock.listen(1)
        GPIO.output(lightConn,0)
        GPIO.output(lightList,1)
        port=server_sock.getsockname()[1]
        uuid="96aba6f4-50b1-4737-b3e8-30a430ea494b"
        BT.advertise_service(server_sock,"Pi-Car",service_id=uuid,service_classes=[uuid,BT.SERIAL_PORT_CLASS],profiles=[BT.SERIAL_PORT_PROFILE])
        try:
            client_sock,address=server_sock.accept()
            GPIO.output(lightList,0)
            GPIO.output(lightConn,1)
            while not done:
                data=client_sock.recv(1024)
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
                    done=True 
        except KeyboardInterrupt:
            client_sock.close()
            done=True
            superDone=True

    except:
        print("")
        #print(SYS.exc_info()[0])
        #TRACE.print_exc()
        dieDamnit(client_sock,server_sock)
dieDamnit(client_sock,server_sock)
