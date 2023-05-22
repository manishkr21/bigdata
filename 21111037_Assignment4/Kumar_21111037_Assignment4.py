import vtk
import numpy as np
import random
import time
from scipy.interpolate import griddata
import sys



def get_sampling(PERCENTAGE_TO_SAMPLE, output):
    

    # Define a sampling percentage
    PERCENTAGE_TO_SAMPLE = PERCENTAGE_TO_SAMPLE/100 

    # Get the number of points in the dataset
    num_points = output.GetNumberOfPoints()
    print("Number of points in the dataset:", num_points)

    # Initialize a list to store the indices of the sampled points
    SAMPLED_INDEXES = []

    # Always include the eight corner points in the sample
    CORNER_INDEXES = [0, output.GetDimensions()[0]-1, 
                      output.GetDimensions()[0]*(output.GetDimensions()[1]-1), 
                      output.GetDimensions()[0]*output.GetDimensions()[1]-1,
                      output.GetNumberOfPoints()-output.GetDimensions()[0]*output.GetDimensions()[1],
                      output.GetNumberOfPoints()-(output.GetDimensions()[0]*(output.GetDimensions()[1]-1))-1,
                      output.GetNumberOfPoints()-1-output.GetDimensions()[0]*(output.GetDimensions()[2]-1),
                      output.GetNumberOfPoints()-1]
    SAMPLED_INDEXES.extend(CORNER_INDEXES)
    print("Corner point indices:", CORNER_INDEXES)

    # Calculate the number of additional points to sample
    NUMBER_SAMPLED = int(round(num_points * PERCENTAGE_TO_SAMPLE)) - len(CORNER_INDEXES)
    print("Number of additional points to sample:", NUMBER_SAMPLED)

    # Randomly select additional points to sample
    REMAINING_INDEXES = list(set(range(num_points)) - set(CORNER_INDEXES))
    SAMPLED_INDEXES.extend(random.sample(REMAINING_INDEXES, NUMBER_SAMPLED))

    # Sort the sampled indices to make sure they're in ascending order
    SAMPLED_INDEXES.sort()

    # Create a new PolyData object to store the sampled points
    POINTS_SAMPLED = vtk.vtkPolyData()

    # Create a new Points object to store the point coordinates
    points = vtk.vtkPoints()

    # Create a new FloatArray to store the point data values
    data = vtk.vtkFloatArray()
    data.SetNumberOfComponents(1)
    data.SetName("pressure")  # Replace "pressure" with the actual name of the data array in your dataset

    # Loop over the sampled indices and add the corresponding points to the PolyData object
    for index in SAMPLED_INDEXES:
        point = output.GetPoint(index)
        points.InsertNextPoint(point)
        data.InsertNextValue(output.GetPointData().GetScalars().GetTuple1(index))

    # Add the points and data to the PolyData object
    POINTS_SAMPLED.SetPoints(points)
    POINTS_SAMPLED.GetPointData().SetScalars(data)

    # Write the sampled points to a VTKPolyData file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName("POINTS_SAMPLED.vtp")
    writer.SetInputData(POINTS_SAMPLED)
    writer.Write()
    print("Sampled points written to POINTS_SAMPLED.vtp")
    return POINTS_SAMPLED


def reconstruction_nearest(POINTS_SAMPLED):

    start_time = time.time()
    # Get the coordinates of the sampled points
    points = POINTS_SAMPLED.GetPoints()
    num_points = points.GetNumberOfPoints()
    coordinates = np.zeros((num_points, 3))
    for i in range(num_points):
        coordinates[i, :] = points.GetPoint(i)

    # Get the data values at the sampled points
    data = POINTS_SAMPLED.GetPointData().GetScalars()

    # Define the extent and spacing of the grid
    extent = [0, output.GetDimensions()[0]-1, 0, output.GetDimensions()[1]-1, 0, output.GetDimensions()[2]-1]
    spacing = output.GetSpacing()

    # Define the grid coordinates
    x, y, z = np.mgrid[extent[0]:extent[1]+spacing[0]:spacing[0],
                        extent[2]:extent[3]+spacing[1]:spacing[1],
                        extent[4]:extent[5]+spacing[2]:spacing[2]]

    # Define the interpolation method
    method = 'nearest'

    # Interpolate the data values onto the grid
    grid_data = griddata(coordinates, data, (x, y, z), method=method)


    # Create a VTKImageData object to store the reconstructed volume data
    reconstructed_data = vtk.vtkImageData()
    reconstructed_data.SetDimensions(grid_data.shape)
    reconstructed_data.SetOrigin(extent[0]*spacing[0], extent[2]*spacing[1], extent[4]*spacing[2])
    reconstructed_data.SetSpacing(spacing[0], spacing[1], spacing[2])

    # Convert the NumPy array to a VTK array
    vtk_data = vtk.vtkFloatArray()
    vtk_data.SetNumberOfComponents(1)
    vtk_data.SetName("pressure")  # Replace "pressure" with the actual name of the data array in your dataset
    for z in range(grid_data.shape[2]):
        for y in range(grid_data.shape[1]):
            for x in range(grid_data.shape[0]):
                value = grid_data[x, y, z]
                if np.isnan(value):
                    value = 0.0
                vtk_data.InsertNextValue(value)

    # Add the data to the VTKImageData object
    reconstructed_data.GetPointData().SetScalars(vtk_data)
    end_time = time.time()
    time_taken = end_time - start_time
    print("Time taken :", time_taken," secs")
    # Write the reconstructed data to a VTKImageData file
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName("reconstructed_data_nearest.vti")
    writer.SetInputData(reconstructed_data)
    writer.Write()
    return reconstructed_data

def reconstruction_linear(POINTS_SAMPLED):
    

    start_time = time.time()
    # Get the coordinates of the sampled points
    points = POINTS_SAMPLED.GetPoints()
    num_points = points.GetNumberOfPoints()
    coordinates = np.zeros((num_points, 3))
    for i in range(num_points):
        coordinates[i, :] = points.GetPoint(i)

    # Get the data values at the sampled points
    data = POINTS_SAMPLED.GetPointData().GetScalars()

    # Define the extent and spacing of the grid
    extent = [0, output.GetDimensions()[0]-1, 0, output.GetDimensions()[1]-1, 0, output.GetDimensions()[2]-1]
    spacing = output.GetSpacing()

    # Define the grid coordinates
    x, y, z = np.mgrid[extent[0]:extent[1]+spacing[0]:spacing[0],
                        extent[2]:extent[3]+spacing[1]:spacing[1],
                        extent[4]:extent[5]+spacing[2]:spacing[2]]

    # Define the interpolation method
    method = 'linear'
    # Interpolate the data values onto the grid
    grid_data = griddata(coordinates, data, (x, y, z), method=method)

    # Create a VTKImageData object to store the reconstructed volume data
    reconstructed_data = vtk.vtkImageData()
    reconstructed_data.SetDimensions(grid_data.shape)
    reconstructed_data.SetOrigin(extent[0]*spacing[0], extent[2]*spacing[1], extent[4]*spacing[2])
    reconstructed_data.SetSpacing(spacing[0], spacing[1], spacing[2])
    #Replace NaN values with nearest neighbor values
    mask = np.isnan(grid_data)
    grid_data[mask] = griddata(coordinates, data, (x, y, z), method='nearest', fill_value=0)[mask]
    # Convert the NumPy array to a VTK array
    vtk_data = vtk.vtkFloatArray()
    vtk_data.SetNumberOfComponents(1)
    vtk_data.SetName("pressure")  # Replace "pressure" with the actual name of the data array in your dataset
    for z in range(grid_data.shape[2]):
        for y in range(grid_data.shape[1]):
            for x in range(grid_data.shape[0]):
                value = grid_data[x, y, z]
                if np.isnan(value):
                    value = 0.0
                vtk_data.InsertNextValue(value)

    # Add the data to the VTKImageData object
    reconstructed_data.GetPointData().SetScalars(vtk_data)
    end_time = time.time()
    time_taken = end_time - start_time
    print("Time taken :", time_taken," secs")

    # Write the reconstructed data to a VTKImageData file
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName("reconstructed_data_linear.vti")
    writer.SetInputData(reconstructed_data)
    writer.Write()
    return reconstructed_data


#compute SNR
def compute_SNR(arr_gt,RECONSTRUCTED_ARRAY):
    diff = arrgt - RECONSTRUCTED_ARRAY
    sqd_max_diff = (np.max(arr_gt)-np.min(arr_gt))**2
    snr = 10*np.log10(sqd_max_diff/np.mean(diff**2))
    return snr


reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("Isabel_3D.vti")
reader.Update()


# Get the output of the reader
output = reader.GetOutput()


num_points = output.GetNumberOfPoints()
whole = []
for index in range(num_points):
    whole.append(output.GetPointData().GetScalars().GetTuple1(index))
arrgt = np.array(whole)
    
SAMPLED_POINTS = get_sampling(float(sys.argv[1]), output)


if sys.argv[2] == "nearest":
    DATA_RECONSTRUCTED = reconstruction_nearest(SAMPLED_POINTS)
else:
    DATA_RECONSTRUCTED = reconstruction_linear(SAMPLED_POINTS)
    
    

# Get the number of points in the dataset
num_points = DATA_RECONSTRUCTED .GetNumberOfPoints()
print("Number of points in the dataset:", num_points)

RECONSTRUCTED_ARRAY = []
for index in range(num_points):
    RECONSTRUCTED_ARRAY.append(DATA_RECONSTRUCTED.GetPointData().GetScalars().GetTuple1(index))
RECONSTRUCTED_ARRAY= np.array(RECONSTRUCTED_ARRAY)

print("SNR value is : ",compute_SNR(arrgt,RECONSTRUCTED_ARRAY))


