from typing import Tuple

import pygame as pg
import speech_recognition as speech
import sprites
import core

recognizer = speech.Recognizer()
recognizer.dynamic_energy_threshold = False

game = core.Game()
debug_room_size = 9
debug_room_center = 4
for j in range(0, debug_room_size):
    for i in range(0, debug_room_size):
        game.ground.add((i, j))
for j in range(0, debug_room_size):
    for i in range(0, debug_room_size):
        delta = (abs(i - debug_room_center), abs(j - debug_room_center))
        manhat_dist = delta[0] if delta[0] >= delta[1] else delta[1]
        if manhat_dist >= 4:
            game.walls.add((i, j))

# pygame setup
pg.init()
pg.font.init()

DEFAULT_FONT = pg.font.SysFont("Arial", 24)
text = "Hello world"
text_surf = DEFAULT_FONT.render(text, False, (255, 255, 255))

SCREEN_SIZE = (240, 144)

screen = pg.display.set_mode((SCREEN_SIZE[0] * 4, SCREEN_SIZE[1] * 4), pg.RESIZABLE)
clock = pg.time.Clock()
running = True

tiles = sprites.Spritesheet("tiles.png", (4, 4))
game_screen = pg.surface.Surface(SCREEN_SIZE)

def ask_voice(recognizer):
    out = None
    with speech.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Rec start.")
            audio_text = recognizer.listen(source, timeout=1.0)
            print("Rec end.")
            out = recognizer.recognize_google(audio_text)
            print("Text: " + out)
        except Exception as e:
            print("Sorry, I did not get that:", e)
    return out
def print_voice():
    global text_surf
    print("printing")
    data = ask_voice(recognizer)
    text = "SPEECH: " + data if data is not None else ""
    text_surf = DEFAULT_FONT.render(text, False, (255, 255, 255))
print_voice_debounce = False

def grid_to_draw(gridpos: Tuple[int, int]) -> Tuple[int, int]:
    return (gridpos[0] * 16, gridpos[1] * 16)

def render_game(game: core.Game):
    for ground_gridpos in game.ground:
        game_screen.blit(tiles.get_sprite(1), grid_to_draw(ground_gridpos))
    for wall_gridpos in game.walls:
        game_screen.blit(tiles.get_sprite(0), grid_to_draw(wall_gridpos))

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                text = "LISTENING: "
                text_surf = DEFAULT_FONT.render(text, False, (255, 255, 255))
                print_voice_debounce = True

    # Render steps
    game_screen.fill("black")
    render_game(game)

    screen.fill("black")
    screen.blit(pg.transform.scale(game_screen, screen.get_rect().size), (0, 0))
    screen.blit(text_surf, (0, 0))

    # flip buffer to display
    pg.display.flip()

    if print_voice_debounce:
        print_voice()
        print_voice_debounce = False

    clock.tick(60)

pg.quit()