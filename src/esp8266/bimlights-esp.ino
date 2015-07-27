/*
 *  This sketch trys to Connect to the best AP based on a given list
 *
 */

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <APA102.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>

const uint8_t dataPin = 15;
const uint16_t ledCount = 50;
const uint8_t brightness = 1;

// pins
const int button = 0;

ESP8266WiFiMulti wifiMulti;
rgb_color colors[ledCount];

void setup() {
    Serial.begin(115200);
    delay(10);
    
    wifiMulti.addAP("/dev/lol", "4dprinter");

    
    if(wifiMulti.run() == WL_CONNECTED) {
      Serial.print("Wifi connected");
    }
}

void loop() {
  // heartbeat
  mil = millis();
  if(mil - isAlive >= 30000) {  
    client.publish(nodeName + "heartbeat", (String)mil);
    isAlive = mil;  
  }
  
  // wifi
  // setLED(0, (rgb_color){0, 255, 0});
  if(WiFi.status() != WL_CONNECTED) {
    // setLED(0, (rgb_color){255, 255, 0});
    if(wifiMulti.run() == WL_CONNECTED) {
      // setLED(0, (rgb_color){0, 255, 0});
    } else {
      // setLED(0, (rgb_color){255, 0, 0});
    }
    delay(1000);
  }
    

    // mqtt
    if (client.connected()) {
      // setLED(1, (rgb_color){0, 255, 0});
      client.loop();
    } else {
      // setLED(1, (rgb_color){255, 0, 0});
      if (client.connect("node")) {
        // setLED(1, (rgb_color){255, 255, 0});
	client.set_callback(mqtt_callback);
	client.subscribe("devlol/#");
      }
    }
    
    // button
    if (digitalRead(button) == LOW) {
      client.publish(nodeName + "button","");
    }
}

void setLED(int i, rgb_color c) {
  colors[i] = c;
  ledStrip.write(colors, ledCount, brightness);
}
