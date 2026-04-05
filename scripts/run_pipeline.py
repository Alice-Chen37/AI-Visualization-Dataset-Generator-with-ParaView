print("🌴 ADVANCED 3D WEATHER + STREAMLINES")

import os
import numpy as np
from vtk.util import numpy_support
from vtk import vtkImageData, vtkXMLImageDataWriter
from paraview.simple import *

# weather
temp = 26
wind = 4

BASE = r"C:\Users\chenm\OneDrive\Desktop\Project\AI Visualization Dataset Generator with ParaView"

img_path = os.path.join(BASE, "outputs", "images", "final_streamlines.png")
vti_path = os.path.join(BASE, "outputs", "data", "weather.vti")

os.makedirs(os.path.dirname(img_path), exist_ok=True)
os.makedirs(os.path.dirname(vti_path), exist_ok=True)

# 3D data
nx, ny, nz = 80, 80, 80

x = np.linspace(-6, 6, nx)
y = np.linspace(-6, 6, ny)
z = np.linspace(0, 12, nz)

X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

gaussian = np.exp(-(X**2 + Y**2 + Z**2/12))
wave = 0.3 * np.sin(wind * X) * np.cos(wind * Y)

field = gaussian + wave

Vx = np.cos(Y)
Vy = np.sin(X)
Vz = np.cos(Z/3)

imageData = vtkImageData()
imageData.SetDimensions(nx, ny, nz)

scalar_data = numpy_support.numpy_to_vtk(field.ravel(), deep=True)
scalar_data.SetName("WeatherField")

vector_data = numpy_support.numpy_to_vtk(
    np.stack((Vx.ravel(), Vy.ravel(), Vz.ravel()), axis=1),
    deep=True
)
vector_data.SetName("Wind")

imageData.GetPointData().SetScalars(scalar_data)
imageData.GetPointData().SetVectors(vector_data)

writer = vtkXMLImageDataWriter()
writer.SetFileName(vti_path)
writer.SetInputData(imageData)
writer.Write()

print("✅ VTI ready")


# ParaView 
view = CreateRenderView()
view.ViewSize = [1200, 900]
view.Background = [0.05, 0.05, 0.1]

view.OrientationAxesVisibility = 1

reader = XMLImageDataReader(FileName=[vti_path])

contour = Contour(Input=reader)
contour.ContourBy = ["POINTS", "WeatherField"]
contour.Isosurfaces = [0.2, 0.4, 0.6]

display = Show(contour, view)
ColorBy(display, ("POINTS", "WeatherField"))

streamTracer = StreamTracer(Input=reader)
streamTracer.Vectors = ["POINTS", "Wind"]
streamTracer.MaximumStreamlineLength = 15

stream_display = Show(streamTracer, view)
ColorBy(stream_display, ("POINTS", "Wind"))

view.ResetCamera()
view.CameraPosition = [20, 20, 15]
view.CameraFocalPoint = [0, 0, 0]
view.CameraViewUp = [0, 0, 1]

Render()

SaveScreenshot(img_path, view, ImageResolution=[1200, 900])

print("🔥 FINAL IMAGE:", img_path)