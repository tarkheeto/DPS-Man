import pygame, sys
import serial

base_station = serial.Serial('COM30', 9600, timeout=1)
dynamic_controller = serial.Serial('COM36', 9600, timeout=1)

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('DPS Demo')
clock = pygame.time.Clock()

def get_float_from_port(port):
	"""Try reading a line from a port and convert to float."""
	try:
		line = port.readline().decode().strip()
		return float(line)
	except ValueError:
		print(f"Couldn't convert '{line}' to float.")
		return None

# importing images 
# Using sprites
ship_surf = pygame.image.load('../graphics/DPSKit2Go.PNG').convert_alpha()
ship_surf = pygame.transform.scale(ship_surf, (50, 180))
ship_rect = ship_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
bg_surf = pygame.image.load('../graphics/background.png').convert()

posY = 360
posX = 0
flagUp = False
flagDown = False

while True:  # run forever -> keeps our game running
	if (base_station.in_waiting > 0) and (dynamic_controller.in_waiting > 0) :
		base_value = get_float_from_port(base_station)
		controller_value = get_float_from_port(dynamic_controller)

	# Only compute the delta if both values are present
	if base_value is not None and controller_value is not None:
		delta = int(controller_value - base_value)
		print(f"Base Station Value: {base_value}, Dynamic Controller Value: {controller_value}, Delta: {delta}")

		if delta > -26:
			flagDown = True
			flagUp = False
		elif delta < -28:
			flagDown = False
			flagUp = True
		else:
			flagDown = False
			flagUp = False
	else:
		# Keep the current flags if data isn't received
		pass

	if ship_rect.top > 10 and flagUp:
		posY -= 2

	if ship_rect.bottom < 710 and flagDown:
		posY += 2

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	clock.tick(120)

	# Update ship position
	ship_rect.center = (200, posY)

	display_surface.fill((0, 0, 0))
	display_surface.blit(bg_surf, (0, 0))
	display_surface.blit(ship_surf, ship_rect)

	pygame.display.update()
