import pygame
from grid import Grid
from algorithm import Algorithm
from utils import loadParameters

def main(win, width, rows):
	"""Main function of the programme."""

	grid = Grid.make_grid(rows, width)

	start = None

	run = True
	while run:
		Grid.draw(win, grid, rows, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = Grid.get_clicked_pos(pos, rows, width)

				# if pos is within the grid
				if row < rows and col < rows:
					spot = grid[row][col]
					if not start:
						start = spot
						start.make_start()

					elif spot != start:
						spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = Grid.get_clicked_pos(pos, rows, width)
				if row < width and col < width:
					spot = grid[row][col]
					spot.reset()
					if spot == start:
						start = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start:
					Grid.clear_old_grid(win, grid, rows, width)
					for row in grid:
						for spot in row:
							spot.update_neighbours(grid)
					
					Algorithm.spread(lambda: Grid.draw_path(win, grid, rows, width), start)

				if event.key == pygame.K_c:
					start = None
					grid = Grid.make_grid(rows, width)

		pygame.display.update()
	pygame.quit()

WIDTH, ROWS = loadParameters()
pygame.display.set_caption('Fire fighters VS fire')
WIN = pygame.display.set_mode((WIDTH, WIDTH))
main(WIN, WIDTH, ROWS)