import os.path
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Pos = complex  # x + j*y, y facing down
type Dir = complex  # direction N,S,W,E


def solve(data: str) -> tuple[int, int]:
    pos: Pos = 0
    d: Dir = -1j  # start facing north
    seen: set[Pos] = set()
    p1, p2 = 0, 0

    for instr in data.split(", "):
        letter = instr[0]
        steps = int(instr[1:])
        d = d*1j if letter == "R" else d*-1j

        if p2 == 0:
            # for p2 make single steps
            for _ in range(steps):
                pos += d
                if pos in seen:
                    p2 = int(abs(pos.real) + abs(pos.imag))
                seen.add(pos)
        else:
            # p2 has been found, make large steps
            pos += steps*d

    p1 = int(abs(pos.real) + abs(pos.imag))
    return p1, p2


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
