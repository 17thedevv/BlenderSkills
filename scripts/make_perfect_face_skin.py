"""Create a clean, seamless, porcelain peach anime skin texture for Kagari."""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from pathlib import Path

SRC_PATH = Path("D:/Project-17/blender/outputs/sources/vroid_textures/_04.png")
OUT_PATH = Path("D:/Project-17/blender/outputs/textures_kagari_vroid/kagari_face_skin.png")

src = Image.open(SRC_PATH).convert("RGBA")
w, h = src.size
arr = np.array(src, dtype=np.float32)

# Find the skin mask (where alpha > 50)
alpha_mask = arr[:, :, 3] > 50

# Base skin color: pale warm peach cream #FFF4EC (255, 244, 236)
# Shade skin color: slightly warmer soft peach #F5E0D3 (245, 224, 211)
clean_skin = np.zeros_like(arr)
clean_skin[:, :, 0] = 254
clean_skin[:, :, 1] = 240
clean_skin[:, :, 2] = 232
clean_skin[:, :, 3] = arr[:, :, 3] # Keep exact alpha

# Soft nose shadow / contour at center
# Subtle blush layer
im_base = Image.fromarray(clean_skin.astype(np.uint8), mode="RGBA")
blush_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
draw = ImageDraw.Draw(blush_layer)

# Cheeks blush: soft sakura peach #FFAAA6 (255, 170, 166)
draw.ellipse([w * 0.20, h * 0.44, w * 0.40, h * 0.56], fill=(255, 165, 160, 110))
draw.ellipse([w * 0.60, h * 0.44, w * 0.80, h * 0.56], fill=(255, 165, 160, 110))

# Nose tip subtle peach hint
draw.ellipse([w * 0.47, h * 0.48, w * 0.53, h * 0.52], fill=(255, 175, 165, 70))

blush_layer = blush_layer.filter(ImageFilter.GaussianBlur(22))
final_skin = Image.alpha_composite(im_base, blush_layer)
final_skin.save(OUT_PATH)
print("Saved perfect Kagari face skin texture:", OUT_PATH)
