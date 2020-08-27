# PathFinding-Visualizer

A simple Pathfinding visualizer built by using pygame. It consists of three pathfinding methods which are A*, breath-first search(BFS) and dijkstra.

# Instruction
* Simply Run from the pathfinding.exe
* To run from the pathfinding.py, one must install pygame beforehand. To install pygame, insert the following in the command line:
    >python3 -m pip install -U pygame --user 
    
# Keyboard Binding
* Mouse Left Click - First click will be the starting point, the second click will be the ending point and the following click will be obstacle
* Mouse Right Click - Erase the spot
* 1 - A*
* 2 - BFS
* 3 - Dijkstra
* r - Clear everything and reset the board
* c - Clear everything except the obstacles
* g - Randomly generate obstacles
 
 # Notes
 * BFS and Dijkstra will nearly identical to each other because of the cost distance for dijkstra are equal for all which is 1.
 * Green color grid - Start Point
 * Red color grid - End Point
 
