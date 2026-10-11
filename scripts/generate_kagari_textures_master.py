"""Generate high fidelity Kagari textures using system Python with PIL and NumPy."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

ROOT = Path("D:/Project-17/blender")
SRC_TEX = ROOT / "outputs/sources/vroid_textures"
OUT_TEX = ROOT / "outputs/textures_kagari_vroid"
OUT_TEX.mkdir(parents=True, exist_ok=True)

print("--- Step 1: Generating High-Fidelity Textures ---")

# 1.1 Face Skin Texture
def make_face_skin():
    src = Image.open(SRC_TEX / "_04.png").convert("RGBA")
    arr = np.array(src, dtype=np.float32)
    
    # Mask scalp hair (dark purple) vs skin
    is_scalp = (arr[:, :, 2] > arr[:, :, 1] * 1.05) & (arr[:, :, 0] < 120) & (arr[:, :, 3] > 50)
    is_skin = (~is_scalp) & (arr[:, :, 3] > 50)
    
    out = arr.copy()
    
    # Porcelain peach tone curve
    r_skin = out[:, :, 0] / 255.0
    g_skin = out[:, :, 1] / 255.0
    b_skin = out[:, :, 2] / 255.0
    
    r_new = 1.0 - (1.0 - r_skin)**1.5
    g_new = 1.0 - (1.0 - g_skin)**1.9
    b_new = 1.0 - (1.0 - b_skin)**2.1
    
    out[is_skin, 0] = np.clip(r_new[is_skin] * 255.0, 0, 255)
    out[is_skin, 1] = np.clip(g_new[is_skin] * 242.0, 0, 255)
    out[is_skin, 2] = np.clip(b_new[is_skin] * 235.0, 0, 255)
    
    # Honey brown scalp hair
    lum_scalp = (0.299 * arr[is_scalp, 0] + 0.587 * arr[is_scalp, 1] + 0.114 * arr[is_scalp, 2]) / 255.0
    out[is_scalp, 0] = np.clip(lum_scalp * 350.0 + 50.0, 0, 255)
    out[is_scalp, 1] = np.clip(lum_scalp * 230.0 + 30.0, 0, 255)
    out[is_scalp, 2] = np.clip(lum_scalp * 140.0 + 15.0, 0, 255)
    
    base_im = Image.fromarray(out.astype(np.uint8), mode="RGBA")
    
    # Clean up ear piercings on top left and top right
    draw_clean = ImageDraw.Draw(base_im)
    ear_skin_color = (252, 230, 222, 255)
    draw_clean.ellipse([60, 60, 140, 120], fill=ear_skin_color)
    draw_clean.ellipse([840, 60, 920, 120], fill=ear_skin_color)
    
    # Add gentle radiant peach blush matching concept art
    w, h = base_im.size
    blush_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_b = ImageDraw.Draw(blush_layer)
    # Cheeks: soft warm sakura peach #FFAAA6
    draw_b.ellipse([w * 0.22, h * 0.47, w * 0.38, h * 0.57], fill=(255, 170, 166, 125))
    draw_b.ellipse([w * 0.62, h * 0.47, w * 0.78, h * 0.57], fill=(255, 170, 166, 125))
    # Soft nose contour
    draw_b.ellipse([w * 0.48, h * 0.49, w * 0.52, h * 0.52], fill=(255, 175, 165, 80))
    blush_layer = blush_layer.filter(ImageFilter.GaussianBlur(16))
    
    final_face = Image.alpha_composite(base_im, blush_layer)
    final_face.save(OUT_TEX / "kagari_face_skin.png")
    print("Saved kagari_face_skin.png")

make_face_skin()

# 1.2 Body Skin Texture
def make_body_skin():
    src = Image.open(SRC_TEX / "_10.png").convert("RGBA")
    arr = np.array(src, dtype=np.float32)
    out = arr.copy()
    
    r_skin = out[:, :, 0] / 255.0
    g_skin = out[:, :, 1] / 255.0
    b_skin = out[:, :, 2] / 255.0
    
    r_new = np.clip((1.0 - (1.0 - r_skin)**1.5) * 255.0, 0, 255)
    g_new = np.clip((1.0 - (1.0 - g_skin)**1.9) * 242.0, 0, 255)
    b_new = np.clip((1.0 - (1.0 - b_skin)**2.1) * 235.0, 0, 255)
    
    is_skin = (arr[:, :, 0] > 120) & (arr[:, :, 1] > 80)
    out[is_skin, 0] = r_new[is_skin]
    out[is_skin, 1] = g_new[is_skin]
    out[is_skin, 2] = b_new[is_skin]
    
    body_im = Image.fromarray(out.astype(np.uint8), mode="RGBA")
    draw = ImageDraw.Draw(body_im)
    
    # Clean choker around neck (x ~ 800-1250, y ~ 120-220)
    neck_skin = (252, 238, 230, 255)
    draw.rectangle([780, 120, 1270, 230], fill=neck_skin)
    # Clean chest tattoo/chain (x ~ 880-1170, y ~ 230-360)
    draw.rectangle([860, 230, 1190, 360], fill=neck_skin)
    
    body_im = body_im.filter(ImageFilter.BoxBlur(1))
    body_im.save(OUT_TEX / "kagari_body_skin.png")
    print("Saved kagari_body_skin.png")

make_body_skin()

# 1.3 Hair Textures (Honey-Brown Gradient)
def make_hair_texture(src_name, out_name):
    src = Image.open(SRC_TEX / src_name).convert("RGBA")
    arr = np.array(src, dtype=np.float32)
    alpha = arr[:, :, 3]
    
    lum = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]) / 255.0
    out = np.zeros_like(arr)
    # Warm honey-brown gradient: shadow (70, 42, 22), mid (165, 110, 58), highlight (240, 195, 135)
    for c, (s, m, h) in enumerate([(70, 165, 240), (42, 110, 195), (22, 58, 135)]):
        val = np.where(lum < 0.5,
                       s + (m - s) * (lum / 0.5),
                       m + (h - m) * ((lum - 0.5) / 0.5))
        out[:, :, c] = val
    out[:, :, 3] = alpha
    res = Image.fromarray(out.astype(np.uint8), mode="RGBA")
    res.save(OUT_TEX / out_name)
    print(f"Saved {out_name}")

make_hair_texture("_15.png", "kagari_hair_01.png")
make_hair_texture("_17.png", "kagari_hair_02.png")

# 1.4 Iris Texture (Amber-Gold Sunset)
def make_iris():
    src = Image.open(SRC_TEX / "_02.png").convert("RGBA")
    arr = np.array(src, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    out = arr.copy()
    is_gold = (g > 100) & (b < 180) & (a > 50)
    out[is_gold, 0] = np.clip(r[is_gold] * 1.12, 0, 255)
    out[is_gold, 1] = np.clip(g[is_gold] * 0.95, 0, 255)
    out[is_gold, 2] = np.clip(b[is_gold] * 0.65, 0, 255)
    res = Image.fromarray(out.astype(np.uint8), mode="RGBA")
    res.save(OUT_TEX / "kagari_iris.png")
    print("Saved kagari_iris.png")

make_iris()

# 1.5 Eyebrow Texture
def make_brows():
    src = Image.open(SRC_TEX / "_07.png").convert("RGBA")
    arr = np.array(src, dtype=np.float32)
    alpha = arr[:, :, 3]
    lum = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]) / 255.0
    out = np.zeros_like(arr)
    out[:, :, 0] = np.clip(lum * 180 + 70, 0, 255)
    out[:, :, 1] = np.clip(lum * 120 + 40, 0, 255)
    out[:, :, 2] = np.clip(lum * 80 + 20, 0, 255)
    out[:, :, 3] = alpha
    res = Image.fromarray(out.astype(np.uint8), mode="RGBA")
    res.save(OUT_TEX / "kagari_brows.png")
    print("Saved kagari_brows.png")

make_brows()

# 1.6 Eyeline Texture
def make_eyeline():
    src = Image.open(SRC_TEX / "_09.png").convert("RGBA")
    arr = np.array(src, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    is_pink = (r > 160) & (b > 60) & (g < 120) & (a > 30)
    out = arr.copy()
    out[is_pink, 0] = 150
    out[is_pink, 1] = 60
    out[is_pink, 2] = 40
    res = Image.fromarray(out.astype(np.uint8), mode="RGBA")
    res.save(OUT_TEX / "kagari_eyeline.png")
    print("Saved kagari_eyeline.png")

make_eyeline()
print("All Kagari master textures generated successfully!")
