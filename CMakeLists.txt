cmake_minimum_required(VERSION 2.8.9)

project(SlicerFab)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://github.com/SlicerFab/SlicerFab")
set(EXTENSION_CATEGORY "Printing")
set(EXTENSION_CONTRIBUTORS "Steve Pieper (Isomics, Inc.), Ahmed Hosney (Harvard Wyss), James Weaver (Harvard Wyss), Steve Keating (MIT Media Lab)")
set(EXTENSION_DESCRIPTION "Tools for 3D object fabrication.")
set(EXTENSION_ICONURL "https://cdn.rawgit.com/SlicerFab/SlicerFab/0f141879/slices.png")
set(EXTENSION_SCREENSHOTURLS "https://cdn.rawgit.com/SlicerFab/SlicerFab/0f141879/rendering.png")

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(BitmapGenerator)
add_subdirectory(Constructor)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
