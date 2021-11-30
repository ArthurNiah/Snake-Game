import pygame
import time
import random 
import time

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("blue.png")
        self.x = random.randrange(0, 600, 30)
        self.y = random.randrange(0, 600, 30)

    def input_apple(self):
        self.parent_screen.blit(pygame.transform.scale(self.apple, (30, 30)), (self.x, self.y))
        pygame.display.update()

    def move(self):
        self.x = random.randrange(0, 600, 30)
        self.y = random.randrange(0, 600, 30)
        self.parent_screen.blit(pygame.transform.scale(self.apple, (30, 30)), (self.x, self.y))


    
        pygame.display.flip()

    def apple_x(self):
        return self.x

    def apple_y(self):
        return self.y


class Snake:
    def __init__(self, parent_screen,length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("white.jpeg")
        self.x = [30]*self.length
        self.y = [30]*self.length 
        self.direction = 'down'

    def draw(self):
        self.parent_screen.fill((0,0,0))
        for i in range(self.length):
            self.parent_screen.blit(pygame.transform.scale(self.block, (30, 30)), (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = "left"
        
    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def get_direction(self):
        return self.direction

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= 30
        if self.direction == 'right':
            self.x[0] += 30
        if self.direction == 'up':
            self.y[0] -= 30
        if self.direction == 'down':
            self.y[0] += 30

        self.draw()

    def snake_x(self):
        return self.x[0]

    def snake_y(self):
        return self.y[0]

    def is_collision(self, x1, y1, x2, y2):
        if x2 >= x1 and x2 < x1 + 30:
            if y2 >= y1 and y2 < y1 + 30:
                return True

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def hit_ends(self):
        if self.x[0] < 0 or self.x[0] > 600:
            return True

        if self.y[0] < 0 or self.y[0] > 600:
            return True
        
        return False

    def game_over(self):
        if self.hit_ends():
            return True


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((600, 600))
        self.surface.fill((0,0,0))
        pygame.display.set_caption("Snake")
        self.snake = Snake(self.surface,2)
        self.apple = Apple(self.surface)
        self.snake.draw()

    def play(self):
        self.snake.walk()
        self.apple.input_apple()
        self.display_score()
        pygame.display.flip()

        if self.snake.is_collision(self.apple.x, self.apple.y, self.snake.x[0], self.snake.y[0]):
            self.snake.increase_length()
            self.apple.move()


        for i in range(1, self.snake.length):
            if self.snake.is_collision(self.snake.x[i], self.snake.y[i], self.snake.x[0], self.snake.y[0]):
                raise "Game Over"

        if self.snake.game_over():
                raise "Game Over"


    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length - 2}", True, (255, 255, 255))
        self.surface.blit(score, (450,30))

    def show_game_over(self):
        self.surface.fill((0,0,0))
        font = pygame.font.SysFont('arial', 30)
        game_over_text = font.render(f"Game Over! Final Score: {self.snake.length-2}", True, (255,255,255))
        self.surface.blit(game_over_text, (110,240))
        restart_text =  font.render("Press Enter to play again or ESC to quit!", True, (255,255,255))
        self.surface.blit(restart_text, (30,330))
        pygame.display.flip()

    def run(self,run = True, pause = False):

        while run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

                    if event.key == pygame.K_RETURN and pause == True:
                        pause = False
                        self.snake = Snake(self.surface,2)
                        self.play()

                    if event.key == pygame.K_UP and self.snake.get_direction() != "down":
                        self.snake.move_up()

                    if event.key == pygame.K_DOWN and self.snake.get_direction() != "up":
                        self.snake.move_down()

                    if event.key == pygame.K_LEFT and self.snake.get_direction() != "right":
                        self.snake.move_left()

                    if event.key == pygame.K_RIGHT and self.snake.get_direction() != "left":
                        self.snake.move_right()

                elif event.type == pygame.QUIT:
                    run = False


            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True


            time.sleep(0.15)


if __name__ == "__main__":

    game = Game()
    game.run()