# Light Refactoring Plan - lab8-pygame

## 1. Quick Baseline Summary (What Is Working)
- The current gameplay loop is stable: event polling, square updates, collision resolution, render, and FPS cap all run in a clear order.
- Behavior is already meaningful for a lab: smaller squares flee larger ones, larger squares chase smaller ones, and random wander keeps motion natural.
- Core controls work and are discoverable in runtime text: speed up/down, reset, and exit.
- `watch.py` gives a practical fast feedback loop for local changes.

## 2. Top Maintainability Risks (Ranked by Impact)
1. Single-file concentration in `main.py` (input, simulation, collisions, rendering)
   - Impact: High
   - Risk to maintenance: Any change can accidentally affect unrelated behavior because responsibilities are tightly coupled.

2. Dictionary-based square state with string keys
   - Impact: High
   - Risk to maintenance: Misspelled keys and mixed value types are only caught at runtime.

3. Dense collision block in `resolve_collisions`
   - Impact: Medium
   - Risk to maintenance: Correctness is hard to verify during edits because overlap math, pushes, swaps, and clamping are in one routine.

4. Input branching complexity inside `main()`
   - Impact: Medium
   - Risk to maintenance: Key handling logic is correct but not isolated, which makes behavior changes harder to review.

5. Runtime-updated globals (`WIDTH`, `HEIGHT`) mixed with constants
   - Impact: Medium
   - Risk to maintenance: Less obvious which values are true constants versus mutable runtime state.

6. Constant definitions are flat and numerous
   - Impact: Low
   - Risk to maintenance: Tuning is possible today, but intent is harder to scan quickly.

## 3. Refactoring Steps in Small Safe Iterations

### Iteration A (15-25 min): Improve naming and local structure without behavior changes
- Scope:
  - Add a local type alias for square data (for readability in signatures and helper docs).
  - Add short section headers for constant groups (display, movement, steering, visuals).
- Why it helps:
  - Improves readability immediately and lowers entry cost for future edits.
- Estimated risk:
  - Low
- Verification checks:
  - Run `python main.py`.
  - Confirm startup, rendering, and controls still behave exactly the same.

### Iteration B (20-30 min): Extract keyboard handling from `main()`
- Scope:
  - Move keydown branching into a helper such as `handle_keydown(event, squares, speed_scale, running)`.
  - Keep existing key mapping unchanged.
- Why it helps:
  - Main loop becomes easier to read and easier to teach.
- Estimated risk:
  - Low
- Verification checks:
  - Validate `Esc`, `R`, `Up/+`, `Down/-`, and numpad plus/minus behavior manually.
  - Confirm speed clamp remains 0.25x to 3.0x.

### Iteration C (25-30 min): Split collision logic into micro-helpers
- Scope:
  - Extract overlap depth calculation.
  - Extract axis push/velocity swap routine.
  - Keep post-push clamping and motion revival exactly as now.
- Why it helps:
  - Makes collision behavior safer to modify and easier to test mentally.
- Estimated risk:
  - Medium
- Verification checks:
  - Run for 2-3 minutes.
  - Observe no persistent overlap stacks.
  - Confirm squares remain on-screen after collisions.

### Iteration D (15-25 min): Clarify runtime state boundaries
- Scope:
  - Separate immutable defaults from mutable runtime dimensions (for example `DEFAULT_WIDTH/DEFAULT_HEIGHT` and runtime variables).
  - Avoid broad global mutation patterns where possible.
- Why it helps:
  - Reduces confusion about what may change during execution.
- Estimated risk:
  - Medium
- Verification checks:
  - Confirm fullscreen dimensions still come from `pygame.display.Info()`.
  - Confirm collisions still use current runtime bounds.

### Iteration E (20-30 min): Optional strict data model upgrade
- Scope:
  - Introduce a small `Square` dataclass only after previous cleanup is stable.
  - Migrate one subsystem at a time (creation, update, collision, draw).
- Why it helps:
  - Improves type safety and IDE support; reduces key typo bugs.
- Estimated risk:
  - Medium
- Verification checks:
  - Full manual pass: movement quality, chase/flee, collision response, reset behavior, speed controls.

## 4. Do Not Change Yet (Risky Areas)
- Do not split into many modules yet; for a student lab, one primary file is still useful for learning flow.
- Do not alter chase/flee constants while structural refactoring is in progress; it complicates regression diagnosis.
- Do not introduce optimization structures (spatial hashing/quadtree) at current square counts.
- Do not change fullscreen behavior in the same pass as collision or input refactoring.

## 5. Verification Routine Per Iteration
1. Run `python main.py`.
2. Check controls: `Up/+`, `Down/-`, `R`, `Esc`.
3. Let simulation run at least 60 seconds and watch for stuck corners or overlap artifacts.
4. If behavior changed unexpectedly, revert only the current iteration and re-apply in smaller edits.

## 6. Suggested Execution Order for Short Sessions
1. Session 1: Iteration A + Iteration B
2. Session 2: Iteration C
3. Session 3: Iteration D
4. Session 4 (optional): Iteration E
