from controller.sim_controller import SimulationController
from utils.utils import *
from model.model import Model


def main(width, rows):
    model = Model(rows, rows, width)
    simulation = SimulationController(model)
    simulation.run_simulation()


if __name__ == '__main__':
    WIDTH, ROWS = loadParameters()
    main(WIDTH, ROWS)
