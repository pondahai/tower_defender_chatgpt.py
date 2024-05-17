import pygame
import math
import random

# 初始化Pygame
pygame.init()

# 設定遊戲窗口
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("簡單塔防遊戲")

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# FPS
FPS = 60

# 設定敵人
class Enemy:
    def __init__(self, path):
        self.path = path
        self.x, self.y = self.path[0]
        self.health = 100
        self.path_index = 0
        self.move_speed = 1
    
    def move(self):
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            direction = (target_x - self.x, target_y - self.y)
            length = math.hypot(*direction)
            direction = (direction[0] / length, direction[1] / length)
            
            self.x += direction[0] * self.move_speed
            self.y += direction[1] * self.move_speed
            
            if abs(self.x - target_x) < self.move_speed and abs(self.y - target_y) < self.move_speed:
                self.path_index += 1
    
    def draw(self, win):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), 10)
        pygame.draw.rect(win, RED, (self.x - 20, self.y - 20, self.health // 5, 5))

# 設定防禦塔
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.cool_down = 0
        self.shooting_lines = []
    
    def draw(self, win):
        pygame.draw.circle(win, BLACK, (self.x, self.y), 10)
        pygame.draw.circle(win, BLACK, (self.x, self.y), self.range, 1)
        # 繪製射擊軌跡
        for line in self.shooting_lines:
            pygame.draw.line(win, BLUE, (self.x, self.y), line, 2)
    
    def shoot(self, enemies):
        if self.cool_down == 0:
            for enemy in enemies:
                distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
                if distance <= self.range:
                    enemy.health -= 30
                    self.cool_down = 30
                    self.shooting_lines.append((enemy.x, enemy.y))
                    print(f"塔攻擊了敵人！敵人剩餘血量：{enemy.health}")
                    break
        else:
            self.cool_down -= 1
        # 移除過時的射擊線
        if self.cool_down == 29:
            self.shooting_lines = []

def main():
    run = True
    clock = pygame.time.Clock()
    path = [(50, 50), (200, 50), (200, 300), (500, 300), (500, 100), (700, 100)]
    
    # 創建敵人和塔
    enemies = [Enemy(path)]
    towers = [Tower(400, 300)]
    
    enemy_timer = 0

    while run:
        clock.tick(FPS)
        WIN.fill(WHITE)
        
        # 移動和繪製敵人
        for enemy in enemies:
            enemy.move()
            enemy.draw(WIN)
        
        # 繪製防禦塔並執行攻擊
        for tower in towers:
            tower.draw(WIN)
            tower.shoot(enemies)
        
        # 檢查敵人生命值並移除死亡敵人
        enemies = [enemy for enemy in enemies if enemy.health > 0]
        
        # 生成新的敵人
        enemy_timer += 1
        if enemy_timer == 120:
            enemies.append(Enemy(path))
            enemy_timer = 0
        
        pygame.display.update()

        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()
