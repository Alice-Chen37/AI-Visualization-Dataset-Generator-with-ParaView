import os
from vtk.util import numpy_support
from paraview.simple import *
from vtk import vtkImageData, vtkXMLImageDataWriter

def render(field, base_path):
    nx, ny, nz = field.shape

    imageData = vtkImageData()
    imageData.SetDimensions(nx, ny, nz)

    vtk_data = numpy_support.numpy_to_vtk(field.ravel(), deep=True)
    vtk_data.SetName("WeatherField")

    imageData.GetPointData().SetScalars(vtk_data)

    vti_path = base_path + "/outputs/data/weather.vti"
    img_path = base_path + "/outputs/images/weather.png"

    os.makedirs(base_path + "/outputs/data", exist_ok=True)
    os.makedirs(base_path + "/outputs/images", exist_ok=True)

    writer = vtkXMLImageDataWriter()
    writer.SetFileName(vti_path)
    writer.SetInputData(imageData)
    writer.Write()

    # -------- ParaView --------
    view = CreateRenderView()
    reader = XMLImageDataReader(FileName=[vti_path])

    contour = Contour(Input=reader)
    contour.ContourBy = ["POINTS", "WeatherField"]
    contour.Isosurfaces = [0.2, 0.4, 0.6]

    display = Show(contour, view)
    ColorBy(display, ("POINTS", "WeatherField"))

    view.ResetCamera()
    Render()

    SaveScreenshot(img_path, view)

    print("✅ Saved:", img_path)