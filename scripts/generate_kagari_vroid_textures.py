"""Generate authentic Kagari textures for the VRoid female base mesh."""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from pathlib import Path

SRC_DIR = Path("D:/Project-17/blender/outputs/sources/vroid_textures")
OUT_DIR = Path("D:/Project-17/blender/outputs/textures_kagari_vroid")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_iris():
    src = Image.open(SRC_DIR / "_02.png").convert("RGBA")
    w, h = src.size
    # Create amber-gold sunset gradient iris
    # Top: deep warm amber #7A3816 (122, 56, 22)
    # Mid: glowing honey gold #F5A623 (245, 166, 35)
    # Bottom: radiant bright gold #FFE266 (255, 226, 102)
    iris = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(iris)
    
    src_alpha = np.array(src)[:, :, 3]
    
    for y in range(h):
        frac = y / float(h)
        if frac < 0.45:
            # Top to mid
            t = frac / 0.45
            r = int(100 + t * (245 - 100))
            g = int(45 + t * (166 - 45))
            b = int(18 + t * (35 - 18))
        else:
            # Mid to bottom
            t = (frac - 0.45) / 0.55
            r = int(245 + t * (255 - 245))
            g = int(166 + t * (226 - 166))
            b = int(35 + t * (102 - 35))
        draw.line([(0, y), (w - 1, y)], fill=(r, g, b, 255))
        
    # Pupil in center-top of each eye
    # In VRoid iris texture, there are two eyes side-by-side around x=256 and x=768
    pupil_color = (45, 20, 10, 255)
    for cx in [w * 0.265, w * 0.735]:
        draw.ellipse([cx - 55, h * 0.28, cx + 55, h * 0.65], fill=pupil_color)
        
    # Re-apply original iris alpha mask
    arr = np.array(iris)
    arr[:, :, 3] = src_alpha
    final_iris = Image.fromarray(arr, mode="RGBA")
    final_iris.save(OUT_DIR / "kagari_iris.png")
    print("Saved kagari_iris.png")

def generate_highlight():
    src = Image.open(SRC_DIR / "_03.png").convert("RGBA")
    w, h = src.size
    hl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(hl)
    
    # Draw Kagari's starry and crescent catchlights for both eyes
    for cx in [w * 0.265, w * 0.735]:
        # Crescent catchlight in bottom outer iris
        draw.arc([cx - 70, h * 0.55, cx + 70, h * 0.88], start=20, end=160, fill=(255, 255, 255, 250), width=18)
        # 4-point star catchlight in top-left
        scx, scy = cx - 45, h * 0.35
        sr = 22
        draw.polygon([(scx, scy - sr), (scx + 5, scy), (scx + sr, scy), (scx + 5, scy + 5),
                      (scx, scy + sr), (scx - 5, scy + 5), (scx - sr, scy), (scx - 5, scy)], fill=(255, 255, 255, 255))
        # Small circular sparkle
        draw.ellipse([cx + 40, h * 0.42, cx + 54, h * 0.42 + 14], fill=(255, 255, 255, 230))
        
    hl_blurred = hl.filter(ImageFilter.GaussianBlur(1.2))
    hl_blurred.save(OUT_DIR / "kagari_highlight.png")
    print("Saved kagari_highlight.png")

def generate_face_skin():
    # Clean up tattoos/stars on face and add Kagari's soft peach blush
    src = Image.open(SRC_DIR / "_04.png").convert("RGBA")
    arr = np.array(src)
    
    # Base skin color: pale warm peach cream #FFF5EE
    # Blend out decorative tattoos (which are bright pink/cyan stars)
    r = arr[:, :, 0].astype(np.float32)
    g = arr[:, :, 1].astype(np.float32)
    b = arr[:, :, 2].astype(np.float32)
    
    # Detect non-skin saturated tattoo colors (magenta/cyan)
    is_tattoo = (r > 200) & (b > 180) & (g < 150) | ((g > 180) & (b > 200) & (r < 100))
    
    # Replace tattoo with average skin
    skin_avg = [252, 232, 222]
    for c in range(3):
        arr[:, :, c] = np.where(is_tattoo, skin_avg[c], arr[:, :, c])
        
    face_im = Image.fromarray(arr, mode="RGBA")
    
    # Add soft radiant peach blush
    blush_layer = Image.new("RGBA", face_im.size, (0, 0, 0, 0))
    draw_b = ImageDraw.Draw(blush_layer)
    # Peach blush: #FFAAA6 with opacity
    w, h = face_im.size
    draw_b.ellipse([w * 0.22, h * 0.46, w * 0.38, h * 0.56], fill=(255, 170, 166, 120))
    draw_b.ellipse([w * 0.62, h * 0.46, w * 0.78, h * 0.56], fill=(255, 170, 166, 120))
    blush_blur = blush_layer.filter(ImageFilter.GaussianBlur(25))
    
    final_face = Image.alpha_composite(face_im, blush_blur)
    final_face.save(OUT_DIR / "kagari_face_skin.png")
    print("Saved kagari_face_skin.png")

def generate_eyebrows():
    src = Image.open(SRC_DIR / "_07.png").convert("RGBA")
    arr = np.array(src)
    # Transform brow color from dark purple/black to soft honey-brown #8D5B4C (141, 91, 76)
    alpha = arr[:, :, 3] > 30
    arr[:, :, 0] = np.where(alpha, 141, arr[:, :, 0])
    arr[:, :, 1] = np.where(alpha, 91, arr[:, :, 1])
    arr[:, :, 2] = np.where(alpha, 76, arr[:, :, 2])
    Image.fromarray(arr, mode="RGBA").save(OUT_DIR / "kagari_brows.png")
    print("Saved kagari_brows.png")

def generate_hair_texture():
    # Hair: 512x1024 warm honey-brown #8D5B4C with golden angel-ring highlight #F5A623
    w, h = 512, 1024
    hair_im = Image.new("RGBA", (w, h), (141, 91, 76, 255))
    draw = ImageDraw.Draw(hair_im)
    
    # Golden angel ring highlight sheen across mid-upper hair
    for y in range(h):
        dist = abs(y - 380)
        if dist < 120:
            t = (1.0 - dist / 120.0)**1.8
            r = int(141 + t * (245 - 141))
            g = int(91 + t * (166 - 91))
            b = int(76 + t * (35 - 76))
            draw.line([(0, y), (w - 1, y)], fill=(r, g, b, 255))
            
    # Add vertical stylized strand lines
    for x in range(0, w, 6):
        var = int(np.random.randint(-15, 15))
        draw.line([(x, 0), (x, h - 1)], fill=(max(0, min(255, 141 + var)), max(0, min(255, 91 + var)), max(0, min(255, 76 + var)), 60))
        
    hair_im.save(OUT_DIR / "kagari_hair.png")
    print("Saved kagari_hair.png")

def generate_kimono_outfit():
    # Kimono tops: 2048x2048
    # Body: cream-white #FFF9F2 (255, 249, 242)
    # Haori lapels & collar: deep carmine burgundy #8B1E3F (139, 30, 63)
    # Trim: radiant astral gold #E6B800 (230, 184, 0)
    w, h = 2048, 2048
    kimono = Image.new("RGBA", (w, h), (255, 249, 242, 255))
    draw = ImageDraw.Draw(kimono)
    
    # Draw burgundy collar / haori lapels
    draw.rectangle([0, 0, w, int(h * 0.42)], fill=(139, 30, 63, 255))
    # Gold border trim
    draw.rectangle([0, int(h * 0.39), w, int(h * 0.42)], fill=(230, 184, 0, 255))
    
    # Sleeves / bottom trim
    draw.rectangle([0, int(h * 0.85), w, h], fill=(139, 30, 63, 255))
    draw.rectangle([0, int(h * 0.83), w, int(h * 0.85)], fill=(230, 184, 0, 255))
    
    kimono.save(OUT_DIR / "kagari_kimono.png")
    print("Saved kagari_kimono.png")

if __name__ == "__main__":
    generate_iris()
    generate_highlight()
    generate_face_skin()
    generate_eyebrows()
    generate_hair_texture()
    generate_kimono_outfit()
