from queue import PriorityQueue
from heuristics import Heuristics
import pygame

class Algorithm:
    """Representation of the algorithm used by programme."""

    def a_star(draw, grid, start, end, heuristic: str):
        heuristic = Heuristics(heuristic)
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float("inf") for row in grid for spot in row}
        g_score[start] = 0
        f_score = {spot: float("inf") for row in grid for spot in row}
        f_score[start] = heuristic.compute_distance(start, end)

        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current.get_pos() == end.get_pos():
                Algorithm.reconstruct_path(came_from, end, draw)
                end.make_end()
                break

            for neighbor in current.neighbours:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + heuristic.compute_distance(neighbor, end)
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            draw()
            if current != start:
                current.make_closed()
        
    def spread(draw, grid, start, end):
        queue = [start]

        while not queue.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = queue.get()[2]
            open_set_hash.remove(current)

            for neighbor in current.neighbours:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + heuristic.compute_distance(neighbor, end)
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

    def reconstruct_path(came_from, current, draw):
        """Draws the path from start to the end point."""
        while current in came_from:
            current = came_from[current]
            if not current.is_start():
                current.make_path()
                draw()