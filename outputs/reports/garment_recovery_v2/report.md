# Kagari — Garment Geometry Recovery, kết quả sau hai lượt

**Khuyến nghị: FAIL — chưa duyệt nhiệm vụ recovery là đã giải quyết ổn định các lỗi cấu trúc.**

Eo cải thiện rõ trên ảnh trước/3/4 và cổ gáy bớt nhô. Số tam giác không tăng, dữ liệu bảo vệ còn khớp.
Tuy nhiên vẫn còn giao nhau cục bộ giữa cổ–áo, tay áo–đai và áo–Body ở pose lưu; vùng vai/dưới nách
chưa có độ rủ thuyết phục. Dừng sửa geometry sau đúng hai lượt theo yêu cầu, bàn giao để người dùng xem.
Không tự chuyển Clay/Full Avatar Art Gate sang PASS.

## 1. Artifact và bằng chứng

- [Candidate cuối: kagari_garment_recovery_v2.blend](../../wip/kagari_garment_recovery_v2.blend).
- Version: `garment-geometry-recovery-v2`.
- SHA256: `9006f5c03019ad0fd4aeeeba1c97b2a30e96f65ac1b8fa0d9093000664017d6d`.
- [Lượt sửa thứ nhất](../../wip/kagari_garment_recovery_v1.blend), SHA256
  `61df33536b9b8caebe9d2bccaa2d7599bb917f10476bb6c67fcc0dab318f61e4`.
- [Bản đối chiếu full_concept_v3](../../wip/kagari_full_concept_v3.blend), SHA256
  `ffbc443b2f4c1af194a77cbfdd1d4a4deb80e7b6ca1d0b1929a2dc767577fd16`.
- [Backup độc lập trước khi sửa](../../backups/garment_recovery_start/kagari_full_concept_v3.blend)
  đã xác minh cùng hash với source.
- [Gallery trước/sau](../../previews/garment_recovery_v2/review.html),
  [phạm vi được giao](user_authorization.md).

Đã xem trực tiếp 9 clay và 4 ảnh màu của mỗi lượt. Candidate dùng đúng camera, tỷ lệ,
thiết lập clay và lighting/vật liệu màu của full_concept_v3. Không đổi framing để che lỗi.
Pose trung tính ở đây là **pose lưu sẵn**; hai stress pose là nâng hai tay thêm 30° từ pose đó
và đặt upper arms ngang. Chưa có animation hay mô phỏng Cloth động.

## 2. Nguyên nhân cụ thể được tìm thấy

Kiểm tra ray/face chỉ ra rằng những mảng vải kem cắt vào hai góc đai không chỉ là thân áo:
ở `x=.13, z=.975`, bề mặt phía trước/sau thuộc **mặt trong của tay áo** trong
`Kagari_Concept_Robe_Two_Sleeves`. Tay áo rủ vào vùng đai khi hạ tay.
Mặt váy dưới cũng giao nhau với đai vì bán kính đai tại mép dưới nhỏ hơn vỏ váy.

`Kagari_Concept_Crossed_Collar` có biên ngoài ở gáy nhô ra khỏi bề mặt áo hỗ trợ,
tạo cảm giác gờ cứng. Nối topology vai–tay đã liền nhưng crown vai và skinning giữ
thể tích theo xương, không tự tái tạo nếp rủ theo trọng lực.

[Chẩn đoán mesh gốc](../garment_recovery_v1/source_mesh_diagnosis.json) và
[kế hoạch trước khi sửa](../garment_recovery_v1/construction_plan.md) ghi rõ các bề mặt/đường nối này.

## 3. Hai lượt sửa đã thực hiện

| Lượt | Thay đổi | Kết quả/giới hạn |
|---|---|---|
| 1 | Chỉnh tiết diện và mép trên đai; đẩy mặt trong tay áo ra khỏi đai với chuyển tiếp mềm; hạ crown vai; chỉnh cung gáy; tạo một số nếp lớn từ vai | Các tam giác vải kem ở đai biến mất trên front/3/4; cổ gáy bớt nhô. Nhưng kiểm tra tìm thấy thêm tiếp xúc áo–Body khi tay ngang |
| 2 | Điều chỉnh khoảng hở áo–Body trên ba pose có sẵn; tách cục bộ cổ khỏi bề mặt áo hỗ trợ | Loại bỏ các crossing áo–Body được phát hiện ở pose tay ngang trong vùng kiểm tra. Giao nhau cổ giảm nhưng chưa hết; còn tiếp xúc nhỏ tay áo–đai ở pose lưu |

Chỉ sửa tọa độ của ba object: `Kagari_Concept_Robe_Two_Sleeves`,
`Kagari_Concept_Crossed_Collar`, `Kagari_Concept_Soft_Waist_Sash`.
Không thêm đỉnh/mặt, không tăng subdivision, không thay weights, UV hay modifier stack.
Các bước chiếu khoảng hở số học ở lượt 2 nằm trong một cấu hình sửa duy nhất, không có vòng mỹ thuật thứ ba.

Mặt, tóc, Body gốc, `Body_GarmentDisplay`, phần váy dưới, phụ kiện có sẵn và rig được giữ nguyên dữ liệu.
Không dựng lại tóc, mặt hoặc phần thân dưới; không thêm vật liệu/trang trí và không phát triển Skills.
Một datablock clay không được gán vào mesh đã bị loại khỏi file khi lưu; vật liệu thực sự gán vào mesh
giữ nguyên các node/default input/link/image name đã đối chiếu.

## 4. Cải thiện nhìn được và thiếu sót còn lại

### Eo: cải thiện rõ, chưa sạch toàn bộ bề mặt

- [Trước — màu](../../previews/full_concept_v3/front_existing_color.png) →
  [sau — màu](../../previews/garment_recovery_v2/front_existing_color.png).
- [Trước — 3/4](../../previews/full_concept_v3/three_quarter_existing_color.png) →
  [sau — 3/4](../../previews/garment_recovery_v2/three_quarter_existing_color.png).
- Silhouette đai trước/sau liên tục hơn; không còn các mảng tam giác kem rõ như v3 trong những ảnh này.
- Kiểm tra vẫn tìm thấy **13 đoạn cạnh cắt bề mặt** tay áo–đai ở cạnh phải/phía sau của đai,
  khoảng `x=.150–.155, y=.020–.027, z=.927–.947` trong pose lưu. Không thể gọi toàn bộ eo collision-free.
- Nguyên nhân dự kiến: chỉnh áo để tránh Body ở nhiều pose làm một vùng mặt trong tay áo tiến lại gần đai.
  Cần giải quyết liên hệ giữa hình dáng đường may, khoảng hở các lớp và biến dạng, thay vì đẩy từng vùng riêng lẻ.

### Cổ–vai: cổ gáy bớt nhô, mối nối vẫn chưa hoàn thiện

- [Nghiêng trước](../../previews/full_concept_v3/side_clay.png) →
  [nghiêng sau](../../previews/garment_recovery_v2/side_clay.png).
- Cung gáy thấp và gọn hơn, giảm cảm giác một dải ngang nhô cứng. Front overlap chính được giữ lại.
- Vẫn tìm thấy **87 đoạn crossing cổ–áo** trong vùng cổ ở cả ba pose; một số mép nối lá cổ–gáy còn gãy nhẹ.
  Số này giảm so với source nhưng không chứng minh thứ tự lớp đã hoàn toàn đúng.
- Vai còn có khối lồi tròn. Cần dựng lại tiếp giáp cổ–vai và độ dư vải ở đường may trên một cấu trúc
  hỗ trợ thống nhất, tránh các tiếp giáp riêng lẻ được xử lý bằng chiếu khoảng hở.

### Nếp rủ và pose: ổn định hơn ở điểm tiếp xúc, chưa đạt chuyển động vải

- [Pose giơ tay](../../previews/garment_recovery_v2/arm_raised_clay.png),
  [tay ngang](../../previews/garment_recovery_v2/arm_horizontal_clay.png).
- Không thấy tay áo tách khỏi vai hoặc sụp toàn bộ trong ảnh pose đã xem.
- Dưới nách vẫn là các khối túi rộng, tròn; có chỗ thắt/gãy ở chuyển tiếp sang tay áo.
  Các nếp lớn thêm vào chưa đủ tạo cảm giác trọng lượng và lực giữ vải.
- Drape hiện tại được tạo hình sẵn rồi skin theo xương. Nó không tự rủ lại khi đổi pose.
  Kiểm tra va chạm tốt hơn chưa đủ để kết luận biến dạng đẹp hoặc animation-ready.

### Những lỗi ngoài phạm vi còn giữ nguyên

Tóc hở scalp, tóc sau dạng tấm, thiếu các lớp haori, phần váy/giày suy luận chưa được duyệt vẫn tồn tại.
Đó là lý do toàn avatar vẫn chưa đạt gate, nhưng **khuyến nghị FAIL cho recovery này còn có căn cứ
ngay trong eo/cổ–vai và nếp rủ**, không chỉ vì tóc nằm ngoài phạm vi.
Turnaround sheet chưa tạo; cần một nhiệm vụ thiết kế riêng nếu người dùng muốn chốt các góc còn thiếu.

## 5. Kiểm tra giao nhau — kết quả có giới hạn

| Cặp bề mặt / pose | Full v3 | Recovery v1 | Recovery v2 |
|---|---:|---:|---:|
| Áo/tay áo–đai, pose lưu | 239 | 0 | 13 |
| Áo/tay áo–đai, nâng tay / ngang | 0 / 0 | 0 / 0 | 0 / 0 |
| Váy dưới–đai, mỗi pose | 592 | 0 | 0 |
| Cổ–áo, pose lưu / nâng tay / ngang | 329 / 329 / 333 | 149 / 149 / 149 | 87 / 87 / 87 |
| Cổ–Body, pose lưu / nâng tay / ngang | 30 / 30 / 18 | 0 / 0 / 0 | 0 / 0 / 0 |
| Áo–Body, pose lưu / nâng tay / ngang | 58 / 0 / 244 | 58 / 0 / 450 | 43 / 0 / 0 |

Các số là **đoạn cạnh của mesh đã đánh giá cắt qua tam giác đối diện**, kiểm tra hai chiều,
có Solidify, trong khoảng cao được ghi ở JSON. Không phải diện tích giao nhau, số lỗi độc lập,
mức độ nghiêm trọng hay chứng nhận toàn model. Số 0 không chứng minh mọi pose/bề mặt đều sạch.
Một vùng giao nhau có thể tạo nhiều crossing segments. Các kết luận hình ảnh được nêu riêng phía trên.

[Kiểm tra kỹ thuật đầy đủ](technical_verification.json) chứa tọa độ mẫu và vùng kiểm tra.
Chưa kiểm tra toàn bộ tự giao nhau, chuyển động liên tục, pose tay trên đầu hay tương tác hair–clothes.

## 6. Bảo toàn, skinning và độ phức tạp

Sau khi mở lại candidate: Face và toàn bộ morph, Hair, Body gốc, rig rest và pose lưu khớp source.
Các mesh ngoài ba object sửa cũng khớp dữ liệu bảo vệ. Bốn garment surfaces giữ nguyên connectivity,
weights, tên group, UV assignment, material assignments, parent và modifier settings so với full v3.

Mỗi garment surface vẫn là một thành phần nối liền; không có mặt diện tích 0 hoặc cạnh nonmanifold
bên trong. Weights có tổng chuẩn hóa, tối đa 4 ảnh hưởng; armature modifier tham chiếu rig gốc.
Tọa độ evaluated hữu hạn ở ba pose. Các điều này là bằng chứng kỹ thuật, không phải duyệt mỹ thuật.

| Phạm vi | Raw triangles | Viewport evaluated triangles | Thay đổi so với full v3 |
|---|---:|---:|---:|
| Bốn bề mặt trang phục | 20.105 | 41.908 | 0 |
| Object bật render | 47.434 | 118.773 | 0 |
| Toàn scene gồm archive/hidden | 86.936 | 189.019 | 0 |

| Garment | Raw | Sau Solidify | Phần tăng do Solidify |
|---|---:|---:|---:|
| Thân áo + hai tay | 11.273 | 23.068 | 11.795 |
| Cổ áo | 1.152 | 2.712 | 1.560 |
| Đai | 1.920 | 4.224 | 2.304 |
| Váy dưới, không sửa | 5.760 | 11.904 | 6.144 |

Armature không tăng số tam giác. Không có modifier mới. Counts dùng viewport evaluation hiện tại;
inventory bật render dựa trên object `hide_render`, không mô phỏng loại trừ collection.
Chưa có số tam giác VRM hoặc FPS. Xem [audit](geometry_audit.json),
[bảo toàn garment/vật liệu](preservation_details.json) và [invariants](protected_invariants.json).

## 7. Vì sao dừng và đề xuất bước tiếp theo

Hai lượt đã chứng minh có thể sửa hình dáng eo rõ hơn **mà không tăng mesh complexity**.
Nhưng mô hình bề mặt điều khiển + skinning cố định chưa xử lý đáng tin cậy đồng thời đường may,
thứ tự lớp, độ dư vải và độ rủ ở mọi pose. Sửa khoảng hở với một bề mặt có thể làm phát sinh tiếp xúc
với bề mặt khác; việc giảm số crossing không tự tạo ra form vải đẹp.

Vì còn các crossing nêu trên và nếp rủ/vai chưa đạt, không đề xuất tiếp tục vòng sửa đỉnh thứ ba
trên cùng phương án trong nhiệm vụ này. Một lần dựng riêng mối nối cổ–vai bằng rập/đường may rõ hơn,
hoặc chỉnh thủ công có kiểm soát trên các pose mục tiêu, cần được xem xét trước khi mở rộng.
Đó là đề xuất, chưa cài công cụ hay thực hiện một reconstruction mới.

VRM export/reimport, expressions trong runtime, tracking, webcam, OBS, full-body animation và
chuyển động váy/chân đều **NOT TESTED**. Archive phải được loại trừ nếu sau này chuẩn bị export.
Trạng thái cuối: `REQUIRES_HUMAN_ART_REVIEW`; khuyến nghị agent: **FAIL**; người dùng chưa duyệt kết quả.
