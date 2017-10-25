import pygame
import threading
import interlock
from input_screen import input_screen
import time
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen_x = 800
screen_y = 500

neg = pygame.image.load('Icons/neg.png')
pos = pygame.image.load('Icons/neg.png')

voltageFactor = 0


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


def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


class TextObject:
    def __init__(self, screen, pos_x, pos_y, text):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.screen = screen
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.text_surf, self.text_rect = text_objects(text, self.font)
        self.text_rect.center = (self.pos_x, self.pos_y)

    def draw(self):
        self.screen.blit(self.text_surf, self.text_rect)

    def set_text(self, text):
        self.text_surf, self.text_rect = text_objects(text, self.font)
        self.text_rect.center = (self.pos_x, self.pos_y)


class Button(Rectangle):
    def __init__(self, screen, width, height, pos_x, pos_y, color, text):
        Rectangle.__init__(self, screen, width, height, pos_x, pos_y, color)
        large_text = pygame.font.Font('freesansbold.ttf', 30)
        self.text_surf, self.text_rect = text_objects(text, large_text)
        self.text_rect.center = (pos_x, pos_y)
        self.debounce = False

    def draw(self):
        Rectangle.draw(self)
        self.screen.blit(self.text_surf, self.text_rect)

    def action(self):
        print("Unset action command called")

    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if click[0]:
            if self.centerx + self.width/2 > mouse[0] > self.centerx - self.width/2 \
                    and self.centery + self.height/2 > mouse[1] > self.centery - self.height/2:
                if self.debounce is False:
                    self.action()
                    self.debounce = True
        else:
            self.debounce = False


class IncreaseButton(Button):
    def __init__(self, screen, width, height, pos_x, pos_y):
        Button.__init__(self, screen, width, height, pos_x, pos_y, GREEN, "+")

    def action(self):
        global voltageFactor
        if voltageFactor < 1:
            voltageFactor += 0.05


class DecreaseButton(Button):
    def __init__(self, screen, width, height, pos_x, pos_y):
        Button.__init__(self, screen, width, height, pos_x, pos_y, RED, "-")

    def action(self):
        global voltageFactor
        if voltageFactor > 0:
            voltageFactor -= 0.05


electron_list = []


class Electron:
    def __init__(self, screen, start_y, spread_start, spread_finish, channel_size):
        electron_list.append(self)
        self.screen = screen
        self.start_y = start_y
        self.pos_y = start_y
        self.pos_x = -20
        w, h = self.screen.get_size()
        self.max_x = w
        self.target_x = w + 20
        self.target_y = self.pos_y
        self.speed = 8
        self.spread_start = spread_start
        self.spread_finish = spread_finish
        self.channel_size = channel_size
        self.stage = 0

    def draw(self):
        self.screen.blit(neg, (self.pos_x, self.pos_y))

    def update(self):
        if self.pos_x > self.max_x + 20:
            self.remove()

        if self.pos_x > self.spread_start and self.stage is 0:
            self.target_y = self.pos_y + random.randint(0, int(self.channel_size))
            self.stage = 1
        if self.pos_x > self.spread_finish:
            self.target_y = self.start_y

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

    terminal_start = terminal_x - (terminal_width / 2)
    wire_height = terminal_height / 4

    terminal_end = terminal_start + terminal_width

    wire_y = (terminal_y - terminal_height/2) + 8

    button_width = 50
    button_height = button_width / 2

    button_x = button_width
    button_center = button_height * 2

    rect = Rectangle(screen, well_width, well_height, screen_x/2, well_y, RED)
    rect2 = RectangleAbove(rect, metal_width, 25, BLACK)
    rect3 = RectangleAbove(rect2, metal_width, 50, GREEN)

    rect4 = Rectangle(screen, terminal_width, terminal_height, terminal_x, terminal_y, BLUE)
    rect5 = Rectangle(screen, terminal_width, terminal_height, screen_x-terminal_x, terminal_y, BLUE)

    rect_wire_left = Rectangle(screen, terminal_start, wire_height, terminal_start / 2, wire_y, BLACK)
    rect_wire_right = Rectangle(screen, terminal_start, wire_height, screen_x - terminal_start / 2, wire_y, BLACK)

    increase_button = IncreaseButton(screen, button_width, button_height, button_x, button_center - button_height * 2/3)
    decrease_button = DecreaseButton(screen, button_width, button_height, button_x, button_center + button_height * 2/3)

    voltage_text = TextObject(screen, button_x + button_width * 3/2, button_center, "test")

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

        ref_voltage = input_screen.supply_voltage.get_hybrid()
        thresh = input_screen.thresh.get_hybrid()
        voltage = voltageFactor * ref_voltage
        voltage_text.set_text(str(round(voltage, 2)) + "V")
        if voltage <= thresh:
            on_proportion = 0
        else:
            on_proportion = (voltage - thresh) / (ref_voltage - thresh)

        current = local_input.max_idsat.get_hybrid() * 100 * on_proportion
        if time.clock() - last_generated_time > 50*(1/(current+0.00001)):
            last_generated_time = time.clock()
            Electron(screen, wire_y-8, terminal_start, screen_x-terminal_end, (terminal_height - 16) * on_proportion)

        rect2.update()
        rect2.draw()

        rect3.update()
        rect3.draw()

        rect4.draw()
        rect5.draw()

        rect_wire_left.draw()
        rect_wire_right.draw()

        increase_button.update()
        increase_button.draw()
        decrease_button.update()
        decrease_button.draw()

        voltage_text.draw()

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
    interlock.running = False

