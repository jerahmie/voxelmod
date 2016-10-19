#!/usr/bin/env python3
"""
Reduces the number of materials in voxel model.

The ReduceVoxel class provides methods to create a voxel object with
a reduced set of materials, according to the provided map file.

This module currently can currently handle Virtual Population biological
models.

Example:
    $ python reduce_voxel.py --input='original_voxel.raw' \
                             --map='mymap.txt' \
                             --output='reduced_vaxel.raw'
"""
from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import os
import sys
import re
from random import random
from voxelmod.virtual_population import VirtualPopulation

MATERIAL_PATTERN = re.compile('^([a-zA-Z_]*)[\s]*([a-zA-Z_][a-zA-Z_\s]*)$')

class ReduceVoxel(object):
    """
    ReduceVoxel: Create a new voxel object with a  reduced set of biological
    materials given a material map file and voxel objet.

    Args:
        voxel_map_file (str): Text file containing material substitutions
                              (mappings) for new voxel object.
        voxel_object (:obj:`VirtualPopulation`): VirtualPopulation object.
    """
    def __init__(self, voxel_map_file, voxel_object):

        self._voxel_map_file = voxel_map_file
        self._voxel_map = {}
        self._voxel_map_byte = {0:0}
        self._original_voxel_object = voxel_object
        self._reduced_voxel_object = VirtualPopulation()
        self._load_map_from_file()
        self._remap_materials()

    def _load_map_from_file(self):
        """Loads the map file and create a python dictionary."""
        if not os.path.isfile(self._voxel_map_file):
            print("Could not find file: ", self._voxel_map_file)
        else:
            print("Found: ", self._voxel_map_file)
            with open(self._voxel_map_file, 'r') as map_fh:
                map_content = map_fh.readlines()

            for map_string in map_content:
                mat_match = MATERIAL_PATTERN.match(map_string)
                if mat_match:
                    self._voxel_map[mat_match.group(1)] = mat_match.group(2)

        # Add reduced set of materials to reduced voxel object
        reduced_mat_map = {}
        map_index = 1
        reduced_materials = set(self._voxel_map.values())

        for (map_index, mat) in enumerate(reduced_materials):
            self._reduced_voxel_object.appendMaterial(mat,
                                                      random(),
                                                      random(),
                                                      random())
            reduced_mat_map[mat] = map_index

        for i in range(self._reduced_voxel_object.numMaterials):
            print(i, " : ", self._reduced_voxel_object.material(i))
        for i in range(1, self._original_voxel_object.numMaterials):
            name = self._original_voxel_object.material(i)[1].split('/')[-1]
            self._voxel_map_byte[i] = reduced_mat_map[self._voxel_map[name]]

    def _remap_materials(self):
        """
        Remap the materials according to the map file and populate voxel
        object.
        """
        self._reduced_voxel_object.name = self._original_voxel_object.name + \
                                          '_reduced'
        self._reduced_voxel_object.nx = self._original_voxel_object.nx
        self._reduced_voxel_object.ny = self._original_voxel_object.ny
        self._reduced_voxel_object.nz = self._original_voxel_object.nz
        self._reduced_voxel_object.dx = self._original_voxel_object.dx
        self._reduced_voxel_object.dy = self._original_voxel_object.dy
        self._reduced_voxel_object.dz = self._original_voxel_object.dz
        reduced_data = self._original_voxel_object.data
        for (index, data) in enumerate(reduced_data):
            if index == 10099596:
                print(index, data, ":", self._voxel_map_byte[data])
            reduced_data[index] = self._voxel_map_byte[data]
        self._reduced_voxel_object.data = reduced_data

    @property
    def voxel_model(self):
        """Return the reduced voxel model object."""
        return self._reduced_voxel_object

def main(argv):
    """
    Main entry function for voxel reduce from command line.
    """
    

if __name__ == '__main__':
    main(sys.argv[1:])
    
