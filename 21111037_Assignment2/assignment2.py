# import libraray
from vtk import *
import vtk

# Ans 1. 2D Isocontour Extraction: Simplified Version of the Marching Squares algorithm}

def Marching_Square_Algo(inputFile,outputFile,isovalue):
    # Load Image data
    imgReader = vtk.vtkXMLImageDataReader()
    imgReader.SetFileName(inputFile)
    imgReader.Update()
    given_Image_Data = imgReader.GetOutput()

    # find Number of Cells and number of Points
    no_Of_Cells = given_Image_Data.GetNumberOfCells()
    no_Of_Points = given_Image_Data.GetNumberOfPoints()
    
    # find the scalar values of each point
    values = []
    for i in range(no_Of_Points):
        values.append(given_Image_Data.GetPointData().GetScalars().GetTuple1(i))
    
    # Create an array to store the contour segments
    contourLines = vtk.vtkCellArray()
    contourPoints = vtk.vtkPoints()
    contourSegments = []
    
    # Loop through each cell and determine the contour segments
    for i in range(no_Of_Cells):
        cell = given_Image_Data.GetCell(i)
        num_cell_points = cell.GetNumberOfPoints()
        cell_points = cell.GetPointIds()
        
        count = 2 # Defining cap, So the we can Ignore rest of the cases 
        
        for currPoint in [0,1,3,2]:
            if count==0:   
                break
            nextPoint = 1
            if currPoint==1:
                nextPoint=3
            elif currPoint==3:
                nextPoint = 2 
            elif currPoint==2:
                nextPoint = 0
            p1 = cell_points.GetId(currPoint)
            p2 = cell_points.GetId(nextPoint)
            
            if (values[p1] <= isovalue and values[p2] > isovalue) or (values[p1] > isovalue and values[p2] <= isovalue):
                # Interpolate the points along the line segment
                count -= 1
                fraction = (isovalue - values[p1]) / (values[p2] - values[p1])
                x1, y1, z1 = given_Image_Data.GetPoint(p1)
                x2, y2, z2 = given_Image_Data.GetPoint(p2)
                x = x1 + fraction * (x2 - x1)
                y = y1 + fraction * (y2 - y1)
                z = 25
                
                # Add the interpolated point to the contour points
                contourPoints.InsertNextPoint(x, y, z)
                # contourSegments.append((len(contourSegments), len(contourSegments) + 1))
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, contourPoints.GetNumberOfPoints()-2)
        line.GetPointIds().SetId(1, contourPoints.GetNumberOfPoints()-1)
        contourLines.InsertNextCell(line)
    
    # Create the object of PolyData
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(contourPoints)
    polydata.SetLines(contourLines)
    
    # Writing the data in VTK’s polydata file format
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(outputFile)
    writer.SetInputData(polydata)
    writer.Write()
    
    print("Output Produce in the format of : ", outputFile)


# Fetching isovalue from the user
isovalue = int(input("Enter an isovalue : "))

# Calling the marching Square Algorithm
Marching_Square_Algo('Data/Isabel_2D.vti', "output.vtp", isovalue)

def extract_isocontour_filter(input_filename, output_filename, isovalue):
    # Read the input VTKImageData file
    imgReader = vtk.vtkXMLImageDataReader()
    imgReader.SetFileName(input_filename)
    imgReader.Update()
    image_data = imgReader.GetOutput()
    
    # Extract geometry from the image data
    geometryFilter = vtk.vtkImageDataGeometryFilter()
    geometryFilter.SetInputData(image_data)
    geometryFilter.Update()
    poly_data = geometryFilter.GetOutput()
    
    # Extract the isocontour
    contourFilter = vtk.vtkContourFilter()
    contourFilter.SetInputData(poly_data)
    contourFilter.SetValue(0, isovalue)
    contourFilter.Update()
    poly_data = contourFilter.GetOutput()
    
    # Write the output VTKPolyData file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(output_filename)
    writer.SetInputData(contourFilter.GetOutput())
    writer.Write()


extract_isocontour_filter('Data/Isabel_2D.vti', "output.vtp", 20)



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

# Applying volume rendering
mapper = vtk.vtkSmartVolumeMapper()
mapper.SetInputConnection(imgReader.GetOutputPort())

# Use Phong shading or not
# use_phong = input("Do you want to use Phong shading? (yes/no) ")
use_phong = "yes"

volume = vtk.vtkVolume()
objVolumeProperty = vtk.vtkVolumeProperty()
objVolumeProperty.SetColor(colorTransferFunction)
objVolumeProperty.SetScalarOpacity(opacityTransferFunction)
objVolumeProperty.ShadeOn()
if use_phong == "yes":
    # Phong Shading Parameters
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
# renderer.SetBackground(1,1,1)
renderer.AddVolume(volume)
renderer.AddActor(objVtkActor)

objRenderWindow = vtk.vtkRenderWindow()
objRenderWindow.SetSize(1000, 1000)
objRenderWindow.AddRenderer(renderer)
objRenderWindow_interactor = vtk.vtkRenderWindowInteractor()
objRenderWindow_interactor.SetRenderWindow(objRenderWindow)

objRenderWindow.Render()
objRenderWindow_interactor.Start()
