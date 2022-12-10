#include "mpu9250.h" //install zip file from bolder github page: https://github.com/bolderflight/invensense-imu

/* Mpu9250 object */
bfs::Mpu9250 imu;

void setup() {
  //make sure baud rate is same is baud rate setting in serial monitor
  Serial.begin(115200); // initialize serial port and set data rate (in bits per sec)
  while(!Serial) {
    // wait for serial port to connect
  }
  Wire.begin(); //initialize Wire library for I2C communication
  Wire.setClock(400000); // change clock frequency in Hz

  /* I2C bus,  0x68 address */
  imu.Config(&Wire, bfs::Mpu9250::I2C_ADDR_PRIM);
  /* Initialize and configure IMU */
  if (!imu.Begin()) {
    Serial.println("Error initializing communication with IMU");
    while(1) {}
  }
  /* Set the sample rate divider */
  if (!imu.ConfigSrd(19)) {
    Serial.println("Error configured SRD");
    while(1) {}
  }

}

// continuously print current state of mpu9250
void loop() {

  // imu.Read() reads data from MPU9250 and stores data in MPU9250 object. Returns true if data is successfully read, otherwise false
  if(imu.Read()) {

    //print to serial monitor
    //Serial.print(imu.new_imu_data()); // Returns true if new data was returned from the accelerometer and gyro.
    //Serial.print("\t");

    Serial.print("accel_x: ");
    Serial.print(100.0*imu.accel_x_mps2()); // x acceleration (m/s/s) from the Mpu9250 object
    Serial.print("\t");
    
    Serial.print("accel_y: ");
    Serial.print(100.0*imu.accel_y_mps2()); // y acceleration (m/s/s) from the Mpu9250 object
    Serial.print("\t");
    
    Serial.print("accel_z: ");
    Serial.print(100.0*imu.accel_z_mps2()); // z acceleration (m/s/s) from the Mpu9250 object
    Serial.print("\t");
    
    Serial.print("gyro_x: ");
    Serial.print(100.0*imu.gyro_x_radps()); //angular velocity around x axis (rad/s) from the Mpu9250 object
    Serial.print("\t");
    
    Serial.print("gyro_y: ");
    Serial.print(100.0*imu.gyro_y_radps()); //angular velocity around y axis (rad/s) from the Mpu9250 object
    Serial.print("\t");
    
    Serial.print("gyro_z: ");
    Serial.print(100.0*imu.gyro_z_radps()); //angular velocity around z axis (rad/s) from the Mpu9250 object
    Serial.print("\n"); // next line

    //send values to odrive
    
  }
}
