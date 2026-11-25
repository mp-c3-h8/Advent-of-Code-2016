import os.path
import os
import sys
import re
from collections import Counter

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


def real_rooms(data: str) -> tuple[int, int]:
    p1, p2 = 0, 0
    regexp = re.compile(r"([a-z-]+)(\d+)\[([a-z]+)\]")
    for line in data.splitlines():
        found = regexp.match(line)
        if not found:
            raise ValueError("Invalid pattern.")
        name, sector_id, checksum = found.groups()
        sector_id = int(sector_id)
        counter = Counter(name.replace("-", ""))
        most_common = counter.most_common()
        most_common.sort(key=lambda x: (-x[1], x[0]))
        real_checksum = "".join(letter for letter, count in most_common[:5])

        if real_checksum != checksum:
            continue

        p1 += sector_id
        real_name = ""
        for c in name:
            if c == "-":
                real_name += " "
                continue
            # ascii: a-z = 97-122, period = 26
            dec = ord(c)
            dec += sector_id % 26  # skip periods
            dec = dec if dec <= 122 else dec-26
            real_name += chr(dec)

        # assuming "pole" is  part of the name
        if real_name.find("pole") != -1:
            print(real_name)
            p2 = sector_id
    return p1, p2


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    p1, p2 = real_rooms(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
