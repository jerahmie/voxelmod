"""
A python class to represent Virtual Population voxel model info and data.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import sys, os, ntpath
from os.path import sep
import re

# Regular expression patterns for reading virtual population voxel data.
VOXEL_NAME_PROG = re.compile("([a-zA-Z0-9_.]*).txt$")
MAT_PROG = re.compile("(^[0-9]+)\s([0|0.[0-9]*|1])\s([0|0.[0-9]*|1])\s([0|0.[0-9]*|1])\s([a-zA-Z0-9_/]*)")
NXYZ_PROG = re.compile("^n([xyz])\s([0-9]*)")
DXYZ_PROG = re.compile("^d([xyz])\s([0-9.]*)")

class VirtualPopulation(object):
    """Holds Virtual Population """
    def __init__(self):
        self._name = ''
        self._nx = 0; self._ny = 0; self._nz = 0
        self._dx = 0; self._dy = 0; self._dz = 0
        self._materials = [[int('0'),
                           'Free Space',
                           float('0'), float('0'), float('0')]]
        self._data = None

    @property
    def name(self):
        """Returns name of Voxel Model."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the Voxel Model name."""
        self._name = value

    @property
    def nx(self):
        """Returns x-dimension of voxel object."""
        return self._nx

    @nx.setter
    def nx(self, value):
        """Sets x-dimension of voxel object."""
        self._nx = value

    @property
    def ny(self):
        """Returns y-dimension of voxel object."""
        return self._ny

    @ny.setter
    def ny(self, value):
        """Sets y-dimension of voxel object."""
        self._ny = value

    @property
    def nz(self):
        """Returns z-dimension of voxel object."""
        return self._nz

    @nz.setter
    def nz(self, value):
        """Sets z-dimension of voxel object."""
        self._nz = value

    @property
    def dx(self):
        """Returns delta-x of voxel object."""
        return self._dx

    @dx.setter
    def dx(self, value):
        """Sets delta-x of voxel object."""
        self._dx = value

    @property
    def dy(self):
        """Returns delta-y of voxel object."""
        return self._dy

    @dy.setter
    def dy(self, value):
        """Sets delta-y of voxel object."""
        self._dy = value

    @property
    def dz(self):
        """Returns delta-z of voxel object."""
        return self._dz

    @dz.setter
    def dz(self, value):
        """Sets delta-z of voxel object."""
        self._dz = value

    @property
    def data(self):
        """Return the Raw Voxel Data"""
        return self._data

    @data.setter
    def data(self, value):
        """Set the raw voxel data."""
        self._data = value

    @property
    def numMaterials(self):
        """Returns the number of materials in voxel object."""
        return len(self._materials)

    def material(self, matNum):
        """Returns the material at specified location."""
        if (0 <= matNum) and (matNum < len(self._materials)):
            return self._materials[matNum]
        else:
            print("Material index, ", matNum ,
                  " is out of range.  Valid range is [0,",
                  len(matNum)-1, ")")

    def appendMaterial(self, materialName, RGB_Red, RGB_Green, RGB_Blue):
        """
        Add a material to the end of the list with optional RGB color.
        """
        
        self._materials.append([self.numMaterials, materialName,
                                RGB_Red, RGB_Green, RGB_Blue])

    def removeMaterial(self, materialName ):
        """Remove material with given name."""
        matRemove = []
        for matIndex in range(len(self._materials)):
            if self._materials[matIndex][1] == materialName:
                matRemove.append(matIndex)
        for matIndex in matRemove:
            del(self._materials[matIndex])
        self._renumberMaterials()

    def _renumberMaterials(self):
        """Fix material numbering after removal."""
        index = 0
        for mat in self._materials:
            mat[0] = index
            index += 1

# Reader helper function
def readVirtualPopulation(infoFile, dataFile):
    """
    Read Virtual Population info and data files and return a Virtual Population voxel object.
    """
    voxelModel = VirtualPopulation()
    
    # Load voxel metadata from .txt file.
    if not os.path.isfile(infoFile):
        raise Exception("File name: ", infoFile, " does not exist.")

    infoFilePath, infoFileTail = ntpath.split(infoFile)
    m = re.match(VOXEL_NAME_PROG, infoFileTail)
    voxelModel.name = m.group(1)

    try:
        fileHandle = open(infoFile, 'r')
        for line in fileHandle:
            m_mat = re.match(MAT_PROG, line)
            m_nxyz = re.match(NXYZ_PROG, line)
            m_dxyz = re.match(DXYZ_PROG, line)
            if m_mat:
                voxelModel.appendMaterial(m_mat.group(5),
                                          float(m_mat.group(2)),
                                          float(m_mat.group(3)),
                                          float(m_mat.group(4)))
            elif m_nxyz:
                if m_nxyz.group(1) == "x":
                    voxelModel.nx = int(m_nxyz.group(2))
                elif m_nxyz.group(1) == "y":
                    voxelModel.ny = int(m_nxyz.group(2))
                elif m_nxyz.group(1) == "z":
                    voxelModel.nz = int(m_nxyz.group(2))
                else:
                    print(m_nxyz.group(1), m_nxyz.group(2))
            elif m_dxyz:
                if m_dxyz.group(1) == "x":
                    voxelModel.dx = float(m_dxyz.group(2))
                elif m_dxyz.group(1) == "y":
                    voxelModel.dy = float(m_dxyz.group(2))
                elif m_dxyz.group(1) == "z":
                    voxelModel.dz = float(m_dxyz.group(2))
                else:
                    print(m_dxyz.group(1), m_dxyz.group(2))
        fileHandle.close()

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise Exception("Unexpected Error.")    

    # Load data file from .raw file
    if not os.path.isfile(dataFile):
        raise Exception("File name: ", dataFile, " does not exist.")
    try:
        fileHandle = open(dataFile, 'rb')
        voxelModel.data = bytearray(fileHandle.read())
        fileHandle.close()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    except:
        print("Unexpected error:", sys_exc_info()[0])
        raise Exception("Unexpected Error.")

    return voxelModel

# Writer helper function
def writeVirtualPopulation(vpVoxel, filePath=os.getcwd()):
    """
    Write Virtual Population info and data files from given Virtual Population voxel object.
    """
    if not os.path.isdir(filePath):
        print("Directory (", filePath, ") not found.")
        return -1
    
    if not vpVoxel:
        print("Voxel object not valid.")
        return -1
    else:
        fileNameInfo = os.path.realpath(filePath + sep + \
                                        vpVoxel.name + '.txt')
        fileNameData = os.path.realpath(filePath + sep + \
                                        vpVoxel.name + '.raw')
        # Write metadata file
        try:
            fileHandle = open(fileNameInfo, 'w')
            # write materials
            for index in range(1,vpVoxel.numMaterials):
                material = vpVoxel.material(index)
                fileHandle.write(str(material[0]) + '\t' + \
                                 "{0:.6f}".format(material[2]) + '\t' + \
                                 "{0:.6f}".format(material[3]) + '\t' + \
                                 "{0:.6f}".format(material[4]) + '\t' + \
                                 material[1] + '\n')
            # write grid extents
            fileHandle.write('\nGrid extent (number of cells)\n')
            fileHandle.write('nx\t' + str(vpVoxel.nx) + '\n')
            fileHandle.write('ny\t' + str(vpVoxel.ny) + '\n')
            fileHandle.write('nz\t' + str(vpVoxel.nz) + '\n')
        
            # write spatial steps (resolution)
            fileHandle.write('\nSpatial steps [m]\n')
            fileHandle.write('dx\t' + str(vpVoxel.dx) + '\n')
            fileHandle.write('dy\t' + str(vpVoxel.dy) + '\n')
            fileHandle.write('dz\t' + str(vpVoxel.dz) + '\n')
            
            fileHandle.close()
        except IOError as e:
            print("I/O Error({0}): {1}".format(e.errno, e.strerror))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise Exception("Unexpected Error.")

        # Write binary data file

        try:
            fileHandle = open(fileNameData, 'wb')
            fileHandle.write(vpVoxel.data)
            fileHandle.close()
        except IOError as e:
            print("I/O Error({0}): {1}".format(e.errno, e.strerror))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise Exception("Unexpected Error.")

    return 0
