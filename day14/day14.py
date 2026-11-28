import os.path
import os
import sys
from collections import Counter
import hashlib
import re
from typing import Generator

# remarks
# - generate every hash once
# - work with "rolling" sets (counter) for fivelets


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


def generate_keys(salt: str, stretch_amount: int = 1) -> int:

    fivelets: dict[int, Counter] = {0: Counter()}
    index_to_hash: dict[int, str] = {}

    def compute_hash(index: int) -> None:
        hash_hex = salt + str(index)
        for _ in range(stretch_amount):
            hash_hex = hashlib.md5(hash_hex.encode()).hexdigest()
        index_to_hash[index] = hash_hex
        

    def gen_fivelets() -> Generator[tuple[int, Counter], int, None]:
        regexp5 = re.compile(r"(\w)\1{4}")
        stop = 0
        i = 0
        last_index = 0
        last_counter = Counter()
        while True:
            while i <= stop:
                if i not in index_to_hash:
                    compute_hash(i)
                hash_hex = index_to_hash[i]
                found = regexp5.findall(hash_hex)
                if found:
                    new_counter = last_counter.copy()
                    new_counter.update(found)
                    fivelets[i] = new_counter
                    last_counter = new_counter
                    last_index = i
                i += 1
            stop = yield (last_index, last_counter)

    regexp3 = re.compile(r"(\w)\1{2}")
    gen5 = gen_fivelets()
    next(gen5)
    keys = []
    i = 0
    while len(keys) < 64:
        if i not in index_to_hash:
            compute_hash(i)
        hash_hex = index_to_hash[i]
        found = regexp3.search(hash_hex)
        if found:
            index_high, counter_high = gen5.send(i+1000)
            index_low = max([k for k in fivelets.keys() if k <= i])
            counter_low = fivelets[index_low]
            hex_digit = found.group(1)
            diff = counter_high[hex_digit] - counter_low[hex_digit]
            if diff > 0:
                keys.append(i)
                # print(f"match #{len(keys)} at index {i}")
        i += 1
    return keys[-1]


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    SALT = data

    p1 = generate_keys(SALT)
    print("Part 1:", p1)

    p2 = generate_keys(SALT, 2017)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
