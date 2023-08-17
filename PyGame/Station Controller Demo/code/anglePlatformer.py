#In this code we're trying to run a game, with an angle sensor


import pygame, sys
import serial


pygame.init()


#Definiteions for Window Dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720

# Create a display surface
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('anglePlatformer')

characterSurf=pygame.Surface((200,100))

clock = pygame.time.Clock()

# importing images 


# Using sprites


characterXPos=500
characterYPos=200



while True: # run forever -> keeps our game running



	# 1. input -> events (mouse click, mouse movement, press of a button, controller or touchscreen)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				characterYPos-=5

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				characterYPos+=5




	# framerate limit
	clock.tick(120)
	

	# 2. updates 
	#display_surface.fill((0, 0, 0)) 
	display_surface.fill('gray')
	characterSurf.fill('black')
	display_surface.blit(characterSurf,(characterXPos,characterYPos))

	# 3. show the frame to the player / update the display surface
	pygame.display.update()
