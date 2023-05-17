import pygame

class PygameGame:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.balls = [Ball((100, 100)), Ball((200, 200)), Ball((300, 300))]
        self.cart = Cart((self.width/2, self.height/2))

    def update_state(self, objects):
        for ball in self.balls:
            if ball in objects:
                self.balls.remove(ball)
        if not self.balls:
            print('Game over!')

    def render(self):
        self.screen.fill((255, 255, 255))
        for ball in self.balls:
            pygame.draw.circle(self.screen, (255, 0, 0), ball.location, 10)
        pygame.draw.rect(self.screen, (0, 0, 255), (self.cart.location[0]-25, self.cart.location[1]-25, 50, 50))
        pygame.display.flip()
