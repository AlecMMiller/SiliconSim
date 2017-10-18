import pygame
import threading
import interlock
from input_screen import input_screen
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen_x = 800
screen_y = 500

neg = pygame.image.load('Icons/neg.png')
pos = pygame.image.load('Icons/neg.png')


class Rectangle(pygame.Rect):
    def __init__(self, screen, width, height, pos_x, pos_y, color):
        self.height = height
        self.width = width
        self.center = (pos_x, pos_y)
        self.screen = screen
        self.color = color

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self)

    def set_thickness(self, thickness):
        self.height = thickness

    def set_pos_y(self, pos_y):
        self.centery = pos_y


class RectangleAbove(Rectangle):
    def __init__(self, below, width, height, color):
        self.rect_below = below
        self.height = height
        self.width = width
        self.center = self.rect_below.center
        self.screen = self.rect_below.screen
        self.color = color

    def update(self):
        y_offset = self.rect_below.centery - (self.rect_below.height/2) - self.height/2
        self.set_pos_y(y_offset)


electron_list = []


class Electron:
    def __init__(self, screen, start_y):
        electron_list.append(self)
        self.screen = screen
        self.pos_y = start_y
        self.pos_x = -20
        w, h = self.screen.get_size()
        self.max_x = w
        self.target_x = w + 20
        self.target_y = self.pos_y
        self.speed = 8

    def draw(self):
        self.screen.blit(neg, (self.pos_x, self.pos_y))

    def update(self):
        if self.pos_x > self.max_x + 20:
            self.remove()

        if self.pos_x > (self.target_x + self.speed - 1):
            self.pos_x -= self.speed
        elif self.pos_x < (self.target_x - self.speed + 1):
            self.pos_x += self.speed

        if self.pos_y > (self.target_y + self.speed - 1):
            self.pos_y -= self.speed
        elif self.pos_y < (self.target_y - self.speed + 1):
            self.pos_y += self.speed

        self.draw()

    def remove(self):
        if self in electron_list:
            electron_list.remove(self)


def frame_run():
    pygame.init()
    size = [screen_x, screen_y]
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    pygame.display.set_caption("Animation")

    metal_width = screen_x/3
    well_height = screen_y*.4
    well_width = screen_x*0.6

    well_y = screen_y*3/4

    terminal_width = well_width / 3
    terminal_height = well_height / 3

    terminal_x = (screen_x-well_width)/2 + terminal_width/2
    terminal_y = well_y - well_height/2 + terminal_height/2

    wire_width = terminal_x - (terminal_width/2)
    wire_height = terminal_height / 4

    wire_y = (terminal_y - terminal_height/2) + wire_height

    rect = Rectangle(screen, well_width, well_height, screen_x/2, well_y, RED)
    rect2 = RectangleAbove(rect, metal_width, 25, BLACK)
    rect3 = RectangleAbove(rect2, metal_width, 50, GREEN)

    rect4 = Rectangle(screen, terminal_width, terminal_height, terminal_x, terminal_y, BLUE)
    rect5 = Rectangle(screen, terminal_width, terminal_height, screen_x-terminal_x, terminal_y, BLUE)

    rect_wire_left = Rectangle(screen, wire_width, wire_height, wire_width/2, wire_y, BLACK)
    rect_wire_right = Rectangle(screen, wire_width, wire_height, screen_x-wire_width/2, wire_y, BLACK)

    last_generated_time = time.clock()

    while not interlock.running:
        pass

    while interlock.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                interlock.running = False
        screen.fill(WHITE)
        with interlock.thread_lock:
            local_input = input_screen
        rect.draw()
        ox_thickness = int(4*local_input.ox_thick.get_input())
        rect2.set_thickness(ox_thickness)

        current = local_input.max_idsat.get_hybrid() * 100
        if time.clock() - last_generated_time > 50*(1/current):
            last_generated_time = time.clock()
            Electron(screen, wire_y-8)

        rect2.update()
        rect2.draw()

        rect3.update()
        rect3.draw()

        rect4.draw()
        rect5.draw()

        rect_wire_left.draw()
        rect_wire_right.draw()

        for electron in electron_list:
            electron.update()

        pygame.display.flip()
        clock.tick_busy_loop(40)


    pygame.quit()


class AnimationThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        frame_run()


animation_thread = AnimationThread(1)


def start():
    animation_thread.start()


def stop():
    global running
    running = False

