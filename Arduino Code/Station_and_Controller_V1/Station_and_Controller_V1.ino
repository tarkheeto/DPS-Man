#include <Dps310.h>
// Dps310 Opject
Dps310 Dps310PressureSensor = Dps310();

void setup()
{
  Serial.begin(9600);
  while (!Serial);
  Dps310PressureSensor.begin(Wire);

  Serial.println("Init complete!");
}


void loop()
{
  float temperature;
  float pressure;
  int pressureInt;
  uint8_t oversampling = 7;
  int16_t ret;

  ret = Dps310PressureSensor.measurePressureOnce(pressure, oversampling);
  
  //pressureInt= (int)pressure;

  Serial.println(pressure);


  //Wait some time
  delay(20);
}
