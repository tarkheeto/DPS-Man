import pygame, sys
import serial
from random import randint, uniform

gameMode=False


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



score=0


cloudSpawnTimer=5000




def display_score():
	score_text = f'Score: {score}'
	text_surf = font.render(score_text, True, (255,255,255))
	text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
	display_surface.blit(text_surf,text_rect)
	pygame.draw.rect(display_surface,(255,255,255),text_rect.inflate(30,30), width = 8, border_radius = 5)


#Now we add a 'game screen'




#Serial Connection Initialisation
base_station = serial.Serial('COM29', 9600, timeout=1)
dynamic_controller = serial.Serial('COM31', 9600, timeout=1)

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
		self.image = pygame.image.load('PyGame/Super Bot/graphics/ifxBotVertical.png').convert_alpha()
		self.image=pygame.transform.scale_by(self.image, 0.3)
		#3 we need a rect
		self.rect = self.image.get_rect(midtop=(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2))
		#Mask for collision Detection
		self.mask= pygame.mask.from_surface(self.image)
	score=0
	

	def collisionsWithClouds(self):
		if pygame.sprite.spritecollide(self,cloudGroup,True,pygame.sprite.collide_mask):

			#print("Collision Detected")
			return True			
			


#The creation of this class takes in the position that it should spawn at and the group, that it should belong to
#and the speed at which it should move
class cloudClass(pygame.sprite.Sprite):
	def __init__(self,pos,speed,groups):
		super().__init__(groups)
		self.image=pygame.image.load('PyGame/Super Bot/graphics/cloud.png').convert_alpha()
		self.image=pygame.transform.scale_by(self.image,0.8)

		#Create the rectangle with the center being at the input pos
		self.rect = self.image.get_rect(center=pos)

		#Create A mask for collision Detection
		self.mask= pygame.mask.from_surface(self.image)

		#For smoother animation Float based positioning
		#we take in position from the rectanle
		self.pos=pygame.math.Vector2(self.rect.center)	
		self.direction=pygame.Vector2(-1,0)
		self.speed=speed



		self.rect.center=pos
	def update(self):
		self.pos += self.direction * self.speed *dt
		self.rect.center=(round(self.pos.x),round(self.pos.y))

		if self.rect.right < 0:
			self.kill()

		
#Sprite Groups
spriteGroup = pygame.sprite.Group()
cloudGroup = pygame.sprite.Group()


#Sprite Creation
hero = ifxMan()
spriteGroup.add(hero)





#Timers
# Meteor timer sets an event every second, which will be used for spawning the clouds
#CHANGE THE TIMER DURATION TO A VARIABLE JUST SO THE HIGHER THE SCORE THE LOWER THE SPAWNING PERIOD
cloudTimer=pygame.event.custom_type()
pygame.time.set_timer(cloudTimer,cloudSpawnTimer)

scoreTimer=pygame.event.custom_type()
pygame.time.set_timer(scoreTimer,1000)

bg_surf = pygame.image.load('PyGame/Super Bot/graphics/background.jpg').convert()
startScreenSurf=pygame.image.load('PyGame/Super Bot/graphics/Start Screen.png').convert()

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
				upperThreshold = calibratedOffset + 1
				lowerThreshold = calibratedOffset -1
				firstCalibrationFlag=True
				print(f"Initial Calibration is succesfully done. Offset = {calibratedOffset} lT = {lowerThreshold} UT = {upperThreshold}")






				
	#Game only starts to run if the first calibration flag is set to true


	#---------LATER INSERT CODE FOR ALSO PRESSING A KEYBOARD BUTTON TO START THE GAME WHICH WILL IN TURN SET A THE GAME MOD FLAG TO ON



	##Delta Value Computation
	if (firstCalibrationFlag and gameMode): 
	# Only compute the delta if both values are present
		if base_value is not None and controller_value is not None:
			delta = int(controller_value - base_value)
			print(f"Base Station Value: {base_value}, Dynamic Controller Value: {controller_value}, Delta: {delta}")

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
			hero.rect.top -= 4

		if hero.rect.bottom < 1080 and flagDown:
			hero.rect.bottom += 4

	for event in pygame.event.get():
		


		if(gameMode):
			if(event.type==cloudTimer):				
				cloudClass((2200,randint(200,800)),score*80 +100, cloudGroup)				
				print("schblanga")
				cloudSpawnTimer-=300
				if(cloudSpawnTimer<600):
					cloudSpawnTimer=500
				pygame.time.set_timer(cloudTimer,cloudSpawnTimer)
				if(score>20):
					cloudClass((2200,randint(200,800)),score*80 +100, cloudGroup)	
				if(score>35):
					cloudClass((2200,randint(200,800)),score*80 +100, cloudGroup)	
				if(score>50):
					cloudClass((2200,randint(200,800)),score*80 +100, cloudGroup)
			if(event.type==scoreTimer):
				score+=1
		
			

		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()


		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_s:
				score=0
				gameMode=True

		if event.type ==pygame.KEYDOWN:
			if event.key == pygame.K_a:
				counterFirstCalibration=0

				

	#
	
	clock.tick()
	dt= clock.tick(120)/1000

	# Update ifxMan position
	hero.center = (200, posY)

	display_surface.fill((0, 0, 0))
	display_surface.blit(startScreenSurf, (0, 0))
	if(gameMode):
		display_surface.blit(bg_surf, (0, 0))
		if(hero.collisionsWithClouds()):
			
			gameMode=False
			cloudSpawnTimer=5000
		#Updating our Groups
		cloudGroup.update()
		#Drawing our Groups
		spriteGroup.draw(display_surface)
		cloudGroup.draw(display_surface)


	display_score()




		



	pygame.display.update()
