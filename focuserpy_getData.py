import serial
import time
import keyboard
from timeit import default_timer as timer
import pandas as pd
import numpy as np

class FocuserController:
    def __init__(self, port, baudrate=9600):
        self.ser = serial.Serial(port, baudrate)
        self.running = True
        self.commands = {
            'l': self.motor_forward,
            'h': self.motor_reverse,
            's': self.motor_stop,
            'q': self.quit
        }
        self.time_start = 0
        self.time_stop = 0
        self.dataframe = pd.DataFrame(columns=['Time(s)', 'D-i(mm)', 
                                               'D-f(mm)', 'D(mm)', 
                                               'Spin', 'Vel(mm/s)'])
        self.initial_distance = 0.0
        self.final_distance = 0.0
        self.distance = 0.0
        self._time = 0.0


    def motor_forward(self):
        """Run motor forward."""
        print("input initial distance")
        self.initial_distance = float(input())        
        self.ser.write(b'L')
        self.time_start = timer()
        print("\n Motor running forward")

    def motor_reverse(self):
        """Run motor in reverse."""
        print("input initial distance")
        self.initial_distance = float(input())                
        self.ser.write(b'H')
        self.time_start = timer()
        print("\n Motor running in reverse")

    def motor_stop(self):
        """Stop the motor."""
        self.ser.write(b'S')
        self.time_stop = timer()
        self._time = self.time_stop - self.time_start
        print("\n Motor stopped")
        print('input final distance')
        self.final_distance = float(input())
        print(f"\n t: {self._time}")

    def quit(self):
        """Quit the control loop."""
        self.running = False
        print("\n Exiting...")

    def run(self):
        """Main loop to listen for keyboard commands."""
        try:
            while self.running:
                print("Press 'l' to move forward, 's' to stop, 'h' to move backward, and 'q' to quit")
                self.command = input()
                if self.command != 's':
                    self.spin = self.command
                for key, action in self.commands.items():
                   if self.command == key:
                        action()
                        if self.command == "s":
                            self.distance = np.linalg.norm(self.final_distance - self.initial_distance)
                            self.new_df = pd.DataFrame([{'Time(s)':self._time, 
                                                     'D-i(mm)':self.initial_distance, 
                                                     'D-f(mm)':self.final_distance,
                                                     'D(mm)':self.distance,
                                                     'Spin':self.spin,
                                                     'Vel(mm/s)':self.distance / self._time}])
                            self.dataframe = pd.concat([self.dataframe, self.new_df])
                            print(self.dataframe)
                            self.dataframe.to_csv("data.csv")
                        time.sleep(0.2)  # Debounce delay
        finally:
            self.ser.close()


# Example usage
if __name__ == "__main__":
    motor_controller = FocuserController('/dev/ttyUSB0')  # Update with your serial port
    motor_controller.run()
