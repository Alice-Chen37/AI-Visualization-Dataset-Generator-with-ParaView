from PIL import Image
import glob

frames = [Image.open(f) for f in sorted(glob.glob("outputs/animation/*.png"))]

#GIF
frames[0].save(
    "outputs/weather.gif",
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=0
)

print("✅ GIF saved: outputs/weather.gif")