from controller.sim_controller import SimulationController
from utils.utils import *
from model.model import Model


def main(width, rows, forest_map):
    model = Model(rows, rows, width, forest_map)
    simulation = SimulationController(model)
    simulation.run_simulation()


if __name__ == '__main__':
    WIDTH, ROWS = loadParameters()
    forest_map = 'maps/niepolomice_1.png' # change to None to generate map randomly
    main(WIDTH, ROWS, forest_map)
