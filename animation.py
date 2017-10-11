import pygame
import threading

lock = threading.Lock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen_x = 800
screen_y = 500

running = False


def frame_run():
    pygame.init()
    size = [screen_x, screen_y]
    screen = pygame.display.set_mode(size)

    global running

    while not running:
        pass

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

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


def enable():
    global  running
    running = True

