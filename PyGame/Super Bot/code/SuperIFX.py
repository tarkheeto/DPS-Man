import pygame, sys
import serial
from random import randint, uniform

gameMode=True


#Calibration
class Buffer:
    def __init__(self, size):
        self.size = size
        self.buffer = []

    def add(self, value):
        if len(self.buffer) >= self.size:
            self.buffer.pop(0)  # Remove the oldest value
        self.buffer.append(value)

    def get(self):
        return self.buffer

    def average(self):
        if not self.buffer:
            return 0  # Return 0 or some other default value if buffer is empty
        return sum(self.buffer) / len(self.buffer)
    

#Used to perform the iterations upon which the average is taken to find the offset
counterFirstCalibration=0
bufFirstCalibration=Buffer(9)
#Variables that dictate the delta threshold for determing motion direction (delta +-2)
upperThreshold=0  
lowerThreshold=0











def display_score():
	score_text = f'Score: {hero.score}'
	text_surf = font.render(score_text, True, (255,255,255))
	text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
	display_surface.blit(text_surf,text_rect)
	pygame.draw.rect(display_surface,(255,255,255),text_rect.inflate(30,30), width = 8, border_radius = 5)


#Now we add a 'game screen'




#Serial Connection Initialisation
base_station = serial.Serial('COM30', 9600, timeout=1)
dynamic_controller = serial.Serial('COM36', 9600, timeout=1)

def get_float_from_port(port):
	"""Try reading a line from a port and convert to float."""
	try:
		line = port.readline().decode().strip()
		return float(line)
	except ValueError:
		print(f"Couldn't convert '{line}' to float.")
		return None





#Basic Setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Super IFX')
clock = pygame.time.Clock()


font = pygame.font.Font('PyGame/Super Bot/graphics/subatomic.ttf', 50)



#Sprites
class ifxMan(pygame.sprite.Sprite):
	def __init__(self):		
		super().__init__()   #1 init the parent class
		#2 we need a surface -> image
		self.image = pygame.image.load('PyGame/Super Bot/graphics/ifxBotHorizontal.png').convert_alpha()
		self.image=pygame.transform.scale_by(self.image, 0.1)
		#3 we need a rect
		self.rect = self.image.get_rect(midtop=(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2))
	score=0

	def collisionsWithClouds(self):
		if pygame.sprite.spritecollide(self,cloudGroup,False):
			print("Collision Detected")
			self.score=0
			


#The creation of this class takes in the position that it should spawn at and the group, that it should belong to
#and the speed at which it should move
class cloudClass(pygame.sprite.Sprite):
	def __init__(self,pos,speed,groups):
		super().__init__(groups)
		self.image=pygame.image.load('PyGame/Super Bot/graphics/cloud.png').convert_alpha()
		self.image=pygame.transform.scale_by(self.image,0.8)

		#Create the rectangle with the center being at the input pos
		self.rect = self.image.get_rect(center=pos)

		#For smoother animation Float based positioning
		#we take in position from the rectanle
		self.pos=pygame.math.Vector2(self.rect.center)	
		self.direction=pygame.Vector2(-1,0)
		self.speed=speed



		self.rect.center=pos
	def update(self):
		self.pos += self.direction * self.speed *dt
		self.rect.center=(round(self.pos.x),round(self.pos.y))

		
#Sprite Groups
spriteGroup = pygame.sprite.Group()
cloudGroup = pygame.sprite.Group()


#Sprite Creation
hero = ifxMan()
#cloud = cloudClass()
spriteGroup.add(hero)

#cloudGroup.add(cloud)




#Timers
# Meteor timer sets an event every second, which will be used for spawning the clouds
#CHANGE THE TIMER DURATION TO A VARIABLE JUST SO THE HIGHER THE SCORE THE LOWER THE SPAWNING PERIOD
cloudTimer=pygame.event.custom_type()
pygame.time.set_timer(cloudTimer,5000)

scoreTimer=pygame.event.custom_type()
pygame.time.set_timer(scoreTimer,1000)

bg_surf = pygame.image.load('PyGame/Super Bot/graphics/background.jpg').convert()

posY = 360
posX = 0
flagUp = False
flagDown = False
firstCalibrationFlag=False


while True:  # run forever -> keeps our game running
	if (base_station.in_waiting > 0) and (dynamic_controller.in_waiting > 0) :
		base_value = get_float_from_port(base_station)
		controller_value = get_float_from_port(dynamic_controller)

		#BOOT UP DELTA CALIBRATION
		#IMPLEMENT A WARNING NOT TO MOVE THE CONTROLLER FROM THE SAME SURFACE AS THE BASE STATION
		if (counterFirstCalibration<10):
			counterFirstCalibration+=1
			bufFirstCalibration.add(int(controller_value - base_value))
			if(counterFirstCalibration==10):
				calibratedOffset=bufFirstCalibration.average()
				upperThreshold = calibratedOffset + 2
				lowerThreshold = calibratedOffset -2
				firstCalibrationFlag=True
				print(f"Initial Calibration is succesfully done. Offset = {calibratedOffset} lT = {lowerThreshold} UT = {upperThreshold}")






				
	#Game only starts to run if the first calibration flag is set to true


	#---------LATER INSERT CODE FOR ALSO PRESSING A KEYBOARD BUTTON TO START THE GAME WHICH WILL IN TURN SET A THE GAME MOD FLAG TO ON



	##Delta Value Computation
	if (firstCalibrationFlag and gameMode): 
	# Only compute the delta if both values are present
		if base_value is not None and controller_value is not None:
			delta = int(controller_value - base_value)
			#print(f"Base Station Value: {base_value}, Dynamic Controller Value: {controller_value}, Delta: {delta}")

			if delta > upperThreshold:
				flagDown = True
				flagUp = False
			elif delta < lowerThreshold:
				flagDown = False
				flagUp = True
			else:
				flagDown = False
				flagUp = False
		else:
			# Keep the current flags if data isn't received
			pass

		

		if hero.rect.top > 10 and flagUp:
			hero.rect.top -= 2

		if hero.rect.bottom < 710 and flagDown:
			hero.rect.bottom += 2

	for event in pygame.event.get():
		


		if(gameMode):
			if(event.type==cloudTimer):
				
				cloudClass((2200,randint(0,1080)),500, cloudGroup)				
				print("schblanga")
			if(event.type==scoreTimer):
				hero.score+=1
		
			

		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()


	#
	
	clock.tick()
	dt= clock.tick(120)/1000

	# Update ifxMan position
	hero.center = (200, posY)

	display_surface.fill((0, 0, 0))
	display_surface.blit(bg_surf, (0, 0))

	hero.collisionsWithClouds()

	#Updating our Groups
	cloudGroup.update()

	#Drawing our Groups
	spriteGroup.draw(display_surface)
	cloudGroup.draw(display_surface)



	display_score()
	#Add eventually a blit for the obstacles


	pygame.display.update()
