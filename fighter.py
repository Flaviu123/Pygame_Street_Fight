import pygame
from pygame.constants import (QUIT, K_ESCAPE, KEYDOWN, K_SPACE, MOUSEBUTTONDOWN, K_d, K_a, K_RIGHT, K_LEFT)
import os

#Settings mit globalen Variabeln
class Settings(object):
    window_width = 500
    window_height = 350
    fps = 60
    title = "Fighter"
    path = {}
    path['file'] = os.path.dirname(os.path.abspath(__file__))
    path['image'] = os.path.join(path['file'], "images")
    Speed = 3

    @staticmethod
    def dim():
        return (Settings.window_width, Settings.window_height)

    @staticmethod
    def filepath(name):
        return os.path.join(Settings.path['file'], name)

    @staticmethod
    def imagepath(name):
        return os.path.join(Settings.path['image'], name)

#Timer für die animation
class Timer(object):
    def __init__(self, duration, with_start = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

    def change_duration(self, delta=10):
        self.duration += delta
        if self.duration < 0:
            self.duration = 0

#Animation wo die Optionen für Animations objekte sind enless mode etc 
class Animation(object):
    def __init__(self, namelist, endless, animationtime, colorkey=None):
        self.images = []
        self.endless = endless
        self.timer = Timer(animationtime)
        for filename in namelist:
            if colorkey == None:
                bitmap = pygame.image.load(Settings.imagepath(filename)).convert_alpha()
            else:
                bitmap = pygame.image.load(Settings.imagepath(filename)).convert()
                bitmap.set_colorkey(colorkey)           # Transparenz herstellen §\label{srcAnimation0101}§
            self.images.append(bitmap)
        self.imageindex = -1

    def next(self):
        if self.timer.is_next_stop_reached():
            self.imageindex += 1
            if self.imageindex >= len(self.images):
                if self.endless:
                    self.imageindex = 0
                else:
                    self.imageindex = len(self.images) - 1
        return self.images[self.imageindex]

    def is_ended(self):
        if self.endless:
            return False
        elif self.imageindex >= len(self.images) - 1:
            return True
        else:
            return False

#classe fighter mit dem movement den Animationen
class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_lock_walk = True
        self.animation_lock_jump = True
        self.animation_lock_hadouken = True
        self.animation_lock_HitUp = True
        self.animation_walk = Animation([f"Walk{i}.png" for i in range(5)], False, 150)
        self.animation_jump = Animation([f"Jump{i}.png" for i in range(7)], False, 150)
        self.animation_hadouken = Animation([f"Hadouken{i}.png" for i in range(5)], False, 150)
        self.image = self.animation_jump.next()
        self.rect = self.image.get_rect()
        self.rect.center = (Settings.window_width // 2, Settings.window_height // 2)

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left - Settings.Speed > 0:
            self.rect.left -= Settings.Speed
        elif keys[pygame.K_RIGHT] and self.rect.left + Settings.Speed + self.get_width() < Settings.window_width:
            self.rect.left += Settings.Speed

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def get_center(self):
        return self.rect.center

    def update(self):
        if self.animation_lock_walk == False:
            self.image = self.animation_walk.next()
            if self.animation_walk.is_ended():
                self.animation_lock_walk = True
        if self.animation_lock_jump == False:
            self.image = self.animation_jump.next()
            if self.animation_jump.is_ended():
                self.animation_lock_jump = True
        if self.animation_lock_HitUp == False:
            self.image = self.animation_HitUp.next()
            if self.animation_HitUp.is_ended():
                self.animation_lock_HitUp = True
        if self.animation_lock_hadouken == False:
            self.image = self.animation_hadouken.next()
            if self.animation_hadouken.is_ended():
                self.animation_lock_hadouken = True
        self.movement()

#FighterAnimations classe mit watch for events
class FighterAnimation(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.dim())
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.Fighter = pygame.sprite.GroupSingle(Fighter())
        self.running = False

    def run(self) -> None:
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_RIGHT:
                    self.Fighter.sprite.animation_lock_walk = False
                    self.Fighter.sprite.animation_walk = Animation([f"Walk{i}.png" for i in range(5)], False, 150)
                elif event.key == K_LEFT:
                    self.Fighter.sprite.animation_lock_walk = False
                    self.Fighter.sprite.animation_walk = Animation([f"Walk{i}.png" for i in range(5)], False, 150)
                elif event.key == K_SPACE:
                    self.Fighter.sprite.animation_lock_jump = False
                    self.Fighter.sprite.animation_jump = Animation([f"Jump{i}.png" for i in range(7)], False, 150)
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.Fighter.sprite.animation_lock_HitUp = False
                    self.Fighter.sprite.animation_HitUp = Animation([f"HitUp{i}.png" for i in range(5)], False, 150)
                elif event.button == 3:
                    self.Fighter.sprite.animation_lock_hadouken = False
                    self.Fighter.sprite.animation_hadouken = Animation([f"Hadouken{i}.png" for i in range(5)], False, 150)


    def update(self) -> None:
        self.Fighter.update()

    def draw(self) -> None:
        self.screen.fill((200, 200, 200))
        self.Fighter.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    anim = FighterAnimation()
    anim.run()
