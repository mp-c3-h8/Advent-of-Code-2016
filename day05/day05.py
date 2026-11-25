import os.path
import os
import sys
from hashlib import md5

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


def crack_pwd(door_id: str) -> tuple[str, str]:
    pwd = ""
    pwd2 = [""] * 8
    index = 0
    while len(pwd) < 8 or "" in pwd2:
        for _ in range(10_000_000):
            to_hash = door_id + str(index)
            hash_hex = md5(to_hash.encode()).hexdigest()
            index += 1

            if not hash_hex.startswith("00000"):
                continue

            if len(pwd) < 8:
                pwd += hash_hex[5]
            pos = int(hash_hex[5], 16)
            if pos < 8 and pwd2[pos] == "":
                pwd2[pos] = hash_hex[6]
                print("Found one!: ", pwd2)
            break
        else:
            raise ValueError("Max iterations reached.")
    pwd2_string = "".join(pwd2)
    return pwd, pwd2_string


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    p1, p2 = crack_pwd(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
