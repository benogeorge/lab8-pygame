from __future__ import annotations

import random
from dataclasses import dataclass

import pygame


WIDTH = 960
HEIGHT = 540
FPS = 60
SQUARE_COUNT = 10
BACKGROUND = (18, 18, 24)


@dataclass
class Square:
    x: float
    y: float
    vx: float
    vy: float
    size: int
    color: pygame.Color

    def update(self, width: int, height: int) -> None:
        self.x += self.vx
        self.y += self.vy

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


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lab 8 - Moving Squares")
    clock = pygame.time.Clock()
    squares = create_squares(SQUARE_COUNT, WIDTH, HEIGHT)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False

        for square in squares:
            square.update(WIDTH, HEIGHT)

        screen.fill(BACKGROUND)
        for square in squares:
            square.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
