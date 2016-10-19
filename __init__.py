"""
voxelmod: a collection of python tools to modify voxel data for biological 
models.
"""
__all__ = ['VirtualPopulation', 'readVirtualPopulation',
           'writeVirtualPopulation']
from voxelmod.virtual_population import (VirtualPopulation,
                                         readVirtualPopulation,
                                         writeVirtualPopulation)
from voxelmod.reduce_voxel import ReduceVoxel
