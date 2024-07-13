import pygame
import random

class RoboPac:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Robo-Pac")
        self.window = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.robot_width = 0
        self.robot_height = 0
        self.coin_width = 0
        self.coin_height = 0
        self.coin_counter = 0
        self.hp = 10
        self.monster_width = 0
        self.monster_height = 0
        self.max_monsters = 5 
        self.spawn_chance = 1  
        self.base_spawn_chance = 1  
        self.monster_spawn_delay = 2000  
        self.last_spawn_time = pygame.time.get_ticks()
        self.coins = []
        self.monsters = []
        self.images = {}
        self.robot_position = None
        self.coin_position = None
        self.door_position = None
        self.to_right = False
        self.to_left = False
        self.to_up = False
        self.to_down = False
        self.game_over = False
        self.monster_timer = 0
        self.load_images()
        self.spawn_monsters()
        self.spawn_coins()
        
    def load_images(self):
        for name in ["coin", "door", "monster", "robot"]:
            self.images[name] = pygame.image.load(name + ".png")
    
        self.robot_width = self.images["robot"].get_width()
        self.robot_height = self.images["robot"].get_height()
        self.coin_width = self.images["coin"].get_width()
        self.coin_height = self.images["coin"].get_height()
        self.monster_width = self.images["monster"].get_width()
        self.monster_height = self.images["monster"].get_height()
        self.door_width = self.images["door"].get_width()
        self.door_height = self.images["door"].get_height()
        self.robot_position = ((640 - self.robot_width) // 2, (480 - self.robot_height) // 2)
        self.coin_position = ((640 - self.coin_width) // 2, (480 - self.coin_height) // 2)
        self.door_position = ((640 - self.door_width) // 2, (480 - self.door_height) // 2)

    def spawn_monsters(self):
        if len(self.monsters) < self.max_monsters:
            spawn_chance = self.spawn_chance
            if len(self.monsters) >= 3:
                spawn_chance *= 2 

            if random.randint(0, 100) < spawn_chance:
                spawn_side = random.randint(0, 3)
                if spawn_side == 0:  
                    x = random.randint(0, 640 - self.monster_width)
                    y = -self.monster_height
                elif spawn_side == 1: 
                    x = random.randint(0, 640 - self.monster_width)
                    y = 480
                elif spawn_side == 2:  
                    x = -self.monster_width
                    y = random.randint(0, 480 - self.monster_height)
                else:  
                    x = 640
                    y = random.randint(0, 480 - self.monster_height)

                self.monsters.append((x, y))

            self.spawn_chance = self.base_spawn_chance

    def spawn_coins(self):
        self.coins = [(random.randint(0, 640 - self.coin_width), random.randint(0, 480 - self.coin_height)) for _ in range(20)]

    def chase_robot(self):
        for idx, monster_pos in enumerate(self.monsters):
            monster_x, monster_y = monster_pos
            robot_x, robot_y = self.robot_position
            dx = robot_x - monster_x
            dy = robot_y - monster_y
            dx += random.uniform(-0.5, 0.5)
            dy += random.uniform(-0.5, 0.5)
            length = (dx ** 2 + dy ** 2) ** 0.5
            if length != 0:
                dx /= length
                dy /= length
            speed = 1
            monster_x += speed * dx
            monster_y += speed * dy
            self.monsters[idx] = (monster_x, monster_y)

    def respawn_coin(self):
        return random.randint(0, 640 - self.coin_width), random.randint(0, 480 - self.coin_height)

    def check_collision(self):
        robot_rect = pygame.Rect(self.robot_position, (self.robot_width, self.robot_height))
        door_rect = pygame.Rect(self.door_position, (self.door_width, self.door_height))

        for idx, monster_pos in enumerate(self.monsters):
            monster_rect = pygame.Rect(monster_pos, (self.monster_width, self.monster_height))
            if robot_rect.colliderect(monster_rect) and self.hp > 0:
                self.hp -= 1
                self.robot_position = (random.randint(0, 640 - self.robot_width), random.randint(0, 480 - self.robot_height))
                break

        for idx, coin_pos in enumerate(self.coins):
            coin_rect = pygame.Rect(coin_pos, (self.coin_width, self.coin_height))
            if robot_rect.colliderect(coin_rect):
                self.coin_counter += 1
                self.coins[idx] = self.respawn_coin()
                break

    def check_coin_counter(self):  
        if self.coin_counter == 500:
            self.door_position = (random.randint(0, 640 - self.door_width), random.randint(0, 480 - self.door_height))
            self.coin_counter = 0
                

    def main_loop(self):
        while True:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_spawn_time > self.monster_spawn_delay:
                self.last_spawn_time = current_time
            while not self.game_over:
                self.check_events()
                self.move_robot()
                self.spawn_monsters()
                self.chase_robot()
                self.check_collision()
                self.check_coin_counter()  
                self.draw_window()
                self.clock.tick(30) 
                if self.hp == 0:
                    self.game_over = True
                    break
            self.game_over_screen()


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: 
                    self.to_left = True
                if event.key == pygame.K_d: 
                    self.to_right = True
                if event.key == pygame.K_w:  
                    self.to_up = True
                if event.key == pygame.K_s:  
                    self.to_down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:  
                    self.to_left = False
                if event.key == pygame.K_d:  
                    self.to_right = False
                if event.key == pygame.K_w: 
                    self.to_up = False
                if event.key == pygame.K_s:  
                    self.to_down = False

            if event.type == pygame.QUIT:
                exit()

    def move_robot(self):
        x, y = self.robot_position 

        if self.to_right:
            x += 15
        if self.to_left:
            x -= 15
        if self.to_up:
            y -= 15
        if self.to_down:
            y += 15

        if x < 0:
            x = 0
        elif x > 640 - self.robot_width:
            x = 640 - self.robot_width
        if y < 0:
            y = 0
        elif y > 480 - self.robot_height:
            y = 480 - self.robot_height

        self.robot_position = (x, y)

    def draw_window(self):
        self.window.fill((255, 255, 255))

        for name, pos_list in [("coin", self.coins), ("monster", self.monsters)]:
            for pos in pos_list:
                self.window.blit(self.images[name], pos)

        self.window.blit(self.images["robot"], self.robot_position)
        game_font = pygame.font.SysFont("Comic Sans MS", 28)
        coin_text = game_font.render(f"Coins: {self.coin_counter}", True, (255, 0, 0))
        next_level_text = game_font.render("300 coins = next level", True, (0, 255, 0))
        commands_text = game_font.render("WASD to move", True, (255, 0, 0))
        hp_text = game_font.render(f"HP: {self.hp}", True, (255, 0, 0))
        self.window.blit(coin_text, (500, 10))
        self.window.blit(next_level_text, (10, 10))
        self.window.blit(hp_text, (350, 10))
        self.window.blit(commands_text, (0, 430))

        pygame.display.flip()

    def game_over_screen(self):
        game_over_font = pygame.font.SysFont("Arial", 36)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        self.window.blit(game_over_text, (200, 200))
        pygame.display.flip()

        pygame.time.wait(2000)
        pygame.quit()

if __name__ == "__main__":
    game = RoboPac()
    game.main_loop()