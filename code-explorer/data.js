export const explorerData = {
  project: {
    name: "Lab 8 Pygame",
    subtitle: "Moving Squares",
    stats: [
      { label: "Python modules", value: "2" },
      { label: "Docs", value: "3" },
      { label: "Squares", value: "20" },
      { label: "Target FPS", value: "60" }
    ]
  },
  files: [
    {
      path: "main.py",
      type: "Source",
      language: "python",
      size: "300+ lines",
      summary: "Main animation loop with flee, chase, wandering, collision response, and overlay rendering.",
      tags: ["loop", "flee", "chase", "wander", "collision", "controls", "draw"],
      highlights: [
        "Square dataclass stores position, velocity, size, and render color.",
        "Small squares steer around larger threats while big squares chase the closest small square.",
        "Wander adds small random pushes so movement stays lively.",
        "Main loop handles events, updates state, resolves collisions, and draws each frame."
      ],
      snippet: "from __future__ import annotations\n\nimport math\nimport random\nfrom dataclasses import dataclass\n\nimport pygame\n\nWIDTH = 1500\nHEIGHT = 800\nFPS = 60\nSQUARE_COUNT = 20\nFLEE_RADIUS = 150\nCHASE_RADIUS = 260\n\n@dataclass\nclass Square:\n    x: float\n    y: float\n    vx: float\n    vy: float\n    size: int\n\n    def apply_flee(self, others: list[\"Square\"]) -> None:\n        if self.size == BIG_SQUARE_SIZE:\n            return\n        # small squares move away from big ones\n\n    def apply_chase(self, others: list[\"Square\"]) -> None:\n        if self.size != BIG_SQUARE_SIZE:\n            return\n        # big squares move toward the closest small one\n\n    def apply_wander(self) -> None:\n        # small random movement for all squares\n        ...\n\ndef main() -> None:\n    pygame.init()\n    screen = pygame.display.set_mode((WIDTH, HEIGHT))\n    clock = pygame.time.Clock()\n\n    running = True\n    while running:\n        for event in pygame.event.get():\n            if event.type == pygame.QUIT:\n                running = False\n\n        # update -> collide -> draw -> flip\n        pygame.display.flip()\n        clock.tick(FPS)"
    },
    {
      path: "watch.py",
      type: "Utility",
      language: "python",
      size: "41 lines",
      summary: "Restarts main.py when Python files in the project change.",
      tags: ["watch", "reload", "subprocess"],
      highlights: [
        "Runs game process with current interpreter from active environment.",
        "Polls file mtimes and restarts on change for quick iteration."
      ],
      snippet: "from __future__ import annotations\n\nimport os\nimport subprocess\nimport sys\nimport time\nfrom pathlib import Path\n\nWATCH_INTERVAL = 0.5\n\ndef latest_mtime(source_dir: Path) -> float:\n    return max(path.stat().st_mtime for path in source_dir.glob(\"*.py\"))\n\ndef main() -> None:\n    source_dir = Path(__file__).resolve().parent\n    source_path = source_dir / \"main.py\"\n\n    while True:\n        child = subprocess.Popen([sys.executable, str(source_path)], env=os.environ.copy())\n        last_mtime = latest_mtime(source_dir)\n"
    },
    {
      path: "README.md",
      type: "Docs",
      language: "markdown",
      size: "~40 lines",
      summary: "Project description, setup commands, controls, and loop notes.",
      tags: ["setup", "controls", "run"],
      highlights: [
        "Keeps startup commands and controls visible for new contributors.",
        "Explains the loop in an easy-to-scan ordered list."
      ],
      snippet: "# Lab 8 - Pygame Moving Squares\n\nA small Pygame demo that draws 10 squares and moves them around the screen.\n\n## Run\n\n```powershell\npy -3.12 -m venv .venv\n.\\.venv\\Scripts\\Activate.ps1\npython -m pip install -r requirements.txt\npython main.py\n```\n\n## Controls\n- Up or +: speed up\n- Down or -: slow down\n- R: randomize all squares\n- Q or Esc: quit"
    },
    {
      path: "REPORT.md",
      type: "Docs",
      language: "markdown",
      size: "student reflection",
      summary: "Assignment reflection about implementation choices and AI prompting.",
      tags: ["reflection", "ai", "lessons"],
      highlights: [
        "Captures assumptions and constraints during the lab.",
        "Documents when AI output was helpful versus noisy."
      ],
      snippet: "# Lab 8 - Pygame Moving Squares Report\n\n## Assumptions Made\nI assumed the goal was a lightweight animation rather than a physics simulation.\n\n## Key Learnings\nThe main loop is the core of Pygame rendering: process events, update state, clear the screen, draw, then flip the buffer.\n"
    },
    {
      path: "requirements.txt",
      type: "Dependency",
      language: "text",
      size: "1 line",
      summary: "Pinned dependency for reproducible setup.",
      tags: ["dependency", "pygame"],
      highlights: [
        "Small dependency surface keeps this lab easy to run."
      ],
      snippet: "pygame-ce==2.5.7"
    },
    {
      path: "JOURNAL.md",
      type: "History",
      language: "markdown",
      size: "rolling log",
      summary: "Reverse-chronological log of prompts, actions, and outcomes.",
      tags: ["journal", "history", "agent"],
      highlights: [
        "Shows how decisions evolved during the lab workflow."
      ],
      snippet: "### **New Interaction**\n- **Date**: MM-DD-YYYY HH:MM\n- **User**: beno.george@epita.fr\n- **Prompt**: ..."
    }
  ],
  architecture: [
    {
      title: "Main Loop",
      body: "The key flow is events, update, collision pass, draw pass, and frame flip at a fixed cadence."
    },
    {
      title: "Behavior Layer",
      body: "Small squares flee, big squares chase, and everyone gets a little wander for less predictable movement."
    },
    {
      title: "Iteration Workflow",
      body: "watch.py shortens feedback cycles by restarting main.py whenever source files change."
    },
    {
      title: "Learning Trace",
      body: "README and REPORT complement source code with project intent, controls, and retrospective context."
    }
  ]
};
