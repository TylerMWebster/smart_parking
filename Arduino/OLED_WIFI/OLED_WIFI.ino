#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "WiFi.h"

//*Setup WiFi*//
const char * ssid = "******";
const char * password = "******";
// Set Static Local IP
IPAddress local_IP(192, 168, 50, 123);
// Set your Gateway IP address
IPAddress gateway(192, 168, 50, 123);
IPAddress subnet(255, 255, 0, 0);
int port = 8888;  //Port number
WiFiServer server(port);

//Setup display
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
#define SCREEN_ADDRESS 0x3C
#define OLED_RESET     4 // Reset pin # 
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

//Setup ultrasonic
const int trigPin = 36;
const int echoPin = 39;
long duration;
int distance;
const int park_thresh = 15;
String dist;
bool occupied = false;
bool prev_occupied = false;
bool stat_change = false;

void getInput(WiFiClient client) {
  //Message Example /123/456/789/321
  String msg = "";
  while (client.available() > 0) {
    msg = String(client.readStringUntil('\n'));
    display_text(msg, true);
  }
  client.flush();
}

void display_wifi_info(bool clr) {
  if (clr) {
    display.clearDisplay();
  }
  display.setCursor(0, 0);
  display.print(F("WiFi: "));
  display.println(ssid);
  display.print(F("IP: "));
  display.println(WiFi.localIP());
  display.print(F("Port: "));
  display.println(port);
  display.display();
}

void display_wifi_connection() {
  display.clearDisplay();
  display.print(F("Connecting to WiFi"));
  display.display();
  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("STA Failed to configure");
  }
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password); //Connect to wifi
  delay(100);
  while (WiFi.status() != WL_CONNECTED) {
    display.print(F("."));
    display.display();
    delay(1000);
  }
  server.begin();
  display_wifi_info(true);
}

void display_text(String text, bool clr) {
  if (clr) {
    display.clearDisplay();
    display.setCursor(0, 0);
  }
  display.setTextSize(1); // Draw 2X-scale text
  display.setTextColor(SSD1306_WHITE);
  display.println(text);
  display.display();      // Show initial text
}

void setup() {
  Serial.begin(115200);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  display.setTextSize(1); // Draw 2X-scale text
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  while (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
  }
  display_wifi_connection();
  delay(1000);
  display.setTextSize(2);
}

void loop() {
  //display_text("looping", true);
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2;

  if (WiFi.status() == WL_CONNECTED) {
    prev_occupied = occupied;
    display.clearDisplay();
    //display_wifi_info(true);
    //display.print("Ready for client");
    //display.print("Distance:");
    //display.println(distance);
    if (distance < park_thresh) {
      occupied = true;
    } else {
      occupied = false;
    }
    if (occupied < 2000 && prev_occupied < 2000) {
      dist = "Distance: " + String(distance);
      display_text(dist, true);
      if (occupied != prev_occupied) {
        stat_change = true;
        display_text("Status change", false);
        delay(1000);
      } else {
        stat_change = false;
      }
    }
    display.display();
    WiFiClient client = server.available();

    if (client) {
      if (client.connected())
      {
        String msg = "Client connected";
        display_text(msg, true);
      }

      while (client.connected()) {
        getInput(client);
      }
      client.stop();
      display_text("Client disconnected", true);
    }
  }
  delay(10);
}
