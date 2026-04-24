import math
import random

import pygame


WIDTH = 1200
HEIGHT = 700
FPS = 60

SQUARE_COUNT = 20
MIN_SIZE = 12
MAX_SIZE = 42
MIN_SPEED = 1.8
MAX_SPEED = 3.2
FLEE_RADIUS = 190
CHASE_RADIUS = 280
WANDER = 0.22
CORNER_MARGIN = 22
MIN_MOTION_RATIO = 0.35

BG = (20, 20, 28)
TEXT = (235, 235, 235)


def speed_for_size(size: int) -> float:
    size_range = MAX_SIZE - MIN_SIZE
    if size_range == 0:
        return MIN_SPEED
    size_ratio = (size - MIN_SIZE) / size_range
    return MAX_SPEED - size_ratio * (MAX_SPEED - MIN_SPEED)


def color_for_size(size: int) -> tuple[int, int, int]:
    size_range = MAX_SIZE - MIN_SIZE
    if size_range == 0:
        ratio = 0.5
    else:
        ratio = (size - MIN_SIZE) / size_range
    red = int(90 + 20 * ratio)
    green = int(230 - 90 * ratio)
    blue = int(120 + 135 * ratio)
    return (red, green, blue)


def new_square() -> dict:
    size = random.randint(MIN_SIZE, MAX_SIZE)
    speed = speed_for_size(size)
    a = random.uniform(0, math.tau)
    return {
        "x": random.randint(0, WIDTH - size),
        "y": random.randint(0, HEIGHT - size),
        "vx": math.cos(a) * speed,
        "vy": math.sin(a) * speed,
        "size": size,
    }


def overlaps(a: dict, b: dict) -> bool:
    return (
        a["x"] < b["x"] + b["size"]
        and a["x"] + a["size"] > b["x"]
        and a["y"] < b["y"] + b["size"]
        and a["y"] + a["size"] > b["y"]
    )


def make_squares() -> list[dict]:
    squares = []
    for _ in range(SQUARE_COUNT):
        placed = False
        for _ in range(150):
            s = new_square()
            if all(not overlaps(s, other) for other in squares):
                squares.append(s)
                placed = True
                break
        if not placed:
            squares.append(new_square())
    return squares


def move_toward(s: dict, tx: float, ty: float, amount: float) -> None:
    cx = s["x"] + s["size"] / 2
    cy = s["y"] + s["size"] / 2
    dx = tx - cx
    dy = ty - cy
    d = math.hypot(dx, dy)
    if d > 0:
        s["vx"] += (dx / d) * amount
        s["vy"] += (dy / d) * amount


def move_away(s: dict, tx: float, ty: float, amount: float) -> None:
    move_toward(s, tx, ty, -amount)


def limit_speed(s: dict) -> None:
    max_speed = speed_for_size(s["size"])
    speed = math.hypot(s["vx"], s["vy"])
    if speed > max_speed:
        scale = max_speed / speed
        s["vx"] *= scale
        s["vy"] *= scale


def keep_motion_alive(s: dict) -> None:
    min_speed = speed_for_size(s["size"]) * MIN_MOTION_RATIO
    speed = math.hypot(s["vx"], s["vy"])
    if speed < min_speed:
        angle = random.uniform(0, math.tau)
        s["vx"] = math.cos(angle) * min_speed
        s["vy"] = math.sin(angle) * min_speed


def unstick_from_corners(s: dict) -> None:
    near_left = s["x"] <= CORNER_MARGIN
    near_right = s["x"] + s["size"] >= WIDTH - CORNER_MARGIN
    near_top = s["y"] <= CORNER_MARGIN
    near_bottom = s["y"] + s["size"] >= HEIGHT - CORNER_MARGIN

    if near_left and near_top:
        s["vx"] = abs(s["vx"]) + 0.3
        s["vy"] = abs(s["vy"]) + 0.3
    elif near_left and near_bottom:
        s["vx"] = abs(s["vx"]) + 0.3
        s["vy"] = -abs(s["vy"]) - 0.3
    elif near_right and near_top:
        s["vx"] = -abs(s["vx"]) - 0.3
        s["vy"] = abs(s["vy"]) + 0.3
    elif near_right and near_bottom:
        s["vx"] = -abs(s["vx"]) - 0.3
        s["vy"] = -abs(s["vy"]) - 0.3


def update_square(s: dict, squares: list[dict], speed_scale: float) -> None:
    cx = s["x"] + s["size"] / 2
    cy = s["y"] + s["size"] / 2

    # Keep random wandering
    s["vx"] += random.uniform(-WANDER, WANDER)
    s["vy"] += random.uniform(-WANDER, WANDER)

    target = None
    best = CHASE_RADIUS
    for other in squares:
        if other is s:
            continue

        ox = other["x"] + other["size"] / 2
        oy = other["y"] + other["size"] / 2
        d = math.hypot(ox - cx, oy - cy)

        if other["size"] > s["size"] and d < FLEE_RADIUS:
            strength = (FLEE_RADIUS - d) / FLEE_RADIUS
            size_gap = (other["size"] - s["size"]) / MAX_SIZE
            move_away(s, ox, oy, (0.28 + size_gap * 0.35) * strength)

        if other["size"] < s["size"] and d < best:
            best = d
            target = (ox, oy)

    if target is not None:
        move_toward(s, target[0], target[1], 0.16)

    limit_speed(s)
    s["x"] += s["vx"] * speed_scale
    s["y"] += s["vy"] * speed_scale

    # Bounce on edges
    if s["x"] < 0:
        s["x"] = 0
        s["vx"] *= -1
    if s["x"] + s["size"] > WIDTH:
        s["x"] = WIDTH - s["size"]
        s["vx"] *= -1
    if s["y"] < 0:
        s["y"] = 0
        s["vy"] *= -1
    if s["y"] + s["size"] > HEIGHT:
        s["y"] = HEIGHT - s["size"]
        s["vy"] *= -1

    unstick_from_corners(s)
    keep_motion_alive(s)
    limit_speed(s)


def resolve_collisions(squares: list[dict]) -> None:
    for i in range(len(squares)):
        a = squares[i]
        for j in range(i + 1, len(squares)):
            b = squares[j]
            if not overlaps(a, b):
                continue

            overlap_x = min(a["x"] + a["size"], b["x"] + b["size"]) - max(a["x"], b["x"])
            overlap_y = min(a["y"] + a["size"], b["y"] + b["size"]) - max(a["y"], b["y"])

            if overlap_x <= 0 or overlap_y <= 0:
                continue

            if overlap_x < overlap_y:
                push = overlap_x / 2
                if a["x"] < b["x"]:
                    a["x"] -= push
                    b["x"] += push
                else:
                    a["x"] += push
                    b["x"] -= push
                a["vx"], b["vx"] = b["vx"], a["vx"]
            else:
                push = overlap_y / 2
                if a["y"] < b["y"]:
                    a["y"] -= push
                    b["y"] += push
                else:
                    a["y"] += push
                    b["y"] -= push
                a["vy"], b["vy"] = b["vy"], a["vy"]

            # keep inside screen after push
            a["x"] = max(0, min(a["x"], WIDTH - a["size"]))
            a["y"] = max(0, min(a["y"], HEIGHT - a["size"]))
            b["x"] = max(0, min(b["x"], WIDTH - b["size"]))
            b["y"] = max(0, min(b["y"], HEIGHT - b["size"]))
            unstick_from_corners(a)
            unstick_from_corners(b)
            keep_motion_alive(a)
            keep_motion_alive(b)


def draw(screen: pygame.Surface, font: pygame.font.Font, squares: list[dict], speed_scale: float) -> None:
    screen.fill(BG)
    for s in squares:
        color = color_for_size(s["size"])
        pygame.draw.rect(screen, color, (int(s["x"]), int(s["y"]), s["size"], s["size"]))
    msg = "Squares compare sizes: chase smaller, flee larger, wander, no overlap | +/- speed | R reset | Esc quit"
    t1 = font.render(msg, True, TEXT)
    t2 = font.render(f"Speed: {speed_scale:.2f}x", True, TEXT)
    screen.blit(t1, (12, 10))
    screen.blit(t2, (12, 36))
    pygame.display.flip()


def change_speed(speed_scale: float, up: bool) -> float:
    if up:
        return min(3.0, speed_scale + 0.25)
    return max(0.25, speed_scale - 0.25)


def main() -> None:
    global WIDTH, HEIGHT
    pygame.init()
    info = pygame.display.Info()
    WIDTH = info.current_w
    HEIGHT = info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Moving Squares - Simple Version")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    squares = make_squares()
    speed_scale = 1.0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    squares = make_squares()
                    speed_scale = 1.0
                elif event.key in (pygame.K_UP, pygame.K_KP_PLUS):
                    speed_scale = change_speed(speed_scale, True)
                elif event.key in (pygame.K_DOWN, pygame.K_KP_MINUS):
                    speed_scale = change_speed(speed_scale, False)
                elif event.unicode in ("+", "="):
                    speed_scale = change_speed(speed_scale, True)
                elif event.unicode in ("-", "_"):
                    speed_scale = change_speed(speed_scale, False)

        for s in squares:
            update_square(s, squares, speed_scale)
        resolve_collisions(squares)
        draw(screen, font, squares, speed_scale)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
