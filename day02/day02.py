import os.path
import os
import sys
from collections.abc import Callable

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


POS_TO_BUTTON = {
    # (x,y): "button"
    (-1, 1): "1",
    (0, 1): "2",
    (1, 1): "3",
    (-1, 0): "4",
    (0, 0): "5",
    (1, 0): "6",
    (-1, -1): "7",
    (0, -1): "8",
    (1, -1): "9",
}

POS_TO_BUTTON2 = {
    # (x,y): "button"
    (-1, 1): "2",
    (0, 1): "3",
    (1, 1): "4",
    (-1, 0): "6",
    (0, 0): "7",
    (1, 0): "8",
    (-1, -1): "A",
    (0, -1): "B",
    (1, -1): "C",
    (0, 2): "1",
    (-2, 0): "5",
    (2, 0): "9",
    (0, -2): "D"
}


def bathroom_code(data: str, x_start: int, y_start: int, is_in_bounds: Callable[[int, int], bool], layout: dict[tuple[int, int], str]) -> str:
    x, y = x_start, y_start
    code = ""
    for line in data.splitlines():
        for letter in line:
            new_x, new_y = x, y
            match letter:
                case "U":
                    new_y += 1
                case "D":
                    new_y -= 1
                case "L":
                    new_x -= 1
                case "R":
                    new_x += 1
                case _:
                    raise ValueError(f"Direction {letter} unknown.")
            if is_in_bounds(new_x, new_y):
                x = new_x
                y = new_y
        code += layout[(x, y)]
    return code


def is_in_bounds_p1(x: int, y: int) -> bool:
    return abs(x) <= 1 and abs(y) <= 1


def is_in_bounds_p2(x: int, y: int) -> bool:
    return abs(x) + abs(y) <= 2


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    p1 = bathroom_code(data, 0, 0, is_in_bounds_p1, POS_TO_BUTTON)
    print("Part 1:", p1)

    p2 = bathroom_code(data, -2, 0, is_in_bounds_p2, POS_TO_BUTTON2)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
