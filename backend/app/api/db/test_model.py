
import pytest

from app.api.db.model import Field, Vertex


@pytest.mark.parametrize(
    'name, field, x, y, expected',
    [
        (
                '0なら周囲の数字まで開く',
                Field(
                    game_id='1',
                    num_mines=10,
                    width=3,
                    height=3,
                    squares=['_0', '_1', '_2',
                             '_0', '_0', '_1',
                             '_0', '_0', '_0'],
                ),
                1,
                1,
                ['0', '1', '2',
                 '0', '0', '1',
                 '0', '0', '0'],
        ),
        (
                '地雷なら地雷だけ開く',
                Field(
                    game_id='1',
                    num_mines=10,
                    width=3,
                    height=3,
                    squares=['_0', '_1', '_X',
                             '_0', '_1', '_1',
                             '_0', '_0', '_0'],
                ),
                2,
                0,
                ['_0', '_1', 'X',
                 '_0', '_1', '_1',
                 '_0', '_0', '_0'],
        ),
        (
                '0以外の数字だったらそのマスだけ開く',
                Field(
                    game_id='1',
                    num_mines=10,
                    width=3,
                    height=3,
                    squares=['_0', '_1', '_X',
                             '_2', '_2', '_1',
                             '_X', '_2', '_1'],
                ),
                1,
                1,
                ['_0', '_1', '_X',
                 '_2', '2', '_1',
                 '_X', '_2', '_1'],
        ),
    ],
)
def test_dig(name: str, field: Field, x: int, y: int, expected: list[str]):
    field.dig(x=x, y=y)
    assert field.squares == expected, name


@pytest.mark.parametrize(
    'width, height, x, y, expected',
    [
        (2, 3, 0, 0, 0),
        (2, 3, 1, 0, 1),
        (2, 3, 0, 1, 2),
        (2, 3, 1, 1, 3),
    ],
)
def test_flat(width, height, x, y, expected):
    field = Field(
        game_id='1',
        num_mines=1,
        width=width,
        height=height,
        squares=[],
    )
    assert field.flatten_index(x=x, y=y) == expected


@pytest.mark.parametrize(
    ('name', 'x', 'y', 'squares', 'expected'),
    [
        ('地雷にフラグを立てられる', 2, 0,
         ['_0', '_1', '_X',
          '_0', '_1', '_1',
          '_0', '_0', '_0'],
         ['_0', '_1', 'FX',
          '_0', '_1', '_1',
          '_0', '_0', '_0']),
        ('地雷じゃなくてもフラグを立てられる', 1, 0,
         ['_0', '_1', '_X',
          '_0', '_0', '_1',
          '_0', '_0', '_0'],
         ['_0', 'F1', '_X',
          '_0', '_0', '_1',
          '_0', '_0', '_0']),
    ],
)
def test_flag(name: str, x: int, y: int, squares: list[str], expected: list[str]):
    field = Field(
        game_id='1',
        num_mines=1,
        width=3,
        height=3,
        squares=squares,
    )
    field.flag(x=x, y=y)
    assert field.squares == expected, name
