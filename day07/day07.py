import os.path
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


def tls_support(data: str) -> int:
    res = 0

    for line in data.splitlines():
        n = len(line)
        abba_allowed = True
        valid = False
        i = 0
        while i < n-3:
            if line[i+3] in "[]":
                abba_allowed = not abba_allowed
                i += 4
                continue
            a, b, c, d = line[i:i+4]
            if a == d and b == c and a != b:
                if not abba_allowed:
                    valid = False
                    break
                else:
                    valid = True
            i += 1
        if valid:
            res += 1

    return res


def ssl_support(data: str) -> int:
    res = 0

    for line in data.splitlines():
        n = len(line)
        aba_seen = set()
        bab_seen = set()
        checking_for_aba = True
        i = 0
        while i < n-2:
            if line[i+2] in "[]":
                checking_for_aba = not checking_for_aba
                i += 3
                continue
            a, b, c = line[i:i+3]
            if a == c and a != b:
                reverse = b+a+b
                if checking_for_aba:
                    if reverse in bab_seen:
                        res += 1
                        break
                    aba_seen.add(line[i:i+3])
                else:
                    if reverse in aba_seen:
                        res += 1
                        break
                    bab_seen.add(line[i:i+3])
            i += 1

    return res


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    p1 = tls_support(data)
    print("Part 1:", p1)

    p2 = ssl_support(data)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
