export const explorerData = {
  project: {
    name: "Lab 8 Pygame",
    subtitle: "Repository Code Explorer",
    stats: [
      { label: "Python modules", value: "2" },
      { label: "Explorer files", value: "5" },
      { label: "Primary docs", value: "5" },
      { label: "Entities", value: "20 squares" },
      { label: "Target FPS", value: "60" }
    ]
  },
  files: [
    {
      path: "main.py",
      type: "Source",
      language: "python",
      size: "~275 lines",
      summary: "Fullscreen Pygame loop where big squares chase and small squares flee, including collision resolution and speed controls.",
      tags: ["loop", "flee", "chase", "wander", "collision", "fullscreen", "controls", "draw"],
      highlights: [
        "`make_squares` tries many placements to spawn non-overlapping big and small squares.",
        "`update_square` adds wander and behavior steering based on square role (big or small).",
        "`resolve_collisions` separates overlaps and swaps velocity components for a simple bounce effect.",
        "Keyboard controls adjust simulation speed and reset entities during runtime."
      ],
      snippet: "import math\nimport random\n\nimport pygame\n\n\nWIDTH = 1200\nHEIGHT = 700\nFPS = 60\n\nSMALL_SIZE = 14\nBIG_SIZE = 36\nSMALL_COUNT = 15\nBIG_COUNT = 5\n\ndef make_squares() -> list[dict]:\n    squares = []\n    for _ in range(BIG_COUNT):\n        placed = False\n        for _ in range(150):\n            s = new_square(True)\n            if all(not overlaps(s, other) for other in squares):\n                squares.append(s)\n                placed = True\n                break\n\ndef main() -> None:\n    pygame.init()\n    info = pygame.display.Info()\n    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)\n\n    squares = make_squares()\n    speed_scale = 1.0\n    while running:\n        for s in squares:\n            update_square(s, squares, speed_scale)\n        resolve_collisions(squares)\n        draw(screen, font, squares, speed_scale)"
    },
    {
      path: "watch.py",
      type: "Utility",
      language: "python",
      size: "40 lines",
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
      size: "~45 lines",
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
      size: "long-form reflection",
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
      path: "code-explorer/index.html",
      type: "Explorer",
      language: "html",
      size: "~70 lines",
      summary: "Page skeleton for the repository explorer: hero, filters, file tree, snippet viewer, and architecture cards.",
      tags: ["html", "layout", "shell", "viewer", "filters"],
      highlights: [
        "Defines semantic regions for stats, tree navigation, viewer, and notes.",
        "Loads modular JavaScript (`app.js`) and site theme (`styles.css`)."
      ],
      snippet: "<main class=\"shell\">\n  <header class=\"hero card\">\n    <p class=\"eyebrow\">Repository Explorer</p>\n    <h1>Lab 8 Pygame</h1>\n  </header>\n\n  <section class=\"toolbar card\">\n    <input id=\"search\" type=\"search\" />\n    <div id=\"filters\" class=\"filters\"></div>\n  </section>\n\n  <section class=\"layout\">\n    <aside class=\"card sidebar\">\n      <nav id=\"tree\" class=\"tree\"></nav>\n    </aside>\n\n    <article class=\"card viewer\">\n      <h2 id=\"file-title\">main.py</h2>\n      <pre class=\"code-wrap\"><code id=\"code\"></code></pre>\n    </article>\n  </section>\n</main>"
    },
    {
      path: "code-explorer/app.js",
      type: "Explorer",
      language: "javascript",
      size: "~130 lines",
      summary: "Client-side renderer that handles filtering, file selection, snippets, and copy-to-clipboard.",
      tags: ["javascript", "state", "render", "search", "clipboard"],
      highlights: [
        "Maintains a small `state` object for query, filter, and selected path.",
        "Renders stats, filters, tree, file details, and architecture cards from `explorerData`."
      ],
      snippet: "import { explorerData } from \"./data.js\";\n\nconst state = {\n  query: \"\",\n  filter: \"All\",\n  selectedPath: explorerData.files[0]?.path ?? \"\"\n};\n\nfunction filterFiles() {\n  const q = state.query.trim().toLowerCase();\n  return explorerData.files.filter((file) => {\n    const typeOk = state.filter === \"All\" || file.type === state.filter;\n    const text = [file.path, file.summary, ...(file.tags ?? [])].join(\" \" ).toLowerCase();\n    return typeOk && (!q || text.includes(q));\n  });\n}\n\nsearchEl.addEventListener(\"input\", () => {\n  state.query = searchEl.value;\n  renderTree();\n});"
    },
    {
      path: "code-explorer/styles.css",
      type: "Explorer",
      language: "css",
      size: "~300 lines",
      summary: "Theme and responsive layout for cards, file tree, syntax-style viewer lines, and highlighted architecture notes.",
      tags: ["css", "theme", "responsive", "layout", "cards"],
      highlights: [
        "Uses layered background effects (grid + glows) to avoid a flat page.",
        "Switches to single-column layout on narrow screens for mobile usability."
      ],
      snippet: ":root {\n  --bg: #0d1117;\n  --panel: #111a23cc;\n  --text: #e8edf3;\n  --accent: #ff8a3d;\n}\n\n.shell {\n  width: min(1200px, 94vw);\n  margin: 1.4rem auto 2rem;\n  display: grid;\n  gap: 1rem;\n}\n\n.layout {\n  display: grid;\n  grid-template-columns: 0.95fr 1.35fr;\n  gap: 1rem;\n}\n\n@media (max-width: 980px) {\n  .layout {\n    grid-template-columns: 1fr;\n  }\n}"
    },
    {
      path: "docs/code_explorer_v1.html",
      type: "Docs",
      language: "html",
      size: "prototype snapshot",
      summary: "Archived first-pass explorer markup kept under docs for reference.",
      tags: ["docs", "prototype", "html"],
      highlights: [
        "Mirrors the explorer structure used in the production `code-explorer` folder.",
        "Useful for comparing narrative/content shifts across versions."
      ],
      snippet: "<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n  <title>Lab 8 Code Explorer</title>\n  <script type=\"module\" src=\"app.js\"></script>\n</head>\n<body>\n  <main class=\"shell\">\n    <header class=\"hero card\">\n      <h1>Lab 8 Pygame</h1>\n    </header>\n  </main>\n</body>\n</html>"
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
      body: "Each frame processes input, updates square velocities and positions, resolves overlaps, draws UI text, and ticks the clock at 60 FPS."
    },
    {
      title: "Behavior Layer",
      body: "Small entities run from nearby big entities, big entities hunt the nearest small target, and all entities get random wander noise."
    },
    {
      title: "Iteration Workflow",
      body: "watch.py shortens feedback cycles by restarting main.py whenever source files change."
    },
    {
      title: "Explorer Frontend",
      body: "The static site relies on a single data model (`data.js`) and rendering layer (`app.js`) so documentation and source snippets stay easy to update."
    }
  ]
};
