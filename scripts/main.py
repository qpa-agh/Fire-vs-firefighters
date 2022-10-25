import pygame
from grid import Grid
from algorithm import Algorithm
from utils import loadParameters
from button import ButtonHandler

def main(win, width, rows, heuristic):
	"""Main function of the programme."""

	grid = Grid.make_grid(rows, width)
	ButtonHandler.initialise_list(width)

	start = None
	end = None

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
					if not start and spot != end:
						start = spot
						start.make_start()

					elif not end and spot != start:
						end = spot
						end.make_end()

					elif spot != end and spot != start:
						spot.make_barrier()

				else: # check pushing button
					y, x = pos
					h = ButtonHandler.click_proper_button(x,y)
					if h is not None: # button was pushed
						heuristic = h

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = Grid.get_clicked_pos(pos, rows, width)
				if row < width and col < width:
					spot = grid[row][col]
					spot.reset()
					if spot == start:
						start = None
					elif spot == end:
						end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					Grid.clear_old_grid(win, grid, rows, width)
					for row in grid:
						for spot in row:
							spot.update_neighbours(grid)
					
					Algorithm.a_star(lambda: Grid.draw_path(win, grid, rows, width), grid, start, end, heuristic)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = Grid.make_grid(rows, width)
		ButtonHandler.draw_all_buttons(win)
		pygame.display.update()
	pygame.quit()

WIDTH, ROWS, HEURISTIC = loadParameters()
pygame.display.set_caption('Fire fighters VS fire')
WIN = pygame.display.set_mode((WIDTH, WIDTH))
main(WIN, WIDTH, ROWS, HEURISTIC)