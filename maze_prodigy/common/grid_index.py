from dataclasses import dataclass


@dataclass(frozen = True)
class GridIndex():
    row: int
    column: int