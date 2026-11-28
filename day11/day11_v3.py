import os.path
import os
import sys
import re
from math import ceil
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
type Item = tuple[int, int, int, tuple[FloorNumber, Facility]]
type NumberOfPairs = int
type FloorState = tuple[Generators, Chips, NumberOfPairs]
type State = tuple[FloorNumber, tuple[FloorState, ...]]


def shortest_path(facility: Facility) -> int:
    num_objects = sum(len(g)+len(c) for g, c in facility)
    pairs = tuple(generators.intersection(chips) for generators, chips in facility)
    floorstates = tuple((generators-pairs, chips-pairs, len(pairs))
                        for (generators, chips), pairs in zip(facility, pairs))
    state_init: State = (0, floorstates)  # first floor and given facility
    shortest_paths: dict[State, int] = {state_init: 0}  # (state: steps)
    done: set[State] = set()
    init: Item = (0, 0, 0, (0, facility))  # (prio,steps,count,(floor_number,facility))
    q: list[Item] = [init]
    heapify(q)

    i = 1
    k = 0
    while q:
        k += 1
        prio, steps, count, (floor_number, curr_facility) = heappop(q)
        # curr_floor zero indexing: curr_floor = 0 -> first floor
        # because curr_facility[0] = first floor

        pairs = tuple(generators.intersection(chips) for generators, chips in curr_facility)
        floorstates = tuple((generators-pairs, chips-pairs, len(pairs))
                            for (generators, chips), pairs in zip(curr_facility, pairs))
        state = (floor_number, floorstates)

        if state in done:
            # print("YO")
            continue
        done.add(state)

        if floor_number == 3 and sum(map(len, curr_facility[3])) == num_objects:
            # are all objects on floor 4?
            print(f"k = {k}")
            return steps

        chips_on_curr_floor = curr_facility[floor_number][1]
        generators_on_curr_floor = curr_facility[floor_number][0]

        # going up
        changes_up: list[tuple[FloorNumber, Facility]] = []
        new_floor_number = floor_number + 1
        if new_floor_number <= 3:

            # first, try to move two items upstairs

            # pick two chips from current floor
            for chips_taken in combinations(chips_on_curr_floor, 2):
                new_facility = is_safe(curr_facility, set(), set(chips_taken), floor_number, new_floor_number)
                if new_facility is not None:
                    changes_up.append((new_floor_number, new_facility))

            # pick two generators from current floor
            for generators_taken in combinations(generators_on_curr_floor, 2):
                new_facility = is_safe(curr_facility, set(generators_taken), set(), floor_number, new_floor_number)
                if new_facility is not None:
                    changes_up.append((new_floor_number, new_facility))

            # pick exactly one chip and one generator
            pairs_on_curr_floor = generators_on_curr_floor.intersection(chips_on_curr_floor)
            if len(pairs_on_curr_floor) > 0:
                pair_taken = next(p for p in pairs_on_curr_floor)
                new_facility = is_safe(curr_facility, {pair_taken}, {pair_taken}, floor_number, new_floor_number)
                if new_facility is not None:
                    changes_up.append((new_floor_number, new_facility))

            # dont bother with one item, if we can move two
            # "kind of important" optimization
            # https://www.reddit.com/r/adventofcode/comments/5hoia9/comment/db1v1ws/
            if len(changes_up) == 0:
                # pick one chip from current floor
                for chip_taken in chips_on_curr_floor:
                    new_facility = is_safe(curr_facility, set(), {chip_taken}, floor_number, new_floor_number)
                    if new_facility is not None:
                        changes_up.append((new_floor_number, new_facility))

                # pick one generator from current floor
                for generator_taken in generators_on_curr_floor:
                    new_facility = is_safe(curr_facility, {generator_taken}, set(), floor_number, new_floor_number)
                    if new_facility is not None:
                        changes_up.append((new_floor_number, new_facility))

        # going down
        changes_down: list[tuple[FloorNumber, Facility]] = []
        new_floor_number = floor_number - 1
        if new_floor_number >= 0:

            # first, try to move one item down

            # pick one chip from current floor
            for chip_taken in chips_on_curr_floor:
                new_facility = is_safe(curr_facility, set(), {chip_taken}, floor_number, new_floor_number)
                if new_facility is not None:
                    changes_down.append((new_floor_number, new_facility))

            # pick one generator from current floor
            for generator_taken in generators_on_curr_floor:
                new_facility = is_safe(curr_facility, {generator_taken}, set(), floor_number, new_floor_number)
                if new_facility is not None:
                    changes_down.append((new_floor_number, new_facility))

            # dont bother with two items, if we can move only one
            # "kind of important" optimization
            # https://www.reddit.com/r/adventofcode/comments/5hoia9/comment/db1v1ws/
            if len(changes_down) == 0:
                # pick two chips from current floor
                for chips_taken in combinations(chips_on_curr_floor, 2):
                    new_facility = is_safe(curr_facility, set(), set(chips_taken), floor_number, new_floor_number)
                    if new_facility is not None:
                        changes_down.append((new_floor_number, new_facility))

                # pick two generators from current floor
                for generators_taken in combinations(generators_on_curr_floor, 2):
                    new_facility = is_safe(curr_facility, set(generators_taken), set(), floor_number, new_floor_number)
                    if new_facility is not None:
                        changes_down.append((new_floor_number, new_facility))

                # pick exactly one chip and one generator
                if len(chips_on_curr_floor) > 0 and len(generators_on_curr_floor) > 0:
                    for chip_taken, generator_taken in product(chips_on_curr_floor, generators_on_curr_floor):
                        if chip_taken != generator_taken:
                            continue
                        new_facility = is_safe(curr_facility, {generator_taken}, {
                            chip_taken}, floor_number, new_floor_number)
                        if new_facility is not None:
                            changes_down.append((new_floor_number, new_facility))

        for new_floor_number, new_facility in changes_up+changes_down:

            new_pairs = tuple(generators.intersection(chips) for generators, chips in new_facility)
            new_floorstates = tuple((generators-pairs, chips-pairs, len(pairs))
                                    for (generators, chips), pairs in zip(new_facility, new_pairs))
            new_state = (new_floor_number, new_floorstates)
            new_steps = steps + 1

            if new_state in done:
                continue

            if new_state in shortest_paths and shortest_paths[new_state] <= new_steps:
                continue
            shortest_paths[new_state] = new_steps

            # A*: penalize bad setups
            # heu = 0
            # carry = 0
            # num_obj = [len(floor[0]) + len(floor[1]) for floor in new_facility]
            # first_non_zero = next(i for i, num in enumerate(num_obj) if num != 0)
            # if (diff := new_floor_number-first_non_zero) != 0:
            #     # must take the elevator diff times down
            #     heu += diff
            #     num_obj[first_non_zero] += 1  # must take at least 1 item with me
            #     num_obj[new_floor_number] -= 1  # must have at least 1 item, because i am here
            # for n in num_obj[first_non_zero:3]:
            #     n += carry
            #     heu += 1 if n <= 2 else 2*n-3
            #     carry = n

            new_prio = new_steps
            new_count = i
            i += 1
            new_item = (new_prio, new_steps, new_count, (new_floor_number, new_facility))
            heappush(q, new_item)

    return 0


def is_safe(facility: Facility, generators_taken: set[Generator], chips_taken: set[Chip], floor_number: FloorNumber, new_floor_number: FloorNumber) -> Facility | None:
    chips_on_curr_floor = facility[floor_number][1]
    generators_on_curr_floor = facility[floor_number][0]
    chips_on_new_floor = facility[new_floor_number][1]
    generators_on_new_floor = facility[new_floor_number][0]

    new_chips_on_curr_floor = chips_on_curr_floor - chips_taken
    new_chips_on_new_floor = chips_on_new_floor | chips_taken
    new_generators_on_curr_floor = generators_on_curr_floor - generators_taken
    new_generators_on_new_floor = generators_on_new_floor | generators_taken

    # safe on current floor?
    if len(new_generators_on_curr_floor) != 0 and not new_chips_on_curr_floor.issubset(new_generators_on_curr_floor):
        return None

    # safe on new floor?
    if len(new_generators_on_new_floor) != 0 and not new_chips_on_new_floor.issubset(new_generators_on_new_floor):
        return None

    this_floor = (new_generators_on_curr_floor, new_chips_on_curr_floor)
    new_floor = (new_generators_on_new_floor, new_chips_on_new_floor)
    if floor_number - new_floor_number == 1:
        new_facility = facility[:new_floor_number] + \
            (new_floor,) + (this_floor,) + facility[floor_number+1:]
    else:
        new_facility = facility[:floor_number] + \
            (this_floor,) + (new_floor,) + facility[new_floor_number+1:]

    return new_facility


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
