print("🎥 FINAL 3D WEATHER ANIMATION (COLOR FIXED)")

import os
from paraview.simple import *

BASE = r"C:\Users\chenm\OneDrive\Desktop\Project\AI Visualization Dataset Generator with ParaView"

vti = os.path.join(BASE, "outputs", "data", "weather_3d.vti")
out_dir = os.path.join(BASE, "outputs", "animation")

os.makedirs(out_dir, exist_ok=True)

# view
view = CreateRenderView()
view.ViewSize = [1200, 900]
view.Background = [0.05, 0.05, 0.1]

# read data
reader = XMLImageDataReader(FileName=[vti])

display = Show(reader, view)
display.Representation = 'Volume'

ColorBy(display, ('POINTS', 'Temperature'))
display.RescaleTransferFunctionToDataRange(True, False)
display.ScalarOpacityUnitDistance = 0.1

view.OrientationAxesVisibility = 1

view.ResetCamera()
Render()

camera = GetActiveCamera()

for i in range(0, 360, 5):
    camera.Azimuth(5)
    Render()

    path = os.path.join(out_dir, f"frame_{i:03d}.png")
    SaveScreenshot(path, view)

    print("Saved:", path)

print("🔥 Animation complete!")