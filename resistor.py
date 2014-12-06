DIFF_THRESHOLD = 1e-40
width = height = 10


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
    mesh[width / 2][height / 2] = Node(1.0, Fixed.A)
    mesh[width / 2 + 2][height / 2 + 1] = Node(-1.0, Fixed.B)


def calc_difference(mesh, difference):
    total = 0.0

    for y in xrange(height):
        for x in xrange(width):
            totalVoltage = 0.0
            numberConnections = 0
            if y != 0:
                totalVoltage += mesh[y-1][x].voltage
                numberConnections += 1
            if x != 0:
                totalVoltage += mesh[y][x-1].voltage
                numberConnections += 1
            if y < height-1:
                totalVoltage += mesh[y + 1][x].voltage
                numberConnections += 1
            if x < width - 1:
                totalVoltage += mesh[y][x + 1].voltage
                numberConnections += 1
            totalVoltage = mesh[y][x].voltage - totalVoltage / numberConnections

            difference[y][x].voltage = totalVoltage
            if mesh[y][x].fixed == Fixed.FREE:
                total += totalVoltage ** 2
    return total


def iter(mesh):
    difference = [[Node() for j in xrange(width)] for i in xrange(height)]

    while True:
        set_boundary(mesh)
        if calc_difference(mesh, difference) < DIFF_THRESHOLD:
            break
        for i, di in enumerate(difference):
            for j, dij in enumerate(di):
                mesh[i][j].voltage -= dij.voltage

    current = [0.0] * 3
    for i, di in enumerate(difference):
        for j, dij in enumerate(di):
            current[mesh[i][j].fixed] += (dij.voltage *
                                          (bool(i) + bool(j) + (i < height - 1) + (j < width - 1)))

    print 2 / ((current[1] - current[2]) / 2.0)
    return (current[Fixed.A] - current[Fixed.B]) / 2.0


def main():
    mesh = [[Node() for j in xrange(width)] for i in xrange(height)]

    print "R = " + str(2 / iter(mesh))


if __name__ == "__main__":
  main()
