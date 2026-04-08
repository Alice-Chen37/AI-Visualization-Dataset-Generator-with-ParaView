print("🌴 HIGH QUALITY 3D WEATHER FIELD")

import os
import numpy as np
from vtk.util import numpy_support
from vtk import vtkImageData, vtkXMLImageDataWriter

BASE = r"C:\Users\chenm\OneDrive\Desktop\Project\AI Visualization Dataset Generator with ParaView"
vti_path = os.path.join(BASE, "outputs", "data", "weather_3d.vti")

os.makedirs(os.path.dirname(vti_path), exist_ok=True)

nx, ny, nz = 80, 80, 50

x = np.linspace(-5, 5, nx)
y = np.linspace(-5, 5, ny)
z = np.linspace(0, 10, nz)

X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# weather
gaussian = np.exp(-(X**2 + Y**2 + Z**2/10))
wave = 0.3*np.sin(3*X)*np.cos(3*Y)

temperature = gaussian + wave

# wind
Vx = -Y
Vy = X
Vz = 0.5*np.sin(Z/2)

# VTK
imageData = vtkImageData()
imageData.SetDimensions(nx, ny, nz)
imageData.SetSpacing(0.15, 0.15, 0.2)

scalar = numpy_support.numpy_to_vtk(temperature.ravel(), deep=True)
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

print("✅ 3D dataset saved:", vti_path)