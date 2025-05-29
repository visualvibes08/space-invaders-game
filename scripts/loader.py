import pygame

BASE_LOAD_PATH='assets/'

def load_img(name:str):
    img=pygame.image.load(BASE_LOAD_PATH+'images/'+name)
    return img

def load_sound(name:str):
    snd=pygame.mixer.music.load(BASE_LOAD_PATH+'sounds/'+name)
    return snd

def play_sfx(name:str):
    snd=pygame.mixer.Sound(BASE_LOAD_PATH+'sounds/'+name).play()
    return snd



