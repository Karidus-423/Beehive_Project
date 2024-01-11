#include <Wire.h>
#include <SD.h>
#include <DS3231.h>

const int chipSelect = 8;
DS3231 rtc(SDA, SCL);

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.print("Initializing SD card..");

  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    while (1);
  }

  rtc.begin();

  //rtc.setTime(6, 28 , 00);
  //D-M-Y
  //rtc.setDate(23, 12, 2023);

  Serial.println("card initialized.");
  // Begin I2C communication protocol
  Wire.begin();
}

void loop() {
  char buffer[64];
  String dataString = "";

  for (int i = 1; i < 6; i++) {
    Wire.requestFrom(i, sizeof(buffer));
    int slaveID = i;
    int sensorID = 1;
    File dataFile = SD.open("datalog.txt", FILE_WRITE);

    while (Wire.available()) {
      char c = Wire.read();

      if (c == ' ' || c == '\n') {
        String entry = "@" + String(slaveID) + ", S_" + String(sensorID) + ", " + dataString + ", " 
        + String(rtc.getDateStr()) + " " + String(rtc.getTimeStr()) +"\n";
        Serial.print(entry);
        dataString += entry;
        dataFile.print(entry.c_str());
        
        Serial.print(dataString); 
        sensorID++;
        dataString = "";  // Reset dataString for the next set of readings
      } else {
        dataString += c;
      }
    }
    dataFile.close();
  }

  Serial.println(rtc.getDateStr());
  Serial.println(rtc.getTimeStr());

  delay(5000);
}
