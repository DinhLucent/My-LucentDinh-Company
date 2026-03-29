# 🚪 OFFBOARDING — Quy trình Sa thải / Rút lui

> Sử dụng khi một Agent không còn cần thiết cho Phase tiếp theo (ví dụ: xong Code, chuyển sang Review) để tiết kiệm token và loại bỏ nhiễu.

## 📋 Checklist 4 Bước (Dành cho Agent)

Khi CEO yêu cầu sa thải (offboard) một Agent, hệ thống phải thực hiện 4 bước này:

- [ ] **1. Dọn dẹp Backlog (Handoff)**
  - Đảm bảo Agent chuẩn bị rời đi KHÔNG còn task ở trạng thái `IN_PROGRESS` (kiểm tra thư mục `.hub/active/`).
  - Nếu có: Viết file bàn giao vào `.hub/handoffs/` hoặc đổi `status` thành `todo` trong `.hub/backlog.yaml`.

- [ ] **2. Cập nhật Manifest**
  - Xóa dòng ID của Agent này khỏi danh sách `active_agents` trong `manifest.yaml`.

- [ ] **3. Cập nhật Đội hình (Dashboard)**
  - Xóa dòng của Agent khỏi bảng `Active Team (Roles)` trong `DASHBOARD.md`.

- [ ] **4. Ghi Log Nhân sự (HR Log)**
  - Thêm 1 dòng vào phần biến động nhân sự `HR Log` trong `DASHBOARD.md`.
  - _Ví dụ format: `[YYYY-MM-DD] CEO — ACTION: Offboarded [agent-id] (Hoàn thành nhiệm vụ Phase [phase-name])`_

---

## 💡 Hướng dẫn cho CEO

Khi bạn thấy một Agent đã rảnh việc và muốn rút họ ra khỏi dự án:

```text
"Dự án đã xong phase X. Hãy chạy quy trình OFFBOARDING cho [agent-id] theo OFFBOARDING.md nhé."
```

Hệ thống sẽ rà soát và cho Agent đó "nghỉ việc" an toàn. Khi cần lại, bạn có thể gọi quy trình `RECRUITMENT.md` để "Tuyển lại".
