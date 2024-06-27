int IN3 = 5; 
int IN4 = 4;

void setup() {
  Serial.begin(9600);
  pinMode(IN4, OUTPUT);    
  pinMode(IN3, OUTPUT);   
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'L') {
      // Motor forward
      digitalWrite(IN4, HIGH);
      digitalWrite(IN3, LOW);
    } else if (command == 'H') {
      // Motor reverse
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
    } else if (command == 'S') {
      // Motor stop
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
    }
  }
}
im