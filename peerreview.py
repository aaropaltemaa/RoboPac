import pygame
import random
 
 
class Player:
    def __init__(self, screen_prop: dict) -> None:
        self.robot = screen_prop['robot']
        self.robot_width = self.robot.get_width()
        self.robot_height = self.robot.get_height()
        self.screen_width = screen_prop['width']
        self.screen_height = screen_prop['height']
        self.screen = screen_prop['screen']
        self.x = 0
        self.y = self.screen_height - self.robot_height
        self.position_player()
 
    def reset(self):
        self.x = 0
        self.y = self.screen_height - self.robot_height
        self.position_player()
 
    def position_player(self):
        self.screen.blit(self.robot, (self.x, self.y))
 
    def move_right(self):
        if self.x + self.robot_width <= self.screen_width:
            self.x += 3
 
    def move_left(self):
        if self.x >= 0:
            self.x -= 3
 
    def move(self, event):
        to_left = False
        to_right = False
 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_left = True
            if event.key == pygame.K_RIGHT:
                to_right = True
 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_left = False
            if event.key == pygame.K_RIGHT:
                to_right = False
 
        if to_left:
            self.move_left()
        if to_right:
            self.move_right()
 
 
class Rock:
    def __init__(self, screen_prop) -> None:
        self.rock = screen_prop['rock']
        self.rock_width = self.rock.get_width()
        self.rock_height = self.rock.get_height()
        self.screen_height = screen_prop['height']
        self.screen_width = screen_prop['width']
        self.screen = screen_prop['screen']
        self.has_gotten_point = False
 
        self.x = random.randint(0, self.screen_width - self.rock_width)
        self.y = random.randint(-3000, 0 - self.rock_height)
 
    def position_rock(self):
        self.screen.blit(self.rock, (self.x, self.y))
 
    def move(self):
        self.y += 1
 
 
class RockManager:
    def __init__(self, screen_prop) -> None:
        self.screen_prop = screen_prop
        self.rocks = []
        self.fill_rocks()
 
    def reset(self):
        self.rocks = []
        self.fill_rocks()
 
    def fill_rocks(self):
        for i in range(30):
            self.rocks.append(Rock(self.screen_prop))
 
    def check_if_over(self):
        for rock in self.rocks:
            if not rock.has_gotten_point and rock.y > rock.screen_height - rock.rock_height:
                return True
        return False
 
    def display_rocks(self, player: Player):
        points = 0
 
        for rock in self.rocks:
            if player.x - player.robot_width/2 <= rock.x <= player.x + player.robot_width/2 and player.y - player.robot_height/2 <= rock.y <= player.y + player.robot_height/2:
                points += 1
                rock.y = rock.screen_height + rock.rock_height
                rock.has_gotten_point = True
 
            rock.move()
            rock.position_rock()
 
        return points
 
 
class Application:
    def __init__(self) -> None:
        pygame.init()
 
        self.width = 640
        self.height = 480
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
 
        self.points = 0
 
        self.robot = pygame.image.load('robot.png')
        self.player = Player({
            'screen': self.screen, 
            'width': self.width, 
            'height': self.height,
            'robot': self.robot
            })
        
        self.rock = pygame.image.load('coin.png')
        self.rock_manager = RockManager({
            'screen': self.screen, 
            'width': self.width, 
            'height': self.height,
            'rock': self.rock
        })
 
    def reset(self):
        self.player.reset()
        self.rock_manager.reset()
        self.points = 0
 
    def begin(self):
        while True:
            is_over = self.rock_manager.check_if_over()
            if is_over:
                self.reset()
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.player.move(event)
 
            self.screen.fill((0, 0, 0))
 
            game_font = pygame.font.SysFont("Arial", 24)
            text = game_font.render(f"points: {self.points}", True, (255, 0, 0))
            self.screen.blit(text, (520, 5))
 
            self.player.position_player()
            points = self.rock_manager.display_rocks(self.player)
            self.points += points
 
            pygame.display.flip()
 
            self.clock.tick(60)
 
Application().begin()