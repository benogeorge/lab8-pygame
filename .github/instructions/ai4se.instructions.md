---
description: AI4SE journaling directive
applyTo: "**/*"
---

## AI4SE Directive

1. Keep the journal logger agent active in `.github/agents/journal-logger.agent.md`.
2. After every user interaction, prepend a new entry to `JOURNAL.md` in reverse chronological order.
3. Use timestamp format `MM-DD-YYYY HH:MM`.
4. Include: Date, User, Prompt, CoPilot Mode, CoPilot Model, Changes Made, Context and Reasons for Changes, My Observations.
5. Reconcile recent interactions before writing to avoid missed entries and duplicates.
