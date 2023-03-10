import numpy as np
import time


class Tetris:
    def __init__(self, blk1=None):
        if blk1 is None:
            blk1 = [('11010000', '0+000'), ('01010100', '1+001'), ('00010101', '2+001')]
        self.ok = []
        self.cube = [np.zeros((3, 3, 3), dtype=np.int8), []]
        self.blocks = [[(str2cube(s[0]), s[1]) for s in blk1]]
        self.blocks += [[str2cube('11100100')]]
        self.blocks += [[str2cube('11100010')]]
        self.blocks += [[str2cube('111100', d=(1, 2, 3))]]
        self.blocks += [[str2cube('110011', d=(1, 2, 3))]]
        self.blocks += [[str2cube('11101000')]]
        self.blocks += [[str2cube('111010', d=(1, 2, 3))]]
        self.stack = [(0, b) for b in reversed(self.blocks[0])]
        self.rotate = [[cube2dstr(bbox(b[0])) for b in self.blocks[0]]]
        self.move_blocks()
        self.filename = 'sol' +'-'.join([s[0] + s[1] for s in blk1]) + '.bin'

    def move_blocks(self):
        for j, bb in enumerate(self.blocks):
            if j == 0:
                print_cube(bbox(self.blocks[0][0][0]))
                print(f'{len(self.blocks[0])}*1', self.rotate[0])
                continue
            cubes = []
            for b in bb:
                print_cube(bbox(b*(j+1)))
                # bb = bbox(b)
                # cube2dstr(bb)
                self.rotate.append(unique_block(rotate(b)))  # 24 = 4*(3+3)
                for k, u in enumerate(self.rotate[-1]):
                    d = [int(x) for x in u[:3]]
                    l = [(x0, x1, x2) for x0 in range(4-d[0]) for x1 in range(4-d[1]) for x2 in range(4-d[2])]
                    # print(l)
                    cubes += [(str2cube(u[3:], d=d, l=x), str(k)+'+'+''.join([str(y) for y in x])) for x in l]
                    # print(len(cubes))
                # pos2block(b)
            self.blocks[j] = cubes  # cubes = [(np[3,3,3], 'k+ddd'), ..]
            # print(len(self.blocks[j]))
            # print(self.rotate)

    def search(self):
        # print(self.stack)
        ns = [len(self.stack)]
        while len(self.stack) > 0:
            n, b_i = self.stack.pop()
            b, info = b_i
            self.cube[0] = np.where(self.cube[0] > n, 0, self.cube[0])
            del self.cube[1][n:]
            ns[n] -= 1
            # print(ns)
            # print_cube(b)
            c0 = count(self.cube[0])
            c = count(b)
            c1 = count(self.cube[0]+b)
            # print(c0, c, c1, len(self.blocks))
            if c0 + c == c1:
                self.cube[0] += b*(n+1)   # (id, n, num): (A, 0, 1), ... , (G, 6, 7)
                self.cube[1].append(info)
                if n == len(self.blocks) - 1:  # n == 7
                    self.ok.append(self.cube[1][:])
                    print('#{:03d} ({})'.format(len(self.ok), ', '.join(self.cube[1])))
                    print_cube(self.info2cube(self.cube[1]))
                else:
                    self.stack += [(n+1, b) for b in reversed(self.blocks[n+1])]
                    if n+1 < len(ns):
                        ns[n+1] += len(self.blocks[n+1])
                    else:
                        ns += [len(self.blocks[n+1])]
                # print_cube(self.cube[0])
        self.write(self.filename)

    def info2cube(self, info):
        b = np.zeros([3, 3, 3], np.int8)
        for j, s in enumerate(info):
            no, ddd = s.split('+')
            dstr = self.rotate[j][int(no)]
            b += str2cube(dstr[3:], d=[int(x) for x in dstr[:3]], l=[int(x) for x in ddd]) * (j + 1)
        return b

    def write(self, fname='sol.bin'):
        with open(fname, 'w+') as f:
            for seq in self.ok:
                for j, info in enumerate(seq):
                    no, trans = info.split('+')
                    f.write(chr(int(no)))
                    dstr = self.rotate[j][int(no)]
                    dim = [int(x) for x in dstr[:3]]
                    cap = [1]
                    for x in dim[:-1]:
                        cap.append(cap[-1]*(4-x))
                    f.write(chr(np.inner(cap, [int(x) for x in trans])[0]))

    def load(self, fname='sol.bin'):
        with open(fname, mode="rb") as f:
            fb = f.read()
        sol = []
        for n in range(0, len(fb), 14):
            seq = []
            for j in range(0, 7):
                no = int(fb[n+2*j])
                dstr = self.rotate[j][no]
                dim = [int(x) for x in dstr[:3]]
                cap = [1]
                for x in dim[:-1]:
                    cap.append(cap[-1]*(4-x))
                r = int(fb[n+2*j+1])
                trans = []
                for c in cap[::-1]:
                    trans.append(r//c)
                    r = r % c
                seq.append('{}+{}'.format(str(no), ''.join([str(s) for s in trans[::-1]])))
            sol.append(seq)
        for j in range(len(sol)):
            print('#{:03d} ({})'.format(j+1, ', '.join(sol[j])))
            print_cube(self.info2cube(sol[j]))
        self.ok = sol

    def distance(self):
        hist = np.zeros([len(self.ok), 8], dtype=np.int16)
        neighbors = {}
        for i in range(len(self.ok)):
            for j in range(i+1, len(self.ok)):
                diff = [0 if self.ok[i][k] == self.ok[j][k] else 1 for k in range(7)]
                dist = np.sum(diff)
                # print(i, j, self.ok[i], self.ok[j], dist)
                hist[i][dist] += 1
                hist[j][dist] += 1
                if dist <= 3:
                    key = ''.join([chr(ord('A')+c) for c in np.where(np.array(diff)==1)[0].tolist()])
                    val = (i+1, j+1)
                    if key not in neighbors:
                        neighbors[key] = [val]
                    else:
                        neighbors[key].append(val)
                elif dist == 3:
                    pass
        print(hist[:10])
        print(np.sum(hist, axis=0))
        nn = sorted([(k, len(neighbors[k])) for k in neighbors])
        for ch in 'ABCDEF':
            print([k for k in nn if k[0].startswith(ch)])


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
    print('\n'.join(['  '.join([''.join([chr(ord('A')+n-1) if n>0 else '.' for n in y]) for y in x]) for x in arr]))


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
    print(f'{len(r)}*{np.prod([4-int(x) for x in r[0][:3]])}', r)
    # for s in r: print_cube(bbox(str2cube(s[3:], d=[int(x) for x in s[:3]])))
    return r


def count(a):
    # print(a, np.where(a > 0))
    return np.shape(np.where(a > 0))[1]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start = time.time()
    cube = Tetris()
    # cube = Tetris([('10110000','0+000')])  # 207
    # cube.search()
    cube.load('sol.bin')
    cube.distance()
    print(f'{time.time()-start:.2f}sec')
