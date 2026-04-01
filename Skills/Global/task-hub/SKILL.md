---
description: "Task Hub Protocol — How Agents pick up, execute, and return tasks"
---

# 🏗️ Task Hub Protocol

> **MANDATORY.** All Agents follow this. The only way to receive and return tasks.

## Hub Structure

```
.hub/
├── backlog.yaml    ← Task queue (source of truth)
├── active/         ← Tasks in progress (1 file per task)
├── done/           ← Completed + detailed report for CEO
└── handoffs/       ← Agent-to-agent transfer files
```

`DASHBOARD.md` at project root = Quick Context + Task Board + Timeline.

---

## Step 0: BOOT SEQUENCE (every new session)

> ⚠️ **Follow the standard Boot Sequence in `ONBOARDING.md`.**
> Order: ONBOARDING → OPERATING_RULES → task-hub → Dashboard → backlog → Work.


---

## Step 1: FIND matching task

In `backlog.yaml`, find tasks where:
- `status: "todo"`
- `assigned_role` = **your** Agent ID
- `dependencies` all `done`

```
┌─────────────────────────────────────────────────┐
│  assigned_role ≠ your ID → MUST REFUSE          │
│  → "Task [ID] is for [assigned_role], not me."  │
│  → DO NOT execute even 1 line                   │
│                                                 │
│  No matching tasks → Tell User:                 │
│  → "No tasks in Hub for my role [my-role]."     │
│                                                 │
│  Task needs expertise outside ALL active roles: │
│  → HIRING REQUEST to User:                      │
│  → "This task requires [skill/role] expertise.  │
│     No active Agent covers this. Recommend      │
│     hiring [suggested-agent-id] via             │
│     RECRUITMENT.md to fill this gap."           │
│  → DO NOT attempt the work yourself             │
└─────────────────────────────────────────────────┘
```

## Step 2: CLAIM

1. `backlog.yaml`: change `status` → `"claimed"`
2. Create `.hub/active/TASK-xxx.md`:
   ```
   # TASK-xxx: [Title]
   - Agent: [id] | Claimed: [time] | Status: 🔄
   ## Acceptance Criteria
   [from backlog]
   ## Work Log
   - [time] Started...
   ```
3. Update `DASHBOARD.md` (move to IN PROGRESS, update Quick Context)
4. Start git workflow for the task:
   - `git pull --ff-only`
   - create a task branch (see `GIT_WORKFLOW.md`)
   - keep this task isolated from unrelated changes


## Step 3: EXECUTE

- Update Work Log in `.hub/active/TASK-xxx.md`
- Blocked → note in Dashboard
- Need another Agent → create handoff (Step 5)

## Step 4: COMPLETE

1. `backlog.yaml`: `status` → `"done"`, fill `output_files`
2. Move `.hub/active/TASK-xxx.md` → `.hub/done/TASK-xxx.md`
3. Add to done file:
   ```
   ## Completion Report
   - Completed: [time]
   - Files: [list]
   - Summary: [2-3 sentences]
   - Decisions: [key decisions]
   - Issues: [if any]
   - Notes for next Agent: [if any]
   ```
4. Update `DASHBOARD.md`:
   - Move task to DONE list
   - Update `Quick Context` progress
   - **Evaluate and Update your Status (Stress %)** in the Active Team table per `OPERATING_RULES.md` §5:
     - **🟢 < 30% (Optimal)**: Normal operation, light context.
     - **🟡 30-65% (High Load)**: Growing context, nearing decision fatigue.
     - **🟠🔴 > 65% (Exhaustion)**: Critical load. Must STOP and Handoff.
   - **Quick Context**: progress %, last agent, 1-line summary
   - **Tasks**: move to DONE
   - **Timeline**: add 1 line (`[date] agent — COMPLETED: description`)

5. Complete git gate:
   - run relevant tests
   - verify `git status`
   - commit task changes before marking `done`
   - if remote/review exists, push branch and open/update PR
   - record branch / commit / PR status in the completion report

### 🚫 GATE — MANDATORY before this task is considered DONE:

> **You MUST now perform ONBOARDING Phase 5: Shutdown Ritual.** 
> Failure to do this means the task is NOT complete.
>
> 1. Write FULL report to `.hub/done/TASK-xxx.md`.
> 2. Create Handoff file if needed.
> 3. Update Dashboard status (🟢/🟡/🔴).
> 4. **Complete Git workflow gate from `GIT_WORKFLOW.md`**.
>
> If there is code or doc output, there should be at least one commit before moving the task to `done`.

| Situation | Action |
| :--- | :--- |
| YES — another agent takes over | **MUST** create handoff file (Step 5) |
| NO — final task | Skip handoff, write `"No handoff needed"` in report |



## Step 5: HANDOFF (required if next agent exists)

Create `.hub/handoffs/TASK-xxx-[from]-to-[to].md`:
```
# Handoff: [from] → [to]
## Task: TASK-xxx — [title]
## Completed: [what was done]
## Needs: [what next agent must do]
## Files: [changed/created]
## Context: [decisions, warnings]
```
Create new task in `backlog.yaml` for next Agent.


---

## Compact Reporting Rules

| Where | What | Limit |
|-------|------|-------|
| `DASHBOARD.md` Quick Context | 1-line summary for AI | ≤10 rows |
| `DASHBOARD.md` Timeline | 1 line per event | ≤20 entries |
| `.hub/done/TASK-xxx.md` | Full report for CEO | No limit |

> Dashboard must stay lean. If too long → new AI can't absorb it.

---

## Anti-Patterns

- ❌ Skip reading Hub before working
- ❌ Accept wrong-role task
- ❌ Skip Dashboard update after task
- ❌ Create tasks without User/Producer approval
- ❌ Skip handoff when transferring work
- ❌ Do work outside your role "to be helpful" — escalate instead
- ❌ Silently skip tasks that need missing roles — always request hiring

## Triggers

Auto-activates on: session start, "get task", "check tasks", "update dashboard", task completion.
