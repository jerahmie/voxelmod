#!/usr/bin/env python3
"""
Test reduce_itis_voxel.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys, os
from os.path import pardir, sep
import unittest
sys.path.append(os.path.realpath(os.path.dirname(os.path.realpath(__file__)) +
                                 sep + pardir ))
from voxelmod import *
#from virtual_population import *
from reduced_voxel import ReduceVoxel

class TestReducedVoxelData(unittest.TestCase):
    """Tests for voxel material reductions."""
    @classmethod
    def setUpClass(cls):
        cls.voxelMapFile = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + \
                                        sep + 'material_map_4.txt')
        fullMaterialInfoFile = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + \
                                                sep + 'full_materials.txt')
        fullMaterialDataFile = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + \
                                                sep + 'full_materials.raw')
        
        print('voxelMapFile: ', cls.voxelMapFile)
        print('dukeVoxelInfoFile: ', fullMaterialInfoFile)
        print('dukeVoxelDatafile: ', fullMaterialDataFile)

        
        cls.fullMaterialVoxel =  readVirtualPopulation(fullMaterialInfoFile,
                                                       fullMaterialDataFile)

    def testEnvironment(self):
        """Verify the test class is set up properly."""
        self.assertIsInstance(self.fullMaterialVoxel, VirtualPopulation)
        

    def testReduceVoxel(self):
        """Test the ReduceVoxel class."""
        fourMatVoxel = ReduceVoxel(self.voxelMapFile, self.fullMaterialVoxel).voxelModel
        self.assertIsInstance(fourMatVoxel, VirtualPopulation)
        fourMatVoxel.name = 'Duke_4_Mat_Head_5mm'
        status = writeVirtualPopulation(fourMatVoxel)

        fourVoxel = readVirtualPopulation('Duke_4_Mat_Head_5mm.txt', 'Duke_4_Mat_Head_5mm.txt')
        # Check if instance is Virtual Population object
        self.assertIsInstance(fourVoxel, VirtualPopulation)
        # Check if reduced voxel object has 5 materials (4 voxel + 'Free space')
        self.assertEqual(5, fourVoxel.numMaterials)
        
if __name__ == '__main__':
    unittest.main()
