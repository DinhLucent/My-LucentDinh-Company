# Agents-of-SHIELD

Control plane cục bộ để đưa một “đội AI” vào dự án phần mềm theo quy trình có packet, verifier, retry và task state rõ ràng.

## Nếu bạn hoàn toàn mới, hãy làm theo đúng 5 bước này

1. Compile knowledge và indexes:

```bash
python run_orchestrator.py compile
```

2. Copy mẫu task từ [templates/task.yaml](templates/task.yaml).
3. Điền task thật của bạn, đặc biệt là:
   - `title`
   - `description`
   - `inputs.related_paths`
   - `acceptance_criteria`
   - `metadata.execution.primary_commands`
4. Xem packet và runtime plan trước khi chạy:

```bash
python run_orchestrator.py plan path/to/task.yaml
```

5. Chạy end-to-end:

```bash
python run_orchestrator.py run path/to/task.yaml
```

Nếu bạn chỉ nhớ một điều: `plan` để preview, `run` để execute thật.

---

## Hệ thống này làm gì?

Khi bạn chạy một task, control plane sẽ đi theo flow:

```text
task.yaml
  -> classify
  -> route
  -> build task packet
  -> execute
  -> verify
  -> retry nếu fail
  -> complete hoặc escalate
```

Hệ thống không còn chỉ là handbook markdown. Ở HEAD hiện tại, nó đã có:

- compile layer sinh indexes và fragments
- orchestrator có execution loop thật
- verifier runners thật
- retry packet augmentation thật
- task state machine thật
- CLI `run` đi qua loop execution/verification/retry

---

## Khi đưa hệ thống vào một dự án mới, nên làm gì?

Đây là quy trình thực dụng nhất cho một người chưa biết gì:

### Bước 1: hiểu repo và compile

Chạy:

```bash
python run_orchestrator.py compile
```

Việc này sẽ sinh:

- `role_index.json`
- `skill_index.json`
- `project_index.json`
- `module_index.json`
- `dashboard_snapshot.json`
- các file trong `knowledge/compiled/context_fragments/`

### Bước 2: bắt đầu bằng một task nhỏ và an toàn

Đừng bắt đầu bằng task lớn. Hãy dùng một task kiểu:

- tạo report nhỏ
- chạy test/lint cụ thể
- sửa một file
- tạo một output file chứng minh executor đang chạy đúng

Mục tiêu của task đầu tiên là xác nhận:

- packet có gọn không
- command có chạy được không
- verifier có pass/fail đúng không
- metrics có được ghi không

### Bước 3: viết task contract rõ ràng

Task tối thiểu cần có:

- file/module liên quan
- điều kiện hoàn thành rõ
- command thực thi rõ

Ví dụ ngắn:

```yaml
schema_version: "2.1"
id: TASK-001
title: Generate a small project status file
description: >
  Create a proof file in runtime/sessions so we can validate the execution loop.
assigned_role: backend
priority: medium
status: queued
domain: general

inputs:
  related_paths:
    - control_plane/orchestrator.py
  related_tests: []
  related_handoffs: []
  related_logs: []
  related_modules:
    - control_plane

constraints:
  - keep_packet_small

acceptance_criteria:
  - proof file created

metadata:
  created_by: user
  created_at: "2026-04-12T00:00:00Z"
  execution:
    primary_commands:
      - "New-Item -ItemType Directory -Force -Path 'runtime\\sessions' | Out-Null"
      - "Set-Content -Path 'runtime\\sessions\\proof.txt' -Value 'ok' -Encoding utf8"
    output_files:
      - runtime/sessions/proof.txt
```

Lưu ý:

- executor hiện tại là `command-driven`
- muốn task chạy thật tốt, bạn phải khai báo `metadata.execution`
- nếu muốn retry làm khác attempt đầu, thêm `retry_commands`

### Bước 4: preview trước, chạy sau

Preview:

```bash
python run_orchestrator.py plan path/to/task.yaml
```

Bạn nên kiểm:

- `execution_mode`
- `task_packet_path`
- packet có kéo đúng `files`, `tests`, `context_fragments`

Sau đó mới chạy:

```bash
python run_orchestrator.py run path/to/task.yaml
```

### Bước 5: đọc artifacts sau khi chạy

Sau một lần `run`, bạn nên xem:

- `runtime/state/task_packets/`
- `runtime/state/agent_runs/`
- `runtime/state/verification_reports/`
- `runtime/reports/metrics/`
- `.hub/done/`
- `.hub/handoffs/` nếu task fail hoặc cần escalate

---

## `plan` và `run` khác nhau thế nào?

### `plan`

`plan` chỉ:

- classify
- route
- decide execution mode
- retrieve context
- build packet
- build runtime plan

Nó không execute command, không chạy verifier, không retry.

### `run`

`run` là flow thật:

- prepare task
- execute command theo `metadata.execution`
- run verifier
- nếu fail thì sinh retry packet
- retry trong giới hạn cho phép
- complete hoặc fail/escalate

---

## Hệ thống ghi ra những gì?

### Packet

Task packet nằm ở:

```text
runtime/state/task_packets/
```

Packet chứa:

- summary task
- role
- rules ngắn
- fragments liên quan
- files liên quan
- tests liên quan

### Execution report

Execution report nằm ở:

```text
runtime/state/agent_runs/
```

Nó ghi:

- commands đã chạy
- return code
- changed files
- output files
- stack trace nếu fail

### Verification report

Verification report nằm ở:

```text
runtime/state/verification_reports/
```

Nó ghi:

- các check đã chạy
- pass/fail
- `next_context_needs`
- `recommended_next_role`

### Metrics

Metrics nằm ở:

```text
runtime/reports/metrics/
```

Các số quan trọng:

- `packet_size`
- `loaded_file_count`
- `retry_count`
- `verifier_status`
- `execution_mode`

### Task state

State machine ghi vào:

- `runtime/state/active_tasks/`
- `.hub/active/`
- `.hub/done/`
- `.hub/handoffs/`

---

## Cấu trúc repo nào quan trọng nhất?

```text
control_plane/
  classifier/          classify task
  router/              choose role + parallel mode
  retriever/           select fragments/files/tests
  context_builder/     build task packet
  execution/           runtime planner + executor + state machine
  verifier/            acceptance/lint/typecheck/test/security
  hooks/               retry/handoff hooks

templates/
  task.yaml
  task_packet.json
  verification_report.json
  module_index.json

runtime/
  state/
  reports/
  cache/

.hub/
  active/
  done/
  handoffs/
```

---

## Các lệnh cần nhớ

```bash
python run_orchestrator.py compile
python run_orchestrator.py plan path/to/task.yaml
python run_orchestrator.py run path/to/task.yaml
```

Nếu bạn quen dùng `make`:

```bash
make compile
make plan TASK=path/to/task.yaml
make orchestrate-task TASK=path/to/task.yaml
```

---

## Hệ thống này chưa làm gì?

Để tránh kỳ vọng sai:

- nó chưa phải agent “tự hiểu mọi task” không cần execution contract
- nó chưa thay thế hoàn toàn việc thiết kế task rõ ràng
- chất lượng runtime vẫn phụ thuộc:
  - `metadata.execution`
  - test harness của repo
  - acceptance criteria

Nói ngắn:

- kiến trúc runtime đã khép vòng
- độ mượt production phụ thuộc chất lượng task contract

---

## Manual Task Hub mode còn dùng không?

Còn, nhưng không phải đường nhanh nhất cho người mới.

Repo này vẫn có:

- `manifest.yaml`
- `OPERATING_RULES.md`

Những file đó phù hợp hơn với mode vận hành “mở nhiều session agent thủ công”.

Nếu bạn là người mới và chỉ muốn dùng hệ thống ngay:

- bắt đầu bằng `compile`
- viết `task.yaml`
- dùng `plan`
- dùng `run`

Đó là entrypoint đúng với control plane hiện tại.

---

## Nên đọc file nào tiếp theo?

- [CHEATSHEET.md](CHEATSHEET.md): bản cực ngắn cho người mới
- [templates/task.yaml](templates/task.yaml): mẫu task chuẩn
- [OPERATING_RULES.md](OPERATING_RULES.md): nguyên tắc vận hành (V2)
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md): quy trình Git cho orchestrator
