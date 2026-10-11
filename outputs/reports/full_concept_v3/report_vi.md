# Kagari — Báo cáo dựng trang phục trên model đầy đủ

**Kết luận: đã hoàn thành bản dựng WIP đầy đủ; chưa đạt duyệt mỹ thuật.**

Cổ áo và tay áo đã cải thiện so với Cycle 03, nhưng lỗi giao nhau ở eo, cổ sau cứng,
nếp vải chưa thuyết phục và lỗi tóc gốc khiến bản này chưa đủ điều kiện chuyển sang
avatar hoàn thiện. Kiểm tra kỹ thuật chạy thành công không đồng nghĩa model đẹp hoặc đạt concept.

## 1. Bản được đánh giá

- Model: [kagari_full_concept_v3.blend](../../wip/kagari_full_concept_v3.blend).
- Phiên bản: `full-kagari-concept-outfit-v3`.
- SHA256: `ffbc443b2f4c1af194a77cbfdd1d4a4deb80e7b6ca1d0b1929a2dc767577fd16`.
- Baseline: [Cycle 03](../../wip/kagari_v03_clay_03.blend), đã bị người dùng từ chối.
- Reference: [concept Kagari hiện có](../../design/concept_option2_kagari.jpg).
- Bằng chứng: [gallery đối chiếu](../../previews/full_concept_v3/review.html),
  [đánh giá hình ảnh](visual_review.json), [kiểm tra kỹ thuật](technical_verification.json).

Báo cáo dựa trên 9 render clay của bản mới, 4 render màu dùng vật liệu sẵn có và
9 render clay đối chiếu Cycle 03 đã xem trực tiếp. Hai bên đối chiếu dùng cùng góc máy,
tỷ lệ khung hình và tư thế tay. Chưa có duyệt mỹ thuật từ người dùng cho bản này.

## 2. Phần đã thực hiện

Lấy model Kagari cũ làm nền, tích hợp phần trang phục dựng theo phương pháp mới lên
toàn bộ nhân vật. Mặt, tóc và rig được giữ lại; đây không phải dựng lại mọi bộ phận từ đầu.

| Bộ phận | Thay đổi thực tế | Mức cải thiện quan sát được |
|---|---|---|
| Cổ áo | Dải cổ rộng, cong; xác định lớp dưới/lớp trên và nối qua gáy | Giao nhau trước ngực rõ hơn, giảm các tam giác gấp bất thường của Cycle 03 |
| Vai–tay áo | Dùng chung đỉnh ở đường nối thân và gốc tay; thêm tay áo thứ hai | Form liền hơn, giảm cảm giác tay áo là vật thể rời đặt trên vai |
| Hai tay áo | Dựng dài, loe rộng, có miệng mở và độ dày | Silhouette rộng và mềm hơn hai ống ngắn cứng của bản cũ |
| Thân áo | Bề mặt có thể tích và một số nếp lớn | Ngực/eo có độ chuyển form; lưng vẫn chưa có độ rủ tốt |
| Đai eo | Dải mỏng, cong và thay đổi tiết diện | Bớt cảm giác khối hộp, nhưng tiếp giáp với thân áo vẫn lỗi |
| Phần váy | Dựng vỏ vải mới từ eo xuống gần mắt cá, có vài nếp dọc | Giảm mép váy cũ dạng răng cưa dưới đai; form mới vẫn đơn giản |

Đã lưu độc lập các bản WIP và giữ nguyên file Cycle 03 cùng mẫu thử một tay áo.
Trong bản mới, `Body` gốc được giữ nguyên dữ liệu trong collection archive.
`Body_GarmentDisplay` là bản sao riêng đã bỏ các mặt trang phục cũ, giữ da, giày và phần áo trong
ở thân trên. Đây là thay đổi bề mặt hiển thị, không phải toàn bộ Body đang hiển thị y hệt bản cũ.

Kiểm tra sau khi mở lại file xác nhận dữ liệu Face, Hair, Body gốc, morph của Face,
UV, weights, rig rest và tư thế đã lưu còn khớp dữ liệu trước khi dựng.

## 3. Phương pháp dựng và giới hạn

Trang phục được dựng bằng các bề mặt vải có hình dáng điều khiển, nối gốc tay áo bằng topology,
thêm độ dày bằng Solidify và gán weights vào armature gốc. Nếp vải và độ rủ được tạo hình
chủ động; không được tính lại bằng mô phỏng Cloth khi đổi pose.

**Bản này chưa thực hiện đầy đủ một quy trình pattern-based với rập 2D, đường may và mô phỏng
rủ vải vật lý.** Nó là phương án tạo hình có kiểm soát, thuận tiện hơn để nối vào rig hiện có.
Do đó, chưa thể coi vấn đề phương pháp dựng vải đã được giải quyết hoàn toàn.

Màu kem và burgundy được dùng lại từ vật liệu cũ để xem form trong render màu.
Chưa làm shader mới, texture mới, thêu, trang trí hay phụ kiện mới. UV của trang phục là UV
làm việc, chưa phải atlas hoàn thiện. Không cài thêm phần mềm và không mở rộng Skills.

## 4. Thiếu sót còn tồn tại

### A. Giao nhau ở thân áo–đai eo — ưu tiên cao

- **Vị trí:** hai góc trên của đai trước bụng, cạnh eo và đường tiếp giáp phía sau.
- **Biểu hiện:** mặt vải kem cắt vào đai burgundy, tạo các mảng tam giác và mép gãy.
  Lỗi rõ hơn khi xem màu; việc giảm răng cưa của váy cũ chưa giải quyết hết giao nhau ở eo.
- **Bằng chứng:** [chính diện màu](../../previews/full_concept_v3/front_existing_color.png),
  [3/4 màu](../../previews/full_concept_v3/three_quarter_existing_color.png),
  [lưng clay](../../previews/full_concept_v3/back_clay.png).
- **Nguyên nhân dự kiến:** tiết diện thân áo, đai và khoảng hở giữa các lớp chưa thống nhất
  sau khi tích hợp; chưa có kiểm tra va chạm toàn bề mặt.
- **Hướng sửa:** đối chiếu mặt cắt eo, điều chỉnh biên thân áo/đai và khoảng hở theo thứ tự lớp;
  kiểm tra lại trước, nghiêng, sau và pose. Kết quả cần là mép đai liên tục, không có các mảng
  vải kem cắt vào mặt đai. Không thể sửa lỗi này chỉ bằng shader hoặc subdivision.

### B. Tóc hở da đầu và tóc sau dạng tấm — lỗi nghiêm trọng của model tổng thể

- **Vị trí:** vùng thái dương/đỉnh đầu ở góc 3/4 và nghiêng; dải tóc sau lưng.
- **Biểu hiện:** lộ mảng scalp tối; một số mép tóc rời và góc cạnh. Tóc phía sau đọc như các
  dải phẳng dài, chưa có khối và dòng tóc tự nhiên.
- **Bằng chứng:** [3/4 màu](../../previews/full_concept_v3/three_quarter_existing_color.png),
  [nghiêng clay](../../previews/full_concept_v3/side_clay.png),
  [sau clay](../../previews/full_concept_v3/back_clay.png).
- **Nguồn lỗi:** tồn tại từ Cycle 03. Dữ liệu tóc được bảo toàn, nên lần dựng trang phục này
  không sửa tóc. Giữ nguyên dữ liệu không đồng nghĩa tóc đạt chất lượng.
- **Hướng sửa:** cần một lượt sửa tóc riêng: kiểm tra phủ scalp, gốc tóc, khối tóc sau và đầu
  lọn theo reference; kết quả cần là phủ kín vùng scalp lỗi và khối tóc đọc được từ bên/sau.
  Nguyên nhân chi tiết cần kiểm tra mesh trước khi sửa. Đây là lỗi chặn duyệt theo rubric.

### C. Cổ sau và vùng vai còn cứng

- **Vị trí:** dải cổ ở gáy và mặt trên vai.
- **Biểu hiện:** cổ sau nhô như một gờ nhỏ; vai có khối lồi tròn, thiếu cảm giác vải nằm trên cơ thể.
- **Bằng chứng:** [nghiêng clay](../../previews/full_concept_v3/side_clay.png),
  [3/4 clay](../../previews/full_concept_v3/three_quarter_clay.png).
- **Nguyên nhân dự kiến:** độ cong dải cổ và độ dư vải ở vai chưa khớp mannequin đầy đủ;
  nối topology liền chưa đảm bảo hình dáng đường may tự nhiên.
- **Hướng sửa:** chỉnh độ ôm gáy, chuyển tiếp cổ–vai và một số nếp chịu lực có chủ đích.
  Cần loại cảm giác cổ dạng gờ cứng mà vẫn giữ chiều rộng và thứ tự chồng lớp phía trước.

### D. Nếp rủ và biến dạng chưa đủ thuyết phục

- **Vị trí:** thân sau, tay áo khi hạ tay, vùng dưới nách khi giơ tay và phần váy dài.
- **Biểu hiện:** bề mặt còn quá trơn; tay ngang tạo các túi tròn lớn dưới nách.
  Vải đổi hình theo xương nhưng không tự rủ lại theo trọng lực. Váy vẫn có nhiều vùng gần phẳng.
- **Bằng chứng:** [tay ngang](../../previews/full_concept_v3/arm_horizontal_clay.png),
  [giơ tay](../../previews/full_concept_v3/arm_raised_clay.png),
  [toàn thân 3/4](../../previews/full_concept_v3/full_three_quarter_clay.png).
- **Nguyên nhân:** độ rủ được tạo hình sẵn và dùng skinning thông thường; chưa có xử lý nếp
  theo pose, chỉnh corrective hoặc hệ thống chuyển động váy.
- **Hướng sửa:** xác định một số nếp lớn xuất phát từ vai, đường may và điểm giữ ở eo;
  kiểm tra chuyển động trước khi chọn corrective/secondary bones. Cần thể hiện trọng lượng
  vải, tránh nếp ngẫu nhiên và tránh chỉ làm mịn các khối túi hiện có.

### E. Chưa tái hiện đầy đủ concept

- Các lớp haori và dải ve dài chưa hoàn chỉnh; hiện mới đọc rõ áo kem, cổ chéo burgundy và tay rộng.
- Reference hiện có không cung cấp phần thân dưới, góc bên hay góc sau. Váy dài chữ A là phần
  suy luận, chưa có bằng chứng người dùng chấp thuận thiết kế đó.
- Giày sneaker và một số chi tiết nền cũ vẫn được giữ lại; chưa thành một tổng thể trang phục
  được thiết kế thống nhất theo concept.
- Trang trí/phụ kiện chưa dựng trong lượt này do phạm vi công việc. Đây là phần chưa làm,
  không phải lý do để duyệt form vải đang lỗi.

## 5. Kiểm tra đã có và kiểm tra còn thiếu

| Hạng mục | Kết quả/bằng chứng | Giới hạn |
|---|---|---|
| Bảo toàn dữ liệu gốc | Khớp sau khi mở lại file | Không chứng minh mặt/tóc đã đẹp hoặc expressions chạy tốt |
| Bốn bề mặt trang phục | Mỗi mesh là một thành phần nối liền; không có face diện tích 0 hoặc cạnh nonmanifold bên trong | Không kiểm tra hết tự giao nhau hoặc va chạm với cơ thể |
| Skin weights | Chuẩn hóa, tối đa 4 ảnh hưởng mỗi đỉnh; dùng Armature gốc | Không chứng minh mọi pose đều ổn |
| Pose tay | Đã xem nâng hai tay 30° từ pose lưu và đặt tay ngang | Không có chuyển động liên tục, pose tay trên đầu hay kiểm tra đầy đủ cổ tay/khuỷu |
| Vải và lớp áo | Độ dày cuff/cổ nhìn được; nối vai cải thiện | Tiêu chí không có giao nhau rõ ràng vẫn FAIL |
| Váy/chân | Có vỏ váy và weights hips/spine | Chưa thử bước đi, ngồi, nâng chân, xoay hông hoặc chuyển động váy |
| UV và vật liệu | Có UV làm việc; render được vật liệu sẵn có | Chưa có atlas hoàn thiện hoặc kiểm chứng MToon/VRM |
| VRM, Warudo, webcam, OBS | NOT TESTED | Chưa xuất/reimport, kiểm tra tracking, expressions hay hiệu năng thực tế |

Không có chứng nhận collision-free, animation-ready hoặc VRM-ready cho bản này.

## 6. Độ phức tạp mesh

| Phạm vi | Tam giác mesh gốc | Tam giác sau đánh giá modifier ở viewport |
|---|---:|---:|
| Bốn bề mặt trang phục mới | 20.105 | 41.908 |
| Năm mesh trang phục riêng của Cycle 03 | 6.880 | 17.544 |
| Các object bật render của bản mới | 47.434 | 118.773 |
| Các object bật render của Cycle 03 | 36.741 | 96.941 |

Năm mesh cũ không bao gồm trang phục nằm trong Body; bốn mesh mới có cả phần váy mới.
Vì vậy không thể coi hai dòng garment là cùng một phạm vi để kết luận phương pháp nào tối ưu hơn.
Số viewport dựa vào modifier hiện tại; danh sách bật render dựa trên `hide_render` của object,
chưa mô phỏng loại trừ collection. Đây không phải số tam giác VRM hay kết quả FPS.
Xem [bảng kiểm đếm](mesh_complexity_comparison.json).

Archive chứa Body và quần áo cũ phải được loại trừ rõ ràng khi chuẩn bị export,
tránh xuất trùng bề mặt. Solidify, normals, triangulation và shaders còn cần kiểm tra ở pipeline VRM.

## 7. Thứ tự xử lý đề xuất

1. Sửa giao nhau tại eo và mép nối phía sau; xác nhận bằng clay và màu ở nhiều góc.
2. Sửa tóc hở scalp và khối tóc sau; đây là lỗi chặn duyệt của toàn model.
3. Chỉnh cổ gáy, vai và nếp lớn trên tay/thân; kiểm tra chuyển động tay, không chỉ pose tĩnh.
4. Chốt thiết kế suy luận phần váy/giày và mức bám concept; kiểm tra chuyển động chân/váy.
5. Chỉ sau khi form được duyệt mới triển khai chi tiết trang trí, UV/vật liệu hoàn thiện và VRM/runtime.

Đây là đề xuất bước tiếp theo, chưa phải các thay đổi đã thực hiện trong bản báo cáo này.
Kết quả hiện tại cải thiện cấu trúc trang phục so với Cycle 03 nhưng vẫn chưa đạt Clay/Full Avatar
Art Gate. Giữ trạng thái `REQUIRES_HUMAN_ART_REVIEW`; không tự chuyển sang PASS.
