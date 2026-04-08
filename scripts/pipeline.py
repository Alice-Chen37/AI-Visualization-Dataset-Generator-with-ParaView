print("🌴 FULL 3D WEATHER PIPELINE")

import os
import numpy as np
from vtk.util import numpy_support
from vtk import vtkImageData, vtkXMLImageDataWriter
from paraview.simple import *

BASE = r"C:\Users\chenm\OneDrive\Desktop\Project\AI Visualization Dataset Generator with ParaView"

vti_path = os.path.join(BASE, "outputs", "data", "weather_3d.vti")
img_path = os.path.join(BASE, "outputs", "images", "weather_render.png")

os.makedirs(os.path.dirname(vti_path), exist_ok=True)
os.makedirs(os.path.dirname(img_path), exist_ok=True)

# 3D data
nx, ny, nz = 60, 60, 40

x = np.linspace(-5, 5, nx)
y = np.linspace(-5, 5, ny)
z = np.linspace(0, 10, nz)

X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

field = np.exp(-(X**2 + Y**2 + Z**2/10))

Vx = np.cos(Y)
Vy = np.sin(X)
Vz = np.cos(Z/3)

# -------------------------
# 转VTK
# -------------------------
imageData = vtkImageData()
imageData.SetDimensions(nx, ny, nz)

scalar = numpy_support.numpy_to_vtk(field.ravel(), deep=True)
scalar.SetName("Temperature")

vector = numpy_support.numpy_to_vtk(
    np.stack((Vx.ravel(), Vy.ravel(), Vz.ravel()), axis=1),
    deep=True
)
vector.SetName("Wind")

imageData.GetPointData().SetScalars(scalar)
imageData.GetPointData().SetVectors(vector)

writer = vtkXMLImageDataWriter()
writer.SetFileName(vti_path)
writer.SetInputData(imageData)
writer.Write()

print("✅ VTI ready")

# ParaView
view = CreateRenderView()
view.ViewSize = [1000, 800]

reader = XMLImageDataReader(FileName=[vti_path])

contour = Contour(Input=reader)
contour.ContourBy = ["POINTS", "Temperature"]
contour.Isosurfaces = [0.2, 0.4, 0.6]

Show(contour, view)

stream = StreamTracer(Input=reader)
stream.Vectors = ["POINTS", "Wind"]

Show(stream, view)

view.OrientationAxesVisibility = 1

view.ResetCamera()
Render()

SaveScreenshot(img_path, view)

print("🔥 Image saved:", img_path)