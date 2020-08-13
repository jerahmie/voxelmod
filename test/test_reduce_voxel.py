#!/usr/bin/env python3
"""
Test reduce_itis_voxel.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys
import os
from os.path import (pardir, sep)
import unittest
sys.path.append(os.path.realpath(os.path.dirname(os.path.realpath(__file__)) +
                                 sep + pardir ))
from voxelmod.virtual_family import(VirtualPopulation,
                                    readVirtualPopulation,
                                    writeVirtualPopulation,
                                    ReduceVoxel)

class TestReduceVoxelData(unittest.TestCase):
    """Tests for voxel material reductions."""
    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.dirname(os.path.realpath(__file__))
        print(cls.test_dir)
        cls.voxel_map_file = os.path.realpath(cls.test_dir + sep +
                                              'material_map_4.txt')
        full_mat_info_file = os.path.realpath(cls.test_dir + sep +
                                              'full_materials.txt')
        full_mat_data_file = os.path.realpath(cls.test_dir + sep +
                                              'full_materials.raw')

        print('voxel_map_file: ', cls.voxel_map_file)
        print('duke_voxel_info_file: ', full_mat_info_file)
        print('duke_voxel_data_file: ', full_mat_data_file)
        cls.full_material_voxel =  readVirtualPopulation(full_mat_info_file,
                                                         full_mat_data_file)

    def testEnvironment(self):
        """Verify the test class is set up properly."""
        self.assertIsInstance(self.full_material_voxel, VirtualPopulation)


    def testReduceVoxel(self):
        """Test the ReduceVoxel class."""
        four_mat_voxel = ReduceVoxel(self.voxel_map_file,
                                     self.full_material_voxel).voxel_model
        self.assertIsInstance(four_mat_voxel, VirtualPopulation)
        four_mat_voxel.name = 'Duke_4_Mat_Head_5mm'
        status = writeVirtualPopulation(four_mat_voxel, self.test_dir)
        
        four_voxel = readVirtualPopulation(self.test_dir + sep + 
                                          'Duke_4_Mat_Head_5mm.txt',
                                          self.test_dir + sep +
                                          'Duke_4_Mat_Head_5mm.raw')

        # Check if instance is Virtual Population object
        self.assertIsInstance(four_voxel, VirtualPopulation)

        # Check if reduced voxel object has 5 materials (4 voxel + 'Free space')
        self.assertEqual(5, four_voxel.numMaterials)

if __name__ == '__main__':
    unittest.main()
