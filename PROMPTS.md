## Table of Contents

- [0) Khối mở đầu dùng chung](#0-khối-mở-đầu-dùng-chung-cho-hầu-hết-session)
- [1) Hiểu hệ thống (Onboarding)](#1-khi-mới-vào-dự-án-và-muốn-hiểu-hệ-thống)
    - [1.1 Onboarding tổng quát](#11-onboarding-tổng-quát)
    - [1.2 Vẽ bản đồ kiến trúc](#12-vẽ-bản-đồ-kiến-trúc-hiện-tại)
    - [1.3 Tóm tắt repo cho người mới](#13-tóm-tắt-repo-cho-người-mới)
    - [1.4 Tìm chỗ đang rối](#14-tìm-đúng-chỗ-tôi-đang-rối)
- [2) Hiểu luồng chạy (Data Flow)](#2-khi-muốn-hiểu-luồng-chạy-thật)
    - [2.1 Truy luồng end-to-end](#21-truy-luồng-end-to-end)
    - [2.2 Tìm nơi quyết định logic](#22-tìm-nơi-quyết-định-logic)
    - [2.3 Tìm state machine](#23-tìm-state-machine)
- [3) Debug lỗi cụ thể](#3-khi-debug-lỗi-cụ-thể)
    - [3.1 Debug bug tổng quát](#31-debug-bug-tổng-quát)
    - [3.2 Debug lỗi compile/build](#32-debug-lỗi-compilebuild)
    - [3.3 Debug lỗi runtime](#33-debug-lỗi-runtime)
    - [3.4 Debug lỗi logic sai](#34-debug-lỗi-logic-sai-nhưng-không-crash)
    - [3.5 Debug test fail](#35-debug-test-fail)
    - [3.6 Debug flaky test](#36-debug-flaky-test)
- [4) Production Issue & Incident](#4-khi-xử-lý-production-issue-hoặc-incident)
    - [4.1 Điều tra incident](#41-điều-tra-incident)
    - [4.2 Patch nóng tối thiểu](#42-patch-nóng-tối-thiểu)
- [5) Review kiến trúc](#5-khi-muốn-review-kiến-trúc-hiện-tại)
- [6) Refactor](#6-khi-muốn-refactor-nhưng-chưa-muốn-rewrite)
- [7) Redesign & Nâng cấp (V2)](#7-khi-muốn-thiết- kế-lại-hoặc-nâng-cấp-hệ-thống)
- [8) Review PR & Branch](#8-khi-xử-lý-pr-branch-hoặc-review-code)
- [9) Giao việc (Task Spec)](#9-khi-muốn-giao-việc-cho-người-khác)
- [11) Thêm test](#11-khi-muốn-thêm-test-đúng-cách)
- [12) Performance](#12-khi-muốn-cải-thiện-performance)
- [13) Dependency & Migration](#13-khi-muốn-xử-lý-dependency-hoặc-migration)
- [14) Tài liệu kỹ thuật](#14-khi-muốn-viết-tài- liệu-kỹ-thuật)
- [15) Giao tiếp trong team](#15-khi-cần-giao-tiếp-ngắn-trong-team)
- [16) Khi bị rối / Chưa biết hỏi gì](#16-khi-bạn-không-biết-nên-hỏi-gì-trước)

---

# 0) Khối mở đầu dùng chung cho hầu hết session

Dán khối này lên đầu trước khi dùng các prompt bên dưới.

```text
Bối cảnh:
- Dự án/repo: [tên repo hoặc mô tả ngắn]
- Mục tiêu hệ thống: [hệ thống này dùng để làm gì]
- Vai trò của tôi: [owner / contributor / reviewer / maintainer]
- Trạng thái hiện tại: [đã chạy được gì, đang kẹt gì]
- Giới hạn: [không rewrite toàn bộ / ưu tiên patch nhỏ / cần giữ backward compatibility / không đổi public API / ...]
- Kết quả tôi muốn từ session này: [ví dụ: hiểu kiến trúc / sửa lỗi / ra spec / review PR]

Nguyên tắc làm việc trong session này:
- Ưu tiên đọc code thật, không đoán
- Nói rõ file/function/module liên quan
- Nếu có assumption thì ghi rõ assumption
- Nếu phát hiện bug hoặc mùi kiến trúc thì nêu sớm
- Không redesign toàn bộ nếu chưa cần
```

---

# 1) Khi mới vào dự án và muốn hiểu hệ thống

## 1.1 Onboarding tổng quát

```text
Tôi sắp tham gia tiếp tục phát triển repo này.

Hãy giúp tôi onboarding kỹ thuật theo hướng thực chiến.

Việc cần làm:
1. Repo này giải bài toán gì
2. Kiến trúc tổng thể gồm những khối nào
3. Entry points chính nằm ở đâu
4. Luồng chạy end-to-end đi qua những file nào
5. Module nào là lõi, module nào là phụ trợ
6. Nếu tôi muốn sửa feature [tên feature], tôi nên đọc file nào trước
7. Nếu tôi muốn debug issue production, tôi nên bắt đầu từ đâu

Đầu ra tôi muốn:
- một bản mental model ngắn gọn của hệ thống
- danh sách module quan trọng nhất
- thứ tự đọc code đề xuất cho người mới
```

## 1.2 Vẽ bản đồ kiến trúc hiện tại

```text
Tôi muốn bạn giúp tôi lập bản đồ kiến trúc hiện tại của repo này.

Hãy làm theo thứ tự:
1. Xác định entrypoints
2. Xác định các module lõi
3. Vẽ luồng dữ liệu và luồng control
4. Chỉ ra state machine / orchestrator / executor / verifier / adapters nằm ở đâu
5. Nêu module nào đang đóng vai trò "core kernel"
6. Nêu module nào chỉ là glue code

Đầu ra mong muốn:
- kiến trúc theo từng khối
- trách nhiệm của từng khối
- file chính cho mỗi khối
```

## 1.3 Tóm tắt repo cho người mới

```text
Hãy giải thích repo này như thể tôi là người mới tham gia team nhưng cần lên việc rất nhanh.

Tôi không muốn giải thích chung chung.
Hãy bám vào codebase và trả lời:
1. Hệ thống này làm gì
2. Nó chạy như thế nào
3. Thành phần nào bắt buộc phải hiểu trước
4. Những chỗ dễ nhầm hoặc dễ làm hỏng nhất là gì
5. Nếu chỉ có 1 giờ để đọc code, tôi nên đọc gì trước

Đầu ra:
- summary ngắn
- top 10 file cần đọc
- các khái niệm cốt lõi cần nắm
```

## 1.4 Tìm đúng chỗ tôi đang rối

```text
Tôi là người đã build hoặc đã làm với hệ thống này, nhưng hiện tại tôi đang bị rối.

Tôi không muốn code ngay.
Tôi muốn bạn giúp tôi gỡ rối hệ thống.

Hãy làm:
1. Xác định mental model đúng của hệ thống
2. Nêu phần nào là control flow chính
3. Nêu phần nào là stateful
4. Nêu phần nào là business logic thật
5. Nêu phần nào là code phụ trợ hoặc workaround
6. Chỉ ra 3 điểm dễ gây rối nhất khi đọc repo này

Đầu ra:
- bản đồ hiểu hệ thống
- 3 nguồn gây rối chính
- bước tiếp theo tốt nhất để giảm độ rối
```

---

# 2) Khi muốn hiểu luồng chạy thật

## 2.1 Truy luồng end-to-end

```text
Tôi muốn truy luồng chạy thực tế của tác vụ sau:

Tác vụ/điểm vào:
- [CLI command / API endpoint / background job / webhook / function]

Hãy làm theo thứ tự:
1. Xác định entrypoint chính xác
2. Liệt kê các function/module được gọi tiếp theo
3. Chỉ ra chỗ đổi state
4. Chỉ ra chỗ gọi external dependency
5. Chỉ ra chỗ tạo output/artifact
6. Chỉ ra chỗ verify hoặc finalize

Đầu ra:
- flow từng bước
- file/function tương ứng
- các điểm rẽ nhánh quan trọng
```

## 2.2 Tìm nơi quyết định logic

```text
Tôi muốn biết logic quyết định thực sự nằm ở đâu trong hệ thống này.

Hãy phân biệt rõ:
- orchestration logic
- business logic
- state transition logic
- retry/error handling logic
- adapter/integration logic

Với mỗi loại, hãy chỉ ra:
- module chính
- file chính
- function quan trọng nhất
- vì sao nó là điểm quyết định
```

## 2.3 Tìm state machine

```text
Tôi nghi hệ thống này có state machine hoặc lifecycle phức tạp.

Hãy giúp tôi:
1. Tìm các trạng thái chính
2. Tìm nơi định nghĩa hoặc ngầm định các trạng thái đó
3. Tìm event hoặc điều kiện làm đổi trạng thái
4. Tìm guard condition
5. Chỉ ra chỗ nào transition không rõ ràng hoặc nguy hiểm

Đầu ra:
- danh sách state
- transition map
- chỗ cần làm rõ hoặc chuẩn hóa
```

---

# 3) Khi debug lỗi cụ thể

## 3.1 Debug bug tổng quát

```text
Tôi muốn debug một lỗi cụ thể, không redesign hệ thống lúc này.

Thông tin:
- Hiện tượng: [mô tả bug]
- Hành vi kỳ vọng: [mô tả đúng]
- Cách tái hiện: [steps]
- Log/error nếu có: [dán vào]
- Phạm vi nghi ngờ: [nếu có]

Hãy làm theo thứ tự:
1. Xác định luồng code liên quan trực tiếp
2. Nêu 3-5 giả thuyết lỗi theo xác suất
3. Chỉ ra file/function cần đọc trước
4. Nêu patch nhỏ nhất hợp lý
5. Nêu rủi ro regression
6. Nếu cần, đề xuất test nên thêm

Ưu tiên:
- patch nhỏ
- đúng chỗ
- giữ nguyên kiến trúc hiện tại nếu có thể
```

## 3.2 Debug lỗi compile/build

```text
Tôi đang bị lỗi compile/build.

Thông tin:
- Command: [lệnh]
- Output lỗi: [dán log]
- Thay đổi gần đây: [commit/PR/thao tác gần nhất]
- Kỳ vọng: [build phải pass]

Hãy làm:
1. Phân loại lỗi theo nguyên nhân có thể
2. Xác định file/module liên quan trực tiếp
3. Chỉ ra nguyên nhân gốc có khả năng cao nhất
4. Đề xuất patch hoặc cách fix tối thiểu
5. Chỉ ra cách xác nhận đã fix đúng

Đừng trả lời chung chung. Bám vào log và code.
```

## 3.3 Debug lỗi runtime

```text
Tôi đang bị lỗi runtime.

Thông tin:
- Trigger: [điều gì làm lỗi xuất hiện]
- Stack trace/log: [dán vào]
- Input gây lỗi: [nếu có]
- Hành vi kỳ vọng: [mô tả]

Hãy:
1. Xác định đường đi từ input tới chỗ crash
2. Nêu điều kiện tiền đề gây ra crash
3. Tìm chỗ thiếu validation / invariant / guard
4. Đề xuất patch nhỏ nhất
5. Đề xuất test để khóa lỗi này về sau
```

## 3.4 Debug lỗi logic sai nhưng không crash

```text
Hệ thống không crash nhưng hành vi sai.

Thông tin:
- Hành vi hiện tại: [mô tả]
- Hành vi đúng: [mô tả]
- Case tái hiện: [input / scenario]
- Vùng code nghi ngờ: [nếu có]

Hãy:
1. Tìm nơi ra quyết định logic
2. So sánh logic hiện tại với kỳ vọng
3. Chỉ ra điều kiện, branch, hoặc state gây sai
4. Đề xuất patch nhỏ nhất
5. Chỉ ra side effects có thể có
```

## 3.5 Debug test fail

```text
Tôi có test fail và muốn xử lý đúng nguyên nhân gốc.

Thông tin:
- Test fail: [tên test]
- Log/test output: [dán vào]
- Commit/PR gây fail: [nếu có]
- Kỳ vọng: [test phải pass theo logic nào]

Hãy:
1. Xác định test này đang bảo vệ behavior gì
2. Xác định code path bị tác động
3. Nêu root cause có khả năng cao nhất
4. Nói rõ nên sửa code hay sửa test
5. Nếu sửa test, giải thích vì sao
6. Đề xuất regression test liên quan nếu cần
```

## 3.6 Debug flaky test

```text
Tôi muốn điều tra flaky test.

Thông tin:
- Tên test: [tên test]
- Tần suất fail: [ví dụ: 2/10 lần]
- Dấu hiệu: [timeout / race / dữ liệu / random]
- Log nếu có: [dán vào]

Hãy:
1. Nêu các nguyên nhân flaky có khả năng nhất
2. Tìm điểm nondeterminism trong code/test
3. Chỉ ra chỗ đang phụ thuộc time / order / shared state / network / randomness
4. Đề xuất cách sửa để test ổn định
5. Đề xuất cách tái hiện flaky nếu có
```

---

# 4) Khi xử lý production issue hoặc incident

## 4.1 Điều tra incident

```text
Tôi đang xử lý một incident.

Thông tin:
- Triệu chứng: [mô tả]
- Mức độ ảnh hưởng: [bao nhiêu user/task]
- Thời điểm bắt đầu: [thời gian]
- Thay đổi gần đây: [deploy/merge/config]
- Dấu hiệu/log: [dán vào]

Hãy giúp tôi:
1. Tạo timeline điều tra
2. Xác định vùng hệ thống đáng nghi nhất
3. Nêu 3 nguyên nhân gốc có xác suất cao nhất
4. Đề xuất các bước kiểm tra theo thứ tự ưu tiên
5. Tách rõ mitigations tạm thời và root fix lâu dài
```

## 4.2 Patch nóng tối thiểu

```text
Tôi cần một hotfix tối thiểu, an toàn, và nhanh.

Thông tin:
- Sự cố: [mô tả]
- Vùng ảnh hưởng: [mô tả]
- Ràng buộc: [không đổi schema / không đổi API / không downtime / ...]

Hãy:
1. Chỉ ra patch nhỏ nhất có thể giảm rủi ro ngay
2. Nêu tradeoff của patch này
3. Chỉ ra phần nào nên làm sau trong root fix
4. Đề xuất cách verify sau khi deploy
```

---

# 5) Khi muốn review kiến trúc hiện tại

## 5.1 Review kiến trúc tổng thể

```text
Hãy review kiến trúc hiện tại của repo này như một technical reviewer.

Tôi muốn bạn đánh giá:
1. Hệ thống hiện tại đang làm được gì
2. Điểm mạnh kiến trúc là gì
3. Nợ kỹ thuật lớn nhất là gì
4. Chỗ coupling cao nhất là gì
5. Chỗ khó test nhất là gì
6. Chỗ khó mở rộng nhất là gì
7. Cái gì nên giữ nguyên
8. Cái gì nên refactor trước

Đầu ra:
- strengths
- weaknesses
- top priorities
- kế hoạch cải thiện theo 3 mức: nhỏ / vừa / lớn
```

## 5.2 Xác định core đáng giữ

```text
Tôi không muốn vứt đi những phần tốt của hệ thống hiện tại.

Hãy giúp tôi tách:
- core kernel đáng giữ
- compatibility layer
- glue code
- workaround tạm thời
- tech debt cần thay

Với mỗi phần, hãy nói:
- vì sao nên giữ hoặc thay
- rủi ro nếu đụng vào
- mức ưu tiên refactor
```

## 5.3 Tìm 3 vấn đề kiến trúc lớn nhất

```text
Hãy đọc hệ thống này và chỉ ra đúng 3 vấn đề kiến trúc lớn nhất.

Tiêu chí:
- gây khó debug
- gây khó mở rộng
- gây khó giữ tính đúng đắn
- gây mơ hồ về ownership/trách nhiệm

Với mỗi vấn đề, hãy nêu:
1. biểu hiện
2. nguyên nhân gốc
3. file/module liên quan
4. tác động
5. hướng xử lý phù hợp nhất
```

---

# 6) Khi muốn refactor nhưng chưa muốn rewrite

## 6.1 Refactor nhỏ và an toàn

```text
Tôi muốn refactor nhỏ, an toàn, không đổi behavior.

Mục tiêu:
- vùng code: [module/file]
- vấn đề: [khó đọc / quá dài / trùng lặp / trách nhiệm lẫn lộn]
- ràng buộc: [không đổi public API / không đổi output / ...]

Hãy:
1. Chỉ ra refactor nhỏ nhất có giá trị cao
2. Nêu trước/sau nên chia lại ra sao
3. Chỉ ra test cần có trước khi sửa
4. Nêu các bước refactor an toàn theo thứ tự
```

## 6.2 Tách module

```text
Tôi muốn tách một module đang quá to hoặc quá nhiều trách nhiệm.

Module hiện tại:
- [tên file/module]
- nó đang làm: [mô tả]
- vấn đề: [quá dài / lẫn domain + IO / khó test / ...]

Hãy:
1. Phân tách trách nhiệm hiện tại
2. Đề xuất cách chia module hợp lý
3. Nêu boundary mới giữa các module
4. Chỉ ra interface nên giữ ổn định
5. Đưa ra kế hoạch refactor từng bước
```

## 6.3 Giảm coupling

```text
Tôi muốn giảm coupling trong vùng code này.

Thông tin:
- module A: [tên]
- module B: [tên]
- vấn đề coupling: [mô tả]

Hãy:
1. Chỉ ra dependency không cần thiết
2. Chỉ ra dependency nên đảo ngược
3. Đề xuất interface hoặc contract mới
4. Nêu cách chuyển đổi dần mà ít rủi ro nhất
```

---

# 7) Khi muốn thiết kế lại hoặc nâng cấp hệ thống

## 7.1 Có nên redesign không

```text
Tôi đang cân nhắc có nên redesign/nâng cấp hệ thống hay không.

Bối cảnh:
- hệ thống hiện tại đang làm được: [mô tả]
- điểm đau chính: [mô tả]
- giới hạn: [deadline / nhân lực / compatibility / ...]

Hãy đánh giá:
1. Có nên refactor, rewrite một phần, hay rewrite lớn
2. Cơ sở cho quyết định đó
3. Phần nào tuyệt đối nên giữ
4. Phần nào có thể thay
5. Rủi ro lớn nhất của từng hướng
6. Khuyến nghị cuối cùng theo hướng thực dụng
```

## 7.2 Thiết kế V2

```text
Tôi muốn một bản thiết kế V2 để bên khác code lại hệ thống.

Hệ hiện tại:
- điểm mạnh: [mô tả]
- điểm yếu: [mô tả]
- thứ cần giữ: [mô tả]
- thứ cần thay: [mô tả]

Hãy tạo design spec gồm:
1. Mục tiêu V2
2. Non-goals
3. Kiến trúc khối
4. Module breakdown
5. Contract/interface chính
6. Data model hoặc state model
7. Luồng chạy chuẩn
8. Migration strategy
9. Milestones
10. Definition of done

Yêu cầu:
- thiên về thực thi
- không nói mơ hồ
- đủ cụ thể để team khác bắt đầu code
```

## 7.3 So sánh 2 phương án kiến trúc

```text
Tôi muốn so sánh 2 hướng kiến trúc.

Phương án A:
[ghi mô tả]

Phương án B:
[ghi mô tả]

Tiêu chí so sánh:
- độ phức tạp
- khả năng maintain
- khả năng debug
- tốc độ triển khai
- độ an toàn khi migrate
- khả năng mở rộng sau này

Hãy:
1. So sánh từng tiêu chí
2. Nêu tradeoff thật
3. Nêu phương án khuyên dùng
4. Nêu lý do vì sao
```

## 7.4 Thiết kế contract/interface

```text
Tôi muốn chuẩn hóa contract/interface cho phần sau:
- [module/hệ con]

Bối cảnh hiện tại:
- contract đang lỏng hoặc ad hoc ở chỗ: [mô tả]

Hãy:
1. Chỉ ra input/output hiện tại
2. Chỉ ra điểm mơ hồ hoặc nguy hiểm
3. Đề xuất interface typed hơn
4. Nêu invariant cần giữ
5. Nêu validation cần có
6. Nêu strategy migrate từ contract cũ sang mới
```

---

# 8) Khi xử lý PR, branch, hoặc review code

## 8.1 Review PR tổng quát

```text
Hãy review PR này như một senior reviewer.

Tôi muốn:
1. Tóm tắt PR đang thay đổi điều gì
2. Xác định intent thực sự của thay đổi
3. Chỉ ra rủi ro logic
4. Chỉ ra rủi ro kiến trúc
5. Chỉ ra rủi ro test/regression
6. Nêu phần nào ổn
7. Nêu phần nào cần sửa trước khi merge

Ưu tiên:
- correctness
- clarity
- maintainability
```

## 8.2 Review patch nhỏ

```text
Tôi muốn review patch này nhanh nhưng đúng trọng tâm.

Hãy tập trung vào:
- bug thật sự đã được fix chưa
- patch có quá rộng không
- có side effect gì không
- test hiện tại đã đủ chưa
- có cách sửa nhỏ hơn không

Đầu ra:
- verdict ngắn
- vấn đề cần sửa
- mức độ rủi ro
```

## 8.3 Chuẩn bị review comment

```text
Hãy giúp tôi viết review comment cho PR này.

Tôi muốn comment theo kiểu:
- rõ ràng
- lịch sự
- technical
- có lý do

Điểm tôi muốn comment:
- [vấn đề 1]
- [vấn đề 2]
- [vấn đề 3]

Với mỗi điểm, hãy viết:
1. comment ngắn gọn
2. lý do kỹ thuật
3. gợi ý sửa nếu có
```

## 8.4 Tóm tắt PR cho người khác

```text
Hãy tóm tắt PR này cho người không đọc toàn bộ diff.

Tôi muốn:
1. mục tiêu PR
2. phần nào bị thay đổi
3. hành vi nào đổi
4. rủi ro chính
5. thứ cần chú ý khi test hoặc rollout

Viết ngắn nhưng đủ để team nắm được.
```

## 8.5 Chuẩn bị merge decision

```text
Tôi cần quyết định merge hay chưa.

Hãy đánh giá PR này theo:
- correctness
- test coverage
- blast radius
- readability
- architectural fit

Kết luận theo 1 trong 3 mức:
- merge được
- merge được sau vài sửa nhỏ
- chưa nên merge

Giải thích ngắn nhưng rõ.
```

---

# 9) Khi muốn giao việc cho người khác

## 9.1 Viết implementation task

```text
Tôi muốn biến vấn đề này thành task rõ ràng để giao cho người khác.

Vấn đề:
- [mô tả]

Hãy viết task spec gồm:
1. Context
2. Problem statement
3. Goal
4. Non-goals
5. Scope
6. Expected changes
7. Acceptance criteria
8. Risks
9. Suggested files/modules to inspect
```

## 9.2 Viết spec cho bên kia code lại

```text
Tôi muốn một spec đủ rõ để team khác code.

Bối cảnh:
- [mô tả]
- mục tiêu: [mô tả]
- giới hạn: [mô tả]

Hãy tạo spec theo format:
1. Overview
2. Current problem
3. Requirements
4. Proposed architecture
5. Interfaces
6. Data/state flow
7. Edge cases
8. Testing plan
9. Rollout/migration
10. Acceptance criteria
```

## 9.3 Chia nhỏ công việc

```text
Tôi muốn chia một việc lớn thành các task nhỏ, độc lập tương đối, có thể giao cho nhiều người.

Việc lớn:
- [mô tả]

Ràng buộc:
- [deadline / số người / dependency / ...]

Hãy:
1. Chia thành các workstreams
2. Với mỗi workstream, nêu deliverable
3. Chỉ ra dependency giữa các task
4. Đề xuất thứ tự triển khai
5. Nêu task nào có thể làm song song
```

---

# 11) Khi muốn thêm test đúng cách

## 11.1 Viết test cho bug fix

```text
Tôi vừa hoặc sắp fix bug này:
- [mô tả bug]

Hãy đề xuất test plan:
1. test nào tái hiện bug cũ
2. test nào xác nhận behavior đúng mới
3. test nào để tránh regression gần kề
4. nên viết unit, integration, hay e2e
5. test data tối thiểu cần có
```

## 11.2 Đánh giá coverage quanh vùng sửa

```text
Tôi muốn biết vùng code này đã được test đủ chưa.

Vùng code:
- [file/module/function]

Hãy:
1. Xác định behavior quan trọng cần được bảo vệ
2. Chỉ ra case nào nên có test mà có thể đang thiếu
3. Chỉ ra case biên
4. Đề xuất test ưu tiên cao nhất
```

---

# 12) Khi muốn cải thiện performance

## 12.1 Điều tra performance bottleneck

```text
Tôi muốn điều tra performance bottleneck.

Thông tin:
- thao tác chậm: [mô tả]
- kỳ vọng: [mô tả]
- đo đạc/log nếu có: [dán vào]

Hãy:
1. Xác định các đoạn có khả năng là bottleneck
2. Phân biệt CPU / IO / network / DB / locking / retry dư thừa
3. Đề xuất cách đo tiếp để xác nhận
4. Đề xuất tối ưu theo thứ tự impact/risk
```

## 12.2 Tối ưu nhưng không đổi semantics

```text
Tôi muốn tối ưu phần này nhưng không muốn đổi semantics.

Vùng code:
- [mô tả]

Hãy:
1. Chỉ ra chỗ đang lãng phí
2. Đề xuất tối ưu an toàn
3. Nêu tradeoff
4. Nêu cách benchmark trước/sau
```

---

# 13) Khi muốn xử lý dependency hoặc migration

## 13.1 Nâng version dependency

```text
Tôi muốn nâng cấp dependency sau:
- [tên package / version cũ -> mới]

Ràng buộc:
- [không downtime / không đổi API / giữ backward compatibility / ...]

Hãy:
1. Nêu vùng code có thể bị ảnh hưởng
2. Nêu breaking changes cần để ý
3. Đề xuất kế hoạch nâng cấp từng bước
4. Nêu test/check cần chạy sau khi nâng
```

## 13.2 Migration module hoặc API

```text
Tôi muốn migrate từ:
- [hệ cũ]
sang:
- [hệ mới]

Hãy:
1. Liệt kê compatibility concerns
2. Đề xuất migration path ít rủi ro
3. Chia thành các pha
4. Nêu rollback strategy
5. Nêu chỉ số hoặc dấu hiệu xác nhận migration thành công
```

---

# 14) Khi muốn viết tài liệu kỹ thuật

## 14.1 Viết design doc

```text
Tôi muốn viết design doc cho thay đổi sau:
- [mô tả]

Hãy giúp tôi tạo document theo cấu trúc:
1. Problem
2. Context
3. Goals
4. Non-goals
5. Current state
6. Proposed design
7. Alternatives considered
8. Risks
9. Rollout plan
10. Acceptance criteria
```

## 14.2 Viết doc giải thích module

```text
Tôi muốn viết tài liệu giải thích module này cho người mới.

Module:
- [tên]

Hãy viết theo cấu trúc:
1. Module này làm gì
2. Nó được gọi từ đâu
3. Nó gọi sang đâu
4. Input/output chính
5. Invariants quan trọng
6. Những chỗ dễ hiểu sai
7. Muốn sửa module này thì cần cẩn thận gì
```

---

# 15) Khi cần giao tiếp ngắn trong team

## 15.1 Xin review kỹ thuật

```text
Tôi muốn nhờ review kỹ thuật cho thay đổi này.

Thông tin:
- mục tiêu thay đổi: [mô tả]
- phạm vi: [mô tả]
- chỗ tôi chưa chắc: [mô tả]

Hãy giúp tôi viết một tin nhắn ngắn, rõ, technical, để gửi đồng đội xin review.
```

## 15.2 Báo status kỹ thuật

```text
Tôi muốn viết update kỹ thuật ngắn cho team.

Thông tin:
- đã làm xong: [mô tả]
- đang làm: [mô tả]
- đang kẹt: [mô tả]
- cần hỗ trợ: [mô tả]

Hãy viết thành status update ngắn gọn, chuyên nghiệp.
```

---

# 16) Khi bạn không biết nên hỏi gì trước

## 16.1 Prompt cứu hộ khi bị rối hoàn toàn

```text
Tôi đang bị rối hoàn toàn với repo này.

Đừng cố giải quyết tất cả cùng lúc.
Hãy giúp tôi theo đúng thứ tự:
1. Tóm tắt hệ thống này trong 5-10 câu
2. Chỉ ra entrypoint quan trọng nhất
3. Chỉ ra module lõi nhất
4. Chỉ ra luồng chạy chính nhất
5. Chỉ ra một nơi tốt nhất để tôi bắt đầu đọc code
6. Chỉ ra một việc nhỏ nhưng giá trị cao tôi nên làm tiếp

Bám sát code, không nói lý thuyết chung.
```

## 16.2 Prompt khi không biết bug nằm đâu

```text
Tôi chưa biết bug nằm ở đâu.

Thông tin hiện có:
- hiện tượng: [mô tả]
- lúc xuất hiện: [mô tả]
- log: [dán nếu có]
- tôi chưa có giả thuyết chắc chắn

Hãy giúp tôi điều tra theo hướng:
1. khoanh vùng phạm vi
2. tạo giả thuyết
3. ưu tiên xác minh
4. xác định chỗ nào cần instrument/log thêm
5. đề xuất bước nhỏ tiếp theo
```
