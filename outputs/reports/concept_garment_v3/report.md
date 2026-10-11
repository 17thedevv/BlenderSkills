# Kagari — dựng lại form theo concept

**Đánh giá agent: CẢI THIỆN, ĐẠT MỘT PHẦN. Chưa được người dùng duyệt.** Không tuyên bố đạt toàn bộ Clay Gate.

## Mẫu và phạm vi

Dùng [concept Kagari hiện có](../../design/concept_option2_kagari.jpg), không có hình concept mới được đính kèm. Các dấu hiệu được quan sát trực tiếp: bản cổ chéo rộng, vai xuôi, tay áo dài loe, eo gọn và nếp vải lớn có tiết chế. Mặt sau và cấu trúc đường may là phần suy diễn. Đây là mẫu một cổ áo, một tay áo và thân hỗ trợ trên mannequin; chưa tái tạo toàn bộ lớp áo khoác, hai tay áo, đai và phần dưới của concept.

Mẫu đã lưu: [kagari_concept_garment_v3.blend](../../wip/kagari_concept_garment_v3.blend). Version `concept-directed-controlled-sheets-v3`; SHA256 `131d3c25f8c4b37c81786bfe2af970c254df256c20c8e114ed6de9f26b652af2`.

## Phương pháp đã thực hiện

Dựng các bề mặt vải mới bằng lưới có tham số, dựa trên đường nét concept và vai của mannequin. Không tái sử dụng mesh áo Cycle 03 hoặc mesh Cloth cũ, không chạy Cloth ở lần này. Hai thân trước chồng lên nhau; cổ chạy theo mép thân, lớp trái phủ trên lớp phải và nối qua gáy bằng chung đỉnh. Phần cổ dưới kết thúc trong vùng được thân trên che phủ, tránh chữ X lộ ra dưới ngực. Vai nối qua các hàng đỉnh tương ứng; gốc tay áo dùng chung đỉnh với thân. Tay áo gồm hai mảnh dài, mặt nối trên/dưới bo cong và cửa tay rỗng rộng.

Mannequin lấy bản sao từ study trước; tư thế dựng hạ hai tay 60° so với phương ngang. Chuyển bề mặt đã dựng về rest space bằng nghịch đảo skinning; gắn xương chest/upperChest/shoulder/upperArm/lowerArm với tối đa bốn ảnh hưởng mỗi đỉnh. Solidify dày 1,5 mm thân/tay và 1,8 mm cổ. Macro folds đặt theo vùng eo, nách và cuff; chưa có mô phỏng trọng lực hay xác nhận pattern may mặc 2D.

Kagari gốc giữ nguyên SHA `4a3dc7560df7d3f0db452a4d0c06faf55238bce2fd045ed23f8c27ac75dd6051`. Mẫu panel cũ cũng giữ nguyên. Không sửa Skills, Face, Hair, morphs hoặc rig gốc; không cài phần mềm, thêm ornament, màu burgundy/cream hay shader trang trí.

## Render và so sánh

Đã nhìn trực tiếp sáu ảnh toàn cảnh: trước, 3/4, nghiêng, sau, nâng tay thêm 30° (còn 30° dưới phương ngang) và stress thêm 60° (tay ngang). Có hai ảnh cận cổ/vai bổ sung, không thay thế ảnh toàn cảnh. Pose dùng Armature thuần, không Cloth hoặc corrective morph. Đã xem các ảnh đối chiếu của Cycle 03 và study panel cũ.

Camera, ánh sáng clay, mannequin và tư thế trong [comparison_manifest.json](comparison_manifest.json) khớp chính xác với bản mới. Study panel cũ vốn dựng ở tư thế tay hạ 30°; render so sánh này cho thấy nó biến dạng ở pose hạ 60°, không thay thế những ảnh neutral gốc của nó. Cycle 03 có hai tay áo và đai, mẫu mới chỉ một tay áo; không so số polygon như cùng phạm vi.

| Phần | Cycle 03 / study panel cũ | Mẫu theo concept |
|---|---|---|
| Cổ | Giao cổ bị nhăn / bản cổ hẹp, vai cao | Cổ rộng cong, một đường chéo che lớp dưới; gáy còn bật |
| Vai | Hở gốc tay / tấm ngang cao | Vai xuôi và mesh nối liên tục; profile còn gợn rộng |
| Tay áo | Ống ngắn / túi ngắn bị nhăn | Tay dài loe, cửa tay rỗng rõ ở 3/4; mặt còn trơn |
| Thân trước | Khối đều / nếp crumple dồn ở root | Thân thoáng hơn, eo gọn, nếp lớn gần eo |
| Mặt sau | Phẳng / nhăn bất đối xứng | Form sạch hơn nhưng vẫn thiếu độ rủ |
| Nâng 30° | Gốc rời / nách gãy nhiều | Không có nếp gãy lớn ở front render; chưa chứng nhận mọi pose |

## Khuyết điểm còn lại

1. **Cổ sau/vai:** ảnh cận 3/4 và nghiêng cho thấy mép gáy bật khỏi cổ và yoke còn có một gờ rộng. Curve/clearance đang đơn giản; cần fit lại mặt cắt sau khi người dùng duyệt hướng form.
2. **Độ rủ:** silhouette tay rộng hơn rõ, nhưng tay và lưng còn giống bề mặt sạch có form hơn là vải có trọng lượng. Cần vài nếp lớn có điểm neo; không tăng chi tiết đồng loạt.
3. **Clearance và rig:** phép nearest-normal trên mannequin cắt có dấu hiệu rủi ro: thân/cổ lần lượt 3/2 mẫu ở neutral, 0/2 ở nâng 30°, 18/1 ở tay ngang. Đây không phải phép kiểm chứng giao mesh đầy đủ, cũng không phải số lỗ xuyên được xác nhận. Chưa được ghi INTERSECTION_FREE. Túi tay xoay theo xương, không tiếp tục rủ theo trọng lực thế giới.

Vùng bụng dưới và cổ mannequin có biên cắt chẩn đoán; đó không phải hình học avatar hoàn chỉnh. Bên không dựng tay áo cố ý để trống.

## Mesh và kiểm tra thật

| Thành phần | Tam giác raw | Tam giác sau modifier viewport |
|---|---:|---:|
| Thân + một tay áo | 8.507 | 17.516 |
| Cổ chéo liên tục | 1.152 | 2.712 |
| Tổng trang phục | 9,659 | 20,228 |
| Scene mannequin | 16.567 | 27.136 |

Hai surface riêng đều một thành phần liên thông, không có face diện tích bằng không hoặc cạnh non-manifold bên trong. Biên mở raw tại neckline, hem, cửa tay là có chủ đích trước Solidify. Weight chuẩn hóa, không thiếu weight, không quá bốn bone; tọa độ sau modifier hữu hạn trong ba pose. Không có subdivision hay Cloth modifier. So với study cũ (6.736 raw / 14.260 evaluated), bản mới tăng mesh để có tay dài và bề mặt nối được kiểm soát; không phải tối ưu runtime.

[Kiểm tra kỹ thuật](technical_verification.json), [audit thật](geometry_audit.json), [render manifest](render_manifest.json), [đánh giá hình ảnh](visual_review.json), [kế hoạch trước mesh](../concept_garment_v1/construction_plan.md).

## Các lượt dựng và giới hạn

Ba candidate mới được giữ riêng. v1 lộ form ngực quá sát, cổ đọc thành X và vai gợn; v2 sửa lớp phủ, bề mặt thân và thứ tự hàng vai nhưng tay quá hẹp khi nhìn trước; v3 mở phần vải dưới tay, mở rộng cổ và thêm hai nếp lớn gần eo. Đây là phương pháp bề mặt điều khiển theo concept, khác các thử nghiệm Cloth trước. Dừng sau v3 để người dùng đánh giá.

VRM export/reimport, Warudo, webcam, OBS và FPS đều NOT_TESTED. Study không phải avatar VRM đầy đủ; chưa có UV/material production, form vải động, pose-corrective hoặc chứng nhận góc xoay rộng. Mặt/người/hair gốc được bảo toàn bằng giữ nguyên source, chưa ghép study vào Kagari.

**REQUIRES_HUMAN_ART_REVIEW.** Trang phục chưa duyệt; không chuyển sang trang trí/materials hoặc tích hợp avatar trong lượt này.
