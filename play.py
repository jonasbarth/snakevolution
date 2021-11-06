import argparse
import os

import pygame
from frametovideo.writer import Mp4Writer
from frametovideo.writer import ImageType

from util.io.importing.genetic_importer import GeneticImporter
from pysnakegym.mdp import SnakeMDP

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--model", nargs='?', type=str, default="", help="the path to the pytorch model that will be loaded")
    parser.add_argument("-r", "--record", dest='record', action='store_true', help="indicates whether the game should be recorded or not")
    parser.set_defaults(record=False)

    args = parser.parse_args()
    model_path = args.model
    record = args.record

    screen_width = 800
    screen_height = 800

    mdp = SnakeMDP(screen_width=screen_width, screen_height=screen_height, snake_size=80, show_game=True)
    importer = GeneticImporter(model_path, mdp, [mdp.state_dims()[0]], mdp.n_actions())
    genetic_agent = importer.import_model()

    state, reward, done = mdp.reset()
    n = 0

    base_path = f'docs/images/{model_path[:-4]}'
    frames_path = f'{base_path}/frames'
    output_path = f'{base_path}/'

    os.makedirs(frames_path, exist_ok=True)

    while not done:
        if record:
            pygame.image.save(mdp.environment.window, f'{frames_path}/game_{n}.jpg')
        action = genetic_agent.choose_action(state)
        state_, reward, done = mdp.step(action=action)
        state = state_
        n += 1

    if record:
        writer = Mp4Writer(frames_path=frames_path, output_path=output_path, frame_size=(screen_width, screen_height), fps=60, image_type=ImageType.JPG)
        writer.convert()
        writer.clean_frames()
