#include <Dps310.h>
// Dps310 Opject

bool messageReceivedFlag=false;
Dps310 Dps310PressureSensor = Dps310();
bool calibration=false;
void setup()
{
  pinMode(14,OUTPUT);
  Serial.begin(9600);
  while (!Serial);

  Dps310PressureSensor.begin(Wire);

  Serial.println("Init complete!");
  digitalWrite(4,LOW);
}



void loop()
{
  if (Serial.available()) {
    String data = Serial.readString(); // Read the string from the HC05
    Serial.println("Received: " + data);

    // Convert the string to an integer, increment, and then send it back
    int receivedPressure = data.toInt();
    if(receivedPressure>1000){
      messageReceivedFlag=true;
    }
    


    
    
  }

  /*// Now we have 2 floats 
  float temperature;
  float pressureReading;
  uint8_t oversampling = 7;
  int16_t ret;
  Serial.println();

  ret = Dps310PressureSensor.measurePressureOnce(pressureReading, oversampling);
  if messageReceivedFlag

  //Wait some time
  */
  
  if (messageReceivedFlag){
    digitalWrite(14,HIGH);
    delay(1000);
    messageReceivedFlag=false;
  }
  delay(20);
}
