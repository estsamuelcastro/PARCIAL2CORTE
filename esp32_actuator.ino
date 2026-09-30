#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>

const char* SSID = "deco tp";
const char* PASS = "Calivasa259191";

WebServer server(80);
Servo gates[5];
const int gatePins[5] = {13, 14, 25, 26, 27};
const int conveyorPin = 33;
const int presencePin = 32;
const int DENOMS[5] = {50, 100, 200, 500, 1000};

String stateName = "IDLE";
unsigned long processed = 0;

int denominationIndex(int value) {
  for (int i = 0; i < 5; i++) {
    if (value == DENOMS[i]) return i;
  }
  return -1;
}

void sendStatus() {
  String out = "{\"state\":\"" + stateName + "\",\"processed\":" + String(processed) +
               ",\"sensor\":" + String(digitalRead(presencePin)) + ",\"currency\":\"COP\"}";
  server.send(200, "application/json", out);
}

void sortCoin() {
  if (!server.hasArg("value")) {
    server.send(400, "application/json", "{\"error\":\"missing value\"}");
    return;
  }
  int value = server.arg("value").toInt();
  int idx = denominationIndex(value);
  if (idx < 0) {
    server.send(400, "application/json", "{\"error\":\"unsupported COP denomination\"}");
    return;
  }

  stateName = "SORTING";
  digitalWrite(conveyorPin, HIGH);
  for (int i = 0; i < 5; i++) gates[i].write(i == idx ? 70 : 10);
  delay(300);
  gates[idx].write(10);
  processed++;
  stateName = "RUNNING";
  server.send(200, "application/json", "{\"ok\":true,\"currency\":\"COP\"}");
}

void setup() {
  Serial.begin(115200);
  pinMode(conveyorPin, OUTPUT);
  pinMode(presencePin, INPUT_PULLUP);
  digitalWrite(conveyorPin, LOW);

  for (int i = 0; i < 5; i++) {
    gates[i].setPeriodHertz(50);
    gates[i].attach(gatePins[i], 500, 2400);
    gates[i].write(10);
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) delay(250);

  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
  server.on("/status", HTTP_GET, sendStatus);
  server.on("/sort", HTTP_GET, sortCoin);
  server.begin();
}

void loop() {
  server.handleClient();
  if (digitalRead(presencePin) == LOW) stateName = "DETECT";
}
