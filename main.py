import numpy as np
import time

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
class Tetris:
    def __init__(self):
        self.ok = []
        self.cube = np.zeros((3, 3, 3), dtype=np.int8)
        self.blocks = [[str2cube('11010000'), str2cube('01010100'), str2cube('00010101')]]
        self.blocks += [[str2cube('11100100')]]
        self.blocks += [[str2cube('11100010')]]
        self.blocks += [[str2cube('111100', d=(1, 2, 3))]]
        self.blocks += [[str2cube('110011', d=(1, 2, 3))]]
        self.blocks += [[str2cube('11101000')]]
        self.blocks += [[str2cube('111010', d=(1, 2, 3))]]
        self.stack = [(0, b) for b in reversed(self.blocks[0])]
        for j, bb in enumerate(self.blocks):
            if j == 0: continue
            print(f'element {j}:')
            cubes = []
            for b in bb:
                print_cube(b)
                # bb = bbox(b)
                # cube2dstr(bb)
                rot = rotate(b)   # 24 = 4*(3+3)
                for u in unique_block(rot):
                    d = [int(x) for x in u[:3]]
                    l = [(x0, x1, x2) for x0 in range(4-d[0]) for x1 in range(4-d[1]) for x2 in range(4-d[2])]
                    # print(l)
                    cubes += [str2cube(u[3:], d=d, l=x) for x in l]
                    # print(len(cubes))
                # pos2block(b)
            self.blocks[j] = cubes
            print(len(self.blocks[j]))

    def update(self):
        # print(self.stack)
        ns = [len(self.stack)]
        while len(self.stack) > 0:
            n, b = self.stack.pop()
            self.cube = np.where(self.cube > n, 0, self.cube)
            ns[n] -= 1
            # print(ns)
            # print_cube(b)
            c0 = count(self.cube)
            c = count(b)
            c1 = count(self.cube+b)
            # print(c0, c, c1, len(self.blocks))
            if c0 + c == c1:
                self.cube += b*(n+1)
                if n == len(self.blocks) - 1:  # n == 7
                    self.ok += [self.cube]
                    print(f'sol:{len(self.ok):03d}', ns)
                    print_cube(self.ok[-1])
                else:
                    self.stack += [(n+1, b) for b in reversed(self.blocks[n+1])]
                    if n+1 < len(ns):
                        ns[n+1] += len(self.blocks[n+1])
                    else:
                        ns += [len(self.blocks[n+1])]
                # print_cube(self.cube)


def str2cube(s, d=(2, 2, 2), l=(0, 0, 0)):
    b = np.pad(np.reshape(np.array([int(p) for p in s], dtype=np.int8), d),
               ((l[0], 3-d[0]-l[0]), (l[1], 3-d[1]-l[1]), (l[2], 3-d[2]-l[2])))
    return b


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
    r = sorted(r, reverse=True)
    print(len(r), r)
    # for s in r: print_cube(bbox(str2cube(s[3:], d=[int(x) for x in s[:3]])))
    return r


def count(a):
    # print(a, np.where(a > 0))
    return np.shape(np.where(a > 0))[1]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start = time.time()
    cube = Tetris()
    cube.update()
    print(f'{time.time()-start:.2f}sec')



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
