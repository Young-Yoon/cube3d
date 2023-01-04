## How many ways to make a 3x3x3 cube from the seven blocks?

![Building blocks](202301011830.jpg)

* Answer: [339](sol.txt) 

## Approach
1. Find all moves of blocks
    1. Rotate each block: Symmetric group S4, Alternating group A4
    2. Translate each rotated block
2. Place blocks in order
    * Depth-first search
