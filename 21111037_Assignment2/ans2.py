# Ans 2. Implement the volume rendering algorithm from the VTK library
import vtk
# import sys

# Load the 3D data
imgReader = vtk.vtkXMLImageDataReader()
imgReader.SetFileName("Data/Isabel_3D.vti")
imgReader.Update()

# Color Transfer Function with given Specification
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(-4931.54, 0, 1, 1)
colorTransferFunction.AddRGBPoint(-2508.95, 0, 0, 1)
colorTransferFunction.AddRGBPoint(-1873.9, 0, 0, 0.5)
colorTransferFunction.AddRGBPoint(-1027.16, 1, 0, 0)
colorTransferFunction.AddRGBPoint(-298.031, 1, 0.4, 0)
colorTransferFunction.AddRGBPoint(2594.97, 1, 1, 0)

# Opacity Transfer Function with given Specification
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(-4931.54, 1.0)
opacityTransferFunction.AddPoint(101.815, 0.002)
opacityTransferFunction.AddPoint(2594.97, 0.0)

# perform the volume rendering
mapper = vtk.vtkSmartVolumeMapper()
mapper.SetInputConnection(imgReader.GetOutputPort())


use_phong = input("Do you want to use Phong shading? (yes/no) ")


volume = vtk.vtkVolume()
objVolumeProperty = vtk.vtkVolumeProperty()
objVolumeProperty.SetColor(colorTransferFunction)
objVolumeProperty.SetScalarOpacity(opacityTransferFunction)
objVolumeProperty.ShadeOn()
if use_phong == "yes":
    # Phong Shading Parameters
    # produce advanced lighting effects to make your volume rendering more realistic
    objVolumeProperty.SetAmbient(0.5)
    objVolumeProperty.SetDiffuse(0.5)
    objVolumeProperty.SetSpecular(0.5)
else:
    objVolumeProperty.ShadeOff()
volume.SetMapper(mapper)
volume.SetProperty(objVolumeProperty)

# Add an outline to the volume rendered data
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(imgReader.GetOutputPort())
outlineDataMapper = vtk.vtkPolyDataMapper()
outlineDataMapper.SetInputConnection(outline.GetOutputPort())
objVtkActor = vtk.vtkActor()
objVtkActor.SetMapper(outlineDataMapper)

# Create a render window
renderer = vtk.vtkRenderer()
renderer.AddVolume(volume)
renderer.AddActor(objVtkActor)

# Create a 1000x1000 sized render window
objRenderWindow = vtk.vtkRenderWindow()
objRenderWindow.SetSize(1000, 1000)
objRenderWindow.AddRenderer(renderer)
objRenderWindow_interactor = vtk.vtkRenderWindowInteractor()
objRenderWindow_interactor.SetRenderWindow(objRenderWindow)

objRenderWindow.Render()
objRenderWindow_interactor.Start()
