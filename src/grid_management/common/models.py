from dataclasses import dataclass


@dataclass
class Coordinate:
    y: int
    x: int

    def __repr__(self) -> str:
        return f"<Coordinate y={self.y}, x={self.x}>"


@dataclass
class Size:
    height: int
    width: int

    def __repr__(self) -> str:
        return f"<Size height={self.height}, width={self.width}>"
