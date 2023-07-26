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

  // For Communication with Master 
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  delay(200);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
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

    if(pressure-pressureBuffer>0.3  ){
      Serial.println(" Down");
      pressureBuffer=pressure;
        digitalWrite(4, LOW);
        digitalWrite(5, HIGH);
    }
    else if(pressure-pressureBuffer<-0.3){
      Serial.println("Up");
      pressureBuffer=pressure;
      digitalWrite(4, HIGH);
      digitalWrite(5, LOW);
    }
    else{
      Serial.println("Nothing");
        digitalWrite(4, LOW);
        digitalWrite(5, LOW);
      }
  

  
  //delay(100);

}
