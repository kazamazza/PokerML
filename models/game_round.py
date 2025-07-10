from enum import Enum


class GameRound(str, Enum):
    Preflop = "Preflop"
    Flop = "Flop"
    Turn = "Turn"
    River = "River"

    @classmethod
    def all(cls):
        return [cls.Preflop, cls.Flop, cls.Turn, cls.River]