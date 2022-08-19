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

void setup() {
  motor.attach(6);
  motor2.attach(9);
  motor3.attach(10);
  motor4.attach(11);
  motor.writeMicroseconds(1000);
  motor2.writeMicroseconds(1000);
  motor3.writeMicroseconds(1000);
  motor4.writeMicroseconds(1000);
  pinMode(5,INPUT);
  pinMode(4,INPUT);
  delay(10000);
  Serial.begin(115200);
  Serial.println("yeşil\t  kırmızı\tsari\tmavi");

  int pin4 = LOW;
  int pin5 = LOW;
}

void Increase()
{
   command = command + 5;
   if (command > 100)
   {
    command = 100;
   }
   for (int i = 0; i <= 10; i++)
   {
    motor.writeMicroseconds(yesil+command);
    motor2.writeMicroseconds(kirmizi+command);
    motor3.writeMicroseconds(sari+command);
    motor4.writeMicroseconds(mavi+command);
    delay(100);
   }
   Serial.print(command);
   Serial.println("Increae");   
}

void Decrease()
{
   }
   for (int i = 0; i <= 10; i++)
   {
    motor.writeMicroseconds(yesil+command);
    motor2.writeMicroseconds(kirmizi+command);
    motor3.writeMicroseconds(sari+command);
    motor4.writeMicroseconds(mavi+command);
    delay(100);
   }
  Serial.print(command);
  Serial.println("Decreae");   
}

void loop() {   
  motor.writeMicroseconds(1000);
  motor2.writeMicroseconds(1000);
  motor3.writeMicroseconds(1000);
  motor4.writeMicroseconds(1000);
  delay(1000);
//  for (int i = 0; i <= 50; i += 3)
//  {
//    motor.writeMicroseconds(yesil + i);
//    motor2.writeMicroseconds(kirmizi + i);
//    motor3.writeMicroseconds(sari + i);
//    motor4.writeMicroseconds(mavi + i);
//    Serial.print(yesil + i);
//    Serial.print("       ");
//    Serial.print(kirmizi + i);
//    Serial.print("       ");
//    Serial.print(sari + i);
//    Serial.print("       ");
//    Serial.println(mavi + i);
//    delay(1000);
//  }
//  delay(10000);
//  for (int i = 50; i <= 100; i += 1)
//  {
//    motor.writeMicroseconds(yesil + i);
//    motor2.writeMicroseconds(kirmizi + i);
//    motor3.writeMicroseconds(sari + i);
//    motor4.writeMicroseconds(mavi + i);
//    Serial.print(yesil + i);
//    Serial.print("       ");
//    Serial.print(kirmizi + i);
//    Serial.print("       ");
//    Serial.print(sari + i);
//    Serial.print("       ");
//    Serial.println(mavi + i);
//    delay(1000);
//  }
    int i = 0;
    while (i<=10)
    {    
      motor.writeMicroseconds(yesil);
      motor2.writeMicroseconds(kirmizi);
      motor3.writeMicroseconds(sari);
      motor4.writeMicroseconds(mavi);
      i++;
      delay(100);
    }
    delay(3000);
    i = 0;
    while (i<=10)
    {    
      motor.writeMicroseconds(yesil+10);
      motor2.writeMicroseconds(kirmizi+10);
      motor3.writeMicroseconds(sari+10);
      motor4.writeMicroseconds(mavi+10);
      i++;
      delay(100);
    }
    i = 0;
    delay(3000);
      while (i<=10)
    {    
      motor.writeMicroseconds(yesil+20);
      motor2.writeMicroseconds(kirmizi+20);
      motor3.writeMicroseconds(sari+20);
      motor4.writeMicroseconds(mavi+20);
      i++;
      delay(100);
    } 
    delay(5000);
    motor.writeMicroseconds(1000);
    motor2.writeMicroseconds(1000);
    motor3.writeMicroseconds(1000);
    motor4.writeMicroseconds(1000);
    Serial.println("Motorlar durdu");
    while (1);
//  }
