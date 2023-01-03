import numpy as np


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
class Tetris:
    def __init__(self):
        self.cubes = []
        self.blocks = [[str2cube('11010000'), str2cube('01010100'), str2cube('00010101')]]
        self.blocks += [[str2cube('11100100')]]
        self.blocks += [[str2cube('11100010')]]
        self.blocks += [[str2cube('111100', d=(1, 2, 3))]]
        self.blocks += [[str2cube('110011', d=(1, 2, 3))]]
        self.blocks += [[str2cube('11101000')]]
        self.blocks += [[str2cube('111010', d=(1, 2, 3))]]
        for j, bb in enumerate(self.blocks):
            if j == 0: continue
            print(f'element {j}:')
            for b in bb:
                print_cube(b)
                bb = bbox(b)
                cube2dstr(bb)
                rot = rotate(b)
                ublock = unique_block(rot)
                for u in ublock:
                    pass
                    # print_cube(bbox(dstr2block(u)))
                # pos2block(b)
        addblock(self.blocks[0][0], self.blocks[1][0])

    def update(self):
        for b in self.blocks[0]:
            pass
            # print_cube(b)


def str2cube(s, d=(2, 2, 2)):
    b = np.pad(np.reshape(np.array([int(p) for p in s], dtype=np.int8), d), ((0, 3-d[0]), (0, 3-d[1]), (0, 3-d[2])))
    return b


def dstr2cube(s):
    d = [int(x) for x in s[:3]]
    return str2cube(s[3:], d)


def cube2dstr(arr):
    msg = ''.join([str(x) for x in arr.shape])
    msg += ''.join([''.join([''.join([str(r2) for r2 in r1]) for r1 in r0]) for r0 in arr])
    # print(msg)
    return msg


def pos2cube(pos):
    # pos = np.array(np.where(pos > 0))
    # print(pos)
    b = np.zeros([3, 3, 3], dtype=np.int8)
    for i in range(np.size(pos, 1)):
        # print(pos[:, i])
        b[pos[0, i], pos[1, i], pos[2, i]] = 1
    # print_cube(b)
    return b


def print_cube(arr):
    arr = np.transpose(np.array(arr), [1, 0, 2])
    print('\n'.join(['  '.join([''.join([str(r2) for r2 in r1]) for r1 in r0]) for r0 in arr]))


def bbox(arr):
    pos = np.array(np.where(arr > 0))
    l, r = np.min(pos, axis=1), np.max(pos, axis=1)
    # print(pos, l, r)
    b = arr[l[0]:r[0] + 1, l[1]:r[1] + 1, l[2]:r[2] + 1]
    # print_cube(b)
    return b


def rotate(arr):
    pos = np.array(np.where(arr > 0))
    x = [pos]
    # print(x)
    xe, xo = [], []
    for y in x:  # flip
        xe += [np.array(y)]  # 000
        y[2, :] = 2 - y[2, :]
        xo += [np.array(y)]  # 001
        y[1, :] = 2 - y[1, :]
        xe += [np.array(y)]  # 011
        y[2, :] = 2 - y[2, :]
        xo += [np.array(y)]  # 010
        y[0, :] = 2 - y[0, :]
        xe += [np.array(y)]  # 110
        y[2, :] = 2 - y[2, :]
        xo += [np.array(y)]  # 111
        y[1, :] = 2 - y[1, :]
        xe += [np.array(y)]  # 101
        y[2, :] = 2 - y[2, :]
        xo += [np.array(y)]  # 100
    # print(xe)
    xr = []
    for y in xe:  # rotate
        xr += [np.array(y)]
        xr += [np.array([y[1], y[2], y[0]])]
        xr += [np.array([y[2], y[0], y[1]])]
    for y in xo:  # flip
        xr += [np.array([y[0], y[2], y[1]])]
        xr += [np.array([y[1], y[0], y[2]])]
        xr += [np.array([y[2], y[1], y[0]])]
    # print(xr)
    return xr


def unique_block(p):
    r = set()
    for j, y in enumerate(p):
        b = pos2cube(y)
        # print(j)
        # print_cube(b)
        bb = bbox(b)
        # print_cube(bb)
        s = cube2dstr(bb)
        if s not in r:
            r.add(s)
            # print_cube(bb)
        # print(r)
    print(len(r), r)
    return r


def count(a):
    # print(a, np.where(a > 0))
    return np.shape(np.where(a > 0))[1]


def addblock(a, b):
    print('add block', count(a), count(b), count(a+b))
    print_cube(a)
    print_cube(b)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cube = Tetris()
    cube.update()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
