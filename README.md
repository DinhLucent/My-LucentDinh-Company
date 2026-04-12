<div align="center">

# 🛡️ Agents-of-SHIELD

### **Autonomous Development Orchestrator**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Architecture](https://img.shields.io/badge/Architecture-V2_Control_Plane-00D4AA)](control_plane/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

*A local, CLI-driven control plane that routes tasks to specialized agent roles<br>and executes them in a strict **compile → plan → execute → verify** loop.*

</div>

---

## Overview

Agents-of-SHIELD replaces manual task management with an automated orchestration engine. Define a task in YAML, and the system classifies it, assigns the right agent role, executes commands locally, verifies the output, and retries or hands off on failure — all without manual intervention.

```
Task YAML → Classifier → Router → Context Builder → Executor → Verifier → Done/Retry
```

---

## Quick Start

```bash
# 1. Compile knowledge indexes (roles, skills, modules, docs)
python run_orchestrator.py compile

# 2. Preview how a task will be routed and packaged
python run_orchestrator.py plan path/to/task.yaml

# 3. Execute end-to-end (execute → verify → retry → finalize)
python run_orchestrator.py run path/to/task.yaml
```

### Defining a Task

Copy `templates/task.yaml` and fill in:

```yaml
id: TASK-2026-001
title: "Fix validation in login endpoint"
assigned_role: backend
acceptance_criteria:
  - "email format validated before save"
  - "clear error messages returned"
metadata:
  execution:
    primary_commands:
      - "python -m pytest tests/api/test_login.py"
    output_files:
      - src/api/auth/login.py
```

> **Key rule:** Without `metadata.execution.primary_commands`, the task won't execute. These are the real shell commands the agent runs.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    run_orchestrator.py                       │
│                  compile │ plan │ run                        │
└──────────────┬──────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────┐
│                     control_plane/                           │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌───────────────────────┐  │
│  │ Classifier │→ │   Router   │→ │   Context Builder     │  │
│  │ task type  │  │ role match │  │ packet + budget        │  │
│  └────────────┘  └────────────┘  └───────────┬───────────┘  │
│                                               │              │
│  ┌────────────────────────────────────────────▼───────────┐  │
│  │              Execution Engine                          │  │
│  │  AgentExecutor → TaskStateMachine → Verifier           │  │
│  │  (commands)      (state tracking)   (lint/test/accept) │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │  Hooks      │  │   Metrics    │  │  Retry / Handoff   │  │
│  │ pre/post    │  │  per-task    │  │  auto-escalation   │  │
│  └─────────────┘  └──────────────┘  └────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

| Component | Role |
|-----------|------|
| **Classifier** | Determines task type, priority, and domain |
| **Router** | Maps task to agent role from `manifest.yaml` |
| **Context Builder** | Assembles a stateless Task Packet with relevant code/docs |
| **Executor** | Runs shell commands locally, tracks file changes |
| **Verifier** | Checks acceptance criteria, lint, typecheck, security |
| **State Machine** | Manages `queued → executing → verifying → completed/failed` |
| **Retry Hook** | On verification failure, builds targeted retry packet |
| **Handoff Hook** | On exhausted retries, creates handoff for another role |

---

## Project Structure

```
├── control_plane/           # Core orchestration engine
│   ├── classifier/          # Task classification
│   ├── router/              # Role routing + parallel policy
│   ├── context_builder/     # Packet assembly
│   ├── execution/           # Agent executor + state machine
│   ├── verifier/            # Acceptance, lint, test, security checks
│   ├── hooks/               # Pre-task, post-task, handoff, retry
│   ├── compiler/            # Knowledge index builders
│   └── contracts/           # JSON schema validation
├── templates/               # Task, packet, and report schemas
├── tests/fixtures/audit/    # Runnable audit fixtures (happy/retry/fail)
├── manifest.yaml            # Role + skill configuration
├── Skills/                  # Agent personas and skill definitions
├── knowledge/compiled/      # Generated indexes (gitignored, regenerable)
├── runtime/                 # Ephemeral execution state (gitignored)
└── run_orchestrator.py      # CLI entrypoint
```

---

## Audit Suite

Three runnable fixtures for system validation:

```bash
# Happy path — passes on first attempt
python run_orchestrator.py run tests/fixtures/audit/happy_path.yaml

# Retry scenario — fails once, passes on retry
python run_orchestrator.py run tests/fixtures/audit/retry_scenario.yaml

# Hard fail — exhausts retries, triggers handoff
python run_orchestrator.py run tests/fixtures/audit/hard_fail.yaml
```

---

## CLI Reference

| Command | Description |
|---------|-------------|
| `python run_orchestrator.py compile` | Build all knowledge indexes |
| `python run_orchestrator.py compile --include-pool` | Include `.skills_pool/` in skill index |
| `python run_orchestrator.py plan <task.yaml>` | Preview classification, routing, and packet |
| `python run_orchestrator.py run <task.yaml>` | Execute full lifecycle with verification |

---

## Documentation

| Document | Purpose |
|----------|---------|
| [CHEATSHEET.md](CHEATSHEET.md) | Quick reference for running tasks |
| [SYSTEM_AUDIT.md](SYSTEM_AUDIT.md) | Re-validation workflow after changes |
| [OPERATING_RULES.md](OPERATING_RULES.md) | Security and execution constraints |
| [GIT_WORKFLOW.md](GIT_WORKFLOW.md) | Git lifecycle conventions |
| [SOUL.md](SOUL.md) | Philosophy of constrained orchestration |
| [GENERAL.md](GENERAL.md) | Project onboarding guidelines |

---

<div align="center">

*Built for deterministic, auditable, autonomous development.*

</div>
