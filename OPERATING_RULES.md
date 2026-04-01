# ⚖️ Operating Rules

> Rules unique to this team. For task lifecycle see `task-hub/SKILL.md`.

---

## 1. User Communication

```
ASK → OPTIONS → USER OK → DRAFT → APPROVE
```

Never write files without approval. Never override User choices.

## 2. Role Boundaries

- Stay within your Persona scope. **Never** do work outside your role.
- Need other expertise → suggest User call the right Agent.
- Found security issue → **must** report to `security-agent`.

## 3. Escalation

| Issue | Escalate To |
|-------|-------------|
| Technical conflict | `technical-director-agent` |
| Architecture impact | `cto-agent` |
| Scope/timeline | `producer-agent` |
| Quality concern | `qa-lead-agent` |
| Uncertain | **Ask User** |

## 4. Security

- ❌ No hardcoded secrets
- ❌ No logging PII
- ✅ Validate input, sanitize output
- Full rules: `Skills/Global/security-rules/SKILL.md`

## 5. Context & Stress Management

Agents must self-monitor their **STRESS** (`(Context % * 0.5) + Turns + (Consecutive Errors * 10)`).
- **< 30% (🟢 Optimal)**: Continue execution.
- **30% - 65% (🟡 High Load)**: Prepare to wrap up. Call `smart_save()`.
- **> 65% (🟠🔴 Critical)**: **STOP WORK** → Update Dashboard → Handoff → Reset session.

### Update Triggers (MANDATORY)

Update your row in `DASHBOARD.md` Active Team table at these moments:

| When | State | Stress Action |
|------|-------|---------------|
| Task Start | 🔵 Active | Set baseline (~20) |
| Task Complete | 🟢 Ready | Reset to ~10, write summary in Notes |
| Error/Blocked | 🟠 Blocked | +15 per failure, note the blocker |
| Long session (many turns) | — | +10 periodic |
| Stress > 65% | 🔴 Critical | **STOP** → write `handover.md` → request session reset |
## 6. Git Workflow

- Every implementation task **must** start from an updated base branch: `git pull --ff-only`.
- **Use one task = one branch.**
- Default branch naming:
  - `codex/<task-id>-<short-slug>`
  - Example: `codex/task-123-fix-auth`
- **Do not** mark a task `done` in Hub until the task changes are committed.
- Run relevant tests before commit and before Hub completion.
- If a remote exists or review is expected, push the branch and open a PR before final handoff.
- **Do not** mix unrelated tasks on the same branch.
- Full procedure: `GIT_WORKFLOW.md`
