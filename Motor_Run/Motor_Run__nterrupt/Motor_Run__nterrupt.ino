#include <Servo.h>
// arduino portları 6 kahverengi 9 yeşil 10 turuncu 11 sarı
// yeşil 1040'da dönmeye başlıyor
Servo motor;
Servo motor2;
Servo motor3;
Servo motor4;
int yesil = 1045;
int kirmizi = 1075;
int sari = 1070;
int mavi = 1070;

int command = 0;

void Increase()
{
  command = command + 10
}
void Decrease()
{
  command = command - 10
}


void setup() {
  motor.attach(6);
  motor2.attach(9);
  motor3.attach(10);
  motor4.attach(11);
  motor.writeMicroseconds(1000);
  motor2.writeMicroseconds(1000);
  motor3.writeMicroseconds(1000);
  motor4.writeMicroseconds(1000);
  delay(10000);
  Serial.begin(115200);
  Serial.println("yeşil\t  kırmızı\tsari\tmavi");
  attachInterrupt(digitalPinToInterrupt(2),Increase,RISING); 
  attachInterrupt(digitalPinToInterrupt(3),Decrease,RISING); 
}

void loop() {
  while (1)
  {    
    motor.writeMicroseconds(yesil+command);
    motor2.writeMicroseconds(kirmizi+command);
    motor3.writeMicroseconds(sari+command);
    motor4.writeMicroseconds(mavi+command);
    i++;
    delay(100);
  }
}
