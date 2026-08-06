#include <DHT.h>

#define DHTPIN 2  // Pin used
#define DHTTYPE DHT22  // DHT type 11 or 22
DHT dht(DHTPIN, DHTTYPE);

// Variables
float hum, temp; // hum stores RH, temp stores Temperature

void setup() {
  // Set baud rate 
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  // Read data and store it to variables
  hum = dht.readHumidity();
  temp = dht.readTemperature();


  // Print data to serial port
  Serial.println(String(hum) + ", " + String(temp));
  
  // Pause for 15 seconds
  delay(15000);
}
