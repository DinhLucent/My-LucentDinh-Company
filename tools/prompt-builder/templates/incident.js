window.promptRegistry = window.promptRegistry || [];

window.promptRegistry.push({
    id: "incident_mgmt",
    title: "Xử lý Incident Production",
    category: "Incident",
    tags: ["incident", "hotfix", "ops"],
    fields: [
        { id: "symptoms", label: "Triệu chứng", type: "textarea", required: true },
        { id: "impact", label: "Mức độ ảnh hưởng", type: "text", placeholder: "Số lượng user, task bị lỗi..." },
        { id: "recent_changes", label: "Thay đổi gần đây", type: "text", placeholder: "Deploy/Config change..." }
    ],
    template: `Tôi đang xử lý một incident nghiêm trọng.

Thông tin:
- Triệu chứng: {{symptoms}}
- Mức độ ảnh hưởng: {{impact}}
- Thay đổi gần đây: {{recent_changes}}

Hãy giúp tôi:
1. Tạo timeline điều tra nhanh
2. Xác định vùng hệ thống đáng nghi nhất
3. Nêu 3 nguyên nhân gốc (Root cause) có xác suất cao nhất
4. Đề xuất các bước kiểm tra (Verify) theo thứ tự ưu tiên
5. Tách rõ mitigations tạm thời (giảm đau ngay) và root fix lâu dài.`
});

window.promptRegistry.push({
    id: "incident_hotfix",
    title: "Patch nóng (Hotfix) tối thiểu",
    category: "Incident",
    fields: [
        { id: "problem", label: "Sự cố", type: "text", required: true },
        { id: "constraints", label: "Ràng buộc hotfix", type: "text", default: "Không downtime, không đổi schema" }
    ],
    template: `Tôi cần một hotfix tối thiểu, an toàn và nhanh cho sự cố: {{problem}}.

Ràng buộc: {{constraints}}

Hãy:
1. Chỉ ra patch nhỏ nhất có thể giảm thiểu rủi ro ngay lập tức
2. Nêu rõ tradeoff/tác dụng phụ của patch này
3. Đề xuất cách verify sau khi deploy (Smoke test)`
});
