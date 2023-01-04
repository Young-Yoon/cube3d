## How many ways to make a 3x3x3 cube from the seven blocks?

![Building blocks](202301011830.jpg)

* Answer: [339](sol.txt) 

## Approach
1. Find all moves of blocks
    1. Rotate each block: Symmetric group S4, Alternating group A4
    2. Translate each rotated block
2. Place blocks in order
    * Depth-first search

## Cube representation
### Solution
```
sol:001 (0+000, 0+100, 2+111, 0+002, 3+021, 2+010, 8+200)
114  224  724
614  233  773
665  655  753
```
* A cube has the three planes of 3x3.
* Numbers indicate the block id's.
* In `i+ddd`, `ddd` represents the translation in each axis.

### Block in string format
```
330  000  000
300  300  000
000  000  000
```
is inside the bounding box of the tensor shape `(2,2,2)` like 
```
11  00
10  10
```
The dimension of the bounding box and the occupancy is combined as 
`'22211100010'`.
