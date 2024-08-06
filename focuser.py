import serial
import time
import numpy as np
from scipy.optimize import fsolve

class FocuserController:
    def __init__(self, port, baudrate=9600):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)
            print(f"Connected to {port} at {baudrate} baud.")
        except serial.SerialException as e:
            print(f"Failed to connect to {port}: {e}")
            self.ser = None
        self.initial_distance = 0.0
        self.distance = 0.0
        self.new_time = 0.0
        self.old_time = 0.0
        self.mov_time = 0.0
        self.coef = [2.19267852, 1.95741252e-01, -4.28436162e-04]
        self.speed = 0.193
        #self.goZero()

    def forceZero(self):
        if self.ser and self.ser.is_open:
            print("Sent command to go to zero.")
            self.moveIn()
            time.sleep(20)
            self.getStop()
            print("Sent command to stop.")
            self.new_time = 0.0
            self.old_time = 0.0
            self.mov_time = 0.0
        
    def goZero(self):
        time.sleep(1)
        if self.ser and self.ser.is_open:
            print("Sent command to go to zero.")
            self.goTo(2.2)
            print("Sent command to stop.")
            self.new_time = 0.0
            self.old_time = 0.0
            self.mov_time = 0.0
        else:
            print("Serial connection not open. Cannot send command.")

    def getStop(self):
        if self.ser and self.ser.is_open:
            self.ser.write(b'S')
            print("Sent command to stop.")
        else:
            print("Serial connection not open. Cannot send command.")

    def getTime(self, position):
        f = lambda x: self.coef[0] - position + self.coef[1]*x + (self.coef[2]*x**2)/2
        for i in fsolve(f, [-20,20]):
            if i > 0:
                self.new_time = i
        print(f"D = {position} mm")

    def getPosition(self):
        f = lambda x: self.coef[0] - self.position + self.coef[1]*x + (self.coef[2]*x**2)/2
        self.position = f(self.old_time)

        self.position = self.old_time    
    def goTo(self, position):
        time.sleep(1)
        if (position >=  2.2) and (position <= 15):
            self.getTime(position)
            if self.new_time < self.old_time:
                self.mov_time = self.old_time - self.new_time
                print(f'time: {self.mov_time}')
                self.old_time = self.new_time
                self.moveIn()
                time.sleep(self.mov_time)
                self.getStop()
            if self.old_time < self.new_time:
                self.mov_time = self.new_time - self.old_time
                print(f'time: {self.mov_time}')
                self.old_time = self.new_time
                self.moveOut()
                time.sleep(self.mov_time)
                self.getStop()
        else:
            print('Invalid position')


    def moveIn(self):
        if self.ser and self.ser.is_open:
            self.ser.write(b'L')
            print("Sent command to move in.")
        else:
            print("Serial connection not open. Cannot send command.")

    def moveOut(self):
        if self.ser and self.ser.is_open:
            self.ser.write(b'H')
            print("Sent command to move out.")
        else:
            print("Serial connection not open. Cannot send command.")


    def quit(self):
        """Quit the control loop."""
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.running = False
        print("\nExiting...")

    def run(self):
        """Main loop to listen for keyboard commands."""
        if self.ser and self.ser.is_open:
            self.ser.close()

"""
if __name__ == "__main__":
    motor_controller = FocuserController('/dev/ttyUSB0')  # Update with your serial port
    if motor_controller.ser and motor_controller.ser.is_open:
        motor_controller.goZero()
        #motor_controller.goTo(7)
        #time.sleep(10)
        #motor_controller.goTo(4)


        
    else:
        print("Failed to initialize the motor controller.")
"""
