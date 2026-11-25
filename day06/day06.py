import os.path
import os
import sys
from collections import Counter

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


def error_correction(data: str) -> tuple[str, str]:
    p1, p2 = "", ""
    signal = [list(line) for line in data.splitlines()]
    for column in zip(*signal):  # transpose
        counter = Counter(column)
        mc = counter.most_common()
        p1 += mc[0][0]
        p2 += mc[-1][0]
    return p1, p2


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    p1, p2 = error_correction(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
