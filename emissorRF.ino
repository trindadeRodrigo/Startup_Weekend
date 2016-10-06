

#include <RH_ASK.h>
#include <SPI.h> // Not actually used but needed to compile

RH_ASK driver;

void setup()
{
    Serial.begin(9600);   // Debugging only
    if (!driver.init())
         Serial.println("init failed");
}

int a=1023;

void loop()
{
    a++;
    if(a>1000){
      a = 0;
    }

    char b[5];

    String str;

    str=String(a);

    str.toCharArray(b,5); 
    Serial.println(b);

    //const char *msg = b;
    driver.send((uint8_t *)b, strlen(b));
    driver.waitPacketSent();
    delay(100);
}


