import pygame, sys
import serial
port = 'COM30'  # Replace with the actual COM port number
ser = serial.Serial(port, baudrate=9600)  

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('DPS Demo')
clock = pygame.time.Clock()

# importing images 
ship_surf = pygame.image.load('../graphics/DPSKit2Go.PNG').convert_alpha()
ship_surf = pygame.transform.scale(ship_surf,(50,180))
ship_rect = ship_surf.get_rect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2))
bg_surf = pygame.image.load('../graphics/background.png').convert()

posY=360
posX=0
flagUp=False
flagDown=False
while True: # run forever -> keeps our game running
	# read serial input
	if ser.in_waiting > 0:
		line = ser.readline().decode('utf-8').strip()
		if line != 'Nothing': 
			if line == 'Up':
				print("Up")
				flagUp=True
				flagDown=False
				#posY -= 20  # decrement posY
			elif line == 'Down':
				print("Down")
				flagDown=True
				flagUp=False
				#posY += 20  # increment posY
		else:
			print("Nothing")
			flagDown=False
			flagUp=False

	if(ship_rect.top>10):
		if(flagUp):
			posY-=5
	if(ship_rect.bottom<710):	
		if(flagDown):
			posY+=5


	# 1. input -> events (mouse click, mouse movement, press of a button, controller or touchscreen)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	# framerate limit
	clock.tick(120)
	
	# place the ship according to posY variable
	ship_rect.center = (200,posY)

	# 2. updates 
	display_surface.fill((0, 0, 0)) 
	display_surface.blit(bg_surf,(0,0))
	display_surface.blit(ship_surf,ship_rect)

	# 3. show the frame to the player / update the display surface
	pygame.display.update()
