#include <Dps3xx.h>
/**
 * @details This example shows how to read temperature and pressure in a loop with a
 *          high oversampling rate.
 *          The oversampling rate can be set between 0 and 7 the higher the value the
 *          more precise the value is.
 */


// Dps3xx Object
Dps3xx Dps3xxPressureSensor = Dps3xx();
float pressureBuffer;
void setup()
{
  Serial.begin(9600);
  while (!Serial)
    ;

  /*
   * Call begin to initialize Dps3xxPressureSensor
   * The parameter 0x76 is the bus address. The default address is 0x77 and does not need to be given.
   * Dps3xxPressureSensor.begin(Wire, 0x76);
   * Use the line below instead of the one above to use the default I2C address.
   * if you are using the Pressure 3 click Board, you need 0x76
   */
  Dps3xxPressureSensor.begin(Wire);

  Serial.println("Init complete!");

  //Find the neutral pressure level so we could figure out what is going on 
  Dps3xxPressureSensor.measurePressureOnce(pressureBuffer, 7);

}

void loop(){
  
  float pressure;
  Serial.println();
  int16_t ret;
  ret = Dps3xxPressureSensor.measurePressureOnce(pressure, 7);
  if (ret != 0)
  {
    // Something went wrong.
    // Look at the library code for more information about return codes
    Serial.print("FAIL! ret = ");
    Serial.println(ret);
  }
  else
  {
    if(pressure-pressureBuffer>0.5){
      Serial.println(" Down");
      Serial.print(pressure - pressureBuffer);
      Serial.println(" Pascal");
      pressureBuffer=pressure;
    }
    else if(pressure-pressureBuffer<-0.5){
      Serial.println("Up");
      Serial.print(pressure - pressureBuffer);
      Serial.println(" Pascal");
      pressureBuffer=pressure;
    }
    else{
      Serial.println("Nothing");
      }
  }

}
