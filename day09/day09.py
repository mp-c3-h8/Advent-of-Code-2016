import os.path
import os
import sys
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

REGEXP = re.compile(r"\((\d+)x(\d+)\)")


def decompress(data: str) -> int:
    global REGEXP
    length = 0
    index = 0
    if matches := REGEXP.finditer(data):
        for match in matches:
            start, end = match.start(), match.end()
            if start < index:
                continue
            length += start - index
            x, y = map(int, match.groups())
            length += x*y
            index = end + x
    # rest or all if no matches
    length += len(data) - index
    return length


def decompress_recursive(data: str) -> int:
    global REGEXP
    if match := REGEXP.search(data):
        start, end = match.start(), match.end()
        x, y = map(int, match.groups())  # eg (3x5) -> x=3, y=5
        return start + y * decompress_recursive(data[end:end+x]) + decompress_recursive(data[end+x:])
    else:
        return len(data)


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    p1 = decompress(data)
    print("Part 1:", p1)

    p2 = decompress_recursive(data)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
