#include <Servo.h>
// arduino portları 6 yeşil 9 turuncu 10 sarı 11 mavi
// yeşil 1040'da dönmeye 0
Servo motor;
Servo motor2;
Servo motor3;
Servo motor4;
int yesil = 1150;
int kirmizi = 1150;
int sari = 1150;
int mavi = 1150;

double throttle = 1160;
char incomingByte;

int command = 0;

void setup() {
  motor.attach(3);
  motor2.attach(5);
  motor3.attach(6);
  motor4.attach(9);
  motor.writeMicroseconds(1000);
  motor2.writeMicroseconds(1000);
  motor3.writeMicroseconds(1000);
  motor4.writeMicroseconds(1000);
    for (int i = 1; i<11; i++)
  {
    delay(1000);
    Serial.println(i);
  }  motor.writeMicroseconds(1000);
  motor2.writeMicroseconds(1000);
  motor3.writeMicroseconds(1000);
  motor4.writeMicroseconds(1000);
  delay(1000);
  Serial.begin(115200);
  Serial.println("3 \t 5 \t 6 \t 9");

  int pin4 = LOW;
  int pin5 = LOW;
}

void loop(){
  if (Serial.available() > 0) {
    // read the incoming byte: 
    incomingByte = Serial.read();
    //delay(10);
    if (incomingByte == 'a')
    {
      command = command + 10;
      Serial.print(command); Serial.print("\r")
    }
    if (incomingByte == 'b')
    {
      command = command - 10;
      Serial.print(command) Serial.print("\r");
    }
    if (incomingByte == 'c')
    {
      throttle = 1150;
      command = 0;
      Serial.print(command); Serial.print("\r")
    }
    //Serial.print("I received: ");
    //Serial.println(incomingByte);
  }
int i = 0;

  if (throttle > 1700)
  {
    throttle = 1700;
  }
 while (i<=10)
  {    
    motor.writeMicroseconds(throttle+command);
    motor2.writeMicroseconds(throttle+command);
    motor3.writeMicroseconds(throttle+command);
    motor4.writeMicroseconds(throttle+command);
    i++;
    delay(100);
  } 
}
