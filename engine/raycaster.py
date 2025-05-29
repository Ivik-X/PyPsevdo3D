"""Система рейкастинга"""
import math
from .math_utils import Vector2
from .config import MAX_RENDER_DISTANCE

class RaycastResult:
    """Результат рейкастинга"""
    def __init__(self, hit=False, distance=0, point=None, side=0):
        self.hit = hit
        self.distance = distance
        self.point = point if point else Vector2()
        self.side = side  # 0 = x-side, 1 = y-side

class Raycaster:
    """Система рейкастинга"""

    def __init__(self, world):
        self.world = world

    def cast_ray(self, start_pos, angle):
        """Выпускает луч и возвращает результат столкновения"""
        ray_dir = Vector2(math.cos(angle), math.sin(angle))

        # Инициализация переменных DDA алгоритма
        map_pos = Vector2(int(start_pos.x // self.world.cell_size),
                         int(start_pos.y // self.world.cell_size))

        # Расчет delta расстояний
        delta_dist_x = abs(1 / ray_dir.x) if ray_dir.x != 0 else float('inf')
        delta_dist_y = abs(1 / ray_dir.y) if ray_dir.y != 0 else float('inf')

        # Расчет шага и начального side_dist
        if ray_dir.x < 0:
            step_x = -1
            side_dist_x = (start_pos.x / self.world.cell_size - map_pos.x) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_pos.x + 1.0 - start_pos.x / self.world.cell_size) * delta_dist_x

        if ray_dir.y < 0:
            step_y = -1
            side_dist_y = (start_pos.y / self.world.cell_size - map_pos.y) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_pos.y + 1.0 - start_pos.y / self.world.cell_size) * delta_dist_y

        # DDA алгоритм
        hit = False
        side = 0

        while not hit:
            # Переход к следующей стороне карты
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_pos.x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_pos.y += step_y
                side = 1

            # Проверка столкновения
            if self.world.get_cell(int(map_pos.x), int(map_pos.y)) == 1:
                hit = True

        # Расчет расстояния
        if side == 0:
            distance = (map_pos.x - start_pos.x / self.world.cell_size + (1 - step_x) / 2) / ray_dir.x
        else:
            distance = (map_pos.y - start_pos.y / self.world.cell_size + (1 - step_y) / 2) / ray_dir.y

        distance = abs(distance * self.world.cell_size)

        # Точка попадания
        hit_point = Vector2(
            start_pos.x + ray_dir.x * distance,
            start_pos.y + ray_dir.y * distance
        )

        return RaycastResult(hit, distance, hit_point, side)
