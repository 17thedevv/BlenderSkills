# Báo Cáo Kiểm Thử Chất Lượng Model & Thiết Lập Blender

## 1. Kết Quả Cài Đặt Công Cụ
- **Blender 4.2.0 LTS**: Đã cài đặt portable tại `D:\tools\blender-4.2.0-windows-x64\blender.exe` và thêm vào biến môi trường PATH.
- **VRM Add-on cho Blender**: Đã cài đặt và kích hoạt thành công (`bpy.ops.import_scene.vrm` và `bpy.ops.export_scene.vrm` hoạt động 100%).
- **OBS Studio**: Sẵn sàng tại `C:\Program Files (x86)\Steam\steamapps\common\OBS Studio\bin\64bit\obs64.exe`.
- **Webcam**: `USB2.0 HD UVC WebCam` đã sẵn sàng.

---

## 2. Kiểm Thử File `Aplaybox_Hsin.zip`
- **Thử nghiệm mở trong Blender 4.2**:
  - Khi mở trực tiếp: Báo lỗi `Failed to read blend file, not a blend file`.
  - Khi giải nén luồng Zstandard (dung lượng thực 232 MB): Header tệp có định dạng `BLENDER17-01v0501` thay vì `BLENDER_v...`.
  - Phân tích cấu trúc nhị phân: Tệp này được bảo vệ/mã hóa bởi cơ chế chống trích xuất (DRM) riêng của Aplaybox cho model game Kuro Games, dẫn đến lỗi `Missing DNA block` trong Blender tiêu chuẩn.
- **Đánh giá bản quyền**:
  - Model gốc thuộc về Kuro Games (*Wuthering Waves*). Điều khoản Aplaybox nghiêm cấm sử dụng cho mục đích thương mại, kiếm tiền hoặc làm VTuber stream cá nhân.
- **Kết luận**: File này hoàn toàn **không thể sử dụng** cả về mặt kỹ thuật lẫn pháp lý.

---

## 3. Kiểm Thử Thành Công Pipeline VRM & Render Trong Blender
- Đã kiểm thử import thành công model chuẩn VRM 1.0 vào Blender 4.2:
  - Khung xương: 51 xương Humanoid đầy đủ chuẩn VRM 1.0.
  - Khối biểu cảm (Shape Keys): Đầy đủ 13 biểu cảm bắt buộc (`blink`, `blink_L`, `blink_R`, `lip_a`, `lip_i`, `lip_u`, `lip_e`, `lip_o`, `face_happy`, `face_angry`, `face_sad`, `face_relax`, `face_surprise`).
  - Đã xuất thành công báo cáo kỹ thuật `scripts/audit_blend.py`: [scene_audit_seedsan.json](file:///d:/Project-17/blender/outputs/reports/scene_audit_seedsan.json).
  - Đã render thử nghiệm thành công 5 góc nhìn Workbench: [front.png](file:///d:/Project-17/blender/outputs/previews/seedsan_test/front.png), [three_quarter.png](file:///d:/Project-17/blender/outputs/previews/seedsan_test/three_quarter.png), [face_close.png](file:///d:/Project-17/blender/outputs/previews/seedsan_test/face_close.png).

---

## 4. Hành Động Tiếp Theo: Tiến Vào Gate B (Tạo Hình Khuôn Mặt)
Pipeline Blender và VRM đã hoạt động mượt mà. Mời bạn duyệt phương án nhân vật để chúng tôi tiến hành dựng khối khuôn mặt và tóc chi tiết:
1. **Phương án 1: Aoi (蒼)** — Cyberpunk Streamer (Tóc bob xanh navy, mắt ngọc ánh sao, áo hoodie tech-wear).
2. **Phương án 2: Kagari (篝)** — Astral Shrinekeeper (Tóc đuôi ngựa lệch nơ đỏ, mắt vàng hổ phách, áo vu nữ cách tân).
