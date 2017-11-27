/*
  Primjer http povezivanja ESP07 WiFi sa linijom pogona
  Dohvaća podatke sa API adrese linije pogona,
  kreirane pomoću Django REST okruženja.

  Aplikacija radi u jednom smjeru
  Šalje GET zahtjev

  Kreirao mariomitte korištenjem osnovnih primjera ESP8266 biblioteke
  Za zahtjeve projekta: linija pogona
*/

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "xxxx";
const char* password = "xxxx";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }
}

void loop() {
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    // API adresa linije pogona: ostaje isti za pogon2, pogon3
    http.begin("http://<ip_adresa>:<port>/api/cvor/");
    http.setAuthorization("linijapogona", "linijapogona");
    int httpCode = http.GET();
    // Pošalji preuzete podatke mikrokontroleru: LPC1768
    if(httpCode > 0) {
      String payload = http.getString();
      Serial.println(payload);
    }
    // Završi prijenos
    http.end();
  }
  // Svakih x vremena zatraži GET zahtjev
  delay(7500);
}
