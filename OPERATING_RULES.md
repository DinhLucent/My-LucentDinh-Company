# ⚖️ Operating Rules

> Rules unique to this team. Focus on communication, security, and the V2 automated workflow.

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
- **30% - 65% (🟡 High Load)**: Prepare to wrap up.
- **> 65% (🟠🔴 Critical)**: **STOP WORK** → Handoff → Reset session.

## 6. Git Workflow

- Every implementation task **must** start from an updated base branch: `git pull --ff-only`.
- **Use one task = one branch.**
- Default branch naming:
  - `codex/<task-id>-<slug>`
  - Example: `codex/TASK-001-fix-auth`
- Run relevant tests before commit and before marking the task as complete in the orchestrator.
- Always push the branch and open a PR before final completion of major features.
- **Do not** mix unrelated tasks on the same branch.
- Full procedure: `GIT_WORKFLOW.md`
