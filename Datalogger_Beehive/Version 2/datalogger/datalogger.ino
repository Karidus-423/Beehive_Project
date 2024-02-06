// Include the required Arduino libraries:
#include "OneWire.h"
#include "DallasTemperature.h"
#include "RTClib.h"
#include "SD.h"
#include "SPI.h"

RTC_PCF8523 rtc;
// Define to which pin of the Arduino the 1-Wire bus is connected:
#define ONE_WIRE_BUS 4
// Create a new instance of the oneWire class to communicate with any OneWire device:
OneWire oneWire(ONE_WIRE_BUS);
// Pass the oneWire reference to DallasTemperature library:
DallasTemperature sensors(&oneWire);

//SD card variables
const int chipSelect = 6;

int deviceCount = 0;
float tempC;
float tempF;

void setup() {
  // Begin serial communication at a baud rate of 9600:
  Serial.begin(9600);
  while(!Serial);
  // Start up the library:
  sensors.begin();

  // Locate the devices on the bus:
  Serial.println("Locating devices...");
  Serial.print("Found ");
  deviceCount = sensors.getDeviceCount();
  Serial.print(deviceCount);
  Serial.println(" devices");

  //SD card Initialization
  Serial.print("Initializing SD card..");
  if (!SD.begin(chipSelect)){
    Serial.println("Card failed, or not present");
    while(1);
  }
  //RTC Initialization
  Serial.println("Scanning for clock..");
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    Serial.flush();
    while(1) delay(10);
  }
  if (! rtc.initialized() || rtc.lostPower()) {
    Serial.println("RTC is NOT initialized, let's set the time!");
    rtc.adjust(DateTime(2024, 2, 5, 6, 40, 0));
  }
  rtc.start();

}

void loop() {
  // Send the command for all devices on the bus to perform a temperature conversion:
  sensors.requestTemperatures();
  String dataString = "";

  // Open the file for writing at the beginning of the loop
  File dataFile = SD.open("datalog.txt", FILE_WRITE);

  // Check if the file opened successfully
  if (dataFile) {
    // Display temperature from each sensor
    for (int i = 0; i < deviceCount; i++) {
      Serial.print("Sensor ");
      Serial.print(i + 1);
      Serial.print(" : ");
      tempC = sensors.getTempCByIndex(i);
      tempF = sensors.getTempFByIndex(i);
      Serial.print(tempC);
      Serial.print(" \xC2\xB0"); // shows degree symbol
      Serial.print("C  |  ");
      Serial.print(tempF);
      Serial.print(" \xC2\xB0"); // shows degree symbol
      Serial.println("F");

      // Construct the data entry string
      String entry = "S_" + String(i+1) + ", " + String(tempC) + " \xC2\xB0" + "C, " + getTimeString();

      // Append the entry to the data string
      dataString += entry;
    }

    // Write the complete data string to the file
    dataFile.println(dataString);

    // Close the file at the end of the loop
    dataFile.close();
  } else {
    Serial.println("error opening datalog.txt");
  }

  // Delay at the end of the loop
  delay(1000);
}


String getTimeString() {
  DateTime now = rtc.now();
  String dateString = String(now.month(), DEC) + "/" + String(now.day(), DEC) + "/" + String(now.year(), DEC);
  String timeString = String(now.hour(), DEC) + ":" + String(now.minute(), DEC) + ":" + String(now.second(), DEC);
  return dateString + " " + timeString + "\n";
}
