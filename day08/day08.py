import os.path
import os
import sys
import numpy as np
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


def print_screen(screen: np.ndarray) -> None:
    for row in screen:
        for i in row:
            print("█" if i == 1 else " ", end="")
        print()


def simulate_screen(instr: str, screen: np.ndarray) -> None:
    regexp = re.compile(r"\d+")
    for line in instr.splitlines():
        a, b = map(int, regexp.findall(line))
        if line.startswith("rect"):
            screen[0:b, 0:a] = 1
        elif line.startswith("rotate row"):
            screen[a] = np.roll(screen[a], b)
        elif line.startswith("rotate column"):
            screen[:, a] = np.roll(screen[:, a], b)
        else:
            raise ValueError("Opcode unknown.")


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    screen = np.zeros((6, 50), dtype=np.int8)
    simulate_screen(data, screen)

    p1 = np.sum(screen)
    print("Part 1:", p1)

    print("Part 2:")
    print_screen(screen)


if __name__ == "__main__":
    main()
