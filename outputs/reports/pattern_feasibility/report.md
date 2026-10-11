# Kagari — Pattern-Based Garment Modeling Feasibility Study

**Kết quả mỹ thuật: FAIL. Khuyến nghị: ABANDON cấu hình dựng rập/sewing tự động hiện tại. Trạng thái: REQUIRES_HUMAN_ART_REVIEW.**

Thử nghiệm đã tạo một nền geometry mới bằng các mảnh rập phẳng và sewing constraints thật của Blender, thay vì sửa vertices của Recovery v2. Tuy nhiên, ảnh thực tế không chứng minh cải thiện đáng kể về cấu trúc vải hoặc silhouette. Cổ áo và vai xấu hơn baseline; tay áo có túi vải dưới trọng lực ở pose giơ tay nhưng không giữ được hình dáng ở neutral. Bản chỉ skinning cũng thất bại. Không nên dùng prototype này để dựng tiếp toàn bộ Kagari.

Khuyến nghị ABANDON áp dụng cho **pipeline tự động và cấu hình rập/constraint đã thử**, không phải kết luận rằng mọi phương pháp pattern-based hoặc Blender Cloth đều bất khả thi. Bước khác đáng xem xét sau quyết định của người dùng là rập được artist fitting trực tiếp hoặc garment base có provenance/license đã kiểm tra. Chưa cài, mua, tải hay dùng asset bên ngoài.

## 1. So sánh phương pháp và quyết định

[Bảng đánh giá bốn chiến lược và nguồn chính thức](strategy_comparison.md) so sánh native sewing/cloth, bề mặt tham số từ rập, phần mềm chuyên dụng và kimono mesh dựng sẵn theo geometry, drape, art control, automation, rigging/VRM và chi phí. [Inventory cục bộ](installed_tools.json) chỉ xác nhận portable Blender và phạm vi registry/D:/tools đã kiểm tra; không khẳng định đã tìm hết mọi ổ đĩa.

Chọn native Blender Cloth với **các cạnh loose-edge sewing**, vì có sẵn và cho phép kiểm tra trực tiếp ảnh hưởng của cut, seam và gravity. Các thử nghiệm panel cũ có bridge/yoke dựng sẵn, ghim vùng vai rộng và freeze drape; lần này bỏ bridge đó, tạo các mép rập riêng rồi dùng lực may. [Kế hoạch trước khi dựng](construction_plan.md) ghi rõ phạm vi, lớp vải, seam, pin và test.

## 2. Nền dựng mới và cấu trúc thật

Chỉ sao chép `Body_GarmentDisplay` và `Armature` từ Recovery v2 vào cảnh rỗng. Mannequin cắt phần thân trên, giữ skin/inner display làm collider, thêm đầu trơn để định hướng. Không đưa mặt/tóc/phụ kiện của Kagari vào cảnh thử. Mọi garment vertices trong generator được tạo mới; script đối chiếu mới là nơi riêng biệt đọc garment cũ.

Trial 3 gồm sáu cut grids có tọa độ 2D theo mét: front under, front over, back trái/phải, sleeve front/back của **một tay áo**. Thân hỗ trợ chỉ dùng cho nối cổ–vai–tay áo và kết thúc gần z=.98m; không dựng sash, áo dưới, trang trí hay cả nhân vật. [Rập và các cặp vertices may](trial3/patterns_and_seams.json), [sơ đồ metric](../../previews/pattern_feasibility/metric_patterns.svg).

Các seam riêng: vai, trung tâm lưng dưới cổ, phần gắn armhole front/back, phần thân dưới vent, mép trên/dưới túi tay áo, distal bag và proximal bag. Cuff và underarm vent được để mở có chủ đích. Hai mép cần may vẫn là vertices độc lập trong scene nguồn, nối bởi cạnh không thuộc face; Cloth bật `use_sewing_springs`. Front positive-X được đặt ngoài front negative-X, nhưng solve không duy trì tốt thứ tự và độ rộng giao lớp.

Trial 3 ghim rất ít điểm cổ, hai điểm ở mép dưới support và hai target trên sleeve front theo armature; không ghim toàn bộ vai/yoke. Đây là constraint phục vụ thử nghiệm, chưa phải fitting may mặc được duyệt. Sau solve, các cặp seam được average/weld thành mesh liên tục. **Weld sau solve có thể che khoảng cách may còn lớn; topology nối liền không chứng minh may vật lý thành công.**

Cổ finishing band được tạo **sau drape** từ mép cut front, có strip UV theo mét, chiều dày và đoạn nape suy diễn, weld chính xác hai seam endpoint. Cổ này là một assembly liên tục, nhưng không có solve riêng của một collar panel phẳng được may vào thân. Đây là hạn chế quan trọng của prototype, không được trình bày như một kết quả cloth collar đã thành công. Side/back và phần cổ gáy là diễn giải từ concept trước, chưa phải blueprint được duyệt.

## 3. Các cấu hình thử và chi phí đo được

| Cấu hình | Thay đổi ở rập/constraint | Kết quả ảnh đã xem | Thời gian solver thực |
|---|---|---|---:|
| Trial 1 | Một back cut, ghim cổ, may các sheet riêng; pose transition ngắn | Sleeve co thành khối, overlap mất, seam rách/nhăn. Một số vertices không thuộc face rơi tự do; không dùng bounds toàn mesh để đánh giá garment | 32.37s / 235 frames |
| Trial 2 | Hai back cuts có số mẫu vai khớp, thêm giữ mép dưới và sparse sleeve targets, tăng quality và thời gian đổi pose | Túi sleeve dễ nhận ra hơn khi giơ tay; thân/vài nhăn gắt, nape còn rời và collar nhọn; rig-only xuyên mép trên | 180.72s / 410 frames |
| Trial 3 — artifact cuối | Không may cặp neck anchor đang bị giữ ở hai vị trí khác nhau; chỉ giữ sleeve front thay vì cả hai mép đối nhau; tăng sewing force; nối collar nape endpoint | Cổ một component và có túi sleeve ở horizontal, nhưng neutral thu hẹp/crumple; vai và front overlap vẫn fail | 207.27s / 410 frames |

Đây là ba cấu hình mới trong cùng feasibility study, không phải ba lượt sửa vertex của garment cũ. Đã dừng modeling sau Trial 3. Thời gian trên chỉ là loop solve đo trên máy này, không bao gồm toàn bộ render/audit và không phải benchmark Warudo/FPS. Trial 3 dùng quality 12, self collision, không subdivision khi solve. Thông số vải chưa được hiệu chuẩn từ chất liệu thực.

Trial 3 trước weld vẫn có seam residual đáng kể:

| Snapshot | Frame | Mean gap trên cặp may | Max gap | RMS đổi từ sample trước |
|---|---:|---:|---:|---:|
| Neutral | 200 | 18.6mm | 96.2mm | 25.4mm từ frame180 |
| Giơ thêm30° | 300 | 14.7mm | 168.4mm | 39.6mm từ frame270 |
| Ngang | 410 | 14.6mm | 175.3mm | 11.5mm từ frame390 |

[Log đo solver](trial3/simulation.json). Các giá trị là khoảng cách endpoint, không phải số lỗi độc lập, và không chứng nhận equilibrium. Kết hợp với ảnh nhăn/vỡ, chúng là bằng chứng solve chưa tạo được garment tốt; không được dùng weld để tuyên bố đã khép seam.

## 4. Render và nhận xét biến dạng

[Gallery đối chiếu tương tác](../../previews/pattern_feasibility/review.html) có front/3-quarter/side/back ở cả ba pose, selector ba cấu hình, và mode rig-only riêng. Có **12 ảnh final từ solve + 2 ảnh rig-only**, cùng **12 ảnh Recovery v2 đối chiếu**. Đã xem trực tiếp toàn bộ 14 final PNG và 12 matched baseline PNG; Trial 1/2 được xem các ảnh đại diện, không khẳng định đã review đủ mọi ảnh của chúng.

Neutral dùng upper-arm bone z −68° ở tay có sleeve, giống saved Recovery v2. +30° nghĩa là bone z −38°; horizontal là 0°. Tay đối diện giữ +68°, lower-arm giữ pose nguồn. Đây là góc bone được đặt, không phải đo góc vật lý của mọi đoạn tay từ ảnh. Source mannequin chuyển pose dần trong Cloth timeline; ảnh final dùng snapshot mesh tại frame tương ứng, không phải cloth hoạt động trong VRM.

| Tiêu chí | Quan sát thật | Kết luận |
|---|---|---|
| Silhouette neutral | Sleeve co hẹp, vùng vai gồ vụn; không có khối áo kem mềm/rộng như concept | FAIL |
| Collar/layer/độ dày | Thickness 1.6mm tồn tại; cổ và front support bị kéo mở, giao nhau thành các dải nhọn phía dưới, under leaf crumple khi raise | FAIL, dù topology collar liên tục |
| Vai–sleeve | Body/support/sleeve có seam relationships rõ trong dữ liệu, nhưng bề mặt vai nhăn gắt; side stress lộ shoulder/body và mép tiếp xúc không thuyết phục | FAIL |
| Fold/volume | Solve tạo túi vải và fold thay đổi với pose, đặc biệt horizontal; fold tập trung thành crumple thay vì broad folds anime có chủ đích | PARTIAL về cơ chế, FAIL về form |
| Neutral→+30°→horizontal | Simulated bag đổi theo gravity/contact nhưng front và lưng bị kéo lệch; dưới nách vẫn vỡ form | FAIL |
| Skinning riêng | Clone neutral dùng armature, không cloth/correctives. +30° có hở mép trên; horizontal để arm nằm trên/xuyên sleeve | FAIL cho rigging production |
| Không giao nhau | Không có chứng nhận intersection-free; visible contacts/breakthrough và seam residual đủ để bác duyệt. Không lặp một chỉ số ray-hit để thay review | NOT_CERTIFIED / không đạt hình ảnh |

[Visual findings có từng vùng, ảnh, giả thuyết nguyên nhân và hướng xử lý](visual_review.json). Các hướng sửa trong đó là **đề xuất chưa thực hiện**. Các biên cắt thân mannequin và phía không sleeve là vùng chẩn đoán, không bị chấm như lỗi áo hoàn chỉnh; những lỗi collar/shoulder trên phía đang thử vẫn quan sát được độc lập.

## 5. So với Recovery v2 và kiểm soát ảnh

Baseline được đọc vào một cảnh so sánh riêng với chính mannequin/head trơn của prototype. Chỉ bản sao garment trong cảnh đối chiếu được cắt bỏ sleeve đối diện và phần dưới support; nguồn Recovery v2 được giữ nguyên. [Manifest và phạm vi crop](comparison_manifest.json). [Gallery Recovery v2 gốc](../../previews/garment_recovery_v2/review.html) vẫn được giữ để xem trang phục trong cả nhân vật, tránh đánh đồng bản crop với bản model gốc.

Camera/location/rotation/ortho scale lấy từ render manifest Recovery v2; neutral dùng framing gốc, các stress dùng scale rộng của raised/horizontal ở cả hai bên. Cùng Workbench Studio `Default`, gray .62, world .15, Standard/None, 1000px, shadow/cavity settings. [Kiểm tra setting source/study](render_settings_inspection.json). Không dùng màu, texture hay lighting mới để che geometry.

| Vùng | Recovery v2 | Mẫu từ rập |
|---|---|---|
| Cổ | Collar crossover ổn định nhưng nape/seam chưa đẹp | Cấu trúc cut mới có provenance rõ, nhưng crossover nhọn, mở và méo hơn |
| Vai | Form trơn, tròn/cứng; chưa giống vải tốt | Bỏ pinned bridge cũ nhưng sinh nhiều crumple và tiếp xúc xấu hơn |
| Sleeve | Neutral dài/rộng, raise thành rounded underarm bag bị đóng băng theo rig | Sim có hanging bag/fold thay đổi thật, nhưng neutral mất silhouette; rig clone vẫn hở/xuyên |
| Lưng | Khá phẳng, thiếu nếp có lực | Có folds nhưng nhăn rối, tension lệch và pull vùng cổ; thêm folds không phải cải thiện mỹ thuật |

**Không có cải thiện tổng thể đáng kể để khuyến nghị proceed.** Khác biệt thấy được đến từ cut/solve/pose; cả hai dùng clay/light cố định. Phạm vi áo, hem và pattern dimensions khác nhau, nên không dùng giảm triangles hay việc bỏ các phần outfit để kết luận đẹp hơn.

## 6. Audit geometry và modifier

| Phạm vi | Vertices raw | Triangles raw | Triangles evaluated |
|---|---:|---:|---:|
| Trial3 support + một sleeve, neutral | 2,275 | 4,400 | 9,108 |
| Collar assembly, neutral | 345 | 544 | 1,376 |
| New garment neutral tổng | 2,620 | **4,944** | **10,484** |
| Recovery v2 robe/collar trong bản crop tương ứng | — | 9,565 | 20,076 |

Counts là Blender viewport evaluation, không phải VRM export/FPS. Baseline có cut/topology/hem khác; số thấp hơn không chứng minh phương pháp tốt hơn. Các bản snapshot, rig clone, archive và collection 2D nằm trong `.blend` nhưng loại khỏi new-garment-neutral total. Audit inventory `hide_render=False` không tính collection exclusion; không dùng tổng đó như số mesh thực xuất hiện trong ảnh.

Frozen garment dùng Solidify; rig-only thêm Armature trước Solidify. Không có live Cloth trong mesh visible final. Support/sleeve và collar đều một face component riêng, zero zero-area faces và zero interior edges có >2faces ở raw mesh. Boundary là chủ ý cho shell/cuff/vent/crop trước thickness, nhưng kết quả đó không bảo đảm contact đẹp. Rig-only có positive normalized weights, tối đa ba deform influences; hình pose vẫn fail.

[Geometry/modifier audit đầy đủ](trial3/geometry_audit.json), [verification](trial3/technical_verification.json), [comparison counts](geometry_comparison.json). Integrity checks PASS: artifact/source/setup/PNG SHA khớp, duplicate backup khớp nguồn, coordinates finite. Đây chỉ là kiểm tra dữ liệu, không phải artistic PASS.

## 7. Cảnh nguồn, script và preservation

- Prototype cuối: [kagari_pattern_trial3_prototype.blend](../../wip/kagari_pattern_trial3_prototype.blend), SHA `07bc9add34e23df5320ff0dfdc36af7c70b9172df778342313f804b2dcdde5a7`.
- Cảnh nguồn rập/sewing trước solve: [kagari_pattern_trial3_source.blend](../../wip/kagari_pattern_trial3_source.blend), SHA `cfc1c49fcde3963cd6a5947f29c121f755baffa70332403bcbbe3b95035800a6`.
- Source character giữ nguyên: [kagari_garment_recovery_v2.blend](../../wip/kagari_garment_recovery_v2.blend), SHA `9006f5c03019ad0fd4aeeeba1c97b2a30e96f65ac1b8fa0d9093000664017d6d`.
- [Độc lập backup nguồn](../../backups/pattern_feasibility_start/kagari_garment_recovery_v2.blend), state và DELIVERY trước task được giữ trong cùng backup folder.
- [Build cả ba cấu hình](../../../scripts/build_pattern_feasibility.py), [render baseline riêng](../../../scripts/render_pattern_comparison.py), [reload/verify](../../../scripts/verify_pattern_feasibility.py), [publisher](../../../scripts/publish_pattern_feasibility.py).
- [Hướng dẫn tái chạy và ý nghĩa từng mesh](reproduce.md), [render/pose/hash manifest](trial3/render_manifest.json), [preservation hash của Recovery v2/fullv3/Cycle03](source_preservation.json).

Trial1/2 source và prototype độc lập cũng được giữ trong `outputs/wip`, với hashes trong manifest riêng. Scene nguồn được lưu trước cache; script tái chạy các frame tuần tự để regenerate solve. Không hứa `.blend` hoặc solver bit-identical trên mọi máy. Không chỉnh hoặc tái lưu bất kỳ artifact nguồn cũ nào; byte hashes đủ để xác nhận nguồn face/hair/morph/rig không bị thay đổi trên disk.

## 8. Production integration và điểm còn thiếu

[Kế hoạch retopology, UV, weight painting, corrective shapes, secondary bones và VRM](production_integration.md) tách rõ phần cần làm và phần chưa thử. Trước production phải có **cut/form tốt**, validate seam closure rồi mới retopo. UV hiện là metric working islands, chưa atlas; thickness chưa export bake/reimport. Weights mới chỉ heuristic; chưa corrective keys hoặc sleeve bones. Các snapshot pose không tự trở thành morph rigged và Blender driver logic không tự được chuyển sang runtime.

Blender cloth cache không tự chạy trong VRM. Spring bones là một hệ bone secondary-motion khác; cần controller/runtime test riêng nếu dùng pose corrective. Không xuất VRM, không thử tracking/OBS/FPS, không integrate prototype vào Kagari đầy đủ.

Điểm thiếu quyết định: rập chưa được fitting thủ công lên mannequin, collar chưa được may/simulate riêng, anchor/force chưa thỏa cả body clearance và ease, solve chưa hội tụ tốt, và phép weld sau solve làm topology đẹp về số liệu hơn trạng thái may thực. Cả hình simulation lẫn rig-only đều cho thấy lỗi đủ nghiêm trọng để dừng.

**Thí nghiệm đã hoàn tất; modeling dừng. Chờ người dùng đánh giá phương hướng. Không mở gate toàn nhân vật, materials, decorations hoặc export.**
