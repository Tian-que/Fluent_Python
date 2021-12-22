from math import hypot


class Vector:

    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y

    # str(Vector) 但 __str__ 优先级高于 __repr__
    def __repr__(self) -> str:
        return 'Vector(%r, %r)' % (self.x, self.y)

    # abs(Vector)
    def __abs__(self):
        return hypot(self.x, self.y)

    # bool(Vector)
    def __bool__(self):
        return bool(abs(self))

    # Vector1 + Vector2
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    # Vector * n
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)


pass
