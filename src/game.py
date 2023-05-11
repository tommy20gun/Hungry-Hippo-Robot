import pygame
import math

class Ball:
    def __init__(self, location):
        self.location = location

class Cart:
    def __init__(self, location):
        self.location = location

    def move(self, target):
        x1, y1 = self.location
        x2, y2 = target
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        speed = 3  # Adjust the speed of the cart
        if distance > speed:
            direction = math.atan2(y2 - y1, x2 - x1)
            dx = speed * math.cos(direction)
            dy = speed * math.sin(direction)
            self.location = (x1 + dx, y1 + dy)
        else:
            self.location = target

class PygameGame:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.balls = [Ball((100, 100)), Ball((200, 200)), Ball((300, 300))]
        self.cart = Cart((self.width/2, self.height/2))

    def update_state(self):
        for ball in self.balls:
            if self.cart.location != ball.location:
                self.cart.move(ball.location)
            else:
                self.balls.remove(ball)
        if not self.balls:
            print('Game over!')

    def render(self):
        self.screen.fill((255, 255, 255))
        for ball in self.balls:
            pygame.draw.circle(self.screen, (255, 0, 0), ball.location, 10)
        pygame.draw.rect(self.screen, (0, 0, 255), (self.cart.location[0]-25, self.cart.location[1]-25, 50, 50))
        pygame.display.flip()

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the Pygame window
    screen = pygame.display.set_mode((640, 480))

    # Initialize the game
    game = PygameGame(screen)

    # Game loop
    running = True
    while running:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the game state
        game.update_state()

        # Render the game to the Pygame window
        game.render()

    # Clean up Pygame
    pygame.quit()

if __name__ == '__main__':
    main()
