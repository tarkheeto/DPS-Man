# Ifx-Pong
The goal of the project is to write a game where the user can play by vertically moving a controller Up and Down. This vertical motion has to be captured and its respective data sent wirelessly to the game station, where a python game is to be played
## Current Setup
2 XMC2Go each connected to a DPS310 sensor. Both uControllers are connected to each other via two GPIO Pins. Where there is only one master uController and another slave. 

<div style="text-align:center">
    <img src="current setup.jpg" alt="Current Setup" width="720"/>
</div>



The slave uController processes its DPS310 reading into either an upward, downward or a still motion. Using the GPIO connection the slave uController will encode the reading into: 


| Motion | Pin4 | Pin5 |
|--------|------|------|
| Upwards     | HIGH | LOW  |
| Downwards   | LOW  | HIGH |
| Still  | LOW  | LOW  |


To process the readings to Upwards, Downwards or still motion the uController runs the following in it's loop: 

```cpp
ret = Dps3xxPressureSensor.measurePressureOnce(pressure, 7);

if(pressure-pressureBuffer>0.8){
  Serial.println(" Down");
  pressureBuffer=pressure;
    digitalWrite(4, LOW);
    digitalWrite(5, HIGH);
}
else if(pressure-pressureBuffer<-0.8){
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
```



**Feel free to change the 0.8 value (it's experimental)**

Practically the same happens in the master variant of the code where the master just has to read what the slave says:

```cpp
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
```
then it takes its own measurement processes it, and then checks if the slave has the same opinion:

```cpp
ret = Dps3xxPressureSensor.measurePressureOnce(pressure, 7);

    if((pressure-pressureBuffer>0.8) && down){
      Serial.println(" Down");
      pressureBuffer=pressure;
        
 
    }
    else if((pressure-pressureBuffer<-0.8) && up){
      Serial.println("Up");
      pressureBuffer=pressure;

    }
    else{
      Serial.println("Nothing");

      }
```



All this data that is serially fed from the master to the computer, (Up,Down or Nothing) is fed to a python script that deals with the whole game.