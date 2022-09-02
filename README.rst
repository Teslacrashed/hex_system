======
README
======

The purpose of this library is to build and test the central building blocks needed for making Hexagonal Grids.

At current this code isn't very useable in a traditional way.

I tend to import new bits into main.py and prototype new code.

Eventually I flesh that code out into a module, and am trying to get better about using tests.

Test cases are slowly being added as I confirm things are accurate.

All code assumes hexes are pointy-topped and that the grid is odd-row rectangles.

This is a side-project of mine and won't be updated in any stable way for the time being
so expect drastic changes from any update until this project is declared stable.

Advice
======

Work out your data structure needs and create those classes first.

Working with Hexagonal grids mainly needs two types of data structures, geometry and coordinate systems.

Geometry mainly deals with screen / pixel representations of objects, which is used for:
   - Drawing objects to the screen
   - Getting pixel coordinates and translationg them to coordiate-friendly postions.

Coordinates deal with cleaner methods of identifying and grabbing hexes on grids.

Geometry:
   - Points
   - Lines
   - Rectangles
   - Hexagons

Coordinates:
   - Cube
   - Offset

Misc
====

This library is more concerned with the raw math of grid needs, so some things that might be needed for UI are ignored.

Like most hex-based systems, much appreciation is given to Red Blob Games.

https://www.redblobgames.com
