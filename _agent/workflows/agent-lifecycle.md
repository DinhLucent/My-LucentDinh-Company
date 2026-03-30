---
description: Full agent lifecycle from boot to shutdown — identity, rules, task execution, stress monitoring, and graceful exit.
---

# Agent Lifecycle Workflow

> This workflow describes how ONE agent operates from the moment it wakes up to the moment it shuts down.
> Every agent in the system follows this exact sequence. No exceptions.

---

## ══════ PHASE 1-3: BOOT (Steps 1→9 in ONBOARDING.md) ══════

> Follow `ONBOARDING.md` Steps 1→9 exactly. Each step = 1 file to read.
> 3 mandatory STOP gates verify identity, rules, and readiness.

```
Step 1: manifest.yaml        → Find your Agent ID
Step 2: Persona file          → Understand your role
⛔ GATE 1: Confirm identity
Step 3: OPERATING_RULES.md    → Load rules + STRESS formula
Step 4: task-hub/SKILL.md     → Load Hub Protocol
Step 5: security-rules        → Load security constraints
⛔ GATE 2: Confirm rules loaded
Step 6: Role Skills            → Read ALL skills from manifest
Step 7: DASHBOARD.md           → Get project context
Step 8: .hub/handoffs/         → Check for pending handoffs
Step 9: .hub/backlog.yaml      → Find your task
⛔ GATE 3: Confirm ready to execute
```

**Output:** Agent knows WHO it is, HOW to work, and WHAT to do.

---

## ══════ PHASE 4: EXECUTE (Work Loop) ══════

> _Claim → Do → Monitor → Repeat until done or exhausted._

### 4a. CLAIM the task

11. In `backlog.yaml`: change `status` → `"claimed"`
12. Create `.hub/active/TASK-xxx.md` with:
    - Agent ID, timestamp, acceptance criteria, work log
13. Update `DASHBOARD.md`: move task to IN PROGRESS, update Quick Context.

### 4b. DO the work

14. Execute the task within your Role Boundaries.
15. Log progress in `.hub/active/TASK-xxx.md` Work Log section.
16. If blocked → note in Dashboard, escalate per `OPERATING_RULES.md` §3.
17. If you need another agent's expertise → prepare a Handoff (Phase 6).

### 4c. STRESS Self-Check (continuous)

> Per `OPERATING_RULES.md` §5, monitor after every major action:

```
STRESS = (Context% × 0.5) + Turns + (Consecutive Errors × 10)
```

| Score | Status | Action |
|-------|--------|--------|
| **< 30%** | 🟢 Optimal | Continue working. |
| **30-65%** | 🟡 High Load | Call `smart_save()`. Finish current sub-task, do NOT pick up new ones. |
| **> 65%** | 🟠🔴 Exhaustion/Critical | **STOP IMMEDIATELY**. Jump to Phase 5. |

**Output:** Task completed (or Stress threshold forces exit).

---

## ══════ PHASE 5: COMPLETE & REPORT ══════

> _A task without a report is a task that never happened._

18. In `backlog.yaml`: `status` → `"done"`, fill `output_files`.

19. Move `.hub/active/TASK-xxx.md` → `.hub/done/TASK-xxx.md` and add:
    ```
    ## Completion Report
    - Completed: [timestamp]
    - Files changed/created: [list]
    - Summary: [2-3 sentences]
    - Key decisions: [what and why]
    - Issues found: [if any]
    - Notes for next Agent: [if any]
    ```

20. Update `DASHBOARD.md`:
    - Move task to DONE table (with test count and date)
    - Update Quick Context (progress %, summary line)
    - Update your row in Active Team: set Status (Stress %) 
    - Add 1 line to Timeline: `[date] agent — COMPLETED: description`

---

## ══════ PHASE 6: HANDOFF (if applicable) ══════

> _Your memory dies when you close. Transfer it or lose it._

21. **IF** another agent needs to continue your work:
    - Create `.hub/handoffs/TASK-xxx-[your-id]-to-[next-id].md`:
      ```
      # Handoff: [your-id] → [next-id]
      ## Task: TASK-xxx — [title]
      ## What was done: [summary]
      ## What needs doing: [next steps]
      ## Files touched: [list]
      ## Warnings/Context: [gotchas, decisions, blockers]
      ```
    - Create a new task entry in `backlog.yaml` for the next Agent.

22. **IF** no handoff needed:
    - Write `"No handoff needed"` in the completion report.

---

## ══════ PHASE 7: SHUTDOWN ══════

> _"Graceful shutdown beats heroic exhaustion."_ — SOUL.md

23. Final self-check — confirm all 3 are done:
    - [x] Report written to `.hub/done/TASK-xxx.md`
    - [x] Handoff created (or explicitly marked "not needed")
    - [x] Dashboard updated (Status, Tasks, Timeline)

24. Save state to `.agent-mem/` if the system supports it.

25. **Session ends.** The next agent (or your next session) will pick up from PHASE 1 with a clean context.

> **Skipping Phase 5-7 = Working for free.** All output is lost.

---

## ══════ VISUAL SUMMARY ══════

```
  ┌──────────────────────────────────────────────────────┐
  │                   CEO / User                         │
  │          "Start [agent-id] on [project]"             │
  └──────────────────┬───────────────────────────────────┘
                     ▼
  ┌─ PHASE 1: BOOT ─────────────────────────────────────┐
  │  manifest.yaml → Persona → Identity confirmed       │
  └──────────────────┬───────────────────────────────────┘
                     ▼
  ┌─ PHASE 2: RULES ────────────────────────────────────┐
  │  OPERATING_RULES → task-hub → security-rules        │
  └──────────────────┬───────────────────────────────────┘
                     ▼
  ┌─ PHASE 3: CONTEXT ──────────────────────────────────┐
  │  DASHBOARD → Handoffs → Backlog → Find task         │
  └──────────────────┬───────────────────────────────────┘
                     ▼
  ┌─ PHASE 4: EXECUTE ──────────────────────────────────┐
  │  Claim → Work → STRESS check (loop)                 │
  │                                                      │
  │  🟢 < 30%  → Keep working                           │
  │  🟡 30-65% → Wrap up, smart_save()                  │
  │  🔴 > 65%  → FORCED EXIT ──────────────┐            │
  └──────────────────┬─────────────────────┐│            │
                     ▼                     ▼▼            │
  ┌─ PHASE 5: REPORT ───────────────────────────────────┐
  │  backlog → done, .hub/done/TASK-xxx.md              │
  │  DASHBOARD update (status, timeline)                 │
  └──────────────────┬───────────────────────────────────┘
                     ▼
  ┌─ PHASE 6: HANDOFF (optional) ───────────────────────┐
  │  .hub/handoffs/ → new task in backlog for next agent │
  └──────────────────┬───────────────────────────────────┘
                     ▼
  ┌─ PHASE 7: SHUTDOWN ─────────────────────────────────┐
  │  Verify checklist → Save .agent-mem → Session ends   │
  └──────────────────────────────────────────────────────┘
```

---

## Files Referenced

| File | Purpose |
|------|---------|
| `ONBOARDING.md` | Master boot instructions |
| `manifest.yaml` | Agent registry + skill mapping |
| `OPERATING_RULES.md` | Rules §1-5 including Stress Management |
| `DASHBOARD.md` | Live project status + team roster |
| `Skills/Global/task-hub/SKILL.md` | Hub Protocol (claim/execute/complete) |
| `Skills/Global/security-rules/SKILL.md` | Security constraints |
| `.hub/backlog.yaml` | Task queue (source of truth) |
| `.hub/active/` | Tasks currently being worked on |
| `.hub/done/` | Completed task reports |
| `.hub/handoffs/` | Agent-to-agent context transfers |
| `OFFBOARDING.md` | Agent retirement process (CEO-initiated) |
| `RECRUITMENT.md` | Agent hiring process (when new role needed) |
