from dataclasses import dataclass

@dataclass(frozen = True)
class Point():
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):
            return Point(self.x + other, self.y + other)
        else:
            raise TypeError(f"The addition opperator can only be used to add 'int's, 'float's, and 'Point's, it can't be used to add a type of {type(other)}.")
        
    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        elif isinstance(other, (int, float)):
            return Point(self.x - other, self.y - other)
        else:
            raise TypeError(f"The addition opperator can only be used to subtract 'int's, 'float's, and 'Point's, it can't be used to subtract a type of {type(other)}.")
    
    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)