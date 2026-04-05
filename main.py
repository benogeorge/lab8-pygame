from __future__ import annotations

import math
import random
from dataclasses import dataclass

import pygame


WIDTH = 960
HEIGHT = 540
FPS = 60
SQUARE_COUNT = 24
BACKGROUND = (18, 18, 24)
TEXT_COLOR = (235, 235, 235)
ACCENT_COLOR = (120, 220, 255)
MIN_SQUARE_SIZE = 18
MAX_SQUARE_SIZE = 72
MIN_SPEED_SCALE = 0.25
MAX_SPEED_SCALE = 4.0
SPEED_STEP = 0.25
MIN_SIZE_SPEED_FACTOR = 1.5
MAX_SIZE_SPEED_FACTOR = 0.55
MIN_TURN_INTERVAL = 8
MAX_TURN_INTERVAL = 26
MAX_TURN_ANGLE = 0.5
MIN_WOBBLE_ANGLE = 0.01
MAX_WOBBLE_ANGLE = 0.11
WOBBLE_CHANCE = 0.22


@dataclass
class Square:
    x: float
    y: float
    vx: float
    vy: float
    size: int
    speed_factor: float
    turn_timer: int
    color: pygame.Color

    def update(self, width: int, height: int, speed_scale: float) -> None:
        if random.random() < WOBBLE_CHANCE:
            wobble_angle = random.uniform(-MAX_WOBBLE_ANGLE, MAX_WOBBLE_ANGLE)
            if abs(wobble_angle) < MIN_WOBBLE_ANGLE:
                wobble_angle = MIN_WOBBLE_ANGLE if wobble_angle >= 0 else -MIN_WOBBLE_ANGLE
            cos_angle = math.cos(wobble_angle)
            sin_angle = math.sin(wobble_angle)
            old_vx = self.vx
            old_vy = self.vy
            self.vx = old_vx * cos_angle - old_vy * sin_angle
            self.vy = old_vx * sin_angle + old_vy * cos_angle

        self.turn_timer -= 1
        if self.turn_timer <= 0:
            angle = random.uniform(-MAX_TURN_ANGLE, MAX_TURN_ANGLE)
            cos_angle = math.cos(angle)
            sin_angle = math.sin(angle)
            old_vx = self.vx
            old_vy = self.vy
            self.vx = old_vx * cos_angle - old_vy * sin_angle
            self.vy = old_vx * sin_angle + old_vy * cos_angle
            self.turn_timer = random.randint(MIN_TURN_INTERVAL, MAX_TURN_INTERVAL)
            self.vx *= random.uniform(0.92, 1.08)
            self.vy *= random.uniform(0.92, 1.08)

        movement_scale = speed_scale * self.speed_factor
        self.x += self.vx * movement_scale
        self.y += self.vy * movement_scale

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
    size = random.randint(MIN_SQUARE_SIZE, MAX_SQUARE_SIZE)
    x = random.randint(0, width - size)
    y = random.randint(0, height - size)
    vx = random.choice([-1, 1]) * random.uniform(1.5, 4.0)
    vy = random.choice([-1, 1]) * random.uniform(1.5, 4.0)
    size_ratio = (size - MIN_SQUARE_SIZE) / (MAX_SQUARE_SIZE - MIN_SQUARE_SIZE)
    speed_factor = MAX_SIZE_SPEED_FACTOR + (1 - size_ratio) * (
        MIN_SIZE_SPEED_FACTOR - MAX_SIZE_SPEED_FACTOR
    )
    color = pygame.Color(
        random.randint(70, 240),
        random.randint(70, 240),
        random.randint(70, 240),
    )
    return Square(
        x=x,
        y=y,
        vx=vx,
        vy=vy,
        size=size,
        speed_factor=speed_factor,
        turn_timer=random.randint(MIN_TURN_INTERVAL, MAX_TURN_INTERVAL),
        color=color,
    )


def create_squares(count: int, width: int, height: int) -> list[Square]:
    return [create_square(width, height) for _ in range(count)]


def draw_overlay(surface: pygame.Surface, font: pygame.font.Font, speed_scale: float) -> None:
    lines = [
        "Lab 8 - Moving Squares",
        f"Squares: {SQUARE_COUNT}",
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
