// Include the Stepper library:
#include "Stepper.h"

// Define number of steps per revolution:
const int stepsPerRevolution = 200;

// Initialize the stepper library on pins 4 through 7:
Stepper myStepper = Stepper(stepsPerRevolution, 4, 5, 6, 7);

// Motor driver pins
const int IN1 = 4;
const int IN2 = 5;
const int IN3 = 6;
const int IN4 = 7;

void setup() {
  // Set the motor speed (RPMs):
  myStepper.setSpeed(100);
  
  // Initialize serial communication:
  Serial.begin(9600);

  // Set motor driver pins as outputs
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    if (command == 'L') {
      // Step one revolution forward:
      myStepper.step(stepsPerRevolution);
      Serial.println("Motor running forward");
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
    } else if (command == 'H') {
      // Step one revolution backward:
      myStepper.step(-stepsPerRevolution);
      Serial.println("Motor running in reverse");
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
    } else if (command == 'S') {
      // Stop the motor and disable the motor driver pins
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
      Serial.println("Motor stopped and powered off");
    }
  }
}

