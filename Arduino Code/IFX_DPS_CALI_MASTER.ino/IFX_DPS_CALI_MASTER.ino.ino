#include <Dps3xx.h>
// Dps3xx Object
Dps3xx Dps3xxPressureSensor = Dps3xx();
float pressureBuffer;
  bool up= false;
  bool down= false;

void setup()
{
  pinMode(6,OUTPUT);
  Serial.begin(9600);
  while (!Serial)
    ;
  Dps3xxPressureSensor.begin(Wire);

  Serial.println("Init complete!");

  //Find the neutral pressure level so we could figure out what is going on 
  Dps3xxPressureSensor.measurePressureOnce(pressureBuffer, 7);

  // For Communication with Master 
  pinMode(4, INPUT);
  pinMode(5, INPUT);
  delay(200);

}

void loop(){
  
  int16_t ret;
  float pressure;
  /*
  Serial.println();
  Serial.println("Pressure1: ");
  ret = Dps3xxPressureSensor.measurePressureOnce(pressure, 7);
  Serial.print(pressure);
  Serial.println();
  Serial.println("Pressure2: ");
  ret = Dps3xxPressureSensor2.measurePressureOnce(pressure, 7);
  Serial.print(pressure);
  */
  int pin4Input = digitalRead(4);
  int pin5Input = digitalRead(5);

  /*Serial.println("pin 4 reading");
  Serial.println(pin4Input);
  Serial.println("pin 5 reading");
  Serial.println(pin5Input);*/

 if(pin5Input && !pin4Input){
  //Serial.println("DOWN");
  down=true;
  up=false;
  }
 if(pin4Input && !pin5Input){
  //Serial.println("UP");
  up=true;
  down=false;
  } 

 if(!pin4Input && !pin5Input){
  //Serial.println("NOTHING");
  up=false;
  down=false;
  }
 
 
  ret = Dps3xxPressureSensor.measurePressureOnce(pressure, 7);

    if((pressure-pressureBuffer>0.4) && down){
      Serial.println(" Down");
      pressureBuffer=pressure;
        
 
    }
    else if((pressure-pressureBuffer<-0.4) && up){
      Serial.println("Up");
      pressureBuffer=pressure;

    }
    else{
      Serial.println("Nothing");

      }
  


}
