// Import required libraries
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <Arduino.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>

const char* ssid = "Pulse";
const char* password = "easypassword1234";

String serverName = "http://192.168.0.106:5000/data";

AsyncWebServer server(80);

int LED = 2;

#define DHTPIN 5     // Digital pin connected to the DHT sensor

// Uncomment the type of sensor in use:
#define DHTTYPE    DHT11     // DHT 11

DHT dht(DHTPIN, DHTTYPE);

// current temperature & humidity, updated in loop()
float t = 0.0;

unsigned long previousMillis = 0;    // will store last time DHT was updated

// Updates DHT readings every 10 seconds
const long interval = 15000;

void turnLEDOn() {
  digitalWrite(LED, LOW);
}

void turnLEDOff() {
  digitalWrite(LED, HIGH);
}

String getStatus() {
  if (digitalRead(LED) == HIGH) {
    return "{\"state\":\"off\"}";
  } else {
    return "{\"state\":\"on\"}";
  }
}

void setup(){
  Serial.begin(115200);
  dht.begin();
  
  pinMode(LED, OUTPUT);
  
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  
  Serial.println();
  
  // Print ESP8266 Local IP Address
  Serial.println(WiFi.localIP());
  
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", getStatus().c_str());
  });
  server.on("/off", HTTP_GET, [](AsyncWebServerRequest *request){
    turnLEDOff();
    request->send(200);
  });
  server.on("/on", HTTP_GET, [](AsyncWebServerRequest *request){
    turnLEDOn();
    request->send(200);
  });
  
  server.begin();
}

void loop(){      
  unsigned long currentMillis = millis();
  
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    
    float newT = dht.readTemperature();
    
    if (isnan(newT)) {
      Serial.println("Failed to read from DHT sensor!");
    }
    else {
      t = newT;
      Serial.println(t);
      
      if(WiFi.status()== WL_CONNECTED){
        WiFiClient client;
        HTTPClient http;
        
        // Your Domain name with URL path or IP address with path
        http.begin(client, serverName.c_str());
        http.addHeader("Content-Type", "application/json");            
        
        String JSON_str = "{\"temperature\": \"" + String(t) + "\"}";
        
        int httpResponseCode = http.PUT(JSON_str);
        if(httpResponseCode>0){
          String response = http.getString();   
          
          Serial.println(httpResponseCode);
          Serial.println(response);          
        } else {
          Serial.print("Error on sending PUT Request: ");
          Serial.println(httpResponseCode);
        }
        // Free resources
        http.end();
      }
      else {
        Serial.println("WiFi Disconnected");
      }
    }
  }
}
