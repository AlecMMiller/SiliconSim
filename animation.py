import pygame
import threading
import interlock

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen_x = 800
screen_y = 500


class Rectangle(pygame.Rect):
    def __init__(self, screen, width, height, pos_x, pos_y):
        self.height = height
        self.width = width
        self.center = (pos_x, pos_y)
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, BLACK, self)

    def set_thickness(self, thickness):
        self.height = thickness

    def set_pos_y(self, pos_y):
        self.centery = pos_y


class RectangleAbove(Rectangle):
    def __init__(self, below, width, height):
        self.rect_below = below
        self.height = height
        self.width = width
        self.center = self.rect_below.center
        self.screen = self.rect_below.screen

    def update(self):
        y_offset = self.rect_below.centery - (self.rect_below.height/2) - self.height/2
        self.set_pos_y(y_offset)


def frame_run():
    pygame.init()
    size = [screen_x, screen_y]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Animation")

    rect = Rectangle(screen, 25, 25, screen_x/2, screen_y/2)
    rect2 = RectangleAbove(rect, 50, 25)

    global running

    while not interlock.animation_ready:
        pass

    while interlock.animation_ready:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                interlock.animation_ready = False
        screen.fill(WHITE)

        rect.draw()
        rect2.update()
        rect2.draw()

        pygame.display.flip()

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

