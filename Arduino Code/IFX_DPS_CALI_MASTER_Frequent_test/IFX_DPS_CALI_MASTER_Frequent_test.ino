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
  float pressureValues[10];
  float sum = 0.0;
  
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
 
  for (int i = 0; i < 10; i++) {
    Dps3xxPressureSensor.measurePressureOnce(pressureValues[i], 7);
    sum += pressureValues[i];
  }

  float average = sum / 10.0;  // calculate the average pressure

    if((average-pressureBuffer>0.5) && down){
      Serial.println(" Down");
      pressureBuffer=average;
        
 
    }
    else if((average-pressureBuffer<-0.5) && up){
      Serial.println("Up");
      pressureBuffer=average;

    }
    else{
      Serial.println("Nothing");

      }
  
  Serial.println();
  Serial.println();
  

}
