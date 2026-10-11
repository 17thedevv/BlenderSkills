"""Generate authentic anime textures for Kagari (篝) matching approved concept art."""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
from pathlib import Path

TEXTURES_DIR = Path("D:/Project-17/blender/outputs/sources/seedsan_textures")
OUTPUT_DIR = Path("D:/Project-17/blender/outputs/textures_kagari")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_kagari_faceparts():
    src_path = TEXTURES_DIR / "faceparts.png"
    im = Image.open(src_path).convert("RGBA")
    arr = np.array(im, dtype=np.float32)

    # 1. Target iris and eye pixels to transform to warm amber-gold
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]
    a = arr[:, :, 3]

    # Mask for hazel/brown eye pixels
    is_eye = (r > 60) & (g > 45) & (b < 100) & (a > 150) & (r >= g)
    
    # Transform eye color to Kagari's amber-gold
    # Dominant amber-gold: R ~ 245, G ~ 166, B ~ 35
    # Blend with original brightness
    brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    
    new_r = np.clip(brightness * 255.0 * 1.25, 0, 255)
    new_g = np.clip(brightness * 175.0 * 1.15, 0, 255)
    new_b = np.clip(brightness * 40.0 * 0.90, 0, 255)
    
    arr[:, :, 0] = np.where(is_eye, new_r, r)
    arr[:, :, 1] = np.where(is_eye, new_g, g)
    arr[:, :, 2] = np.where(is_eye, new_b, b)

    out_im = Image.fromarray(arr.astype(np.uint8), mode="RGBA")
    
    # 2. Add peach blush accents on cheeks
    draw = ImageDraw.Draw(out_im)
    # Left and right cheek blush ellipses in faceparts UV
    # Soft peach blush color: (255, 170, 166, 120)
    blush_overlay = Image.new("RGBA", out_im.size, (0, 0, 0, 0))
    draw_blush = ImageDraw.Draw(blush_overlay)
    
    # Soft radiant blush circles
    draw_blush.ellipse([180, 520, 320, 600], fill=(255, 170, 166, 100))
    draw_blush.ellipse([700, 520, 840, 600], fill=(255, 170, 166, 100))
    blush_blurred = blush_overlay.filter(ImageFilter.GaussianBlur(15))
    
    out_im = Image.alpha_composite(out_im, blush_blurred)
    
    dest_path = OUTPUT_DIR / "faceparts_kagari.png"
    out_im.save(dest_path)
    print("Saved:", dest_path)

def create_kagari_hair_texture():
    # Kagari's hair texture: 512x512 honey brown (#8D5B4C) with gold sheen (#F5A623)
    hair_im = Image.new("RGBA", (512, 512), (141, 91, 76, 255))
    draw = ImageDraw.Draw(hair_im)
    
    # Draw stylized anime hair shine / angel ring gradient bands
    for y in range(512):
        # Sine wave highlight band around y = 200..320
        dist = abs(y - 250)
        if dist < 60:
            factor = (1.0 - dist / 60.0)**1.5
            hr = int(141 + factor * (245 - 141))
            hg = int(91 + factor * (166 - 91))
            hb = int(76 + factor * (35 - 76))
            draw.line([(0, y), (511, y)], fill=(hr, hg, hb, 255))
            
    # Add vertical hair strand micro-texture
    noise = np.random.randint(-10, 10, (512, 512), dtype=np.int16)
    arr = np.array(hair_im, dtype=np.int16)
    arr[:, :, 0] = np.clip(arr[:, :, 0] + noise, 0, 255)
    arr[:, :, 1] = np.clip(arr[:, :, 1] + noise, 0, 255)
    arr[:, :, 2] = np.clip(arr[:, :, 2] + noise, 0, 255)
    
    hair_final = Image.fromarray(arr.astype(np.uint8), mode="RGBA")
    dest_path = OUTPUT_DIR / "hair_kagari.png"
    hair_final.save(dest_path)
    print("Saved:", dest_path)

def create_kagari_wear_texture():
    src_path = TEXTURES_DIR / "wear.png"
    im = Image.open(src_path).convert("RGBA")
    
    # Create miko kimono color scheme:
    # Cream-white body (#FFF9F2) + burgundy haori (#8B1E3F) + gold trims (#E6B800)
    w, h = im.size
    wear_new = Image.new("RGBA", (w, h), (255, 249, 242, 255))
    draw = ImageDraw.Draw(wear_new)
    
    # Burgundy collar / lapel blocks (typically in top half of wear UV)
    draw.rectangle([0, 0, w, int(h * 0.45)], fill=(139, 30, 63, 255))
    # Gold accent trims
    draw.rectangle([0, int(h * 0.42), w, int(h * 0.45)], fill=(230, 184, 0, 255))
    
    # Blend with original occlusion/shading
    orig_l = im.convert("L")
    arr_new = np.array(wear_new, dtype=np.float32)
    arr_l = np.array(orig_l, dtype=np.float32) / 255.0
    
    for c in range(3):
        arr_new[:, :, c] = np.clip(arr_new[:, :, c] * (0.5 + 0.5 * arr_l), 0, 255)
        
    wear_final = Image.fromarray(arr_new.astype(np.uint8), mode="RGBA")
    dest_path = OUTPUT_DIR / "wear_kagari.png"
    wear_final.save(dest_path)
    print("Saved:", dest_path)

if __name__ == "__main__":
    create_kagari_faceparts()
    create_kagari_hair_texture()
    create_kagari_wear_texture()
