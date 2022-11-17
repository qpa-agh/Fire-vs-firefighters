import pygame
from grid import Grid
from algorithm import Algorithm
from utils import loadParameters


def main(width, rows):
    pygame.display.set_caption("Fire figters vs fire")
    win = pygame.display.set_mode((WIDTH, WIDTH))
    grid = Grid(win, rows, width)

    run = True
    while run:
        grid.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_pos(pos)

                # if pos is within the grid
                if row < rows and col < rows:
                    grid.make_fire(row, col)

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_pos(pos)
                if row < width and col < width:
                    grid.reset(row, col)

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         Grid.clear_old_grid(win, grid, rows, width)
            #         for row in grid:
            #             for spot in row:
            #                 spot.update_neighbours(grid)

            #         Algorithm.spread(lambda: Grid.draw_path(
            #             win, grid, rows, width), None)

            #     if event.key == pygame.K_c:
            #         grid = Grid.make_grid(rows, width)

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    WIDTH, ROWS = loadParameters()
    main(WIDTH, ROWS)
