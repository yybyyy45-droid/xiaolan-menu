"""Remove white/light background from hand-drawn drink images."""
from PIL import Image
import os, glob

IMG_DIR = os.path.join(os.path.dirname(__file__), "img")
THRESHOLD = 220  # pixels with R,G,B all above this are treated as background

for path in glob.glob(os.path.join(IMG_DIR, "*.png")):
    img = Image.open(path).convert("RGBA")
    data = img.getdata()
    new_data = []
    for r, g, b, a in data:
        # If pixel is very light (close to white/cream), make it transparent
        if r > THRESHOLD and g > THRESHOLD and b > THRESHOLD:
            new_data.append((r, g, b, 0))
        # Semi-transparent for near-white pixels (smooth edge)
        elif r > 200 and g > 200 and b > 200:
            # Gradual fade: the lighter, the more transparent
            lightness = min(r, g, b)
            alpha = max(0, int((THRESHOLD - lightness) / (THRESHOLD - 200) * 255))
            new_data.append((r, g, b, alpha))
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    img.save(path)
    print(f"✅ {os.path.basename(path)}")

print("\nDone! All backgrounds removed.")
