import pygame

import game

pygame.init()

pygame.display.set_caption("Test")
pygame.display.set_mode((500, 500))

game = game.Game()

while game.is_started():

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game.set_started(False)
            pygame.quit()
