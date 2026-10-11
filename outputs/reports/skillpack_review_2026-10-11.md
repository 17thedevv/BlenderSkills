# Đánh giá bộ skills VTuber Kagari

Ngày đánh giá: 11/10/2026. Phạm vi: 13 `SKILL.md` trong `.agents/skills`, hợp đồng agent, workflow, brief, scripts kiểm chứng và bằng chứng từ lượt chỉnh trang phục Kagari. Đây là đánh giá nội dung và một số hành vi kiểm chứng thực tế; chưa phải thử nghiệm độc lập toàn bộ 13 skills.

## Nhận định chính

Bộ skills khá tốt ở tổ chức quy trình, bảo toàn dữ liệu và yêu cầu bằng chứng thật. Phần hướng dẫn tạo hình còn mỏng, đặc biệt với trang phục, tóc, UV và vật liệu. Dùng làm khung phối hợp công việc được; chưa đủ để bảo đảm một model anime có độ hoàn thiện cao.

Tách hai nguyên nhân: skills chưa cụ thể ở một số khâu; cách thực hiện của agent cũng chưa đáp ứng hết các quy tắc đã có. Trong lượt vừa rồi, áo vẫn là một shell đơn giản, gán xương chủ yếu để xem trước, nếp rủ chưa hoàn thiện. Không thể quy toàn bộ chất lượng model cho bộ skills.

## Đánh giá từng skill

| Skill | Mức hữu ích từ nội dung hiện tại | Điểm mạnh | Khoảng trống cần sửa |
|---|---|---|---|
| character-director | Khá | Brief, silhouette, ưu tiên crop, checkpoint rõ. | Thiếu cách ghi những thuộc tính đã duyệt và cách xử lý điều chỉnh nhỏ theo yêu cầu mới. |
| base-mesh-strategy | Tốt | Ưu tiên base có nguồn và giữ bản gốc; so sánh deformability. | Cần bảng so sánh base theo tóc, trang phục và công sức chuyển đổi; tránh chỉ chọn theo khuôn mặt. |
| anime-face-specialist | Khá | Form lớn trước, blink thật, viseme và mức 0.5. | Thiếu hướng dẫn đặt guide/landmark theo reference và kiểm tra deltas khi chỉnh mesh. Một số câu nhầm readability của avatar với điều kiện tracking webcam. |
| hair-outfit-builder | Yếu nhất cho nhu cầu hiện tại | Phân cấp tóc, lớp trang phục, attachment và collision. | Quá chung: thiếu cách dựng tay áo, cổ áo chồng lớp, nếp rủ, thickness, UV, density của đồ trang trí và kiểm tra material xuất VRM sớm. |
| reference-fidelity-guardian | Cần sửa đáng kể | Giữ những dấu hiệu nhận diện của Kagari, yêu cầu so sánh với concept. | “1:1” không có tiêu chí đo; khóa cứng `AvatarSample_B`; mô tả tracking gây hiểu nhầm; trộn luật dùng chung và thiết kế riêng Kagari. |
| topology-expert | Tốt về nguyên tắc | Bảo toàn shape keys, không sửa mọi boundary, pose-test khớp. | Script hỗ trợ chưa kiểm tra đầy đủ điều kiện được yêu cầu, như trọng số thiếu và geometry sau modifier. |
| vtuber-rigging | Tốt về nguyên tắc | Binding VRM rõ, test 0/0.5/1 và tổ hợp, tránh driver trùng. | Cần quy trình kiểm tra weight theo vùng và trạng thái material/physics trước export. Tính tương thích thực tế chưa được chứng minh bởi lượt này. |
| basic-animation-maker | Khá | Tách Actions, kiểm tra seam, không giả định VRM chứa Actions. | Cần cách chuyển animation sang runtime đã chọn và bằng chứng clip, thay vì chỉ hướng dẫn khái quát. |
| visual-critic | Tốt nhưng chưa ràng buộc đủ | Render thật, cùng camera/lights, top defects, giới hạn vòng sửa. | Cần gắn báo cáo với phiên bản model và khóa duyệt vào artifact; phát hiện trường hợp render đẹp nhưng material/runtime chưa tương thích. |
| vrm-delivery | Tốt về nguyên tắc | Export, re-import, texture packing, báo cáo giới hạn. | Nên kiểm tra vật liệu/export từ giai đoạn áo và tóc, tránh dồn mọi incompatibility đến cuối. |
| webcam-tracking | Khá | Calibration, mappings, smoothing, dropout, không giả PASS. | Phân biệt chất lượng tín hiệu webcam và chất lượng biểu cảm avatar; ghi phiên bản và blueprint được kiểm tra. |
| live-broadcast-integration | Khá | Capture thật, crop, expression mixing, test có OBS. | Thiếu mẫu kết quả và settings có thể tái lập, nhưng chưa nên hardcode UI theo một phiên bản. |
| streaming-performance | Tốt về mục tiêu | Profile theo workload, không đồng nhất poly count với FPS. | Cần cả mesh gốc và mesh evaluated, số mesh/material draw-call; cảnh báo chi phí phát sinh ngay khi dựng chi tiết. |

Các mức trên là nhận định của người đánh giá, không phải điểm benchmark hoặc chứng nhận runtime.

## Các phát hiện ưu tiên

### 1. Audit hiện chưa phản ánh đầy đủ geometry sau modifier

`scripts/audit_blend.py` tính tam giác từ `obj.data.polygons`, không từ mesh evaluated.

Trên cùng `outputs/wip/kagari_outfit_detail_v1.blend`:

- Audit hiện có: **50.587 tam giác**, 119 mesh objects.
- Kiểm tra evaluated: **134.067 tam giác**, gồm **105.372** tam giác của phần thêm mới.

Bằng chứng: `kagari_outfit_skillpack_audit.json` và `kagari_outfit_detail_verification.json`.
Đây là khác biệt giữa geometry gốc và sau modifier, không phải phép đo FPS hay số tam giác của một VRM đã xuất. Mục tiêu 80k trong brief là mục tiêu khởi điểm, không phải giới hạn tuyệt đối.

Sửa đề xuất: xuất riêng raw/evaluated/export counts; ghi modifier và phần geometry đóng góp nhiều nhất. Dùng sampling tiết kiệm cho piping và relief trước khi triển khai hàng loạt.

### 2. Không có một trạng thái dự án được đối chiếu bằng artifact

`config/character_brief.json` vẫn ghi Gate B và face approval false. `outputs/DELIVERY.md` trỏ tới `outputs/wip/kagari_gate_b_final.blend`, nhưng file này không tồn tại tại thời điểm kiểm tra. Candidate hiện tại là `kagari_outfit_detail_v1.blend`.

`python scripts/check_skillpack.py` vẫn trả về `SKILLPACK OK (13 skills, workflow/config/scripts present)`.

Validator chỉ kiểm tra files, frontmatter và một số giá trị config. Nó không kiểm tra artifact trong DELIVERY, nội dung mâu thuẫn, bằng chứng approval hoặc chất lượng model. README còn ghi 12 skills dù thực tế có 13.

Sửa đề xuất: một file trạng thái chứa current artifact, version/hash, gate, evidence và approval; các báo cáo trỏ vào trạng thái đó. Tách kết quả kiểm tra cấu trúc khỏi kết quả kiểm tra bằng chứng dự án. Khi sửa model, chỉ đánh dấu lại những kiểm tra bị ảnh hưởng; không bắt lặp lại toàn bộ duyệt từ đầu.

### 3. Hướng dẫn trang phục chưa đủ cụ thể để ngăn hình thức “thêm nhiều chi tiết”

`hair-outfit-builder` hiện có bảy bước khái quát và exit chủ yếu dựa trên silhouette/no clipping. Chưa có tiêu chí riêng cho bề mặt vải, cổ áo, tay áo, UV, độ dày và material dùng được trong runtime.

Lượt Kagari chứng minh có thể thêm piping, hoa văn và phụ kiện nhưng vẫn thiếu nếp rủ tự nhiên, nối vai sạch và deformation phù hợp. Báo cáo hiện đã ghi rõ giới hạn; đó không phải thành công production.

Sửa đề xuất: giữ skill chính ngắn, thêm references cho kimono/collar/sleeves, tóc clump và MToon. Chọn một vùng để hoàn thiện và kiểm tra đủ front/side/pose trước khi nhân rộng ornament. Cho phép texture/normal detail khi phù hợp thay vì dựng mọi đường thêu thành geometry.

### 4. Một số câu đang nhầm điều kiện tracking với hình dáng avatar

`reference-fidelity-guardian` yêu cầu tóc không che lông mày/mắt “for webcam tracking”; `anime-face-specialist` cũng có ngôn ngữ tương tự.

Warudo MediaPipe nhận webcam để tạo dữ liệu tracking, sau đó blueprint/mapping dùng dữ liệu đó để điều khiển character. Vì vậy, với pipeline được mô tả trong dự án, suy luận đúng là tóc trên avatar ảnh hưởng khả năng người xem đọc biểu cảm và collision, không trực tiếp quyết định nhận diện khuôn mặt người dùng trong webcam.

Nguồn chính thức: [MediaPipe](https://docs.warudo.app/docs/mocap/mediapipe), [Customizing Face Tracking](https://docs.warudo.app/docs/mocap/face-tracking).

Sửa đề xuất: ghi hai nhóm tiêu chí riêng — tín hiệu camera của người dùng và readability/deformation của avatar. Không thay đổi kiểu mái theo một lý do tracking chưa đúng.

### 5. Fidelity và lựa chọn base đang quá cứng

`reference-fidelity-guardian` vừa yêu cầu fidelity “1:1”, vừa chỉ định duy nhất `AvatarSample_B`. Trong khi `base-mesh-strategy` yêu cầu đánh giá base tốt nhất theo chất lượng và giấy phép. Hai hướng dẫn chưa mô tả cách giải quyết khi base bắt buộc gây sai tóc/trang phục.

Concept hiện chỉ cung cấp một hình minh họa; những hình khối ở góc khuất không được xác định đủ để kiểm tra “1:1” cho mọi góc.

Sửa đề xuất: ghi các dấu hiệu nhận diện bắt buộc, tỷ lệ và silhouette ở góc có reference, cùng phần được phép diễn giải ở góc khuất. Đưa thiết kế Kagari sang brief/reference của dự án; base là lựa chọn có lý do, không phải tiêu chuẩn chung bất biến. Đánh giá thể tích và kết quả thị giác thay vì chỉ cấm một phương pháp tạo mesh.

## Thứ tự cải thiện đề xuất

1. Sửa phân biệt webcam input/avatar readability và cập nhật trạng thái/artifact hiện tại.
2. Nâng audit raw/evaluated và validator bằng chứng, giữ validator cấu trúc đơn giản.
3. Bổ sung hướng dẫn dựng trang phục/tóc/UV/material có tiêu chí quan sát được, dựa trên những lỗi thật của Kagari.
4. Nối visual review, pose tests, material export và approval với đúng phiên bản model.
5. Thử lại một nhiệm vụ hẹp — cổ áo/tay áo Kagari — với bằng chứng trước/sau và giới hạn chi phí; sau đó mới mở rộng.

Không cần tăng số skills trước khi sửa những khoảng trống này. Việc chia thêm vai trò chỉ hữu ích khi mỗi skill có quyết định, quy trình hoặc tài nguyên thực thi khác biệt.

## Những gì đã kiểm tra trong lần đánh giá

- Đọc cả 13 SKILL.md và tài liệu điều phối chính.
- Chạy validator cấu trúc: PASS.
- Kiểm tra đường dẫn .blend được DELIVERY nhắc tới: không tồn tại.
- Chạy audit Blender hiện có trên candidate mới nhất và đối chiếu với evaluated verification.
- Đối chiếu mô tả tracking với tài liệu chính thức Warudo.
- Không thay đổi nội dung bộ skills trong lượt đánh giá này; chỉ tạo báo cáo và một file audit bổ sung.
