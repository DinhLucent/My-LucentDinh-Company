## Table of Contents

- [1) Debugging Task Lifecycle](#1-debugging-task-lifecycle)
    - [1.1 Task Packet Analysis](#11-task-packet-analysis)
    - [1.2 Execution Hook Failures](#12-execution-hook-failures)
- [2) Debugging Verification & Retry Loops](#2-debugging-verification--retry-loops)
    - [2.1 Verification Verdict Discrepancy](#21-verification-verdict-discrepancy)
    - [2.2 Retry Loop Stuck](#21-retry-loop-stuck)
- [3) Control Plane Maintenance](#3-control-plane-maintenance)
    - [3.1 Adding a New Verifier](#31-adding-a-new-verifier)
    - [3.2 Modifying Task State Machine](#32-modifying-task-state-machine)

---

# 1) Debugging Task Lifecycle

## 1.1 Task Packet Analysis
```text
Tôi đang debug một task packet bị sai lệch hoặc thiếu context.

Thông tin:
- Task ID: [ID]
- Classification: [module]
- Routing: [role]
- Vấn đề: [thiếu related_paths / sai role / budget sai / ...]

Hãy giúp tôi:
1. Xem lại log của `TaskClassifier` và `RoleRouter`
2. Kiểm tra `KnowledgeRetriever` có lấy đúng file context không
3. Chỉ ra chỗ nào trong `PacketBuilder` đang map metadata sai
4. Đề xuất cách sửa logic retrieval hoặc classification
```

## 1.2 Execution Hook Failures
```text
Một execution hook đang fail hoặc không trigger đúng.

Thông tin:
- Hook type: [PreTask / PostTask / OnHandoff / on_verification_fail]
- Hiện tượng: [không chạy / crash / output sai]

Hãy:
1. Truy ngược luồng gọi hook từ `orchestrator.py`
2. Kiểm tra state của `TaskStateMachine` tại thời điểm đó
3. Chỉ ra rào cản làm hook fail (ví dụ: lack of permissions, file locking, missing env)
4. Đề xuất patch nhỏ nhất cho hook logic
```

---

# 2) Debugging Verification & Retry Loops

## 2.1 Verification Verdict Discrepancy
```text
Verifier trả về kết quả không như kỳ vọng.

Thông tin:
- Check name: [acceptance / lint / typecheck / test / security]
- Expected result: [passed / failed]
- Actual result: [mô tả]
- Log: [dán vào]

Hãy giúp tôi:
1. Đọc code của runner tương ứng trong `control_plane/verifier/`
2. Xác định vì sao verifier lại skip hoặc fail sai chỗ
3. Kiểm tra logic `_derive_next_context_needs` xem có gợi ý đúng cho attempt sau không
4. Đề xuất sửa verifier hoặc sửa accept criteria
```

## 2.1 Retry Loop Stuck
```text
Task đang bị kẹt trong retry loop (max attempts reached hoặc loop vô tận).

Thông tin:
- Task ID: [ID]
- Attempts: [số attempt]
- Lỗi lặp lại: [mô tả]

Hãy:
1. Tìm điểm nondeterminism làm agent reproduce lỗi cũ
2. Xem lại logic `handle_verification_failure` và `on_verification_fail` hook
3. Kiểm tra xem packet mới có thực sự thêm context cần thiết không
4. Đề xuất chiến thuật "break the loop" (ví dụ: đổi role, giảm scope, hoặc manual pause)
```

---

# 3) Control Plane Maintenance

## 3.1 Adding a New Verifier
```text
Tôi muốn thêm một verifier mới vào hệ thống (ví dụ: performance check / documentation check).

Hãy:
1. Thiết kế contract cho verifier mới tuân thủ `control_plane.contracts`
2. Chỉ ra chỗ cần register verifier này trong `orchestrator.py`
3. Đề xuất logic `derive_next_context_needs` cho verifier này
4. Viết unit test cho verifier mới
```

## 3.2 Modifying Task State Machine
```text
Tôi muốn thêm một trạng thái mới hoặc rẽ nhánh mới trong task lifecycle.

Hành vi mới: [mô tả]

Hãy giúp tôi:
1. Cập nhật `TaskStateMachine` (trên disk và in-memory)
2. Cập nhật metric transition trong `RuntimeMetricsLogger`
3. Đảm bảo backward compatibility với các task log cũ
4. Đề xuất cách migration dashboard snapshot
```
