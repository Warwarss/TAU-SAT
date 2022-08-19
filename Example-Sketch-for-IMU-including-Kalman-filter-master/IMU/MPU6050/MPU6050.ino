#include <Wire.h>
#include "Kalman.h" // Source: https://github.com/TKJElectronics/KalmanFilter
#include <Servo.h>
// arduino portları 6 yeşil 9 turuncu 10 sarı 11 mavi
// yeşil 1040'da dönmeye başlıyor
Servo motor;
Servo motor2;
Servo motor3;
Servo motor4;
int incomingByte = 0;
float PID[2], pwmLeft, pwmRight, pwmFront, pwmBack, error_roll, error_pitch, previous_error_roll, previous_error_pitch;
float pid_p[2]={0, 0};
float pid_i[2]={0, 0};
float pid_d[2]={0, 0};
/////////////////PID CONSTANTS/////////////////
double kp[2]={0, 0.5};//3.55
double ki[2]={0.000, 0.000};//0.003
double kd[2]={1, 2};//2.05
///////////////////////////////////////////////
double throttle=1450; //initial value of throttle to the motors
double upperlimit = 1600;
double lowerlimit = 1150;
float desired_angle = 0; //This is the angle in which we whant the
                         //balance to stay steady

#define RESTRICT_PITCH // Comment out to restrict roll to ±90deg instead - please read: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf

Kalman kalmanX; // Create the Kalman instances
Kalman kalmanY;

/* IMU Data */
double accX, accY, accZ;
double gyroX, gyroY, gyroZ;

double gyroXangle, gyroYangle; // Angle calculate using the gyro only
double compAngleX, compAngleY; // Calculated angle using a complementary filter
double kalAngleX, kalAngleY; // Calculated angle using a Kalman filter

uint32_t timer;
uint8_t i2cData[14]; // Buffer for I2C data

// TODO: Make calibration routine

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Serial.println("Started");
  TWBR = ((F_CPU / 400000L) - 16) / 2; // Set I2C frequency to 400kHz

  i2cData[0] = 7; // Set the sample rate to 1000Hz - 8kHz/(7+1) = 1000Hz
  i2cData[1] = 0x00; // Disable FSYNC and set 260 Hz Acc filtering, 256 Hz Gyro filtering, 8 KHz sampling
  i2cData[2] = 0x00; // Set Gyro Full Scale Range to ±250deg/s
  i2cData[3] = 0x00; // Set Accelerometer Full Scale Range to ±2g
  while (i2cWrite(0x19, i2cData, 4, false)); // Write to all four registers at once
  while (i2cWrite(0x6B, 0x01, true)); // PLL with X axis gyroscope reference and disable sleep mode

  while (i2cRead(0x75, i2cData, 1));
  if (i2cData[0] != 0x68) { // Read "WHO_AM_I" register
    Serial.print(F("Error reading sensor"));
    while (1);
  }

  delay(100); // Wait for sensor to stabilize

  /* Set kalman and gyro starting angle */
  while (i2cRead(0x3B, i2cData, 6));
  accX = (i2cData[0] << 8) | i2cData[1];
  accY = (i2cData[2] << 8) | i2cData[3];
  accZ = (i2cData[4] << 8) | i2cData[5];

  // Source: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf eq. 25 and eq. 26
  // atan2 outputs the value of -π to π (radians) - see http://en.wikipedia.org/wiki/Atan2
  // It is then converted from radians to degrees
#ifdef RESTRICT_PITCH // Eq. 25 and 26
  double roll  = atan2(accY, accZ) * RAD_TO_DEG;
  double pitch = atan(-accX / sqrt(accY * accY + accZ * accZ)) * RAD_TO_DEG;
#else // Eq. 28 and 29
  double roll  = atan(accY / sqrt(accX * accX + accZ * accZ)) * RAD_TO_DEG;
  double pitch = atan2(-accX, accZ) * RAD_TO_DEG;
#endif

  kalmanX.setAngle(roll); // Set starting angle
  kalmanY.setAngle(pitch);
  gyroXangle = roll;
  gyroYangle = pitch;
  compAngleX = roll;
  compAngleY = pitch;
  motor.attach(9);
  motor2.attach(6);
  motor3.attach(3);
  motor4.attach(5);
  motor.writeMicroseconds(1000);
  motor2.writeMicroseconds(1000);
  motor3.writeMicroseconds(1000);
  motor4.writeMicroseconds(1000);
  delay(10000);
  motor.writeMicroseconds(1000);
  motor2.writeMicroseconds(1000);
  motor3.writeMicroseconds(1000);
  motor4.writeMicroseconds(1000);
  delay(1000);
  Serial.begin(115200);
  timer = micros();
}

void loop() {
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();
    throttle = incomingByte;
    Serial.print("I received: ");
    Serial.println(incomingByte, DEC);
  }
  /* Update all the values */
  while (i2cRead(0x3B, i2cData, 14));
  accX = ((i2cData[0] << 8) | i2cData[1]);
  accY = ((i2cData[2] << 8) | i2cData[3]);
  accZ = ((i2cData[4] << 8) | i2cData[5]);
  gyroX = (i2cData[8] << 8) | i2cData[9];
  gyroY = (i2cData[10] << 8) | i2cData[11];
  gyroZ = (i2cData[12] << 8) | i2cData[13];

  double dt = (double)(micros() - timer) / 1000000; // Calculate delta time
  timer = micros();

  // Source: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf eq. 25 and eq. 26
  // atan2 outputs the value of -π to π (radians) - see http://en.wikipedia.org/wiki/Atan2
  // It is then converted from radians to degrees
#ifdef RESTRICT_PITCH // Eq. 25 and 26
  double roll  = atan2(accY, accZ) * RAD_TO_DEG;
  double pitch = atan(-accX / sqrt(accY * accY + accZ * accZ)) * RAD_TO_DEG;
#else // Eq. 28 and 29
  double roll  = atan(accY / sqrt(accX * accX + accZ * accZ)) * RAD_TO_DEG;
  double pitch = atan2(-accX, accZ) * RAD_TO_DEG;
#endif

  double gyroXrate = gyroX / 131.0; // Convert to deg/s
  double gyroYrate = gyroY / 131.0; // Convert to deg/s

#ifdef RESTRICT_PITCH
  // This fixes the transition problem when the accelerometer angle jumps between -180 and 180 degrees
  if ((roll < -90 && kalAngleX > 90) || (roll > 90 && kalAngleX < -90)) {
    kalmanX.setAngle(roll);
    compAngleX = roll;
    kalAngleX = roll;
    gyroXangle = roll;
  } else
    kalAngleX = kalmanX.getAngle(roll, gyroXrate, dt); // Calculate the angle using a Kalman filter

  if (abs(kalAngleX) > 90)
    gyroYrate = -gyroYrate; // Invert rate, so it fits the restriced accelerometer reading
  kalAngleY = kalmanY.getAngle(pitch, gyroYrate, dt);
#else
  // This fixes the transition problem when the accelerometer angle jumps between -180 and 180 degrees
  if ((pitch < -90 && kalAngleY > 90) || (pitch > 90 && kalAngleY < -90)) {
    kalmanY.setAngle(pitch);
    compAngleY = pitch;
    kalAngleY = pitch;
    gyroYangle = pitch;
  } else
    kalAngleY = kalmanY.getAngle(pitch, gyroYrate, dt); // Calculate the angle using a Kalman filter

  if (abs(kalAngleY) > 90)
    gyroXrate = -gyroXrate; // Invert rate, so it fits the restriced accelerometer reading
  kalAngleX = kalmanX.getAngle(roll, gyroXrate, dt); // Calculate the angle using a Kalman filter
#endif

  gyroXangle += gyroXrate * dt; // Calculate gyro angle without any filter
  gyroYangle += gyroYrate * dt;
  //gyroXangle += kalmanX.getRate() * dt; // Calculate gyro angle using the unbiased rate
  //gyroYangle += kalmanY.getRate() * dt;

  compAngleX = 0.93 * (compAngleX + gyroXrate * dt) + 0.07 * roll; // Calculate the angle using a Complimentary filter
  compAngleY = 0.93 * (compAngleY + gyroYrate * dt) + 0.07 * pitch;

  // Reset the gyro angle when it has drifted too much
  if (gyroXangle < -180 || gyroXangle > 180)
    gyroXangle = kalAngleX;
  if (gyroYangle < -180 || gyroYangle > 180)
    gyroYangle = kalAngleY;

  /* Print Data */
  Serial.print(kalAngleX); Serial.print(" Roll\t");
  Serial.print(kalAngleY); Serial.print(" Pitch\t");
  Serial.print("\r\n");
  delay(2);

  error_roll = kalAngleX - desired_angle;
  error_pitch = kalAngleY - desired_angle;

  pid_p[0] = kp[0]*error_roll;
  pid_p[1] = kp[1]*error_pitch;

  if(-3 <error_roll <3)
 {
  pid_i[0] = pid_i[0]+(ki[0]*error_roll);  
 }

 if(-3 <error_pitch <3)
 {
  pid_i[1] = pid_i[1]+(ki[1]*error_pitch);  
 }

 pid_d[0] = kd[0]*((error_roll - previous_error_roll)/dt);
 pid_d[1] = kd[1]*((error_pitch - previous_error_pitch)/dt);

 PID[0] = pid_p[0] + pid_i[0] + pid_d[0];
 PID[1] = pid_p[1] + pid_i[1] + pid_d[1];

 pwmLeft = throttle + PID[0];
 pwmRight = throttle - PID[0];
 pwmFront = throttle + PID[1];
 pwmBack = throttle - PID[1];


 if(pwmRight < lowerlimit)
{
  pwmRight = lowerlimit;
}
if(pwmRight > upperlimit)
{
  pwmRight = upperlimit;
}
//Left
if(pwmLeft < lowerlimit)
{
  pwmLeft = lowerlimit;
}
if(pwmLeft > upperlimit)
{
  pwmLeft = upperlimit;
}

 if(pwmFront < lowerlimit)
{
  pwmFront = lowerlimit;
}
if(pwmFront > upperlimit)
{
  pwmFront = upperlimit;
}

if(pwmBack < lowerlimit)
{
  pwmBack = lowerlimit;
}
if(pwmBack > upperlimit)
{
  pwmLeft = upperlimit;
}

  Serial.print(pwmLeft); Serial.print("\t");
  Serial.print(pwmRight); Serial.print("\t");
  Serial.print(pwmFront); Serial.print("\t");
  Serial.print(pwmBack); Serial.print("\t");

  motor.writeMicroseconds(pwmLeft);
  motor2.writeMicroseconds(pwmRight);
  motor3.writeMicroseconds(pwmFront);
  motor4.writeMicroseconds(pwmBack);
  previous_error_roll = error_roll;
  previous_error_pitch = error_pitch;
  delay(100);
}
