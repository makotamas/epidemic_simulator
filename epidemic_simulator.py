import pygame
import sys
from random import randint

#Constants
SCREEN_SIZE = WIDTH, HEIGHT = (1280, 680) 
NUMBER_OF_PEOPLE = 75 
PERSON_SPEED = 30
PERSON_COLOR_CLEAR = (200, 150, 0)
PERSON_COLOR_INFECTED = (200, 0, 0)
PERSON_COLOR_IMMUNE = (0, 150, 0)
PERSON_AURA = 20
ILLNES_TIME = 500
IMMUNE_TIME = 800
INFACTION_PROBABILITY_WITH_MASK = 60
INFACTION_PROBABILITY_WITHOUT_MASK = 2
FIRST_CONTACT = 1
BUDGET = 2000
VACCINE_PRICE = 100
MASK_PRICE = 25


#Initialization
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE) 
pygame.display.set_caption("Epidemic Simulator 1.0") 
fps = pygame.time.Clock() 
pause = False   
time = 0

#Person Class
class Person:
    def __init__(self, x, y):
        self.x = x 
        self.y = y 
        self.dx = randint(-1, 1) 
        self.dy = randint(-1, 1)
        self.illnes = 0
        self.immune = 0
        self.mask = False

    def move(self):
        if randint(1, 30) == 1: 
            self.dx = randint(-1, 1)
        if randint(1, 30) == 1:
            self.dy = randint(-1, 1)

        if PERSON_AURA < self.x + self.dx < WIDTH-PERSON_AURA:    
            self.x += self.dx
        if PERSON_AURA + 50 < self.y + self.dy < HEIGHT-PERSON_AURA:    
            self.y += self.dy

    def cure(self):
        if self.illnes > 0:
            self.illnes -= 1
            if self.illnes == 0:
                self.immune = IMMUNE_TIME
        if self.immune > 0:
            self.immune -= 1

def vaccine(people, pos):
    global BUDGET
    for person in people:
        if person.x - PERSON_AURA < pos[0] < person.x + PERSON_AURA \
            and person.y - PERSON_AURA < pos[1] < person.y + PERSON_AURA:
            if person.illnes == 0 and person.immune == 0:
                if BUDGET >= VACCINE_PRICE:
                    person.immune = IMMUNE_TIME
                    BUDGET -= VACCINE_PRICE

def mask(people, pos):
    global BUDGET
    for person in people:
        if person.x - PERSON_AURA < pos[0] < person.x + PERSON_AURA \
            and person.y - PERSON_AURA < pos[1] < person.y + PERSON_AURA:
            if not person.mask and BUDGET >= MASK_PRICE:
                person.mask = True
                BUDGET -= MASK_PRICE
            else:
                person.mask = False


def modify(people):
    for person in people:
        person.move()
        person.cure()

        for other_person in people:
            if id(person) != id(other_person):
                if other_person.x - 2 * PERSON_AURA < person.x < other_person.x + 2 * PERSON_AURA \
                        and other_person.y - 2 * PERSON_AURA < person.y < other_person.y + 2 * PERSON_AURA:
                    if other_person.illnes > 0 and person.illnes == 0 and person.immune == 0:
                        if person.mask == True or other_person.mask == True:
                            if randint(1, INFACTION_PROBABILITY_WITH_MASK) == 1:
                                person.illnes = ILLNES_TIME
                        else:
                            if randint(1, INFACTION_PROBABILITY_WITHOUT_MASK) == 1:
                                person.illnes = ILLNES_TIME


def draw(people):
    global pause
    _count_infected_people = 0

    screen.fill((0, 0, 0)) 

    for person in people:
        _mask = 0
        if person.illnes > 0:
            _color = PERSON_COLOR_INFECTED
            if person.mask:
                _mask = 5
        elif person.immune > 0:
            _color = PERSON_COLOR_IMMUNE
            if person.mask:
                _mask = 5
        else:
            _color = PERSON_COLOR_CLEAR
            if person.mask:
                _mask = 5


        pygame.draw.circle(screen, _color, (person.x, person.y), PERSON_AURA, _mask) 

        if person.illnes > 0:
            _count_infected_people += 1

    if _count_infected_people == 0:
        pause = True
    
    font = pygame.font.SysFont('Calibri', 30)

    text = font.render("Active cases: " + str(_count_infected_people), True, (200, 200, 200))
    textRect = text.get_rect()
    textRect.left = 10
    textRect.top = 10
    screen.blit(text, textRect) 

    text = font.render("Time " + str(time), True, (200, 200, 200))
    textRect = text.get_rect()
    textRect.left = 300
    textRect.top = 10
    screen.blit(text, textRect) 

    text = font.render("Budget " + str(BUDGET), True, (200, 200, 200))
    textRect = text.get_rect()
    textRect.left = 450
    textRect.top = 10
    screen.blit(text, textRect)

    text = font.render("Clear:      Infected:      Immune:      Mask:", True, (200, 200, 200))
    textRect = text.get_rect()
    textRect.left = 700
    textRect.top = 10
    screen.blit(text, textRect)

    pygame.draw.circle(screen, PERSON_COLOR_CLEAR, (790, 23), PERSON_AURA, 0)
    pygame.draw.circle(screen, PERSON_COLOR_INFECTED, (940, 23), PERSON_AURA, 0)
    pygame.draw.circle(screen, PERSON_COLOR_IMMUNE, (1090, 23), PERSON_AURA, 0)
    pygame.draw.circle(screen, PERSON_COLOR_CLEAR, (1205, 23), PERSON_AURA, 5)
    
    pygame.display.update() 
    fps.tick(PERSON_SPEED)


# Create people
main_people_list = [Person(randint(50, WIDTH-50), randint(50, HEIGHT-50)) for i in range(NUMBER_OF_PEOPLE)] 

# The first infection
for i in range(FIRST_CONTACT):
    main_people_list[i].illnes = ILLNES_TIME


#Main program
while True: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE: 
                pause = not pause 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                vaccine(main_people_list, pygame.mouse.get_pos())
            if event.button == pygame.BUTTON_RIGHT:
                mask(main_people_list, pygame.mouse.get_pos())
    if not pause: 
        modify(main_people_list)
        draw(main_people_list)
        time += 1

