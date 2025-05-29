import pygame
import sys
from engine.game import Game

def main():
    """Точка входа в приложение"""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Ошибка запуска игры: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
