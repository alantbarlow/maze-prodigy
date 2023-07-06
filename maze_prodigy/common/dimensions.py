from dataclasses import dataclass


@dataclass(frozen = True)
class Dimensions():
    height: int
    width: int

    def __truediv__(self, other):
        return Dimensions(self.height / other, self.width / other)
    
    def __sub__(self, other):
        if isinstance(other, Dimensions):
            return Dimensions(self.height - other.height, self.width - other.width)