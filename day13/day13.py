import os.path
import os
import sys
from heapq import heapify, heappop, heappush

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Pos = tuple[int, int]  # (y,x) y downwards
type Grid = dict[Pos, int]  # 0 = open, 1 = wall
type Item = tuple[int, int, Pos]  # (prio,steps,pos)


def shortest_path(magic_number: int, dest_y: int, dest_x: int, part2: bool = False) -> int:
    pos_start = (1, 1)
    grid: Grid = {pos_start: 0}  # start in waiting area at (1,1)
    shortest_paths: dict[Pos, int] = {pos_start: 0}
    done: set[Pos] = set()
    init: Item = (0, 0, pos_start)
    q: list[Item] = [init]
    heapify(q)

    k = 0
    while q:
        k += 1
        prio, steps, pos = heappop(q)

        if pos in done:
            continue
        done.add(pos)

        if part2:
            if steps == 50:
                continue
        else:
            if pos == (dest_y, dest_x):
                print(f"k = {k}")
                return steps

        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_y, new_x = pos[0]+dy, pos[1]+dx
            if new_y < 0 or new_x < 0:
                continue

            new_pos = (new_y, new_x)
            if new_pos not in grid:
                determine_open_or_wall(grid, new_y, new_x, magic_number)
            if grid[new_pos] == 1:  # wall
                continue

            if new_pos in done:
                continue
            new_steps = steps + 1
            if new_pos in shortest_paths and shortest_paths[new_pos] <= new_steps:
                continue
            shortest_paths[new_pos] = new_steps

            heuristic = abs(dest_y - new_y) + abs(dest_x - new_x)
            new_prio = new_steps + heuristic
            heappush(q, (new_prio, new_steps, new_pos))

    # part 2
    return len(shortest_paths)


def determine_open_or_wall(grid: Grid, y: int, x: int, magic_number: int) -> None:
    z = x*x + 3*x + 2*x*y + y + y*y + magic_number
    bit_count = z.bit_count()
    grid[(y, x)] = 0 if bit_count % 2 == 0 else 1


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    MAGIC_NUMBER = int(data)

    p1 = shortest_path(MAGIC_NUMBER, 39, 31)
    print("Part 1:", p1)

    p2 = shortest_path(MAGIC_NUMBER, 0, 0, True)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
