from vtk.util import numpy_support
import os
import numpy as np
from vtk.util import numpy_support
from paraview.simple import *

# 输出路径
output_dir = "C:/Users/chenm/OneDrive/Desktop/Project/AI Visualization Dataset Generator with ParaView/outputs"
os.makedirs(output_dir, exist_ok=True)

vti_file = os.path.join(output_dir, "sample.vti")
image_file = os.path.join(output_dir, "out.png")

# 创建简单 3D 网格
nx, ny, nz = 50, 50, 50
x = np.linspace(-10, 10, nx)
y = np.linspace(-10, 10, ny)
z = np.linspace(-10, 10, nz)

X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
scalars = np.sin(X) * np.cos(Y) * np.sin(Z)

# 转成 VTK 数据
from vtk import vtkImageData
imageData = vtkImageData()
imageData.SetDimensions(nx, ny, nz)
imageData.SetSpacing(x[1]-x[0], y[1]-y[0], z[1]-z[0])
imageData.GetPointData().SetScalars(numpy_support.numpy_to_vtk(scalars.ravel(), deep=True))

# 保存为 VTI
from vtk import vtkXMLImageDataWriter
writer = vtkXMLImageDataWriter()
writer.SetFileName(vti_file)
writer.SetInputData(imageData)
writer.Write()
print(f"VTI file saved to {vti_file}")

# --- ParaView 渲染 ---
renderView = CreateRenderView()
reader = XMLImageDataReader(FileName=[vti_file])
contour = Contour(Input=reader)
contour.ContourBy = ["POINTS", "ImageScalars"]  # 默认标量名
contour.Isosurfaces = [0.5]  # 设定等值面

display = Show(contour, renderView)
renderView.Background = [0.1, 0.1, 0.1]
renderView.Update()

# 输出 PNG
SaveScreenshot(image_file, renderView, ImageResolution=[800, 800])
print(f"Screenshot saved to {image_file}")