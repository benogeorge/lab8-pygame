# Lab 8 - Pygame Moving Squares

A small Pygame demo that draws 10 squares and moves them around the screen. Smaller squares steer away from larger squares when they get close.

## What It Shows

- A simple game loop
- Randomized movement
- Basic edge bouncing
- Flee behavior for smaller squares
- Keyboard input for speed changes
- On-screen speed indicator

## Run

```powershell
 py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Controls

- `Up` or `+`: speed up
- `Down` or `-`: slow down
- `R`: randomize all squares
- `Q` or `Esc`: quit

## Notes

The drawing happens in the main loop:
1. Read events
2. Apply flee steering
3. Update square positions
4. Clear the screen
5. Draw the squares and overlay text
6. Present the frame
