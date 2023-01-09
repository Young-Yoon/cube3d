## How many ways to make a 3x3x3 cube from the seven blocks?

![Building blocks](202301011830.jpg)
```
C B A F  # Blocks in the above figure
G  E  D
```

* Answer: [339](sol.txt) 

### Description
* A cube consists of 27 voxels. Each voxel has three dimension. 
```
000 001 002  100 101 102  200 201 202
010 011 012  110 111 112  210 211 212
020 021 022  120 121 122  220 221 222
```

* There are 7 building blocks: A .. G.
Blocks have 4 voxels except that A has 3 voxels.

* The shape of a block can be depicted with voxels.
```
CC ..  BB .B  AA ..  FF F.
C. C.  B. ..  A. ..  .. ..

.G. ...  .EE ...   ..D ...
GGG ...  EE. ...   DDD ...
```

## Approach
1. Find all movable position of each block
    1. Rotatation: Subgroup of symmetric group S4
    2. Translation
2. Place blocks in order
    * Depth-first search



## Rotation
### Position Type
Type is preserved by rotation  
* Vertex
```
{000, 002, 020, 022, 200, 202, 220, 222}
```
* Edge
```
{001, 010, 012, 021,
 100, 102, 120, 122,
 201, 210, 212, 221}
```
* Face
```
{011, 101, 110, 112, 121, 211}
```
* Center
```
{111}
```
* 8Vertex+12Edge+6Face+1Center  
`8eee+12eeo+6eoo+1ooo=(2e+o)^3`

### Rotation Operation
* Properties
    1. Preserve Even/Odd  
 `(a,b,c), (2-a,b,c), (a,2-b,c), (a,b,2-c)`
    2. Permutation  
 `(a,b,c), (a,c,b), (b,a,c), (b,c,a), (c,a,b), (c,b,a)`
* Simple operation: Rotation & Flip
    1. Rotation through diagonal axis  
`(a,b,c) <-> (b,c,a) <-> (c,a,b)`
    2. Flip against the parallel faces  
`(a,b,c) <-> (2-a,b,c)`  
`(a,b,c) <-> (a,2-b,c)`  
`(a,b,c) <-> (a,b,2-c)`
    3. Flip against the diagonal planes  
`(a,b,c) <-> (a,c,b)`  
`(a,b,c) <-> (b,a,c)`  
`(a,b,c) <-> (c,b,a)`  

## Solution
```
#001 (0+000, 0+100, 2+111, 0+002, 3+021, 2+010, 8+200)
AAD  BBD  GBD
FAD  BCC  GGC
FFE  FEE  GEC
```
* A cube has the three planes of 3x3.
* Alphabets indicate the block id's.
* In `i+ddd`, `ddd` represents the translation in each axis.

### Block in string format
```
CC.  ...  ...
C..  C..  ...
...  ...  ...
```
has the bounding box of size `(2,2,2)`:  
```
11  00
10  10
```
where `1` is the occupied position by the block and `0` is the empty position. 
The sequence is serialized as `11 10 00 10` in the tensor order.  
The dimension of the bounding box `222` and the occupancy sequence `11100010` are combined into 
`'22211100010'`.
