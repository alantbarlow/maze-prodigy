from dataclasses import dataclass


@dataclass(frozen = True)
class GridSize():
    rows: int
    columns: int