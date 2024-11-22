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

Pa2psi = 0.000145038
Pa2MPa = 1e-6  

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

    attributes_names = ['pressure', 'elementCenter']

    # Specify the path to the .pvd file
  
    base_directory = os.path.dirname(file)
    vtk_files_dir  = os.path.splitext(os.path.basename(file))[0]
    base_directory = os.path.join(base_directory, vtk_files_dir) 

    tree = ET.parse(file)
    root = tree.getroot()

    time = []
    time_steps = []
    pressure = []
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
        vtu_dir_path = os.path.join(base_directory, f"{time_step:06d}/mesh1/Level0/InjectionZone")

        # List all files in the directory
        all_files = os.listdir(vtu_dir_path)

        # Filter files with the .vtu extension
        vtu_files = [file for file in all_files if file.endswith(".vtu")]

        for vtu_file in vtu_files:
            vtu_file_path = os.path.join(vtu_dir_path, vtu_file)   
       
            attributes_array = read_attributes_from_vtu( vtu_file_path, attributes_names )

            injection_location = [199, 239, 297]
            index = np.where(np.all(attributes_array['elementCenter'] == injection_location, axis=1))
            if index[0].size > 0:
                pressure.append( attributes_array['pressure'][index].tolist() )

    pressure = [item for pressure in pressure for item in pressure]

    pressure = [element * Pa2psi for element in pressure]
    print(len(pressure))
    print(pressure)

    return time, pressure

def plotWellheadPressure( file ):
    
    time, pressure = readDataFromVTK( file )

    fig, ax = plt.subplots(figsize=(24, 18))
    
    ax.plot(np.array(time)/60.0, np.array(pressure), marker='o', linestyle='-')
        
    # Customize the plot
    ax.set_title('BHP vs. Time', size=30)
    ax.set_xlabel('Time (min)', size=30)
    ax.set_ylabel('BHP (psi)', size=30)
    # ax.set_xlim(100, 360000)
    # ax.set_ylim(24, 40)
    # ax.legend(fontsize="30")

    ax.xaxis.set_tick_params(labelsize=30)
    ax.yaxis.set_tick_params(labelsize=30)

    vtk_files_dir  = os.path.splitext(os.path.basename(file))[0]

    plt.savefig( vtk_files_dir + "_pressure.png", dpi=200 )

    outputData = {}
    outputData = pd.DataFrame( outputData )

    outputData["Time"] = time
    outputData["Pressure (psi)"] = pressure
    outputData.to_csv( vtk_files_dir + '_data.csv', index=False)
    
    return True 

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-sol", "--solution-file", help=" solution file")
    args = parser.parse_args()
    
    plotWellheadPressure( args.solution_file )

    
if __name__ == '__main__':
    main()
