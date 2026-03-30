# Lab 8 - Pygame Moving Squares Report

# First Impressions - Initial Take on the Project Assignment
## In this section, students will provide their initial thoughts on the project assignment, including their understanding of the requirements, any assumptions they made, points that need clarification, and their overall approach to tackling the project.
## Initial Thoughts
This looked like a small graphics lab focused on Pygame basics: create a simple window, animate a handful of objects, and understand the render loop.
## Assumptions Made
I assumed the goal was a lightweight animation rather than a physics simulation. I also assumed the squares should bounce off the edges of the window and keep moving until the app is closed.
## Points Needing Clarification
The slide did not specify whether the squares should be constant speed, accelerate, or change color, so I kept the behavior simple and readable.

# Key Learnings
## Here, students will summarize the most important things they learned while working on the project. This could include computer science related concepts, technical skills, insights about using CoPilot effectively, and any new concepts or tools they encountered
## Computer Science Concepts and Technical Skills
The main loop is the core of Pygame rendering: process events, update state, clear the screen, draw, then flip the buffer. Keeping movement logic inside a small dataclass made the behavior easy to follow.
## Insights about Using CoPilot Effectively
Ask mode is useful for understanding the render loop and animation ideas, while agent mode is helpful for scaffolding the project and keeping the setup files consistent.
## New Concepts or Tools Encountered
I used Pygame for the first time in this lab setup and learned how rectangle drawing and frame timing work together to create motion.

# Report on CoPilot Prompting Experience
## Student may pull examples from the JOURNAL.md to illustrate their experience, including specific interactions that were particularly helpful or challenging.
### Types of prompts that worked well
“Review this function against these constraints (pure / no loops / immutable inputs)” and “suggest test cases for this function”.

#### Prompts I Used
- “I tried to run `main.py`, but Python isn’t available in this terminal environment. Give me step-by-step commands to check if Python exists,  install it if missing, and  rerun the script.”
- “Write a `run.ps1` that finds a local Python install, falls back to installing via `winget` if needed, then runs `main.py` with forwarded args.”
- “I’m getting an error when running the game.”
- “List the game state variables for a Hangman-style word game and the invariants I should maintain.”
- “Suggest edge cases and common bugs for Hangman/word-guess games.”
- “Review my function.”
- “Propose a test plan.”
- “Generate test cases.”
- “After these changes, review the diff and call out any behavior changes or rule violations I might have introduced.”
- “I updated the journal/report—suggest how to summarize what worked well vs what failed when prompting Copilot, with concrete examples.”
### Types of prompts that did not work well or failed
Vague prompts like “finish the whole game” tended to produce code that didn’t match the lab constraints until I asked for a review against the requirements.

# Limitations, Hallucinations and Failures
## In this section, students will document any instances where CoPilot provided incorrect or misleading information (hallucinations) or where it failed to provide a useful response. They will analyze why these issues occurred and how they impacted their work on the project.
## For example: Fabricated APIs, Deprecated functions, Subtle logical errors, Confident but wrong explanations, Over-engineered solutions, Under-engineered solutions, overcomplicated code, oversimplified code, etc.
## Examples of Hallucinations or Failures or Misleading Information or Confident but Wrong Explanations, or Over-engineered or Under-engineered Solutions
Sometimes suggestions added extra complexity (extra classes / frameworks) that were not needed for a small lab.
## Analysis of Why These Issues Occurred
The model optimizes for “general best practices”, which can conflict with assignment-specific constraints unless those constraints are repeated explicitly.
## Impact on the Project
It mainly cost time in review: I had to re-check constraints and simplify code.

# AI Trust
## When did I trust the AI?
When it produced small, verifiable suggestions (test cases, edge cases, refactors that keep behavior the same).
## When did I stop trusting it?
When answers were broad, introduced features not asked for, or when constraints were ignored.
## What signals or situations or patterns indicated low reliability?
Not mentioning key constraints, or proposing code with loops/replacements when those were explicitly forbidden.

# What I Learned
## What did you learn about software development?
Small pure functions + tests make it easier to build the full program safely.
## What did you learn about using AI tools?
AI is strongest as a reviewer and brainstorming partner; I still need to own the requirements and verify behavior.
## When should you trust AI? When should you double-check it?
Trust for ideas; double-check anything that changes logic, touches constraints, or affects correctness.

# Reflection
## Did AI make you faster? Why or why not?
Faster overall for brainstorming and testing ideas, but only after I learned to constrain prompts and verify the output.
## Did you feel in control of the code?
Yes, when I implemented and tested core logic first and used AI mainly for review.
## Would you use AI the same way next time? What would you change?
I would start with a clearer plan and ask for tests and edge cases earlier.
