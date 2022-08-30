
The purpose of this library is to build and test the central building blocks needed for making Hexagonal Grids.

No UI implementations are done, everything strictly deals in the math-space.

https://codeberg.org/ldesousa/hex-utils/src/branch/develop/hex_utils

Advice
======

Work out your data structure needs and create those classes first.

Working with Hexagonal grids mainly needs two types of data structures, geometry and coordinate systems.

Geometry mainly deals with screen / pixel representations of objects, which is used for:
   - Drawing objects to the screen
   - Getting pixel coordinates and translationg them to coordiate-friendly postions.

Coordinates mainly deal with turning pixel-based positions and turning them into easier and cleaner to use math for hexagons.

Geometry:
   - Points
   - Lines
   - Rectangles
   - Hexagons

Coordinates:
   - Offset
   - Axial
   - Cube


Misc
====

This library is more concerned with the raw math of grid needs, so some things that might be needed for UI are ignored.

