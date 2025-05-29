"""Игрок и управление"""
import math
import pygame
from .math_utils import Vector2, clamp
from .config import *

class Player:
    """Класс игрока"""

    def __init__(self, x=PLAYER_START_X, y=PLAYER_START_Y, angle=0):
        self.position = Vector2(x, y)
        self.angle = angle
        self.speed = PLAYER_SPEED
        self.rotation_speed = ROTATION_SPEED

        # Состояния движения
        self._movement_state = {
            'forward': False,
            'backward': False,
            'left': False,
            'right': False,
            'rotate_left': False,
            'rotate_right': False
        }

    def handle_input(self, keys):
        """Обрабатывает ввод с клавиатуры"""
        self._movement_state['forward'] = keys[pygame.K_w]
        self._movement_state['backward'] = keys[pygame.K_s]
        self._movement_state['left'] = keys[pygame.K_a]
        self._movement_state['right'] = keys[pygame.K_d]
        self._movement_state['rotate_left'] = keys[pygame.K_q]
        self._movement_state['rotate_right'] = keys[pygame.K_e]

    def update(self, world, dt):
        """Обновляет позицию игрока"""
        # Вращение
        if self._movement_state['rotate_left']:
            self.angle -= self.rotation_speed
        if self._movement_state['rotate_right']:
            self.angle += self.rotation_speed

        # Движение
        new_pos = Vector2(self.position.x, self.position.y)

        if self._movement_state['forward']:
            new_pos.x += math.cos(self.angle) * self.speed
            new_pos.y += math.sin(self.angle) * self.speed

        if self._movement_state['backward']:
            new_pos.x -= math.cos(self.angle) * self.speed
            new_pos.y -= math.sin(self.angle) * self.speed

        if self._movement_state['left']:
            new_pos.x += math.cos(self.angle - math.pi/2) * self.speed
            new_pos.y += math.sin(self.angle - math.pi/2) * self.speed

        if self._movement_state['right']:
            new_pos.x += math.cos(self.angle + math.pi/2) * self.speed
            new_pos.y += math.sin(self.angle + math.pi/2) * self.speed

        # Коллизии со стенами
        if not world.is_wall(new_pos.x, self.position.y):
            self.position.x = new_pos.x
        if not world.is_wall(self.position.x, new_pos.y):
            self.position.y = new_pos.y

        # Ограничения по краям экрана
        self.position.x = clamp(self.position.x, 20, SCREEN_WIDTH - 20)
        self.position.y = clamp(self.position.y, 20, SCREEN_HEIGHT - 20)

    def get_direction_vector(self):
        """Возвращает вектор направления взгляда"""
        return Vector2(math.cos(self.angle), math.sin(self.angle))
