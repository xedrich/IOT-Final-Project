#include "ESP8266WiFi.h"

const char* ssid = "XXXX";
const char* password = "avfnn63155";
const int ANALOG_PIN = A0; // Analog pin for photoresistor

void setup(void) {
  Serial.begin(115200);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connection Successful");
  Serial.print("The IP Address of ESP8266 Module is: ");
  Serial.println(WiFi.localIP());// Print the IP address
}

void loop() {
  // Read light intensity from photoresistor
  int lightIntensity = analogRead(ANALOG_PIN);
  Serial.print("Light Intensity: ");
  Serial.println(lightIntensity);

  // Add your logic here to take action based on the light intensity value

  delay(2000); // Adjust the delay based on your project requirements
}
