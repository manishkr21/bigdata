# import libraray
from vtk import *
import vtk

# Ans 1. 2D Isocontour Extraction: Simplified Version of the Marching Squares algorithm}

def contour_Extraction_Algorithm(inputFile,outputFile,isovalue):
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

    
    # Loop through each cell and determine the contour segments
    for i in range(no_Of_Cells):
        cell = given_Image_Data.GetCell(i)
       # num_cell_points = cell.GetNumberOfPoints()
        cell_points = cell.GetPointIds()
        
        count = 2 # Defining cap, So the we can Ignore rest of the cases 
        # traversing the vertices of each cell in the counterclockwise order while finding the isocontour segments
        line_point_ids = []
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
                line_point_ids.append(contourPoints.GetNumberOfPoints() - 1)

        if line_point_ids:
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, line_point_ids[0])
            line.GetPointIds().SetId(1, line_point_ids[1])
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
    
    print("Output Produce in : ", outputFile)


# Fetching isovalue from the user
isovalue = int(input("Enter an isovalue : "))

# Calling the marching Square Algorithm
contour_Extraction_Algorithm('Data/Isabel_2D.vti', "output.vtp", isovalue)
