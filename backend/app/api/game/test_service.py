import dataclasses

from ..db.model import Vertex


def test_is_adjacent():
    @dataclasses.dataclass
    class TestCase:
        v1: Vertex
        v2: Vertex
        expected: bool
    
    test_cases = [
        TestCase(
            v1=Vertex(3, 3),
            v2=Vertex(3, 3),
            expected=True
        ),
        TestCase(
            v1=Vertex(3, 3),
            v2=Vertex(2, 3),
            expected=True,
        ),
        TestCase(
            v1=Vertex(3, 3),
            v2=Vertex(2, 2),
            expected=True
        ),
        TestCase(
            v1=Vertex(3, 3),
            v2=Vertex(4, 4),
            expected=True
        ),
        TestCase(
            v1=Vertex(3, 3),
            v2=Vertex(1, 1),
            expected=False
        )
    ]
    for testCase in test_cases:
        assert testCase.v1.is_adjacent(testCase.v2) == testCase.expected
