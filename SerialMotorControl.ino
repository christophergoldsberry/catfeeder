/*
  Motor Test connection over serial
 */
 #include <AFMotor.h>

// Connect a stepper motor with 48 steps per revolution (7.5 degree)
// to motor port #2 (M3 and M4)
AF_Stepper motor(200, 2);

// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int led = 13;

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(led, OUTPUT);
  Serial.begin(9600);
  Serial.println("stepper control test");
  
  motor.setSpeed(10); //10 RPM
}

// the loop routine runs over and over again forever:
void loop() {
  motor.release();
  while(1){
    if (Serial.available()) {
      motortest(Serial.read()- '0');
    }
    delay(500);
  }
}

void motortest(int n) {
  if(n == 1){
    digitalWrite(led, HIGH);
    motor.step(150,FORWARD,DOUBLE);
    digitalWrite(led, LOW);
    delay(500);
    motor.release();
  }
  else {
    for(int i=1;i<3;i++){
      digitalWrite(led, HIGH);
      delay(5000);
      digitalWrite(led, LOW);
      delay(5000);
     }
  }
}
/*
  digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);               // wait for a second
  digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);               // wait for a second
}*/
