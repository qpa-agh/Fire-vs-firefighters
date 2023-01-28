import warnings
from controller.sim_controller import SimulationController
from utils.utils import *
from model.model import Model

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

with warnings.catch_warnings():
    warnings.filterwarnings('error')

def main(gap, rows, forest_map):
    model = Model(rows, rows, gap, forest_map)
    simulation = SimulationController(model)
    simulation.run_simulation()

if __name__ == '__main__':
    import pygame
    ROWS, GAP = loadParameters()
    forest_map = 'maps/niepolomice_1.png' # change to None to generate map randomly
    pygame.init()
    main(GAP, ROWS, forest_map)
