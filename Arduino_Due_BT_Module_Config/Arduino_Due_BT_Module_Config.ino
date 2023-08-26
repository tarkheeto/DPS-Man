#include <SoftwareSerial.h>

SoftwareSerial btSerial(10, 11); // RX, TX - Define software serial pins. Change if needed.

void setup() {
  // Open serial communications:
  Serial.begin(9600);
  while (!Serial) {
    ; // Wait for Serial to be ready
  }

  // Set up the HC-05 to the default baud rate for AT commands
  btSerial.begin(38400);
  delay(1000); // Give module a bit of time to initialize
  //Serial.println("Type AT commands!");
}

void loop() {
  // Read from HC-05 and print to the Arduino Serial Monitor
  if (btSerial.available()) {
    Serial.write(btSerial.read());
  }

  // Read from the Serial Monitor and print to HC-05
  if (Serial.available()) {
    btSerial.write(Serial.read());
  }
}
