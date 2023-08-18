# IFX-Man
The goal of the project is to write a game where the user can play by vertically moving a controller Up and Down. This vertical motion has to be captured and its respective data sent wirelessly to the game station, where a python game is to be played
<div style="text-align:center">
    <img src="Photos/Game Start Screen.PNG" alt="Current Setup" width="720"/>
</div>




## Current Setup
2 XMC2Go each connected to a DPS310 sensor. Both uControllers are connected to a computer and both are simultaneously serially transmiting their air pressure readings.

<div style="text-align:center">
    <img src="Photos/setupExplanation.PNG" alt="Current Setup" width="480"/>
</div>

These two microcotrollers are setup as follows:
   * station (placed on a reference surface)
   * Dynamic Controller (Held in the hand of the user)

The computer then calculates the difference delta between the pressure measured at the station and the dynamic controller. This delta value is used as an offset, where an upper and lower threshold is calculated for detecting the vertical motion of the dynamic controller



This setup allows maximum noise negation as only the difference delta between both readings of the sensors is taken into account


**ISSUE:**: Overtime the **delta** value drifts

### calibration

<pre>
```python
		if (counterFirstCalibration<10):
		  counterFirstCalibration+=1
			bufFirstCalibration.add(int(controller_value - base_value))
			if(counterFirstCalibration==10):
				calibratedOffset=bufFirstCalibration.average()
				upperThreshold = calibratedOffset + 2
				lowerThreshold = calibratedOffset -2
				firstCalibrationFlag=True
				print(f"Initial Calibration is succesfully done. Offset = {calibratedOffset} lT = {lowerThreshold} UT = {upperThreshold}")

```
</pre>