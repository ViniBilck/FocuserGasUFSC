import serial
import time

class FocuserController:
    def __init__(self, port, baudrate=9600):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)
            print "Connected to {} at {} baud.".format(port, baudrate)
        except serial.SerialException as e:
            print "Failed to connect to {}: {}".format(port, e)
            self.ser = None
        self.initial_distance = 0.0
        self.distance = 0.0
        self.new_time = 0.0
        self.old_time = 0.0
        self.mov_time = 0.0
        self.coef = [2.74463053, 0.45783398]

    def forceZero(self):
        if self.ser and self.ser.is_open:
            print "Sent command to go to zero."
            self.moveIn()
            time.sleep(20)
            self.getStop()
            print "Sent command to stop."
            self.new_time = 0.0
            self.old_time = 0.0
            self.mov_time = 0.0
        
    def goZero(self):
        time.sleep(1)
        if self.ser and self.ser.is_open:
            print "Sent command to go to zero."
            self.goTo(2.2)
            print "Sent command to stop."
            self.new_time = 0.0
            self.old_time = 0.0
            self.mov_time = 0.0
        else:
            print "Serial connection not open. Cannot send command."

    def getStop(self):
        if self.ser and self.ser.is_open:
            self.ser.write(b'S')
            print "Sent command to stop."
        else:
            print "Serial connection not open. Cannot send command."

    def getTime(self, position):
        self.new_time = (-self.coef[0] + position) / self.coef[1]
        print "D = {} mm".format(position)

    def getPosition(self):
        self.position = self.old_time    
    
    def goTo(self, position):
        time.sleep(1)
        if (position >=  2.2) and (position <= 15):
            self.getTime(position)
            if self.new_time < self.old_time:
                self.mov_time = self.old_time - self.new_time
                print 'time: {}'.format(self.mov_time)
                self.old_time = self.new_time
                self.moveIn()
                time.sleep(self.mov_time)
                self.getStop()
            if self.old_time < self.new_time:
                self.mov_time = self.new_time - self.old_time
                print 'time: {}'.format(self.mov_time)
                self.old_time = self.new_time
                self.moveOut()
                time.sleep(self.mov_time)
                self.getStop()
        else:
            print 'Invalid position'


    def moveIn(self):
        if self.ser and self.ser.is_open:
            self.ser.write(b'L')
            print "Sent command to move in."
        else:
            print "Serial connection not open. Cannot send command."

    def moveOut(self):
        if self.ser and self.ser.is_open:
            self.ser.write(b'H')
            print "Sent command to move out."
        else:
            print "Serial connection not open. Cannot send command."


