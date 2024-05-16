#include <Wire.h>

String logData;
uint8_t Sensors[4] = {A0,A1,A2,A3};

void setup() {
  Wire.begin(5);
  Wire.onRequest(send);
  Serial.begin(9600);
}

void loop() {
  send();
  delay(1000);
}

void send(){
  for (int i = 0; i < 4; i++) {
    uint32_t reading = analogRead(Sensors[i]);
    float voltage = reading * (4000 / 1024.0);
    float temp = voltage / 10;

    logData =String(temp) + "\n";
    Serial.print(logData);
    Wire.write(logData.c_str());
  }
  delay(2000);
}

