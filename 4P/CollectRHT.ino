#include <DHT.h>

#define DHTPIN 2  // Pin used
#define DHTTYPE DHT22  // DHT type 11 or 22
DHT dht(DHTPIN, DHTTYPE);

// Variables
float hum, temp; // hum stores RH, temp stores Temperature

// 30-minute collection duration
const unsigned long collectionDuration = 30UL * 60UL * 1000UL;
unsigned long startTime;

void setup() {
  // Set baud rate 
  Serial.begin(9600);
  dht.begin();
  startTime = millis();
}

void loop() {
  // Stop collecting after 30 minutes
  if (millis() - startTime >= collectionDuration) {
    Serial.println("COLLECTION COMPLETE");
    while (true) {
      // Stop the program
    }
  }
  
  // Read data and store it to variables
  hum = dht.readHumidity();
  temp = dht.readTemperature();

  // Print data to serial port
  Serial.println(String(hum) + ", " + String(temp));
  
  // Pause for 30 seconds
  delay(30000);
}


