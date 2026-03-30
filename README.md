# 🏢 LucentDinhCompany — Trung Tâm Điều Hành Agent AI

> **Mục tiêu:** Biến session AI của bạn thành một phòng ban phát triển phần mềm chuyên nghiệp.
> **Version:** 3.1 | **Framework:** Diamond Standard + Task Hub

---

## Mục lục

1. [Tổng quan](#1-tổng-quan)
2. [Kiến trúc hệ thống](#2-kiến-trúc-hệ-thống)
3. [Task Hub — Cách Agent giao tiếp](#3-task-hub--cách-agent-giao-tiếp)
4. [Quy trình End-to-End](#4-quy-trình-end-to-end)
5. [Bắt đầu sử dụng](#5-bắt-đầu-sử-dụng)
6. [Đội ngũ AI & Slash Commands](#6-đội-ngũ-ai--slash-commands)
7. [Nguyên tắc cốt lõi](#7-nguyên-tắc-cốt-lõi)

---

## 1. Tổng quan

**LucentDinhCompany** là **Trụ sở chính (HQ)** của một đội ngũ AI Agent chuyên nghiệp. Thay vì một AI đơn lẻ làm mọi việc, hệ thống cung cấp **27 "nhân viên" AI** với Persona và kỹ năng riêng biệt.

Bạn vẫn là CEO — người ra quyết định cuối cùng.

- **Task Hub**: Trung tâm giao tiếp duy nhất — Agent tự lấy task đúng role
- **Role Enforcement**: Sai role → Agent bị từ chối, không thực hiện
- **Session Recovery**: AI mới vào đọc Dashboard 10 giây nắm ngay bối cảnh
- **Compact Reporting**: Sơ lược cho AI, chi tiết cho CEO

---

## 2. Kiến trúc hệ thống

```
LucentDinhCompany/
├── manifest.yaml           ← Sổ cái nhân sự (Agent → Persona → Skills)
├── DASHBOARD.md            ← 📊 Quick Context + Task Board + Timeline
├── ONBOARDING.md           ← Checklist nhận việc cho Agent mới
├── OFFBOARDING.md          ← Checklist sa thải / rút lui Agent
├── RECRUITMENT.md          ← Quy trình thuê Agent mới
├── OPERATING_RULES.md      ← Quy tắc vận hành (tóm tắt)
├── .hub/                   ← 🏗️ TASK HUB
│   ├── backlog.yaml        ← Hàng đợi task (gán theo role)
│   ├── active/             ← Task đang thực hiện
│   ├── done/               ← Báo cáo chi tiết cho CEO
│   └── handoffs/           ← Chuyển giao giữa Agent
├── Skills/
│   ├── Global/             ← Skills chung (task-hub, security, evolution...)
│   └── Roles/              ← Skills chuyên môn theo phòng ban
└── templates/              ← Khuôn mẫu task, handoff, skill
```

---

## 3. Task Hub — Cách Agent giao tiếp

### Agent KHÔNG nói chuyện trực tiếp

```
       ┌──────────────┐
       │   TASK HUB   │
       │ backlog.yaml │
       │ DASHBOARD.md │
       └──────┬───────┘
    ┌─────────┼───────────┐
┌───▼───┐ ┌──▼────┐ ┌───▼──────┐
│  CTO  │ │Backend│ │ Security │
└───────┘ └───────┘ └──────────┘
Tất cả đọc/ghi vào Hub. Không có đường nối ngang.
```

### Luồng hoạt động

```
1. User/Producer tạo task → backlog.yaml (gán assigned_role)
2. Agent mở session → Đọc Dashboard → Đọc backlog → Tìm task đúng role
3. Agent claim → Thực hiện → Cập nhật Dashboard (1 dòng)
4. Agent tạo handoff file → Task mới cho Agent tiếp theo
5. ❌ User KHÔNG cần copy-paste giữa session
```

### Quy tắc nghiêm ngặt

- ✅ `assigned_role` = Agent ID của bạn → ĐƯỢC nhận
- ❌ `assigned_role` ≠ Agent ID → **PHẢI TỪ CHỐI**, không thực hiện dù 1 dòng
- ❌ Không có task phù hợp → Báo User: "Không có task cho role của tôi"

### Khi session bị kill / đổi AI

AI mới vào → Đọc `DASHBOARD.md` (Quick Context) → Backlog → Handoffs → Bắt đầu làm. Không cần User giải thích lại.

> 📖 Chi tiết protocol: `Skills/Global/task-hub/SKILL.md`

---

## 4. Quy trình End-to-End

```
[⬜ PLAN] → [⬜ DESIGN] → [⬜ IMPLEMENT] → [⬜ REVIEW] → [⬜ RELEASE]
```

| Phase | Ai làm | Kết quả |
|-------|--------|---------|
| **PLANNING** | Producer/PM | Tạo tasks vào Hub, gán role |
| **DESIGN** | CTO | Kiến trúc, API contract, ADR |
| **IMPLEMENT** | Backend/Frontend | Code + Test, lấy task từ Hub |
| **REVIEW** | Lead + Security + QA | Code review, security scan, gate check |
| **RELEASE** | Release Manager + DevOps | Build, deploy, monitor |

### Task Lifecycle

```
TODO → CLAIMED → IN_PROGRESS → IN_REVIEW → DONE
```

### Báo cáo: 2 tầng

| Tầng | Nơi lưu | Cho ai | Dung lượng |
|------|---------|--------|-----------|
| Sơ lược | `DASHBOARD.md` | AI khác | 1 dòng |
| Chi tiết | `.hub/done/TASK-xxx.md` | CEO | Đầy đủ |

> 📖 Chi tiết rules: `OPERATING_RULES.md` (50 dòng)

---

## 5. Bắt đầu sử dụng

### Bước 1: Clone vào dự án

```bash
git clone https://github.com/<your-username>/LucentDinhCompany.git .agents-skills
```

### Bước 2: Chọn đội hình

| Quy mô | Đội hình |
|--------|---------|
| Nhỏ | `fullstack-agent` + `qa-lead-agent` + `security-agent` |
| Trung bình | + `cto-agent` + `producer-agent` + `frontend-agent` |
| Lớn | Full team (active agents trong manifest) |

### Bước 3: Khởi chạy

| Trạng thái | Chạy | Kết quả |
|-----------|------|---------|
| Chỉ có ý tưởng | `/brainstorm` | Cụ thể hóa |
| Có concept | `/map-systems` | Phân rã module |
| Có thiết kế | `/sprint-plan` | Tasks vào Hub |
| Có code sẵn | `/project-stage-detect` | Phân tích phase |

### Bước 4: Thực thi

```
Mở session Agent → Agent tự đọc Hub → Lấy task đúng role → Thực hiện → Cập nhật Dashboard
Mở session Agent khác → Agent đọc Hub → Thấy handoff → Tiếp tục → Không cần copy-paste
```

---

## 6. Đội ngũ AI & Slash Commands

### Agents theo Tier

```
Tier 1 — Leadership (Opus / GPT-4o)
  CTO • Technical Director • Producer

Tier 2 — Department Leads (Sonnet / GPT-4o-mini)
  Product Manager • Lead Programmer • QA Lead • UX Designer • Release Manager

Tier 3 — Specialists (Sonnet / Gemini Flash)
  Backend • Frontend • Fullstack • AI • Network • Tools • UI
  Security • DevOps • Data Engineer

Tier 4 — Executors (Haiku / Flash)
  QA Tester • Community Manager • Analytics Engineer
```

### Chuỗi chỉ huy

```
Bạn (CEO)
  ├── CTO → Tech Director → Lead Programmer → Developers
  ├── Product Manager → UX Designer
  ├── Producer → Phối hợp toàn bộ
  └── QA Lead → QA Tester
```

### Slash Commands chính

| Category | Commands |
|----------|---------|
| **Khởi chạy** | `/start` `/project-stage-detect` `/gate-check` |
| **Thiết kế** | `/brainstorm` `/design-system` `/map-systems` `/prototype` |
| **Code** | `/code-review` `/api-design` `/db-review` `/tech-debt` `/perf-profile` |
| **Sprint** | `/sprint-plan` `/estimate` `/retrospective` `/release-checklist` `/changelog` |
| **Team** | `/team-feature` `/team-backend` `/team-frontend` `/team-ui` `/team-release` |
| **Security** | `/deep-scan` `/secret-audit` `/threat-model` |

---

## 7. Nguyên tắc cốt lõi

- **Bạn luôn là CEO** — Agents đề xuất, bạn quyết định
- **Task Hub là Single Source of Truth** — Mọi task qua Hub
- **Diamond Standard** — Output rõ ràng, có cấu trúc, chuyên nghiệp
- **Verify trước Done** — Review trước Merge — Test trước Deploy
- **STRESS Monitoring** — Tự theo dõi mức bộ ngộp context và độ mệt mỏi của Agent

### Tài liệu tham khảo

| File | Nội dung |
|------|----------|
| `OPERATING_RULES.md` | Quy tắc vận hành (50 dòng) |
| `ONBOARDING.md` | Checklist nhận việc (30 dòng) |
| `RECRUITMENT.md` | Quy trình thuê Agent mới |
| `Skills/Global/task-hub/SKILL.md` | Protocol Hub chi tiết |

---
*Chúc bạn xây dựng được đội ngũ AI hùng mạnh! 🚀*
