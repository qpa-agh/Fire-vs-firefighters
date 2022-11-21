from cell import *
from colors import *
import pygame
import random


class Model:
    def __init__(self, cells_y, cells_x, width):
        self.win = pygame.display.set_mode((width + 100, width ))
        self.cells_y = cells_y       # nr of rows
        self.cells_x = cells_x       # nr of columns
        self.width = width           # display width
        self.gap = width // cells_y  # width of the spot
        self.cells_on_fire = set()

        Spot.set_parameters(self.gap, self.win)
        self.grid = [[Cell(j, i)
                      for i in range(cells_x)] for j in range(cells_y)]
        self.update_neigbours()
        self.generate_random_forest(20000)

    def generate_random_forest(self, trees=None):
        if not trees:
            trees = int(self.cells_y * self.cells_x * 0.8)
        random_list = random.sample(
            range(0, self.cells_y*self.cells_x - 1), trees)
        for nr in random_list:
            self.grid[nr//self.cells_x][nr % self.cells_x].wood = random.randint(1, 5)
            self.grid[nr//self.cells_x][nr % self.cells_x].make_tree()
            

    def draw(self):
        """Draws square grid with colored spots."""
        self.win.fill(Color.grass_green)
        for row in self.grid:
            for cell in row:
                cell.visual.draw()

    def get_clicked_pos(self, pos) -> tuple():
        """Returns row and columns idx of clicked place."""
        y, x = pos
        row = y // self.gap
        col = x // self.gap
        return row, col

    def animate(self):
        pygame.display.set_caption("Fire figters vs fire")
        run = True
        animation_started = False
        while run:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if not animation_started:
                    if pygame.mouse.get_pressed()[0]:  # LEFT
                        pos = pygame.mouse.get_pos()
                        row, col = self.get_clicked_pos(pos)

                        # if pos is within the model.visual
                        if row < self.cells_y and col < self.cells_x:
                            self.make_spot_fire(row, col)

                    elif pygame.mouse.get_pressed()[2]:  # RIGHT
                        pos = pygame.mouse.get_pos()
                        row, col = self.get_clicked_pos(pos)
                        if row < self.cells_y and col < self.cells_x:
                            self.reset_spot(row, col)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            animation_started = True

                        if event.key == pygame.K_c: # reset
                            self.reset_model()
            if animation_started:
                self.spread_fire()
                if not self.cells_on_fire:
                    animation_started = False

            pygame.display.update()
        pygame.quit()

    def make_spot_fire(self, row, col):
        if self.grid[row][col].cell_type == CellType.TREE:
            self.grid[row][col].make_fire()
            self.cells_on_fire.add(self.grid[row][col])
    
    def reset_spot(self, row, col):
        if self.grid[row][col].cell_type == CellType.FIRE:
            self.grid[row][col].make_tree()
            self.cells_on_fire.remove(self.grid[row][col])

    def reset_model(self):
        self.grid = [[Cell(j, i)
                      for i in range(self.cells_x)] for j in range(self.cells_y)]
        self.update_neigbours()
        self.generate_random_forest()

    def update_neigbours(self):
        for row_idx in range(self.cells_y):
            for col_idx in range(self.cells_x):
                if row_idx > 0:
                    # left top corner
                    if col_idx > 0:
                        self.grid[row_idx][col_idx].neighbours[0] = self.grid[row_idx-1][col_idx-1]
                    # top
                    self.grid[row_idx][col_idx].neighbours[1] = self.grid[row_idx-1][col_idx]
                    # right top corner
                    if col_idx < self.cells_x - 1:
                        self.grid[row_idx][col_idx].neighbours[2] = self.grid[row_idx-1][col_idx+1]
                # left
                if col_idx > 0:
                    self.grid[row_idx][col_idx].neighbours[7] = self.grid[row_idx][col_idx-1]
                # right
                if col_idx < self.cells_x - 1:
                    self.grid[row_idx][col_idx].neighbours[3] = self.grid[row_idx][col_idx+1]
                if row_idx < self.cells_y - 1:
                    # left bottom corner
                    if col_idx > 0:
                        self.grid[row_idx][col_idx].neighbours[4] = self.grid[row_idx+1][col_idx-1]
                    # bottom
                    self.grid[row_idx][col_idx].neighbours[5] = self.grid[row_idx+1][col_idx]
                    # right bottom corner
                    if col_idx < self.cells_x - 1:
                        self.grid[row_idx][col_idx].neighbours[6] = self.grid[row_idx+1][col_idx+1]

    def spread_fire(self):
        new_generation = set()
        for cell in self.cells_on_fire:
            for key, neighbour in cell.neighbours.items():
                if neighbour.cell_type == CellType.TREE:
                    if key in [1,3,5,7]: # corners
                        if random.random() < 0.5:
                            neighbour.make_fire()
                            new_generation.add(neighbour)
                    else:
                        neighbour.make_fire()
                        new_generation.add(neighbour)
            cell.wood -= 0.25
            cell.burned_wood += 0.25
            if cell.wood <= 0:
                cell.make_burned()
            else:
                cell.make_fire()
                new_generation.add(cell)
        self.cells_on_fire = new_generation
