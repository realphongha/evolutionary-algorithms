import numpy as np
import random
from typing import Optional


class SnakePlayer:
    def __init__(self, window_size=(400, 400), board_size=(8, 8), fps=5):
        import pygame

        self.pygame = pygame
        self.pygame.init()
        self.window_w, self.window_h = window_size
        self.board_w, self.board_h = board_size
        assert (self.window_w % self.board_w == 0)
        assert (self.window_h % self.board_h == 0)
        self.block_w = self.window_w // self.board_w
        self.block_h = self.window_h // self.board_h
        self.window_size = window_size
        self.pygame.display.set_caption("Snake game. Press 'Q' to quit")
        self.screen = self.pygame.display.set_mode(window_size)
        self.background_color = (0, 0, 0)
        self.line_color = (211, 211, 211)
        self.snake_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.snake_color = random.choice(self.snake_colors)
        self.food_color = (255, 255, 255)
        self.font = self.pygame.font.Font(None, 25)
        self.font_color = (255, 255, 255)
        self.fps = fps
        self.clock = self.pygame.time.Clock()

    def change_snake_color(self):
        new_color = random.choice(self.snake_colors)
        while new_color == self.snake_color:
            new_color = random.choice(self.snake_colors)
        self.snake_color = new_color

    def draw_board(self):
        # fills background
        self.screen.fill(self.background_color)

    def draw_snake_and_food(self, snake, food):
        # draws snake
        for w, h in snake:
            self.pygame.draw.rect(self.screen, self.snake_color, 
                self.pygame.Rect(w * self.block_w, h * self.block_h,
                                 self.block_w, self.block_h))
        # draws food
        w, h = food
        self.pygame.draw.rect(self.screen, self.food_color, 
            self.pygame.Rect(w * self.block_w, h * self.block_h,
                             self.block_w, self.block_h))

    def game_over_screen(self):
        while True:
            # captures events
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    # quits game
                    print("Quit")
                    return "quit"
                elif event.type == self.pygame.KEYDOWN:
                    if event.key == self.pygame.K_r:
                        return "restart"
                    elif event.key == self.pygame.K_q:
                        # quits game
                        print("Quit")
                        return "quit"

            # draws board
            self.draw_board()

            # draws text
            text = self.font.render("Game over! Press 'R' to restart!",
                True, self.font_color)
            text_rect = text.get_rect(
                center=(self.window_w//2, self.window_h//2))
            self.screen.blit(text, text_rect)

            # updates screen
            self.pygame.display.update()
            self.clock.tick(self.fps)
            

class SnakeGame:
    def __init__(self, board_size=(8, 8), patience=20):
        self.w, self.h = board_size
        assert self.w >= 8, "board width should larger than 8"
        assert self.h >= 8, "board height should larger than 8"
        self.board = np.zeros((self.h, self.w), dtype=np.ubyte)
        self.patience = patience
        assert self.patience >= self.w + self.h, \
            f"patience should be large than {self.w + self.h}"
        self.init_new_game()

    def init_new_game(self):
        self.patience_now = self.patience
        self.snake = [(self.w//2-2, self.h//2), 
                      (self.w//2-1, self.h//2), 
                      (self.w//2, self.h//2)]
        self.velocity = (1, 0)
        self.food = None
        self.spawn_food()

    def spawn_food(self):
        self.food = (np.random.randint(0, self.w), 
                     np.random.randint(0, self.h))
        while self.food in self.snake:
            self.food = (np.random.randint(0, self.w), 
                         np.random.randint(0, self.h))

    def loop(self, player: Optional[SnakePlayer]=None):
        while True:
            if player:
                # captures events
                for event in player.pygame.event.get():
                    if event.type == player.pygame.QUIT:
                        # quits game
                        break
                    elif event.type == player.pygame.KEYDOWN:
                        if event.key == player.pygame.K_LEFT:
                            if self.velocity[0] != 1:
                                self.velocity = (-1, 0) 
                        elif event.key == player.pygame.K_RIGHT:
                            if self.velocity[0] != -1:
                                self.velocity = (1, 0) 
                        elif event.key == player.pygame.K_UP:
                            if self.velocity[1] != 1:
                                self.velocity = (0, -1) 
                        elif event.key == player.pygame.K_DOWN:
                            if self.velocity[1] != -1:
                                self.velocity = (0, 1) 
                        elif event.key == player.pygame.K_q:
                            # quits game
                            break
            # game logic:
            head = self.snake[-1]
            new_head = (head[0] + self.velocity[0], head[1] + self.velocity[1])
            if new_head[0] < 0 or new_head[0] >= self.w or \
                new_head[1] < 0 or new_head[1] >= self.h:
                # game over: go outside of screen
                break
            elif new_head in self.snake:
                # game over: eat yourself
                break
            elif new_head == self.food:
                self.snake.append(new_head)
                if len(self.snake) == self.w * self.h:
                    # win!!!
                    break
                if player:
                    player.change_snake_color()
                self.spawn_food()
            else:
                self.snake = self.snake[1:]
                self.snake.append(new_head) 
            if player:
                # draws
                player.draw_board()
                player.draw_snake_and_food(self.snake, self.food)
                # updates screen
                player.pygame.display.update()
                player.clock.tick(player.fps)
        
        # game over
        if player:
            print("Game over!")
            command = player.game_over_screen()
            if command == "restart":
                print("Restart")
                self.init_new_game()
                self.loop(player)



if __name__ == "__main__":
    snake_game = SnakeGame()
    snake_player = SnakePlayer(fps=3)
    snake_game.loop(player=snake_player)
