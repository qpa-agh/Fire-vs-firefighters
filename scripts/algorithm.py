import pygame
import time

class Algorithm:
    """Representation of the algorithm used by programme."""

    def spread(draw, start):
        queue = [start]

        while queue:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            old_queue = queue
            queue = []

            for border_member in old_queue:
                border_member.make_closed()
                for neighbour in border_member.get_neighbours():
                    if neighbour not in old_queue and neighbour not in queue and not neighbour.is_closed() and not neighbour.is_open():
                        queue.append(neighbour)
                        neighbour.make_open()
            draw()
            time.sleep(0.158)
