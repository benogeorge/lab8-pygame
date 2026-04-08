from __future__ import annotations

import math
import random
from dataclasses import dataclass

import pygame


WIDTH = 1500
HEIGHT = 800
FPS = 60
SQUARE_COUNT = 20
BACKGROUND = (18, 18, 24)
TEXT_COLOR = (235, 235, 235)
ACCENT_COLOR = (120, 220, 255)
SHADOW_COLOR = (6, 6, 10)
TRAIL_COLOR = (150, 215, 255)
SMALL_SQUARE_SIZE = 10
BIG_SQUARE_SIZE = 40
BIGGER_SQUARE_COUNT = 5
MIN_SPEED_SCALE = 0.25
MAX_SPEED_SCALE = 4.0
SPEED_STEP = 0.25
SMALL_SPEED_FACTOR = 1.24
BIG_SPEED_FACTOR = 0.62
BASE_CRUISE_SPEED = 2.0
FLEE_RADIUS = 150
STEER_STRENGTH = 0.2
MAX_STEER_SPEED = 4.6
STEER_DAMPING = 0.988
COLLISION_BOUNCE = 0.92
SHADOW_OFFSET = 4
LOOKAHEAD_FRAMES = 10
SIDE_STEER_WEIGHT = 0.96
AWAY_STEER_WEIGHT = 0.16


@dataclass
class Square:
    x: float
    y: float
    vx: float
    vy: float
    size: int
    speed_factor: float
    color: pygame.Color

    def apply_flee(self, others: list["Square"]) -> None:
        if self.size == BIG_SQUARE_SIZE:
            return

        center_x = self.x + self.size / 2
        center_y = self.y + self.size / 2
        threats: list[tuple[float, float, float]] = []
        self_speed = math.hypot(self.vx, self.vy)
        if self_speed > 0.01:
            forward_x = self.vx / self_speed
            forward_y = self.vy / self_speed
        else:
            forward_x = 1.0
            forward_y = 0.0

        for other in others:
            if other is self or other.size <= self.size:
                continue

            predicted_other_x = (
                other.x
                + other.size / 2
                + other.vx * other.speed_factor * LOOKAHEAD_FRAMES
            )
            predicted_other_y = (
                other.y
                + other.size / 2
                + other.vy * other.speed_factor * LOOKAHEAD_FRAMES
            )
            dx = center_x - predicted_other_x
            dy = center_y - predicted_other_y
            distance = math.hypot(dx, dy)

            if distance == 0 or distance > FLEE_RADIUS:
                continue

            influence = (FLEE_RADIUS - distance) / FLEE_RADIUS
            size_bias = 1 + (other.size - self.size) / BIG_SQUARE_SIZE
            away_x = dx / distance
            away_y = dy / distance
            side_a_x = -away_y
            side_a_y = away_x
            side_b_x = away_y
            side_b_y = -away_x
            if forward_x * side_a_x + forward_y * side_a_y >= forward_x * side_b_x + forward_y * side_b_y:
                side_x = side_a_x
                side_y = side_a_y
            else:
                side_x = side_b_x
                side_y = side_b_y
            threats.append(
                (
                    distance,
                    (side_x * SIDE_STEER_WEIGHT + away_x * AWAY_STEER_WEIGHT) * influence * size_bias,
                    (side_y * SIDE_STEER_WEIGHT + away_y * AWAY_STEER_WEIGHT) * influence * size_bias,
                )
            )

        if not threats:
            return

        threats.sort(key=lambda item: item[0])
        steer_x = 0.0
        steer_y = 0.0
        weight_total = 0.0
        for index, (distance, away_x, away_y) in enumerate(threats[:2]):
            weight = 1.0 if index == 0 else 0.45
            closeness = 1 - distance / FLEE_RADIUS
            steer_x += away_x * weight * closeness
            steer_y += away_y * weight * closeness
            weight_total += weight

        if weight_total > 0:
            steer_x /= weight_total
            steer_y /= weight_total

        accel = math.hypot(steer_x, steer_y)
        if accel > STEER_STRENGTH:
            scale = STEER_STRENGTH / accel
            steer_x *= scale
            steer_y *= scale
        self.vx += steer_x
        self.vy += steer_y

        speed = math.hypot(self.vx, self.vy)
        max_speed = MAX_STEER_SPEED * self.speed_factor
        if speed > max_speed:
            scale = max_speed / speed
            self.vx *= scale
            self.vy *= scale

    def recover_cruise_velocity(self) -> None:
        speed = math.hypot(self.vx, self.vy)
        target_speed = BASE_CRUISE_SPEED * self.speed_factor

        if speed < 0.01:
            angle = random.uniform(0, math.tau)
            self.vx = math.cos(angle) * target_speed
            self.vy = math.sin(angle) * target_speed
            return

        if speed < target_speed:
            blend = 0.18
            scale = (speed * (1 - blend) + target_speed * blend) / speed
            self.vx *= scale
            self.vy *= scale

    def update(self, width: int, height: int, speed_scale: float, squares: list["Square"]) -> None:
        self.apply_flee(squares)
        movement_scale = speed_scale
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
        self.vx *= STEER_DAMPING
        self.vy *= STEER_DAMPING
        self.recover_cruise_velocity()

    def draw(self, surface: pygame.Surface) -> None:
        center_x = self.x + self.size / 2
        center_y = self.y + self.size / 2
        speed = math.hypot(self.vx, self.vy)
        if speed > 0.01:
            trail_length = self.size * 0.55
            trail_end = (
                int(center_x - (self.vx / speed) * trail_length),
                int(center_y - (self.vy / speed) * trail_length),
            )
            pygame.draw.line(
                surface,
                TRAIL_COLOR,
                (int(center_x), int(center_y)),
                trail_end,
                width=2,
            )

        shadow_rect = pygame.Rect(
            int(self.x) + SHADOW_OFFSET,
            int(self.y) + SHADOW_OFFSET,
            self.size,
            self.size,
        )
        pygame.draw.rect(surface, SHADOW_COLOR, shadow_rect)

        rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)
        pygame.draw.rect(
            surface,
            self.color,
            rect,
        )
        highlight = tuple(min(255, channel + 28) for channel in self.color[:3])
        pygame.draw.rect(surface, highlight, rect, width=2)


def create_square(width: int, height: int, size: int) -> Square:
    x = random.randint(0, width - size)
    y = random.randint(0, height - size)
    angle = random.uniform(0, math.tau)
    speed_factor = SMALL_SPEED_FACTOR if size == SMALL_SQUARE_SIZE else BIG_SPEED_FACTOR
    base_speed = BASE_CRUISE_SPEED * speed_factor
    vx = math.cos(angle) * base_speed
    vy = math.sin(angle) * base_speed
    color = pygame.Color(
        110 if size == BIG_SQUARE_SIZE else 170,
        190 if size == BIG_SQUARE_SIZE else 235,
        220 if size == BIG_SQUARE_SIZE else 120,
    )
    return Square(
        x=x,
        y=y,
        vx=vx,
        vy=vy,
        size=size,
        speed_factor=speed_factor,
        color=color,
    )


def create_squares(count: int, width: int, height: int) -> list[Square]:
    squares: list[Square] = []
    big_count = min(BIGGER_SQUARE_COUNT, count)
    small_count = count - big_count

    for _ in range(big_count):
        squares.append(create_square(width, height, BIG_SQUARE_SIZE))
    for _ in range(small_count):
        squares.append(create_square(width, height, SMALL_SQUARE_SIZE))

    return squares


def resolve_collisions(squares: list[Square]) -> None:
    total = len(squares)
    for i in range(total):
        a = squares[i]
        for j in range(i + 1, total):
            b = squares[j]
            overlap_x = min(a.x + a.size, b.x + b.size) - max(a.x, b.x)
            overlap_y = min(a.y + a.size, b.y + b.size) - max(a.y, b.y)

            if overlap_x <= 0 or overlap_y <= 0:
                continue

            center_ax = a.x + a.size / 2
            center_ay = a.y + a.size / 2
            center_bx = b.x + b.size / 2
            center_by = b.y + b.size / 2

            if overlap_x < overlap_y:
                push = overlap_x / 2
                if center_ax < center_bx:
                    a.x -= push
                    b.x += push
                else:
                    a.x += push
                    b.x -= push

                old_a_vx = a.vx
                a.vx = b.vx * COLLISION_BOUNCE
                b.vx = old_a_vx * COLLISION_BOUNCE
            else:
                push = overlap_y / 2
                if center_ay < center_by:
                    a.y -= push
                    b.y += push
                else:
                    a.y += push
                    b.y -= push

                old_a_vy = a.vy
                a.vy = b.vy * COLLISION_BOUNCE
                b.vy = old_a_vy * COLLISION_BOUNCE


def draw_overlay(surface: pygame.Surface, font: pygame.font.Font, speed_scale: float) -> None:
    small_count = SQUARE_COUNT - BIGGER_SQUARE_COUNT
    lines = [
        "Lab 8 ",
        f"Squares: {small_count} small, {BIGGER_SQUARE_COUNT} big",
        f"Speed: {speed_scale:.2f}x",
        "Small squares steer away from big squares, Up/Down or +/- change speed, R resets, Q/Esc quit",
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
    pygame.display.set_caption("Lab 8 - Fleeing Squares")
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
            square.update(WIDTH, HEIGHT, speed_scale, squares)
        resolve_collisions(squares)

        screen.fill(BACKGROUND)
        for square in squares:
            square.draw(screen)
        draw_overlay(screen, font, speed_scale)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
