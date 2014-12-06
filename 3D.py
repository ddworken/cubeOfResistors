DIFF_THRESHOLD = 1e-40
width = height = zIndex = 3


class Fixed:
    FREE = 0
    A = 1
    B = 2


class Node:
    __slots__ = ["voltage", "fixed"]

    def __init__(self, v=0.0, f=Fixed.FREE):
        self.voltage = v
        self.fixed = f


def set_boundary(mesh):
    mesh[width / 2][height / 2][zIndex/2] = Node(1.0, Fixed.A)
    mesh[width / 2 + 1][height / 2][zIndex/2] = Node(-1.0, Fixed.B)


def calc_difference(mesh, difference):
    total = 0.0
    for z in xrange(zIndex):
        for y in xrange(height):
            for x in xrange(width):
                totalVoltage = 0.0
                numberConnections = 0
                if z != 0:
                    totalVoltage += mesh[y][x][z-1].voltage
                    numberConnections += 1
                if y != 0:
                    totalVoltage += mesh[y-1][x][z].voltage
                    numberConnections += 1
                if x != 0:
                    totalVoltage += mesh[y][x-1][z].voltage
                    numberConnections += 1
                if z < zIndex-1:
                    totalVoltage += mesh[y][x][z+1].voltage
                    numberConnections += 1
                if y < height-1:
                    totalVoltage += mesh[y + 1][x][y].voltage
                    numberConnections += 1
                if x < width - 1:
                    totalVoltage += mesh[y][x + 1][y].voltage
                    numberConnections += 1
                totalVoltage = mesh[y][x][z].voltage - totalVoltage / numberConnections

                difference[y][x][z].voltage = totalVoltage
                if mesh[y][x][z].fixed == Fixed.FREE:
                    total += totalVoltage ** 2
    return total


def iter(mesh):
    difference = [[[Node() for x in xrange(width)] for y in xrange(height)] for z in xrange(zIndex)]

    while True:
        set_boundary(mesh)
        if calc_difference(mesh, difference) < DIFF_THRESHOLD:
            break
        for i, di in enumerate(difference):
            for j, dij in enumerate(di):
                for z, dijz in enumerate(dij):
                    mesh[i][j][z].voltage -= dijz.voltage

    current = [0.0] * 3
    for i, di in enumerate(difference):
        for j, dij in enumerate(di):
            for z, dijz in enumerate(dij):
                current[mesh[i][j][z].fixed] += (dijz.voltage * (bool(i) + bool(j) + bool(z) + (i < height - 1) + (j < width - 1) + (z < zIndex -1)))

    return (current[Fixed.A] - current[Fixed.B]) / 2.0


def main():
    mesh = [[[Node() for x in xrange(width)] for y in xrange(height)] for z in xrange(zIndex)]

    print "R = " + str(3 / iter(mesh))

if __name__ == "__main__":
    main()
