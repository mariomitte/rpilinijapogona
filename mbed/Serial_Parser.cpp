/* C-based low-memory footprint JSON parser for mbed
 * Based on Serge Zaitsev's JSMN https://bitbucket.org/zserge/jsmn/wiki/Home
 * JSMN is distributed under MIT license.
 *
 * Copyright (c) 2010 Serge A. Zaitsev
 * Copyright (c) 2014 YoongHM
 *
 * Uredio mariomitte za zahtjeve projekta: linija pogona
 */

#include "mbed.h"
#include "jsmn.h"
#include <string>
#include <cctype>

#define       MAXTOKEN       64

//================================= TIP TOKENA
const char *jsmn_type_str[] = {
  "PRIMITIVE",
  "OBJECT",
  "ARRAY",
  "STRING"
};

/*
typedef struct {
    int kreirao;
    char   kod;
    char  model;
    char extra;
}SER_DATA;*/

//================================= LPC1768 JSON STATUS
Serial pc(USBTX, USBRX);
//Motor sg90(p23, p6, p5); // pwm, fwd, rev
Serial esp(p28, p27); // tx, rx
DigitalOut reset(p26);
DigitalOut led1(LED1);
DigitalOut led4(LED4);
Timer t;

//================================= UPRAVLJANJE AKTUATORIMA
DigitalOut _a1(LED2);
DigitalOut _a2(LED3);
DigitalOut _en(p23);

int  count,ended,timeout;
char buf[1024];
char korisnik[25];
char kod[25];
char model[25];
char extra[25];
int pos;

void getreply();
void ser_korisnik(char* inBuf, int start, int end);
void ser_kod(char* inBuf, int start, int end);
void ser_model(char* inBuf, int start, int end);
void ser_extra(char* inBuf, int start, int end);

int main() {

    pc.printf("\n ESP 01 - jsmn \r\n");

    // jsmn var
    const char *js;            // Pointer to json string
    int         r;             // Number of token parsed
    jsmn_parser p;             // jsmn parser
    jsmntok_t   t[MAXTOKEN];   // Parsed token

    //================================= KREIRAJ TOKENE NA PC
    reset = 0;
    pc.baud(115200);
    wait(1);
    reset = 1;
    timeout = 2;
    getreply();

    while(1) {
        pc.printf("\r\n");
        pc.printf("\n Počinjem preuzimati - wifi \r\n");
        esp.baud(115200);
        getreply();
        timeout=7;

        //============================== KREIRAJ TABLICU TOKENA
        jsmn_init(&p);
        r = jsmn_parse(&p, buf, strlen(buf), t, MAXTOKEN);
        pc.printf("Parsed %d tokens\n", r);
        pc.printf("            TYPE       START   END  SIZE PAR\n");
        pc.printf("           ----------  -----  ----  ---- ---\n");
        char        ch;
        jsmntok_t   at;            // A token for general use

        for (int i = 0; i < r; i++){
            at = t[i];
            pc.printf("Token %2d = %-10.10s (%4d - %4d, %3d, %2d) ",
                   i, jsmn_type_str[at.type],
                   at.start, at.end,
                   at.size, at.parent);

            switch (i){
                  // Pohrani token: korisnik
                  case 3:
                    ser_korisnik(buf, at.start, at.end);
                    pc.printf("\n");
                    break;

                  // Pohrani token: kod
                  case 5:
                    ser_kod(buf, at.start, at.end);
                    pc.printf("\n");
                    break;

                  // Pohrani token: model
                  case 7:
                    ser_model(buf, at.start, at.end);
                    pc.printf("\n");
                    break;

                  // Pohrani token: extra
                  case 9:
                    ser_extra(buf, at.start, at.end);
                    pc.printf("\n");
                    break;

                  default:
                    pc.printf("\n");
                    break;
            }
        }

        //==================================== POPUNI TABLICU SA REZULTATIMA
        pc.printf("\n");
        pc.printf("Korisnik: %s\n", korisnik);
        pc.printf("Kod: %s\n", kod);
        pc.printf("Model: %s\n", model);
        pc.printf("Extra: %s\n", extra);
        pc.printf("\n");
        pc.printf("ESP Json - Django linija pogona\n");
        pc.printf(buf);
        pc.printf("\n");
        //wait(2);

        //==================================== UPRAVLJAJ AKTUATORIMA
        // Usporedi sa tokenom: extra
        if(strcmp(extra, "lijevo") == 0){
            pc.printf("Lijevo");
            _en = 1;
            _a1 = 0;
            _a2 = 1;
            led4 = !led4;
            memset(&extra[0], 0, 25);
        }
        // Usporedi sa tokenom: extra
        if(strcmp(extra, "desno") == 0){
            pc.printf("Desno");
            _en = 1;
            _a1 = 1;
            _a2 = 0;
            led4 = !led4;
            memset(&extra[0], 0, 25);
        }
        // Usporedi sa tokenom: extra
        if(strcmp(extra, "brze") == 0){
            pc.printf("Brze");
            _a1 = !_a1;
            memset(&extra[0], 0, 25);
        }
        // Usporedi sa tokenom: extra
        if(strcmp(extra, "sporije") == 0){
            pc.printf("Sporije\n");
            _a2 = !_a2;
            memset(&extra[0], 0, 25);
        }
        // Usporedi sa tokenom: extra
        if(strcmp(extra, "stop") == 0){
            pc.printf("Stop");
            _en = 0;
            _a1 = 0;
            _a2 = 0;
            memset(&extra[0], 0, 25);
        }
        // Usporedi sa tokenom: extra
        if(strcmp(extra, "pauziraj") == 0){
            pc.printf("Pauziraj");
            _en = 0;
            _a1 = 0;
            _a2 = 0;
            memset(&extra[0], 0, 25);
        }
    }
}

//==================================== METODE
// Preuzmi JSON
void getreply() {
    memset(buf, '\0', sizeof(buf));
    t.start();
    ended=0;
    count=0;

    while(!ended) {
        if(esp.readable()) {
            led1 = !led1;
            buf[count] = esp.getc();
            count++;
        }
        if(t.read() > timeout) {
            ended = 1;
            t.stop();
            t.reset();
        }
    }
}

// Pohrani JSON za token: korisnik
void ser_korisnik(char* inBuf, int start, int end){
  char* data = inBuf;
  int j = 0;
  for (int i = start; i < end; i++){
    korisnik[j] = data[i];
    j++;
  }
}

// Pohrani JSON za token: kod
void ser_kod(char* inBuf, int start, int end){
  char* data = inBuf;
  int j = 0;
  for (int i = start; i < end; i++){
    kod[j] = data[i];
    j++;
  }
}

// Pohrani JSON za token: model
void ser_model(char* inBuf, int start, int end){
  char* data = inBuf;
  int j = 0;
  for (int i = start; i < end; i++){
    model[j] = data[i];
    j++;
  }
}

// Pohrani JSON za token: extra
void ser_extra(char* inBuf, int start, int end){
  char* data = inBuf;
  int j = 0;
  for (int i = start; i < end; i++){
    extra[j] = data[i];
    j++;
  }
}
