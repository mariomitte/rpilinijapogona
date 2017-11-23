#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "xxxx";
const char* password = "xxxx";

void setup() {
  //pinMode(poz, INPUT);
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }
}

void loop() {
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    //Specify request destination
    http.begin("https://ip_adresa/api/cvor/");
    http.setAuthorization("linijapogona", "linijapogona");
    int httpCode = http.GET();
    //Send the request
    if(httpCode > 0) {
      String payload = http.getString();
      Serial.println(payload);
    }
    http.end();
  }
  //Send a request every x seconds
  delay(1800);

}
