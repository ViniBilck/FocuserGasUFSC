import serial
import time
import keyboard


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

    def motor_forward(self):
        """Run motor forward."""
        self.ser.write(b'L')
        print("Motor running forward")

    def motor_reverse(self):
        """Run motor in reverse."""
        self.ser.write(b'H')
        print("Motor running in reverse")

    def motor_stop(self):
        """Stop the motor."""
        self.ser.write(b'S')
        print("Motor stopped")

    def quit(self):
        """Quit the control loop."""
        self.running = False
        print("Exiting...")

    def print_ascii_art(self):

        art = """
  ______                             _____       
 |  ____|                           |  __ \      
 | |__ ___   ___ _   _ ___  ___ _ __| |__) |   _ 
 |  __/ _ \ / __| | | / __|/ _ \ '__|  ___/ | | |
 | | | (_) | (__| |_| \__ \  __/ |  | |   | |_| |
 |_|  \___/ \___|\__,_|___/\___|_|  |_|    \__, |
                                            __/ |
                                           |___/ 
        """
        print(art)

    def run(self):
        """Main loop to listen for keyboard commands."""
        self.print_ascii_art()
        print("Press 'l' to move forward, 's' to stop, 'h' to move backward, and 'q' to quit")
        try:
            while self.running:
                for key, action in self.commands.items():
                    if keyboard.is_pressed(key):
                        action()
                        time.sleep(0.2)  # Debounce delay
        finally:
            self.ser.close()


# Example usage
if __name__ == "__main__":
    motor_controller = FocuserController('/dev/ttyUSB0')  # Update with your serial port
    motor_controller.run()
