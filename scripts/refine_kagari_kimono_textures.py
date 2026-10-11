"""Refine Kagari textures:
- Paint authentic Miko Kimono onto body skin (_10.png)
- Paint cream-white kimono haori with burgundy/gold trim onto tops (_13.png)
- Add gold floral motifs
- Clean shoulder straps and wristbands
"""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from pathlib import Path

ROOT = Path("D:/Project-17/blender")
SRC_TEX = ROOT / "outputs/sources/vroid_textures"
OUT_TEX = ROOT / "outputs/textures_kagari_vroid"

# 1. Body Skin with Miko Kimono
src_body = Image.open(SRC_TEX / "_10.png").convert("RGBA")
arr_b = np.array(src_body, dtype=np.float32)

# Lift skin tone to porcelain peach
r_skin = arr_b[:, :, 0] / 255.0
g_skin = arr_b[:, :, 1] / 255.0
b_skin = arr_b[:, :, 2] / 255.0

r_new = np.clip((1.0 - (1.0 - r_skin)**1.5) * 255.0, 0, 255)
g_new = np.clip((1.0 - (1.0 - g_skin)**1.9) * 242.0, 0, 255)
b_new = np.clip((1.0 - (1.0 - b_skin)**2.1) * 235.0, 0, 255)

is_skin = (arr_b[:, :, 0] > 120) & (arr_b[:, :, 1] > 80)
arr_b[is_skin, 0] = r_new[is_skin]
arr_b[is_skin, 1] = g_new[is_skin]
arr_b[is_skin, 2] = b_new[is_skin]

body_im = Image.fromarray(arr_b.astype(np.uint8), mode="RGBA")
draw = ImageDraw.Draw(body_im)

cream_white = (255, 249, 242, 255)
burgundy = (139, 30, 63, 255)
burgundy_deep = (110, 20, 48, 255)
gold = (230, 184, 0, 255)
neck_skin = (252, 238, 230, 255)

# Clean neck & throat hollow
draw.rectangle([760, 60, 1280, 260], fill=neck_skin)

# Clean shoulder straps with logo at top corners
draw.rectangle([20, 0, 220, 80], fill=cream_white)
draw.rectangle([780, 0, 980, 80], fill=cream_white)
draw.rectangle([1820, 0, 2020, 80], fill=cream_white)

# Torso Base: Cream-White Inner Kimono
draw.rectangle([480, 240, 1560, 960], fill=cream_white)
draw.rectangle([0, 150, 480, 960], fill=cream_white)
draw.rectangle([1560, 150, 2048, 960], fill=cream_white)

# Clean wristbands (y: 180 to 240, x: 230 to 310 and 680 to 760)
draw.rectangle([230, 170, 310, 245], fill=neck_skin)
draw.rectangle([680, 170, 760, 245], fill=neck_skin)

# Crossover V-Neck Collar
# Inner White V-Collar
draw.polygon([(910, 220), (1020, 380), (1130, 220)], fill=neck_skin)
draw.polygon([(890, 220), (910, 220), (1030, 400), (1010, 400)], fill=(245, 240, 235, 255))

# Outer Burgundy Lapels (wrapping kimono)
# Left lapel (character right / viewer left): from (820, 220) to (980, 640)
draw.polygon([(800, 220), (920, 220), (1140, 640), (1000, 640)], fill=burgundy)
draw.line([(800, 220), (1000, 640)], fill=gold, width=10)

# Right lapel (character left / viewer right): crossing over
draw.polygon([(1120, 220), (1240, 220), (1040, 640), (920, 640)], fill=burgundy)
draw.line([(1240, 220), (1040, 640)], fill=gold, width=10)
draw.line([(1120, 220), (920, 640)], fill=gold, width=10)

# Floral gold vine ornaments on lapels
for y_pt in [320, 420, 520]:
    # Gold leaf/flower dots
    draw.ellipse([880, y_pt, 896, y_pt + 16], fill=gold)
    draw.ellipse([865, y_pt - 10, 877, y_pt + 2], fill=gold)
    draw.ellipse([895, y_pt + 8, 907, y_pt + 20], fill=gold)
    
    draw.ellipse([1140, y_pt, 1156, y_pt + 16], fill=gold)
    draw.ellipse([1155, y_pt - 10, 1167, y_pt + 2], fill=gold)
    draw.ellipse([1125, y_pt + 8, 1137, y_pt + 20], fill=gold)

# Burgundy Obi Sash at waist (y: 640 to 860)
draw.rectangle([480, 640, 1560, 860], fill=burgundy_deep)
draw.line([(480, 640), (1560, 640)], fill=gold, width=8)
draw.line([(480, 860), (1560, 860)], fill=gold, width=8)
# Back obi
draw.rectangle([0, 640, 480, 860], fill=burgundy_deep)
draw.rectangle([1560, 640, 2048, 860], fill=burgundy_deep)
draw.line([(0, 640), (480, 640)], fill=gold, width=8)
draw.line([(0, 860), (480, 860)], fill=gold, width=8)
draw.line([(1560, 640), (2048, 640)], fill=gold, width=8)
draw.line([(1560, 860), (2048, 860)], fill=gold, width=8)

body_im.save(OUT_TEX / "kagari_body_skin.png")
print("Saved refined kagari_body_skin.png with Miko Kimono!")

# 2. Tops Kimono Outer Haori (_13.png)
src_tops = Image.open(SRC_TEX / "_13.png").convert("RGBA")
w_t, h_t = src_tops.size
tops_im = Image.new("RGBA", (w_t, h_t), (0, 0, 0, 0))
draw_t = ImageDraw.Draw(tops_im)

# Keep the alpha mask of the tops jacket
src_alpha = np.array(src_tops)[:, :, 3]

# Fill kimono cream-white
tops_base = Image.new("RGBA", (w_t, h_t), cream_white)
draw_tb = ImageDraw.Draw(tops_base)

# Wide kimono sleeves borders (top: y around 30 to 120, x across sleeves)
# Add burgundy hem and gold trim to sleeves and jacket base
draw_tb.rectangle([0, 0, w_t, 80], fill=burgundy)
draw_tb.line([(0, 80), (w_t, 80)], fill=gold, width=12)

# Outer hem (bottom: y around 600 to 700)
draw_tb.rectangle([0, 600, w_t, 700], fill=burgundy)
draw_tb.line([(0, 600), (w_t, 600)], fill=gold, width=12)

# Apply alpha mask
arr_tb = np.array(tops_base)
arr_tb[:, :, 3] = src_alpha
final_tops = Image.fromarray(arr_tb, mode="RGBA")
final_tops.save(OUT_TEX / "kagari_kimono_tops.png")
print("Saved kagari_kimono_tops.png!")
