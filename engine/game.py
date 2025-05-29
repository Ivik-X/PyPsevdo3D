"""Основной класс игры"""
import pygame
import math
from .config import *
from .world import World
from .player import Player
from .raycaster import Raycaster
from .renderer import Renderer, MinimapRenderer

class Game:
    """Основной класс игры"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("3D Raycasting Engine")
        self.clock = pygame.time.Clock()
        self.running = True

        # Инициализация компонентов
        self.world = World()
        self.player = Player()
        self.raycaster = Raycaster(self.world)
        self.renderer = Renderer(self.screen)
        self.minimap_renderer = MinimapRenderer(self.screen, self.world)

        # Кэш для результатов рейкастинга
        self._raycast_cache = []

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # Обработка нажатых клавиш
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

    def update(self, dt):
        """Обновление логики игры"""
        self.player.update(self.world, dt)
        self._update_raycast_cache()

    def _update_raycast_cache(self):
        """Обновляет кэш результатов рейкастинга"""
        self._raycast_cache.clear()

        # Корректировка FOV для четности
        fov = FOV if FOV % 2 == 0 else FOV - 1

        for i in range(fov):
            # Вычисление угла луча
            angle_offset = math.radians(i - fov // 2)
            ray_angle = self.player.angle + angle_offset

            # Рейкастинг
            result = self.raycaster.cast_ray(self.player.position, ray_angle)
            self._raycast_cache.append(result)

    def render(self):
        """Рендеринг кадра"""
        self.renderer.clear()

        # Рендер 3D вида
        fov = FOV if FOV % 2 == 0 else FOV - 1
        slice_width = SCREEN_WIDTH / fov

        for i, result in enumerate(self._raycast_cache):
            if result.hit:
                x = int(i * slice_width + slice_width // 2)
                self.renderer.render_wall_slice(x, result.distance)

        # Рендер мини-карты
        self.minimap_renderer.render(self.player, self._raycast_cache)

        # Рендер FPS
        self.renderer.render_fps(self.clock)

        pygame.display.flip()

    def run(self):
        """Основной игровой цикл"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Время в секундах

            self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()
