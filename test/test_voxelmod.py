#!/usr/bin/env python3
"""
Test Voxel python classes.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys, os
from os.path import pardir, sep
from random import random
import unittest
sys.path.append(os.path.realpath(os.path.dirname(os.path.realpath(__file__)) +
                                 sep + pardir))
from virtual_population import *


class TestReducedVoxelData(unittest.TestCase):
    """Tests for Voxel Info and Data."""
    @classmethod
    def setUpClass(cls):
        """Class-wide files"""
        cls.voxelInfoFile = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + sep + 'full_materials.txt')
        cls.voxelDataFile = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + sep + 'full_materials.raw')
        print('Voxel metadata file: ', cls.voxelInfoFile)
        print('Voxel data file: ', cls.voxelDataFile)

    def testVoxelEnvironment(self):
        """Test Voxel Info (meta-data) class."""
        self.assertTrue(os.path.isfile(self.voxelInfoFile))
        self.assertTrue(os.path.isfile(self.voxelDataFile))

    def testCreateVirtPopVoxel(self):
        """Create a virtual population object."""
        testVoxel = VirtualPopulation()
        self.assertIsInstance(testVoxel, VirtualPopulation)
        testVoxel.name = 'myVoxel'
        self.assertEqual('myVoxel',testVoxel.name)
        testVoxel.nx = 100; testVoxel.ny = 200; testVoxel.nz = 300
        testVoxel.dx = 0.005; testVoxel.dy = 0.005; testVoxel.dz = 0.005;
        self.assertEqual(100, testVoxel.nx)
        self.assertEqual(200, testVoxel.ny)
        self.assertEqual(300, testVoxel.nz)
        self.assertEqual(0.005, testVoxel.dx)
        self.assertEqual(0.005, testVoxel.dy)
        self.assertEqual(0.005, testVoxel.dz)
        testVoxel.appendMaterial('Bone', 1.0, 1.0, 1.0)
        self.assertEqual([1, 'Bone', 1.0, 1.0, 1.0], testVoxel.material(1))
        testVoxel.appendMaterial('Fat', random(), random(), random())
        testVoxel.appendMaterial('Muscle', random(), random(), random())
        testVoxel.appendMaterial('Air', random(), random(), random())
        self.assertEqual(5, testVoxel.numMaterials)
        testVoxel.removeMaterial('Bone')
        self.assertEqual(4, testVoxel.numMaterials)

    def testReadVirtualPopulationFromFile(self):
        """Test Virtual Population reader."""
        testVoxel = readVirtualPopulation(self.voxelInfoFile,
                                          self.voxelDataFile)
        self.assertIsInstance(testVoxel, VirtualPopulation)
        self.assertEqual(122, testVoxel.nx)
        self.assertEqual(62, testVoxel.ny)
        self.assertEqual(93, testVoxel.nz)
        self.assertEqual(0.005, testVoxel.dx)
        self.assertEqual(0.005, testVoxel.dy)
        self.assertEqual(0.005, testVoxel.dz)
        self.assertEqual(78, testVoxel.numMaterials)
        self.assertEqual('Adult_male_1_34y/Adrenal_gland',
                         testVoxel.material(1)[1])
        self.assertEqual('Adult_male_1_34y/Heart_muscle',
                         testVoxel.material(30)[1])
        self.assertEqual('Adult_male_1_34y/Vertebrae',
                         testVoxel.material(77)[1])
        self.assertEqual(testVoxel.nx * testVoxel.ny * testVoxel.nz,
                         len(testVoxel.data))

    def testWriteVirtualPopulation(self):
        """Write Virtual Population object data to raw and info files."""
        newVoxel = VirtualPopulation()
        newVoxel.name = 'newVoxel'
        newVoxel.nx = 100; newVoxel.ny = 200; newVoxel.nz = 300
        newVoxel.dx = 0.005; newVoxel.dy = 0.005; newVoxel.dz = 0.005;
        newVoxel.appendMaterial('Bone', 1.0, 1.0, 1.0)
        newVoxel.appendMaterial('Fat', random(), random(), random())
        newVoxel.appendMaterial('Muscle', random(), random(), random())
        newVoxel.appendMaterial('Air', 0.0, 0.0, 0.0)
        newVoxel.data = bytearray([0,1,2,3])
        self.assertEqual('newVoxel', newVoxel.name)
        status = writeVirtualPopulation(newVoxel, os.getcwd())
        self.assertEqual(0, status)
        self.assertTrue(os.path.isfile('newVoxel.txt'))
        self.assertTrue(os.path.isfile('newVoxel.raw'))

if __name__ == '__main__':
    unittest.main()
