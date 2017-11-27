/*
  Kreirao FILIPEFLOP

  Uredio mariomitte za zahtjeve projekta: linija pogona
*/

#include <SPI.h>
#include <MFRC522.h>
#include <LiquidCrystal.h>
#include <Wire.h>

#define SLAVE_ADDRESS 0x04

#define SS_PIN 10
#define RST_PIN 9

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.
LiquidCrystal lcd(6, 7, 2, 3, 4, 5);   // LCD 16x2

int LED = 8;
//int tag_id[4];

/**
 * RPi3 upravlja Arduinom, sa I2C
 * Upravljanje aktuatorima u pogon1
 */
void receiveEvent(int howMany) {
  int x = Wire.read();    // receive byte as an integer
  Serial.print(x);
  switch(x){
    case 1:
      digitalWrite(LED, HIGH);
      break;
    case 2:
      digitalWrite(LED, LOW);
      break;
    case 3:
      digitalWrite(LED, HIGH);
      break;
    case 4:
      digitalWrite(LED, LOW);
      break;
    case 8:
      digitalWrite(LED, LOW);
      break;
    case 9:
      digitalWrite(LED, LOW);
      break;
  }
}

/**
 * LCD Status u mirovanju
 */
void cekam(String data1, String data2) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(data1);
  lcd.setCursor(0, 1);
  lcd.print(data2);
}

/**
 * Pošalji UID kartice liniji pogona
 */
// void sendData(){
//   for (byte i = 0; i < 5; i++)
//   {
//     Wire.write(tag_id[i]);
//   }
// }

void setup()
{
  pinMode(LED, OUTPUT);
    Serial.begin(9600);                   // Uspostavi vezu
    while (!Serial);                      // Ako nema veze, miruj
    SPI.begin();                          // MISO-MOSI
    lcd.begin(16, 2);                     // LCD 16x2
    mfrc522.PCD_Init();                   // MFRC522, čitač kartica
    Wire.begin(SLAVE_ADDRESS);            // Adresa radnika
    Wire.onReceive(receiveEvent);         // Primaj naredbe linije
    //Wire.onRequest(sendData);           // Pošalji UID liniji

    Serial.println();
    Serial.println("Postavljanje...");
    cekam("  Linija pogona  ", "Cekam korisnika ");

}

void loop()
{
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent())
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial())
  {
    return;
  }
  //Show UID on serial monitor
  Serial.print("UID tag :");
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++)
  {
     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();
  // Usporedi podatke sa kartice
  Serial.print("Message : ");
  content.toUpperCase();
  if(content.substring(1) == "D7 E7 A2 21") {
    cekam(" Dobrodosao ", " Administrator 1");
    delay(3000);
    cekam("  Linija pogona  ", "Cekam korisnika ");
  } else if(content.substring(1) == "07 8C AD 21") {
    Serial.println("Admin");
    cekam(" Dobrodosao ", " Administrator 2");
    Serial.println();
    delay(3000);
    cekam("  Linija pogona  ", "Cekam korisnika ");
  } else if(content.substring(1) == "F3 63 8A D9") {
      Serial.println("Admin");
      cekam(" Dobrodosao ", " Administrator 3");
      Serial.println();
      delay(3000);
      cekam("  Linija pogona  ", "Cekam korisnika ");
  }

  Serial.println(" Locked");
  delay(3000);

}
