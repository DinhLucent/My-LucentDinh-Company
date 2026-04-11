window.promptRegistry = window.promptRegistry || [];

window.promptRegistry.push({
    id: "review_pr",
    title: "Review Pull Request",
    category: "Review",
    tags: ["PR", "review", "audit"],
    description: "Đánh giá chi tiết một PR về tính đúng đắn và kiến trúc.",
    fields: [
        { id: "pr_goal", label: "Mục tiêu PR", type: "text", required: true },
        { id: "concerns", label: "Điểm cần soi kỹ", type: "list", placeholder: "Ví dụ: performance, security, logic..." },
        { id: "strictness", label: "Mức độ khắt khe", type: "select", options: ["Thoải mái (Nitpick only)", "Tiêu chuẩn (Maintainability)", "Sát sao (Correctness critical)"], default: "Tiêu chuẩn (Maintainability)" }
    ],
    template: `Hãy review PR này như một senior reviewer với thái độ: {{strictness}}.

Mục tiêu PR: {{pr_goal}}

Tôi muốn bạn tập trung vào:
{{concerns}}

Hãy thực hiện:
1. Tóm tắt PR đang thay đổi điều gì
2. Xác định intent thực sự của thay đổi
3. Chỉ ra rủi ro logic và rủi ro kiến trúc
4. Chỉ ra những chỗ thiếu test hoặc có nguy cơ regression
5. Nêu phần nào ổn và phần nào bắt buộc sửa trước khi merge.`
});

window.promptRegistry.push({
    id: "review_arch",
    title: "Review Kiến Trúc Tổng Thể",
    category: "Review",
    tags: ["architecture", "audit", "debt"],
    description: "Technical reviewer đánh giá 'mùi' kiến trúc và nợ kỹ thuật.",
    template: `Hãy review kiến trúc hiện tại của repo này như một technical reviewer.

Tôi muốn bạn đánh giá:
1. Hệ thống hiện tại đang làm được gì tốt nhất?
2. Điểm mạnh kiến trúc là gì?
3. Nợ kỹ thuật (Tech debt) lớn nhất nằm ở đâu?
4. Chỗ coupling cao nhất hoặc khó test nhất?
5. Cái gì nên giữ nguyên, cái gì nên refactor trước?

Đầu ra:
- Báo cáo Strengths & Weaknesses
- Danh sách top priorities cần cải thiện
- Kế hoạch refactor theo 3 mức: nhỏ / vừa / lớn.`
});
