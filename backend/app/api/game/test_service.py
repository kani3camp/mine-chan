import dataclasses

from app.api.game.model import Vertex
from app.api.game.service import is_adjacent


def test_is_adjacent():
    @dataclasses.dataclass
    class TestCase:
        v1: Vertex
        v2: Vertex
        is_adjacent: bool
    
    testCases = [
        TestCase(
            v1=Vertex(3, 3),
            v2=Vertex(3, 3),
            is_adjacent=True
        ),
        TestCase(
            v1=Vertex(3, 3),
            v2=Vertex(2, 3),
            is_adjacent=True,
        ),
        TestCase(
            v1=Vertex(3, 3),
            v2=Vertex(2, 2),
            is_adjacent=True
        ),
        TestCase(
            v1=Vertex(3, 3),
            v2=Vertex(4, 4),
            is_adjacent=True
        ),
        TestCase(
            v1=Vertex(3, 3),
            v2=Vertex(1, 1),
            is_adjacent=False
        )
    ]
    for testCase in testCases:
        assert is_adjacent(testCase.v1, testCase.v2) == testCase.is_adjacent
