#include <Wire.h>

void setup() {
  Serial.begin(9600);
  Wire.begin(); // Initialize I2C communication as Master
}

void loop() {
  Wire.requestFrom(8, 6); // Request data from Slave with address 8 and expect 6 bytes

  while (Wire.available()) {
    char c = Wire.read(); // Read a byte
    Serial.print(c);
  }

  Serial.println();
  delay(1000);
}

