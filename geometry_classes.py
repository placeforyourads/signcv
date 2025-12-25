from math import *
epsilon = 1e-7
def rnd(p, epsilon=14):
    return round(p, epsilon)
class Point:
    def __init__(self, inp: bool, x=None, y=None, polar=False):
        if inp:
            x, y = map(float, input().split())
        if not polar:
            if type(x) in (int, float):
                self.x = x
                self.y = y
            elif type(x) == Point:
                self.x = x.x
                self.y = x.y
        else:
            self.x = x * cos(y)
            self.y = x * sin(y)

        self.x = rnd(self.x)
        self.y = rnd(self.y)

    def __abs__(self):
        return self.dist()

    def dist(self, point=None, y=None, polar=False):
        if type(point) == Point:
            difx = abs(self.x - point.x)
            dify = abs(self.y - point.y)
        elif point == None:
            difx = abs(self.x)
            dify = abs(self.y)
        elif type(point) in (int, float):
            difx = abs(self.x - point)
            dify = abs(self.y - y)
        else:
            raise TypeError
        return rnd(hypot(difx, dify))

    def __str__(self):
        return f'({self.x}, {self.y})'


    def __eq__(self, other):
        if type(other)!=Point:
            return False
        else:
            if isclose(self.x, other.x, abs_tol=epsilon) and isclose(self.y, other.y, abs_tol=epsilon):
                return True
            else:
                return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        xx = str(int(self.x/epsilon))
        yy = str(int(self.y/epsilon))
        if xx.startswith('-'):
            xx = xx.replace('-', '1')
        else:
            xx = '2'+xx
        if yy.startswith('-'):
            yy = yy.replace('-', '1')
        else:
            yy = '2'+yy
        return int(xx+yy)


def PointFromAngle(x, y, dist, angle):
    old = Point(False, dist, angle, polar = True)
    return Point(False, old.x+x, old.y+y, polar=False)

class Vector(Point):
    def __init__(self, inp: bool, a=None, b=None, c=None, d=None):
        if type(d) in (int, float):
            A = c - a
            B = d - b
        elif type(b) in (int, float):
            A = a
            B = b
        elif type(b) == Point:
            A = b.x - a.x
            B = b.y - a.y
        elif type(a) == Point:
            A = a.x
            B = a.y
        elif type(a) == Vector:
            A = a.x
            B = a.y
        else:
            raise ValueError
        self.point = super().__init__(False, A, B)

    def __mul__(self, other):
        if type(other) == Vector:
            return self.dot_product(other)
        elif type(other) in (int, float):
            return Vector(False, self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

    def __xor__(self, other):
        return self.cross_product(other)

    def dot_product(self, other):
        if type(other) == Vector:
            return self.x * other.x + self.y * other.y
        else:
            raise TypeError(f'{other} is not a vector')

    def cross_product(self, other):
        if type(other) == Vector:
            return self.x * other.y - self.y * other.x
        else:
            raise TypeError(f'{other} is not a vector')

    @property
    def length(self):
        return hypot(self.x, self.y)

    def sin(self, other):
        if type(other) == Vector:
            try:
                return (self.x * other.y - self.y * other.x) / (self.length * other.length)
            except Exception:
                return False
        else:
            raise TypeError(f'{other} is not a vector')

    def cos(self, other):
        if type(other) == Vector:
            try:
                return (self.x * other.x + self.y * other.y) / (self.length * other.length)
            except Exception:
                return False
        else:
            raise TypeError(f'{other} is not a vector')

    def __str__(self):
        return f'Vector{super().__str__()}'

    def angle_between(self, other, rad = True):
        sn = self.sin(other)
        cs = self.cos(other)
        a = atan2(sn, cs)
        if a < 0:
            a += (pi * 2)

        return a if rad else degrees(a)

class Line:
    def __init__(self, inp = False, a = None, b=None, c=None):
        if inp:
            a, b = map(int, input().split())
            a = Point(False, a, b)
            c, d = map(int, input().split())
            b = Point(False, c, d)
        if type(b) == Point:
            a_ = a.x - b.x
            b_ = a.y - b.y
            if isclose(a_, 0, abs_tol=epsilon) and isclose(b_, 0, abs_tol=epsilon):
                self.a = 1
                self.b = -1
                self.c = a.x - a.y
            elif isclose(a_, 0, abs_tol=epsilon):
                self.a = 1
                self.b = 0
                self.c = -a.x
            elif isclose(b_, 0, abs_tol=epsilon):
                self.a = 0
                self.b = 1
                self.c = -a.y
            elif a_ and b_:
                self.a = b.y - a.y
                self.b = a.x - b.x
                self.c = a.y * (b.x - a.x) - a.x * (b.y - a.y)

        elif type(c) in {int, float}:
            self.a = a
            self.b = b
            self.c = c
        elif type(a) == Line:
            self.a = a.a
            self.b = a.b
            self.c = a.c
        else:
            pass
        if isclose(self.a, int(self.a), abs_tol=epsilon):
            self.a = int(self.a)
        if isclose(self.b, int(self.b), abs_tol=epsilon):
            self.b = int(self.b)
        if isclose(self.c, int(self.c), abs_tol=epsilon):
            self.c = int(self.c)

        self.a = rnd(self.a)
        self.b = rnd(self.b)
        self.c = rnd(self.c)

    def has(self, pt: Point):
        if type(pt)==Point and isclose(self.a * pt.x + self.b * pt.y + self.c, 0, abs_tol = epsilon):
            return True
        return False

    def intercept(self, ln):
        if type(ln) == Line:
            if isclose(self.a, ln.a, abs_tol = epsilon) and isclose(self.b, ln.b, abs_tol = epsilon):
                if isclose(self.c, ln.c, abs_tol = epsilon):
                    return True
                else:
                    return None
            else:
                dl = self.a*ln.b-self.b*ln.a
                if dl:
                    x = (self.b * ln.c - self.c * ln.b) / (self.a * ln.b - self.b * ln.a)
                    y = (ln.a * self.c - self.a * ln.c) / (self.a * ln.b - self.b * ln.a)
                    return Point(False, x, y)
                else:
                    return None

    def __str__(self):
        return f"{self.a}x+{self.b}y+{self.c}=0"