window.promptRegistry = window.promptRegistry || [];

window.promptRegistry.push({
    id: "test_plan",
    title: "Lập Test Plan cho Bug Fix",
    category: "Test",
    tags: ["QA", "testing", "bug-fix"],
    fields: [
        { id: "bug_desc", label: "Mô tả bug", type: "textarea", required: true },
        { id: "behavior", label: "Hành vi đúng", type: "text" }
    ],
    template: `Tôi chuẩn bị fix bug: {{bug_desc}}.

Hành vi đúng kỳ vọng: {{behavior}}

Hãy đề xuất test plan:
1. Test case nào tái hiện được bug cũ (Reproduce)?
2. Test case nào xác nhận behavior mới là đúng (Verification)?
3. Các case biên (Edge cases) cần lưu ý?
4. Nên viết unit, integration, hay e2e cho phần này?
5. Cần chuẩn bị test data tối thiểu như thế nào?`
});

window.promptRegistry.push({
    id: "test_coverage",
    title: "Đánh giá Coverage vùng sửa",
    category: "Test",
    fields: [
        { id: "file_path", label: "File/Module/Function", type: "text", required: true }
    ],
    template: `Tôi muốn biết vùng code {{file_path}} đã được test đủ chưa.

Hãy giúp tôi:
1. Xác định các behavior quan trọng nhất trong vùng này cần được bảo vệ
2. Chỉ ra các case (luồng chạy) quan trọng mà có thể đang thiếu test
3. Chỉ ra các case biên tiềm ẩn nguy cơ
4. Đề xuất danh sách test ưu tiên cao nhất cần bổ sung.`
});
