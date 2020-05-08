import pygame
from pygame.locals import *
from random import randrange

class block: #Single block data representation
    def __init__(self,x=0,y=0): #Initlise with x,y, not strictly needed
        self.x,self.y = x, y
    def intersect(self, other): #Tests if another block lies at same position as self
        return True if (self.x==other.x and self.y==other.y) else False
    def render(self,screen,blocksize,color): #Renders one block
        pygame.draw.rect(screen,color,(50+self.x*blocksize,50+self.y*blocksize,blocksize,blocksize))

class snake:
    def __init__(self, playing_field): #Initialise a snake of length 3
        self.surroundings  =playing_field
        self.midpoint = int(playing_field.size/2)
        self.segments = [block(x=self.midpoint,y=self.midpoint+i) for i in range(2,-1,-1)]
        self.direction = (0,-1)
    def random_block(self):   #Generate a random position which does NOT overlap with any snake elements
        while True:
            ok=True
            trial_x, trial_y = randrange(0,self.surroundings.size), randrange(0,self.surroundings.size)
            trial_block=block(x=trial_x,y=trial_y)
            for seg in self.segments:
                if seg.intersect(trial_block):  ok = False 
            if ok: return trial_block
    def direction_update(self,keyboard_in): #Changedirection, don't allow to move directly opposite!
        if keyboard_in[0]!=0 or keyboard_in[1]!=0:
            if not ((self.direction[0] + keyboard_in[0]) == 0 and (self.direction[1] + keyboard_in[1]) == 0):
                self.direction=keyboard_in
    def move(self,food):     #Propagate snake, eat food if applicable
        trial_x = (self.segments[len(self.segments)-1].x+self.direction[0])%self.surroundings.size
        trial_y = (self.segments[len(self.segments)-1].y+self.direction[1])%self.surroundings.size
        trial_block = block(x=trial_x, y= trial_y)
        self_intersect = False
        for seg in self.segments:   #Check for biting its own tail
            if trial_block.intersect(seg): self_intersect=True
        if not self_intersect:
            has_eaten=False
            for f in food:  # Check for food and eat
                if trial_block.intersect(f):
                    self.segments.append(f)
                    food.remove(f)
                    has_eaten=True
            if not has_eaten:   # Propagate
                self.segments.append(trial_block)
                del self.segments[0]
            return 1
        else: return 0
    def render(self,screen,blocksize):
        for seg in self.segments:
            seg.render(screen, blocksize,(255,255,255))

class field:
    def __init__(self,size=20): #Initiliase a playing field
        self.size=size
        self.snake = snake(self)
        self.fruits = [self.snake.random_block()]
        self.game_over=False
    def advance(self, keyboard_in): #All game advance mechanisms
        if not self.game_over:
            self.snake.direction_update(keyboard_in)
            if self.snake.move(self.fruits) == 0: #Move snake and eat, test for game over
                self.game_over=True
            if len(self.fruits)==0:     #Add new fruits if was eaten
                self.fruits=[self.snake.random_block()]
    def render(self,screen):
        blocksize = int(400/self.size)
        pygame.draw.rect(screen,(0,0,0),(50,50,400,400)) # draw background
        if not self.game_over:
            render_text = "Length: "+str(len(self.snake.segments))
        else:
            render_text = "Game Over!  Score: "+str(len(self.snake.segments))+"   ENTER to restart ..."
        font = pygame.font.SysFont(None, 24)
        img = font.render(render_text, True, (255,255,255))
        screen.blit(img, (50, 20))
        for f in self.fruits:   # draw fruits in red
            f.render(screen,blocksize,(200,0,0))
        self.snake.render(screen,blocksize) # draw snake

        


def main_loop():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake")
    pygame.mouse.set_visible(0)
    screen = pygame.display.set_mode((500, 500))
    running=1
    game=field() #This is the main game instance
    while running:
        keyboard_in = (0,0)
        for event in pygame.event.get(): #Check arrow keys and enter for restart
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    keyboard_in=(0,-1)
                elif event.key == pygame.K_RIGHT:
                    keyboard_in=(1,0)
                elif event.key == pygame.K_DOWN:
                    keyboard_in=(0,1)
                elif event.key == pygame.K_LEFT:
                    keyboard_in=(-1,0)
                elif event.key == pygame.K_RETURN:
                    game=field()

        #Render and advance game
        game.advance(keyboard_in)
        screen.fill((50,50,50))
        game.render(screen)
        clock.tick(2+int(len(game.snake.segments)/3))
        pygame.display.update()
        
main_loop()