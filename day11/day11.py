import os.path
import os
import sys
import re
from heapq import heapify, heappop, heappush
from itertools import combinations, product

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Generator = int
type Chip = int
type Generators = frozenset[Generator]
type Chips = frozenset[Chip]
type Floor = tuple[Generators, Chips]
type Facility = tuple[Floor, ...]  # floors 1,2,3,4


def create_facility(data: str, is_part_2: bool = False) -> Facility:
    # each element gets an id, eg. hydrogen = 1
    # hydrogen chip and hydrogen generator would both be labeled "1"
    # we distinguish through different tuples
    element_to_id: dict[str, int] = {}
    id = 3
    facility = []
    chip_ids = [1, 2] if is_part_2 else []
    generator_ids = [1, 2] if is_part_2 else []

    for floor_str in data.splitlines():
        chips = re.findall(r"([a-z]+)-compatible microchip", floor_str)
        generators = re.findall(r"([a-z]+) generator", floor_str)
        for chip_element in chips:
            if chip_element not in element_to_id:
                element_to_id[chip_element] = id
                id += 1
            chip_ids.append(element_to_id[chip_element])
        for generator_element in generators:
            if generator_element not in element_to_id:
                element_to_id[generator_element] = id
                id += 1
            generator_ids.append(element_to_id[generator_element])

        floor = (frozenset(generator_ids), frozenset(chip_ids))
        facility.append(floor)
        chip_ids = []
        generator_ids = []

    return tuple(facility)


type FloorNumber = int
type State = tuple[FloorNumber, Facility]
type Item = tuple[int, int, int, State]


def shortest_path(facility: Facility) -> int:
    num_objects = sum(len(g)+len(c) for g, c in facility)
    state_init: State = (0, facility)  # first floor and given facility
    shortest_paths: dict[State, int] = {state_init: 0}  # (state: steps)
    seen: set[State] = set()
    init: Item = (0, 0, 0, state_init)  # (prio,steps,count,state)
    q: list[Item] = [init]
    heapify(q)

    i = 1
    k = 0
    while q:
        k += 1
        prio, steps, count, state = heappop(q)
        # curr_floor zero indexing: curr_floor = 0 -> first floor
        # because curr_facility[0] = first floor
        floor_number, curr_facility = state

        if state in seen:
            # print("YO")
            continue
        seen.add(state)

        if floor_number == 3 and sum(map(len, curr_facility[3])) == num_objects:
            # are all objects on floor 4?
            print(f"k = {k}")
            return steps

        candidates: list[State] = []
        for inc in (1, -1):
            new_floor_number = floor_number + inc
            if new_floor_number < 0 or new_floor_number > 3:
                continue

            chips_on_curr_floor = curr_facility[floor_number][1]
            chips_on_new_floor = curr_facility[new_floor_number][1]
            generators_on_curr_floor = curr_facility[floor_number][0]
            generators_on_new_floor = curr_facility[new_floor_number][0]

            # pick one or two chips from current floor
            for amount in (1, 2):
                for chips_taken in combinations(chips_on_curr_floor, amount):
                    chips_taken = set(chips_taken)

                    new_chips_on_curr_floor = chips_on_curr_floor - chips_taken
                    new_chips_on_new_floor = chips_on_new_floor | chips_taken

                    this_floor = (generators_on_curr_floor, new_chips_on_curr_floor)
                    new_floor = (generators_on_new_floor, new_chips_on_new_floor)
                    (low, low_floor), (high, high_floor) = sorted(
                        ((floor_number, this_floor), (new_floor_number, new_floor)))
                    new_facility = curr_facility[:low] + (low_floor,) + (high_floor,) + curr_facility[high+1:]
                    new_state = (new_floor_number, new_facility)
                    candidates.append(new_state)

            # pick one or two generators from current floor
            for amount in (1, 2):
                for generators_taken in combinations(generators_on_curr_floor, amount):
                    generators_taken = set(generators_taken)

                    new_generators_on_curr_floor = generators_on_curr_floor - generators_taken
                    new_generators_on_new_floor = generators_on_new_floor | generators_taken

                    this_floor = (new_generators_on_curr_floor, chips_on_curr_floor)
                    new_floor = (new_generators_on_new_floor, chips_on_new_floor)
                    (low, low_floor), (high, high_floor) = sorted(
                        ((floor_number, this_floor), (new_floor_number, new_floor)))
                    new_facility = curr_facility[:low] + (low_floor,) + (high_floor,) + curr_facility[high+1:]
                    new_state = (new_floor_number, new_facility)
                    candidates.append(new_state)

            # pick exactly one chip and one generator
            if len(chips_on_curr_floor) > 0 and len(generators_on_curr_floor) > 0:
                for chip_taken, generator_taken in product(chips_on_curr_floor, generators_on_curr_floor):

                    new_chips_on_curr_floor = chips_on_curr_floor - {chip_taken}
                    new_chips_on_new_floor = chips_on_new_floor | {chip_taken}
                    new_generators_on_curr_floor = generators_on_curr_floor - {generator_taken}
                    new_generators_on_new_floor = generators_on_new_floor | {generator_taken}

                    this_floor = (new_generators_on_curr_floor, new_chips_on_curr_floor)
                    new_floor = (new_generators_on_new_floor, new_chips_on_new_floor)
                    (low, low_floor), (high, high_floor) = sorted(
                        ((floor_number, this_floor), (new_floor_number, new_floor)))
                    new_facility = curr_facility[:low] + (low_floor,) + (high_floor,) + curr_facility[high+1:]
                    new_state = (new_floor_number, new_facility)
                    candidates.append(new_state)

        for new_state in candidates:
            new_floor_number, new_facility = new_state

            # safe on current floor?
            if len(new_facility[floor_number][0]) != 0 and not new_facility[floor_number][1].issubset(new_facility[floor_number][0]):
                continue

            # safe on new floor?
            if len(new_facility[new_floor_number][0]) != 0 and not new_facility[new_floor_number][1].issubset(new_facility[new_floor_number][0]):
                continue

            new_steps = steps + 1
            if new_state in shortest_paths and shortest_paths[new_state] <= new_steps:
                continue
            shortest_paths[new_state] = new_steps

            # A*: penalize bad setups
            # heuristic = new_floor_number + sum(sum(map(len, floor))//2 * (3-i) for i, floor in enumerate(new_facility))
            new_prio = new_steps  # + heuristic
            new_count = i
            i += 1
            new_item = (new_prio, new_steps, new_count, new_state)
            heappush(q, new_item)

    return 0


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    facility = create_facility(data)

    p1 = shortest_path(facility)
    print("Part 1:", p1)

    facility2 = create_facility(data, True)

    p2 = shortest_path(facility2)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
