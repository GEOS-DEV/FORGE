import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from vtk.util.numpy_support import vtk_to_numpy
import xml.etree.ElementTree as ET
import math
import pandas as pd
from dataclasses import dataclass, asdict
from typing import Iterable, List

from vtkmodules.vtkIOLegacy import (
    vtkUnstructuredGridReader,
)
from vtkmodules.vtkIOXML import (
    vtkXMLUnstructuredGridReader,
    vtkXMLMultiBlockDataReader
)


def get_attribute_array(unstructured_grid, attribute_name):
     # Get the point data
    cell_data = unstructured_grid.GetCellData()

    # Find the index of the attribute by name
    attribute_array = cell_data.GetArray(attribute_name)

    numpy_array = vtk_to_numpy(attribute_array)

    return numpy_array


def read_attributes_from_vtu(file_path, attribute_names):
    reader = vtkXMLUnstructuredGridReader()
    reader.SetFileName(file_path)
    reader.Update()
    unstructured_grid = reader.GetOutput()

    attibutes_array = {}
    for attribute_name in attribute_names:
        attibutes_array[attribute_name] = get_attribute_array( unstructured_grid, attribute_name)

    return attibutes_array

def readDataFromVTK( file ):

    attributes_names = ['elementCenter']

    # Specify the path to the .pvd file
  
    base_directory = os.path.dirname(file)
    vtk_files_dir  = os.path.splitext(os.path.basename(file))[0]
    base_directory = os.path.join(base_directory, vtk_files_dir) 

    tree = ET.parse(file)
    root = tree.getroot()

    time = []
    time_steps = []
    max_vertical = []
    max_horizontal = []
    # Iterate through the Collection elements
    for collection in root.findall("Collection"):
        # Iterate through the DataSet elements within the Collection 
        for dataset in collection.findall("DataSet"):
            time.append( float( dataset.get("timestep") ) )
            vmt_file_path = dataset.get("file")
            time_steps.append( int ( vmt_file_path.split('/')[-1].split('.')[0] ) )

    print(len(time))
    print( time )
    print( time_steps )

    # Loop through time step indices
    for time_step in time_steps:
        vtu_dir_path = os.path.join(base_directory, f"{time_step:06d}/mesh1/Level0/Fracture")

        # List all files in the directory
        all_files = os.listdir(vtu_dir_path)

        # Filter files with the .vtu extension
        vtu_files = [file for file in all_files if file.endswith(".vtu")]

        max_vertical_tmp = 0
        max_horizontal_tmp = 0

        for vtu_file in vtu_files:
            vtu_file_path = os.path.join(vtu_dir_path, vtu_file)   
       
            attributes_array = read_attributes_from_vtu( vtu_file_path, attributes_names )

            if attributes_array['elementCenter'].size > 0:
                max_vertical_tmp = max(np.max(attributes_array['elementCenter'][:,2]), max_vertical_tmp)
                max_horizontal_tmp = max(np.max(attributes_array['elementCenter'][:,1]), max_horizontal_tmp)

        max_vertical.append(max_vertical_tmp - 298.0)
        max_horizontal.append(max_horizontal_tmp - 240.0)

    print(len(max_vertical))
    print(max_vertical)
    print(max_horizontal)

    return time, max_vertical, max_horizontal

def plotPropagationDistance( file ):
    
    time, max_vertical, max_horizontal = readDataFromVTK( file )

    fig, ax = plt.subplots(figsize=(24, 18))
    
    ax.plot(np.array(time)/60.0, np.array(max_vertical), 'r-', label='Vertical growth')
    ax.plot(np.array(time)/60.0, np.array(max_horizontal), 'b-', label='Horizontal growth')
        
    # Customize the plot
    ax.set_xlabel('Time (min)', size=30)
    ax.set_ylabel('Fracture growth (m)', size=30)
    # ax.set_xlim(100, 360000)
    # ax.set_ylim(24, 40)
    ax.legend(fontsize="30")

    ax.xaxis.set_tick_params(labelsize=30)
    ax.yaxis.set_tick_params(labelsize=30)

    vtk_files_dir  = os.path.splitext(os.path.basename(file))[0]

    plt.savefig( vtk_files_dir + "fracGrowth.png", dpi=200 )

    outputData = {}
    outputData = pd.DataFrame( outputData )

    outputData["Time"] = time
    outputData["Vertical growth"] = max_vertical
    outputData["Horizontal growth"] = max_horizontal
    outputData.to_csv( vtk_files_dir + '_fracGrowth.csv', index=False)
    
    return True 

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-sol", "--solution-file", help=" solution file")
    args = parser.parse_args()
    
    plotPropagationDistance( args.solution_file )

    
if __name__ == '__main__':
    main()
