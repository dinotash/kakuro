"""
Defines types used to represent kakuro puzzles at
various stages of the processing pipeline.
"""

from enum import Enum
import collections

IndexPuzzle = collections.namedtuple('IndexPuzzle',
                                     ['id', 'timestamp_millis', 'page_url', 'difficulty'])

class Difficulty(Enum):
    """
    Defines the valid difficulty levels that a puzzle can be.
    """
    EASY = 1
    MEDIUM = 2
    HARD = 3
