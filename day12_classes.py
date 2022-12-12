from __future__ import annotations
from typing import Optional


class State:
    def __init__(
        self,
        letter: str,
        number: int,
        available: bool = True,
        sequence: Optional[list] = None
    ):
        self.letter = letter
        self.number = number
        self.available = available
        if sequence is None:
            self.sequence = []
    
    @classmethod
    def create(cls, letter: str) -> State:
        number = ord(letter)
        return cls(
            letter=letter,
            number=number
        )
    
    def __repr__(self) -> str:
        available = "." if self.available else "x"
        return f"({self.letter}, {available})"

    def is_accessible(self, number: int, reverse: bool = False) -> bool:
        if reverse:
            return self.available and (number - self.number <= 1)
        else:
            return self.available and (self.number - number <= 1)
