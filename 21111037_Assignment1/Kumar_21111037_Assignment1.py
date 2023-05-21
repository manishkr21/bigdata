#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import VTK
from vtk import *


# In[2]:


# Load data
reader = vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()


# In[3]:


# Query how many cells the dataset has
print("Number of Cells in the dataset : ",data.GetNumberOfCells())


# In[4]:


# Query to find the dimension of the dataset
print("Dimensions of the dataset : ",data.GetDataDimension())


# In[5]:


# Query to find number of points present in the uniform grid of the data
print("Number of points present in the uniform grid of the data : ",data.GetNumberOfPoints())


# In[6]:


# Get the point data
pointData = data.GetPointData()
pressureArray = pointData.GetArray("Pressure")

# Get the range of Pressure values
ans = pressureArray.GetRange()
print("Range of Pressure values: ", ans[0], " to ", ans[1])


# In[7]:


# Find the average of the pressure values
numPoints = pressureArray.GetNumberOfTuples()
totalPressure = 0
for i in range(numPoints):
    totalPressure += pressureArray.GetValue(i)
avgPressure = totalPressure / numPoints
print("Average Pressure value of entire dataset : ", avgPressure)


# In[8]:


def show_information(id):
    '''
    funtion take id as argument, and generate the information of the dataset such as :
    1. Print the indices of the four corner vertices of the cell.
    2. Print the 3D coordinate of each vertex
    3. Compute the 3D coordinate of the cell center using its four corner vertices
    4. Print the Pressure Value for all the four vertices
    5. Compute and print the mean (average) Pressure value at the cell center
    '''
    cell = data.GetCell(id)
    
    # Get the indices of the corner vertices
    pointIds = cell.GetPointIds()
    
    pressureArray = pointData.GetArray("Pressure")
    
    # Create a vtkPoints object
    points = vtk.vtkPoints()

    # Print the indices of the corner vertices
    print("Indices of corner vertices:")
    print("{0},{1},{2},{3} ".format(pointIds.GetId(0),pointIds.GetId(1),pointIds.GetId(2),pointIds.GetId(3)),'\n')
        
    # Print the cell information
    print("Number of Points:", cell.GetNumberOfPoints())
    print("Number of Edges:", cell.GetNumberOfEdges())
    print("Number of Faces:", cell.GetNumberOfFaces(),'\n')
    
#     for calculating the x_mean and y_mean and we know z_mean remain same as z_value, so no need to find it.
    x_value = 0
    y_value = 0
    point = data.GetPoint(pointIds.GetId(0))
    x_value += point[0]
    y_value += point[1]
    z_value = point[2]
    print("Coordinates V1: ({0},{1},{2})".format(point[0], point[1], point[2]))
    point1 = [point[0], point[1], point[2]]
    points.InsertNextPoint(point[0], point[1], point[2])
    pres1 = pressureArray.GetValue(pointIds.GetId(0))
    print("Pressure Value ",pres1,'\n')
    
    point = data.GetPoint(pointIds.GetId(1))
    x_value += point[0]
    y_value += point[1]
    print("Coordinates V2:  ({0},{1},{2})".format(point[0], point[1], point[2]))
    point2 = [point[0], point[1], point[2]]
    points.InsertNextPoint(point[0], point[1], point[2])
    pres2 = pressureArray.GetValue(pointIds.GetId(1))
    print("Pressure Value ",pres2,'\n')
    
    point = data.GetPoint(pointIds.GetId(2))
    x_value += point[0]
    y_value += point[1]
    print("Coordinates V3: ({0},{1},{2})".format(point[0], point[1], point[2]))
    point3 = [point[0], point[1], point[2]]
    points.InsertNextPoint(point[0], point[1], point[2])
    pres3 = pressureArray.GetValue(pointIds.GetId(2))
    print("Pressure Value ",pres3,'\n')
    
    point = data.GetPoint(pointIds.GetId(3))
    x_value += point[0]
    y_value += point[1]
    print("Coordinates V4:  ({0},{1},{2})".format(point[0], point[1], point[2]))
    point4 = [point[0], point[1], point[2]]
    points.InsertNextPoint(point[0], point[1], point[2])
    pres4 = pressureArray.GetValue(pointIds.GetId(3))
    print("Pressure Value ",pres4,'\n')
    
    print("3D coordinate of the cell center : ({0},{1},{2})".format(x_value/4,y_value/4,z_value))
    
    print("Average Pressure value at the cell center : ", (pres1+pres2+pres3+pres4)/4)
    
    
# Create a vtkPolyData object
    new_poly = vtk.vtkPolyData()
    new_points = vtk.vtkPoints()
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName("Colors")

    for i in range(4):
        vertex_coordinates = data.GetPoint(pointIds.GetId(i))
        new_points.InsertNextPoint(vertex_coordinates)
# Add a color for each point
    colors.InsertNextTuple3(0, 0, 255) 
    colors.InsertNextTuple3(255, 0, 0)  
    colors.InsertNextTuple3(0, 255, 0)  
    colors.InsertNextTuple3(255, 25, 0)   
    new_poly.SetPoints(new_points)
# Add the colors to the polydata
    new_poly.GetPointData().SetScalars(colors)   
# Create visual representations for each point in the form of a Vertex Glyph
    glyph_filter = vtk.vtkVertexGlyphFilter()
    glyph_filter.SetInputData(new_poly)
# Create an mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(glyph_filter.GetOutputPort())
# Create an actor
    actor = vtk.vtkActor()
    actor.GetProperty().SetPointSize(5)
    actor.SetMapper(mapper)
# Create a renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
# Create a render window
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
# Create a render window interactor
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    render_window.Render()
#     render_window.Render()
    render_window_interactor.Start()
    return ""


# In[9]:


# Extract a vtkCell object with cell id
print(show_information(0))


# In[ ]:




