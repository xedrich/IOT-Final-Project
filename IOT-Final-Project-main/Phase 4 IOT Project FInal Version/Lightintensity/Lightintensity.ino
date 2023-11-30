#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "wifiname";
const char* password = "wifi pass";
const char* server_url = "http://192.168.0.113:5000";  // Replace with your Flask server IP and route
const int ANALOG_PIN = A0;

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
  Serial.println(WiFi.localIP()); // Print the IP address
}

void loop() {
  // Read light intensity from photoresistor
  int lightIntensity = analogRead(ANALOG_PIN);
  Serial.print("Raw Light Intensity: ");
  Serial.println(lightIntensity);

  // Send the data to the Flask server
  WiFiClient client;
  HTTPClient http;
  http.begin(client, server_url);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  String post_data = "light_intensity=" + String(lightIntensity);
  int http_code = http.POST(post_data);

  if (http_code > 0) {
    Serial.printf("[HTTP] POST request to %s was successful. Response code: %d\n", server_url, http_code);
  } else {
    Serial.printf("[HTTP] POST request to %s failed. Error: %s\n", server_url, http.errorToString(http_code).c_str());
  }

  http.end();

  delay(2000); // Adjust the delay based on your project requirements
}
