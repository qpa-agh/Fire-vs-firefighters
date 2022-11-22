from utils import *
from model import Model


def main(width, rows):
    model = Model(rows, rows, width)
    model.animate()


if __name__ == '__main__':
    WIDTH, ROWS = loadParameters()
    main(WIDTH, ROWS)
