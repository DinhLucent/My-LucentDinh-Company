# CHEATSHEET

Mở file này khi bạn không biết bắt đầu từ đâu.

## Bắt đầu nhanh trong 60 giây

```bash
python run_orchestrator.py compile
python run_orchestrator.py plan path/to/task.yaml
python run_orchestrator.py run path/to/task.yaml
```

Thứ tự đúng là:

1. `compile`
2. viết task
3. `plan`
4. `run`
5. đọc artifacts

---

## Nếu bạn là người mới hoàn toàn

Hãy làm đúng 4 việc này:

1. Copy [templates/task.yaml](templates/task.yaml).
2. Điền `inputs.related_paths` và `acceptance_criteria`.
3. Thêm `metadata.execution.primary_commands`.
4. Chạy `plan` trước, `run` sau.

Nếu task không có `metadata.execution`, runtime có thể build packet được nhưng execution sẽ không làm việc hữu ích.

---

## Mẫu task ngắn nhất để smoke test

```yaml
schema_version: "2.1"
id: TASK-SMOKE-001
title: Create proof file
description: Create a small proof file to validate the execution loop.
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

---

## `plan` dùng khi nào?

Dùng `plan` khi bạn muốn kiểm:

- classifier có đúng không
- role/routing có đúng không
- packet có gọn không
- `execution_mode` là gì

`plan` không execute command.

---

## `run` dùng khi nào?

Dùng `run` khi bạn muốn:

- execute task thật
- chạy verifier
- tự retry nếu verify fail
- sinh state và reports đầy đủ

---

## Xem kết quả ở đâu?

### Packet

```text
runtime/state/task_packets/
```

### Execution reports

```text
runtime/state/agent_runs/
```

### Verification reports

```text
runtime/state/verification_reports/
```

### Metrics

```text
runtime/reports/metrics/
```

### Final task reports

```text
.hub/done/
```

### Failure escalations / handoffs

```text
.hub/handoffs/
```

---

## Khi nào biết task đã chạy ổn?

Bạn muốn thấy tối thiểu:

- `summary.agent_status = completed`
- `verification_report.status = passed`
- `retry_count = 0` cho happy path
- output file hoặc changed file đúng như mong đợi

---

## Khi verify fail thì làm gì?

Đừng sửa bừa ngay. Hãy xem:

1. `runtime/state/verification_reports/<TASK>.verification.json`
2. `next_context_needs`
3. `runtime/state/task_packets/<TASK>.retry-1.json`
4. `runtime/reports/metrics/<TASK>.metrics.json`

Nếu retry packet vẫn quá to hoặc sai trọng tâm, task contract hoặc retriever vẫn cần siết.

---

## 5 lỗi thường gặp

### 1. `run` không làm gì hữu ích

Nguyên nhân thường là task chưa có `metadata.execution.primary_commands`.

### 2. Packet quá to

Giảm:

- `related_paths`
- `related_modules`
- handoff không cần thiết

### 3. Verifier fail ngay lần đầu

Kiểm:

- `acceptance_criteria` có quá rộng không
- command có thực sự tạo output/changed files không

### 4. Retry không cải thiện

Kiểm:

- `next_context_needs` có đúng lỗi không
- `retry_commands` có khác `primary_commands` khi cần không

### 5. Không biết nên đọc file nào

Thứ tự đọc:

1. `README.md`
2. `templates/task.yaml`
3. `runtime/...` artifacts sau khi chạy

---

## Câu ngắn nhất để nhớ

```text
Compile -> Write task -> Plan -> Run -> Read reports
```
