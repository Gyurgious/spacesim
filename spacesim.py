import pygame
import math

pygame.init()

width = 1200
height = 1000

window = pygame.display.set_mode((width, height)) # set screen
pygame.display.set_caption("Planet Simulation") #set title of tab

bg = pygame.image.load("space.png")

white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)
blue = (30, 144, 255)
red = (188, 39, 50)
gray = (128, 128, 128)
orange = (255, 165, 0)
brown = (150, 75, 0)

font = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = (149.6e6 * 1000)  # distance from center of earth to sun
    G = 6.67428e-11 # force of gravitational attaction between two objects
    scale = 100/ AU   # 1AU = 100pixels
    timestep = 3600 * 24   # 1 day



    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_velocity = 0
        self.y_velocity = 0

    def draw(self, win):
        x = self.x * self.scale + width/2
        y = self.y * self.scale + height/2


        if len(self.orbit) > 2:

            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.scale + width/2
                y = y * self.scale + height/2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        if not self.sun:
            distance_text = font.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, white)
            win.blit(distance_text, (x-distance_text.get_width()/2, y - distance_text.get_height()/2))
            text_test = font.render(self.name, 1, white)
            win.blit(text_test, (x, y+15))


        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other): # physics/math calculation
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x) # find angle
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_velocity += total_fx/self.mass * self.timestep # f = ma
        self.y_velocity += total_fy/self.mass * self.timestep

        self.x += self.x_velocity * self.timestep
        self.y += self.y_velocity * self.timestep
        self.orbit.append((self.x, self.y))





def main():
    run = True
    clock = pygame.time.Clock()


    sun = Planet(0, 0, 15, yellow, 1.98891*10**30, "sun")
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 9, gray, 3.30 * 10 ** 23, "Mercury")
    mercury.y_velocity = 47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, orange, 4.865 * 10 ** 24,  "Venus")
    venus.y_velocity = -35.02 * 1000

    earth = Planet(1 * Planet.AU, 0, 16, blue, 5.9722 * 10 ** 24, "Earth")  # -1*planet is distance from sun
    earth.y_velocity = 29.783 * 1000  # km to m

    mars = Planet(1.524 * Planet.AU, 0, 12, red, 6.39 * 10 ** 23, "Mars")
    mars.y_velocity = 24.077 * 1000

    jupiter = Planet(5.204 * Planet.AU, 0, 20, brown, 1.89813 * 10 ** 27, "Jupiter")
    jupiter.y_velocity = 13.1 * 1000






    planets = [sun, earth, mars, mercury, venus, jupiter]

    while run:
        clock.tick(60) # keep game on steady framerate
        window.blit(bg, (0, 0))
        # pygame.display.update() #keep screen as white

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if user clicks on 'x'
                run = False # end game

        for planet in planets:
            planet.update_position(planets)
            planet.draw(window)

        pygame.display.update()

    pygame.quit()

main()

