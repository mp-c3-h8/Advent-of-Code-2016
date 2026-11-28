import os.path
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


class Computer:
    def __init__(self, code: str) -> None:
        self.code: list[str] = code.splitlines()
        self.registers: dict[str, int] = {l: 0 for l in "abcd"}
        self.pointer = 0

    def reset(self) -> None:
        self.registers = {l: 0 for l in "abcd"}
        self.pointer = 0

    def run(self) -> None:
        n = len(self.code)
        while self.pointer < n and self.pointer >= 0:
            instr, *args = self.code[self.pointer].split(" ")
            match instr:
                case "cpy":
                    x, y = args
                    x = int(x) if x.isdigit() else self.registers[x]
                    self.registers[y] = x
                case "inc":
                    x, = args
                    self.registers[x] += 1
                case "dec":
                    x, = args
                    self.registers[x] -= 1
                case "jnz":
                    x, y = args
                    x = int(x) if x.isdigit() else self.registers[x]
                    if x != 0:
                        self.pointer += int(y)-1
                case _:
                    raise ValueError(f"Opcode {instr} unknown.")
            self.pointer += 1


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    computer = Computer(data)
    computer.run()
    p1 = computer.registers["a"]
    print("Part 1:", p1)

    computer.reset()
    computer.registers["c"] = 1
    computer.run()
    p2 = computer.registers["a"]
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
