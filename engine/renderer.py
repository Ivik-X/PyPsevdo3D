import pygame
import math
from .config import *
from .math_utils import clamp

class Renderer:
    """Основной рендерер"""

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 70)

        # Прекомпилированные прямоугольники
        self.sky_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        self.floor_rect = pygame.Rect(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2)

    def clear(self):
        """Очищает экран"""
        pygame.draw.rect(self.screen, SKY_COLOR, self.sky_rect)
        pygame.draw.rect(self.screen, FLOOR_COLOR, self.floor_rect)

    def render_wall_slice(self, x, distance, brightness_factor=1.0):
        """Рендерит вертикальную полосу стены"""
        if distance <= 0:
            return

        # Расчет высоты стены на экране
        wall_height = (WALL_HEIGHT * FOCAL_LENGTH) / max(distance, 0.1)

        # Позиция стены по Y
        wall_top = (SCREEN_HEIGHT - wall_height) // 2
        wall_bottom = wall_top + wall_height

        # Расчет яркости (затухание с расстоянием)
        brightness = max(0, 255 - distance / 3) * brightness_factor
        brightness = clamp(brightness, 0, 255)

        color = (brightness, brightness, brightness)

        pygame.draw.line(self.screen, color, (x, wall_top), (x, wall_bottom), 20)

    def render_fps(self, clock):
        """Отображает FPS"""
        fps = str(int(clock.get_fps()))
        fps_text = self.font.render(fps, True, FPS_COLOR)
        self.screen.blit(fps_text, (SCREEN_WIDTH - 100, 10))

class MinimapRenderer:
    """Рендерер мини-карты"""

    def __init__(self, screen, world):
        self.screen = screen
        self.world = world
        self.scale = MINIMAP_SCALE
        self.cell_size = world.cell_size * self.scale
        self.width = world.width * self.cell_size
        self.height = world.height * self.cell_size

    def render(self, player, raycast_results):
        """Рендерит мини-карту"""
        # Фон мини-карты
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.width, self.height))

        # Стены
        for row_i, row in enumerate(self.world.map):
            for col_i, cell in enumerate(row):
                if cell == 1:
                    x = col_i * self.cell_size
                    y = row_i * self.cell_size
                    rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)

        # Лучи
        for result in raycast_results:
            if result.hit:
                start_x = player.position.x * self.scale
                start_y = player.position.y * self.scale
                end_x = result.point.x * self.scale
                end_y = result.point.y * self.scale
                pygame.draw.line(self.screen, RAY_COLOR,
                               (start_x, start_y), (end_x, end_y), 1)

        # Игрок
        player_x = int(player.position.x * self.scale)
        player_y = int(player.position.y * self.scale)
        pygame.draw.circle(self.screen, PLAYER_COLOR,
                          (player_x, player_y), int(20 * self.scale))

        # Направление взгляда
        dir_vector = player.get_direction_vector()
        end_x = player_x + dir_vector.x * 30 * self.scale
        end_y = player_y + dir_vector.y * 30 * self.scale
        pygame.draw.line(self.screen, DIRECTION_COLOR,
                        (player_x, player_y), (end_x, end_y), int(2 * self.scale))
