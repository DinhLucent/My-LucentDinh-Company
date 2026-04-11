PYTHON ?= python

.PHONY: compile compile-roles compile-docs compile-skills build-indexes dashboard-snapshot plan plan-task orchestrate orchestrate-task clean help

# ============================================================================
# Agents-of-SHIELD v2 - Local Control Plane
# ============================================================================

help: ## Show this help
	@echo.
	@echo   Agents-of-SHIELD v2 Control Plane
	@echo   ==================================
	@echo.
	@echo   make compile            Compile all knowledge indexes
	@echo   make plan               Build packet + runtime plan for default task
	@echo   make compile-roles      Compile manifest.yaml -> role_index.json
	@echo   make compile-docs       Compile markdown docs -> fragments
	@echo   make compile-skills     Compile Skills/ -> skill_index.json
	@echo   make build-indexes      Build module_index.json
	@echo   make dashboard-snapshot Parse DASHBOARD.md -> JSON snapshot
	@echo   make orchestrate        Execute default task end-to-end
	@echo   make plan-task          Build packet + runtime plan for TASK=path/to/task.yaml
	@echo   make orchestrate-task   Execute TASK=path/to/task.yaml end-to-end
	@echo   make clean              Remove generated runtime/compiled files
	@echo.

compile: ## Compile all knowledge source -> indexes
	$(PYTHON) run_orchestrator.py compile

plan: ## Build packet + runtime plan for default task
	$(PYTHON) run_orchestrator.py plan

compile-roles: ## Compile roles from manifest.yaml
	$(PYTHON) control_plane/compiler/compile_roles.py

compile-docs: ## Compile docs into JSON fragments
	$(PYTHON) control_plane/compiler/compile_docs.py

compile-skills: ## Compile skills from Skills/
	$(PYTHON) control_plane/compiler/compile_skills.py

build-indexes: ## Build module index from source tree
	$(PYTHON) control_plane/compiler/build_indexes.py

dashboard-snapshot: ## Parse DASHBOARD.md into JSON snapshot
	$(PYTHON) control_plane/compiler/dashboard_snapshot.py

orchestrate: ## Execute the default task end-to-end
	$(PYTHON) run_orchestrator.py run

plan-task: ## Build packet + runtime plan: make plan-task TASK=path/to/task.yaml
	$(PYTHON) run_orchestrator.py plan $(TASK)

orchestrate-task: ## Execute a specific task: make orchestrate-task TASK=path/to/task.yaml
	$(PYTHON) run_orchestrator.py run $(TASK)

clean: ## Remove all generated runtime/compiled files
	@if exist runtime\cache rd /s /q runtime\cache
	@if exist runtime\reports rd /s /q runtime\reports
	@if exist "runtime\state\task_packets" rd /s /q "runtime\state\task_packets"
	@if exist "runtime\state\verification_reports" rd /s /q "runtime\state\verification_reports"
	@if exist "runtime\state\agent_runs" rd /s /q "runtime\state\agent_runs"
	@if exist "runtime\state\active_tasks" rd /s /q "runtime\state\active_tasks"
	@if exist knowledge\compiled rd /s /q knowledge\compiled
	@echo Cleaned runtime and compiled artifacts.
