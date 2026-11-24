import os.path
import os
import sys
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


def valid_triangles(data: str) -> int:
    valid = 0
    regexp = re.compile(r"\d+")
    for line in data.splitlines():
        a, b, c = map(int, re.findall(regexp, line))
        if all((a + b > c,
                a + c > b,
                b + c > a)):
            valid += 1
    return valid


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    p1 = valid_triangles(data)
    print("Part 1:", p1)

    p2 = 0
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
