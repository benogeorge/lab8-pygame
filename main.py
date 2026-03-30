from __future__ import annotations

import random
from dataclasses import dataclass

import pygame


WIDTH = 960
HEIGHT = 540
FPS = 60
SQUARE_COUNT = 10
BACKGROUND = (18, 18, 24)
TEXT_COLOR = (235, 235, 235)
ACCENT_COLOR = (120, 220, 255)
MIN_SPEED_SCALE = 0.25
MAX_SPEED_SCALE = 4.0
SPEED_STEP = 0.25


@dataclass
class Square:
    x: float
    y: float
    vx: float
    vy: float
    size: int
    color: pygame.Color

    def update(self, width: int, height: int, speed_scale: float) -> None:
        self.x += self.vx * speed_scale
        self.y += self.vy * speed_scale

        if self.x <= 0:
            self.x = 0
            self.vx *= -1
        elif self.x + self.size >= width:
            self.x = width - self.size
            self.vx *= -1

        if self.y <= 0:
            self.y = 0
            self.vy *= -1
        elif self.y + self.size >= height:
            self.y = height - self.size
            self.vy *= -1

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(int(self.x), int(self.y), self.size, self.size),
        )


def create_square(width: int, height: int) -> Square:
    size = random.randint(24, 54)
    x = random.randint(0, width - size)
    y = random.randint(0, height - size)
    vx = random.choice([-1, 1]) * random.uniform(1.5, 4.0)
    vy = random.choice([-1, 1]) * random.uniform(1.5, 4.0)
    color = pygame.Color(
        random.randint(70, 240),
        random.randint(70, 240),
        random.randint(70, 240),
    )
    return Square(x=x, y=y, vx=vx, vy=vy, size=size, color=color)


def create_squares(count: int, width: int, height: int) -> list[Square]:
    return [create_square(width, height) for _ in range(count)]


def draw_overlay(surface: pygame.Surface, font: pygame.font.Font, speed_scale: float) -> None:
    lines = [
        "Lab 8 - Moving Squares",
        f"Speed: {speed_scale:.2f}x",
        "Up/Down or +/- change speed, R randomizes all squares, Q/Esc quit",
    ]

    x = 18
    y = 14
    for index, line in enumerate(lines):
        color = ACCENT_COLOR if index == 0 else TEXT_COLOR
        text = font.render(line, True, color)
        surface.blit(text, (x, y))
        y += text.get_height() + 4


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lab 8 - Moving Squares")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    squares = create_squares(SQUARE_COUNT, WIDTH, HEIGHT)
    speed_scale = 1.0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_UP, pygame.K_EQUALS, pygame.K_PLUS):
                speed_scale = min(MAX_SPEED_SCALE, speed_scale + SPEED_STEP)
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_DOWN, pygame.K_MINUS, pygame.K_KP_MINUS):
                speed_scale = max(MIN_SPEED_SCALE, speed_scale - SPEED_STEP)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                squares = create_squares(SQUARE_COUNT, WIDTH, HEIGHT)
                speed_scale = 1.0

        for square in squares:
            square.update(WIDTH, HEIGHT, speed_scale)

        screen.fill(BACKGROUND)
        for square in squares:
            square.draw(screen)
        draw_overlay(screen, font, speed_scale)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
