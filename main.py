import math
import random

import pygame


WIDTH = 1200
HEIGHT = 700
FPS = 60

SMALL_SIZE = 14
BIG_SIZE = 36
SMALL_COUNT = 15
BIG_COUNT = 5

SMALL_SPEED = 2.8
BIG_SPEED = 2.2
FLEE_RADIUS = 170
CHASE_RADIUS = 260
WANDER = 0.22

BG = (20, 20, 28)
SMALL_COLOR = (100, 230, 120)
BIG_COLOR = (90, 140, 255)
TEXT = (235, 235, 235)


def new_square(is_big: bool) -> dict:
    size = BIG_SIZE if is_big else SMALL_SIZE
    speed = BIG_SPEED if is_big else SMALL_SPEED
    a = random.uniform(0, math.tau)
    return {
        "x": random.randint(0, WIDTH - size),
        "y": random.randint(0, HEIGHT - size),
        "vx": math.cos(a) * speed,
        "vy": math.sin(a) * speed,
        "size": size,
        "big": is_big,
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
    for _ in range(BIG_COUNT):
        placed = False
        for _ in range(150):
            s = new_square(True)
            if all(not overlaps(s, other) for other in squares):
                squares.append(s)
                placed = True
                break
        if not placed:
            squares.append(new_square(True))
    for _ in range(SMALL_COUNT):
        placed = False
        for _ in range(150):
            s = new_square(False)
            if all(not overlaps(s, other) for other in squares):
                squares.append(s)
                placed = True
                break
        if not placed:
            squares.append(new_square(False))
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
    max_speed = BIG_SPEED if s["big"] else SMALL_SPEED
    speed = math.hypot(s["vx"], s["vy"])
    if speed > max_speed:
        scale = max_speed / speed
        s["vx"] *= scale
        s["vy"] *= scale


def update_square(s: dict, squares: list[dict], speed_scale: float) -> None:
    cx = s["x"] + s["size"] / 2
    cy = s["y"] + s["size"] / 2

    # Keep random wandering
    s["vx"] += random.uniform(-WANDER, WANDER)
    s["vy"] += random.uniform(-WANDER, WANDER)

    if s["big"]:
        # Big squares chase nearest small square
        target = None
        best = CHASE_RADIUS
        for other in squares:
            if other["big"]:
                continue
            ox = other["x"] + other["size"] / 2
            oy = other["y"] + other["size"] / 2
            d = math.hypot(ox - cx, oy - cy)
            if d < best:
                best = d
                target = (ox, oy)
        if target is not None:
            move_toward(s, target[0], target[1], 0.18)
    else:
        # Small squares flee from close big squares
        for other in squares:
            if not other["big"]:
                continue
            ox = other["x"] + other["size"] / 2
            oy = other["y"] + other["size"] / 2
            d = math.hypot(ox - cx, oy - cy)
            if d < FLEE_RADIUS:
                strength = (FLEE_RADIUS - d) / FLEE_RADIUS
                move_away(s, ox, oy, 0.45 * strength)

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


def draw(screen: pygame.Surface, font: pygame.font.Font, squares: list[dict], speed_scale: float) -> None:
    screen.fill(BG)
    for s in squares:
        color = BIG_COLOR if s["big"] else SMALL_COLOR
        pygame.draw.rect(screen, color, (int(s["x"]), int(s["y"]), s["size"], s["size"]))
    msg = "Solid squares (no overlap) | Big chase | Small flee | Wander | +/- speed | R reset | Esc quit"
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
