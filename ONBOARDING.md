# 🚀 Agent Boot Sequence

> **10 steps. In order. No skipping.**

---

## 🗺️ ROADMAP (Memorize this — refer back when unsure)

```
BOOT:  1→2→⛔→3→4→5→⛔→6→7→8→9→⛔→10
WORK:  Claim → Execute → STRESS check → Report → Handoff → Dashboard
DONE:  Report + Handoff + Dashboard = Session complete
```

---

## BOOT

1. Read `manifest.yaml` → Find your Agent ID in `active_agents`
2. Read your Persona file (path in manifest `persona:` field)

⛔ **Say: "I am [agent-id], role [role-name]."**

3. Read `OPERATING_RULES.md` (Rules §1-5 + STRESS formula)
4. Read `Skills/Global/task-hub/SKILL.md` (Hub Protocol)
5. Read `Skills/Global/security-rules/SKILL.md`

⛔ **Say: "Rules loaded."**

6. Read each skill in your `skills:` list from manifest
7. Read `DASHBOARD.md` → project status
8. Check `.hub/handoffs/` → any handoff for you?
9. Read `.hub/backlog.yaml` → find task where `assigned_role` = you

⛔ **Say: "I will execute [TASK-ID]: [title]."**

10. Execute per task-hub protocol (Claim → Work → Complete)

---

## WORK RULES (keep visible throughout session)

- **STRESS** = `(Context% × 0.5) + Turns + (Errors × 10)`
- 🟢 <30% → Continue | 🟡 30-65% → Wrap up | 🔴 >65% → **STOP**
- Wrong role task → **REFUSE**
- No task found → Tell User

## SHUTDOWN (mandatory before session ends)

1. Report → `.hub/done/TASK-xxx.md`
2. Handoff → `.hub/handoffs/` (if next agent exists)
3. Dashboard → update Status (Stress %), Tasks, Timeline
