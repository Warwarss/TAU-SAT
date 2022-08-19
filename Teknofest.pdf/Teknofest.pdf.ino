#include "I2Cdev.h" //I2C kütüphanesi
#include "MPU6050.h" //Mpu6050 kütüphanesi
#include "Wire.h"
MPU6050 accelgyro; // Mpu6050 sensör tanımlama
int16_t ax, ay, az; //ivme tanımlama
int16_t gx, gy, gz; //gyro tanımlama
float temp;
int16_t temp_raw;
  
void setup() {
Wire.begin();
Serial.begin(9600);
accelgyro.initialize();
}
  
void loop() {
accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz); // ivme ve gyro değerlerini okuma
temp_raw=accelgyro.getTemperature();
temp = float(temp_raw + 521)/340 + 35.0;
  
//açısal ivmeleri ve gyro değerlerini ekrana yazdırma
Serial.println(temp);
delay(1000);
}
