#include <Dps3xx.h>
// Dps3xx Object
Dps3xx Dps3xxPressureSensor = Dps3xx();
float pressureBuffer;
void setup()
{
  Serial.begin(9600);
  while (!Serial)
    ;
  Dps3xxPressureSensor.begin(Wire);

  Serial.println("Init complete!");

  //Find the neutral pressure level so we could figure out what is going on 
  Dps3xxPressureSensor.measurePressureOnce(pressureBuffer, 7);

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
  ret = Dps3xxPressureSensor.measurePressureOnce(pressure, 7);

    if(pressure-pressureBuffer>0.8){
      Serial.println(" Down");
      pressureBuffer=pressure;
    }
    else if(pressure-pressureBuffer<-0.8){
      Serial.println("Up");
      pressureBuffer=pressure;
    }
    else{
      Serial.println("Nothing");
      }
  

  
  

}
