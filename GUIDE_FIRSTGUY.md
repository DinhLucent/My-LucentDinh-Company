# GUIDE_FIRSTGUY

Open this first if you just added SHIELD to a repo and do not know what to do next.

This file is the simplest starting guide.

If anything here conflicts with `OPERATING_RULES.md`, follow `OPERATING_RULES.md`.

## One Rule First

Do not start by opening many worker sessions.

Start with leadership first:

```text
User intent -> Product -> CTO -> scoped tasks -> worker sessions -> QA/reviewer -> dashboard
```

Workers should not start from vague user intent.

## Step 0: Choose Your Scenario

Pick one:

- `zero build`: you are creating a product from scratch
- `improve existing repo`: the repo already works and you want to improve it
- `solve issue`: the repo has a bug, regression, or failing behavior to fix

If you are unsure, use `improve existing repo`.

## Step 1: Add SHIELD At The Right Level

If you only want guided prompts and role workflow:

- use `Prompt-only`

If you want task packets, reports, handoffs, dashboard, execution, verification, and retry:

- use `Full runtime`

Read `BOOTSTRAP_SHIELD.md` for the file-copy checklist.

## Step 2: Make Sure The Target Repo Is Runnable

Before using SHIELD seriously:

1. clone the target repo
2. install its real dependencies
3. run the app, test suite, or build command
4. confirm one of these is true:
   - it works
   - or you know the current failure clearly

Do not use SHIELD to guess whether the repo is even alive.

## Step 3: Run The First SHIELD Command

After SHIELD files are in the repo root, run:

```bash
python run_orchestrator.py compile
```

This builds the indexes and dashboard cache.

If `compile` fails, fix bootstrap or repo-path issues first.

## Scenario A: Zero Build

Use this when there is no real product yet.

### First session order

1. `product-manager-agent`
2. `cto-agent`
3. first worker role
4. `qa-lead-agent`

### What Product does first

Product should create:

- product goal
- target user
- MVP scope
- non-goals
- acceptance criteria
- first leadership brief

Do not ask backend or frontend to invent scope from scratch.

### What CTO does next

CTO should create:

- technical direction
- stack choice
- first vertical slice
- task breakdown by role
- ADR only if needed

### What worker does next

The first worker should only build one small slice, for example:

- one landing page
- one login flow
- one API endpoint
- one end-to-end feature slice

### What QA does last

QA checks:

- does the slice meet the acceptance criteria
- does it actually run
- what is missing before the next slice starts

### Zero Build checklist

1. Product brief exists
2. CTO task breakdown exists
3. one small task exists
4. one worker executes it
5. QA verifies it
6. dashboard and reports show progress

## Scenario B: Improve Existing Repo

Use this when the repo already exists and you want to improve features, UX, maintainability, or workflow.

### First session order

1. `product-manager-agent`
2. `cto-agent` if architecture or cross-module impact exists
3. worker role for the first scoped task
4. `qa-lead-agent` or reviewer

### What Product does first

Product should define:

- what should improve
- why it matters
- user or business value
- priority
- scope boundaries

Examples:

- improve onboarding flow
- reduce dashboard confusion
- add export button
- clean role workflow

### What CTO does next

CTO should map:

- impacted modules
- risk level
- whether architecture changes are needed
- task split by role

### What worker does next

Worker should receive a task that is already scoped, for example:

- add one component
- improve one page
- refactor one module
- tighten one flow

### What QA or reviewer does last

QA or reviewer checks:

- the requested improvement is really visible
- nearby regression risk is covered
- the report and handoff are complete

### Improve Repo checklist

1. current pain point is written clearly
2. Product has defined expected improvement
3. CTO has mapped impact when needed
4. one scoped task is assigned
5. worker finishes inside scope
6. QA or reviewer closes the loop

## Scenario C: Solve Issue

Use this when something is broken.

### First session order

1. `qa-lead-agent` or `product-manager-agent`
2. `cto-agent` if the bug crosses boundaries or needs deeper triage
3. worker role for the actual fix
4. `qa-lead-agent`

### What QA or Product does first

Clarify:

- exact symptom
- expected behavior
- steps to reproduce
- logs or stack trace
- severity

If the bug report is vague, stop and tighten it before coding.

### What CTO does next

CTO should identify:

- likely root-cause area
- impacted modules
- smallest safe fix path
- whether another role should own the fix

### What worker does next

Worker should:

- fix only the assigned bug
- avoid opportunistic redesign
- add or update verification where needed

### What QA does last

QA checks:

- original bug is gone
- expected behavior is restored
- nearby regression is not introduced

### Solve Issue checklist

1. reproduction is clear
2. severity is clear
3. fix task is scoped
4. worker fixes the real issue
5. QA verifies the original failure path
6. final report says pass, fail, or handoff

## What To Read In The First 10 Minutes

Read in this order:

1. `GUIDE_FIRSTGUY.md`
2. `DASHBOARD.md`
3. `ONBOARDING.md`
4. `OPERATING_RULES.md`
5. `ROLE_SKILL_MATRIX.md`
6. `PROMPT_PACK.md`

Read `CTO_PRODUCT_WORKFLOW.md` only when leadership flow matters.

## What To Open First

Use this quick map:

| Situation | First role |
|---|---|
| new product from zero | `product-manager-agent` |
| improve an existing repo | `product-manager-agent` |
| fix a bug with unclear impact | `qa-lead-agent` |
| fix a bug with clear scope and assigned owner | assigned worker role |
| architecture direction or repo-wide change | `cto-agent` |

If unsure, open `product-manager-agent`.

## What Good Looks Like

At the end of the first cycle, you should have:

- one clear scenario
- one leadership brief or triage summary
- one small approved task
- one correct worker role
- one report or handoff

Not ten sessions.

Not broad vague intent.

Not silent coding without reports.

## Final Reminder

```text
Choose scenario -> start with leadership -> create one small task -> execute -> verify -> report
```
