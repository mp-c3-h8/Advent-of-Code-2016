import os.path
import os
import sys
import re
from collections import deque

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Bots = list[Bot]
type Outputs = list[Output]


class Bot:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.values: list[int] = []
        self.low_to: Bot | Output = self
        self.high_to: Bot | Output = self


class Output:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.values: list[int] = []


def create_bots_and_outputs(data: str) -> tuple[Bots, Outputs]:
    bots: dict[int, Bot] = {}
    outputs: dict[int, Output] = {}
    name_to_class = {"output": Output, "bot": Bot}
    name_to_dict = {"output": outputs, "bot": bots}
    for line in data.splitlines():
        if line.startswith("value"):
            value, bot_id = map(int, re.findall(r"\d+", line))
            if bot_id not in bots:
                bots[bot_id] = Bot(bot_id)
            bots[bot_id].values.append(value)
        else:
            found = re.finditer(r"([a-z]+) (\d+)", line)
            if not found:
                raise ValueError
            bot, low, high = found
            bot_id = int(bot.group(2))
            if bot_id not in bots:
                bots[bot_id] = Bot(bot_id)

            low_name, low_id = low.groups()
            high_name, high_id = high.groups()
            low_id, high_id = int(low_id), int(high_id)

            if low_id not in name_to_dict[low_name]:
                name_to_dict[low_name][low_id] = name_to_class[low_name](low_id)
            bots[bot_id].low_to = name_to_dict[low_name][low_id]

            if high_id not in name_to_dict[high_name]:
                name_to_dict[high_name][high_id] = name_to_class[high_name](high_id)
            bots[bot_id].high_to = name_to_dict[high_name][high_id]

    return list(bots.values()), list(outputs.values())


def simulate(bots: Bots, low_to_find, high_to_find) -> int | None:
    # simulate until every bot had its turn
    # find the bot that compares low_to_find with high_to_find
    two_chips = [bot for bot in bots if len(bot.values) == 2]
    if len(two_chips) == 0:
        raise ValueError("No Bot with two chips found.")
    q = deque(two_chips)
    seen: set[Bot] = set()
    n = len(bots)
    bot_id = None
    while q and len(seen) < n:
        bot = q.popleft()

        if len(bot.values) > 2:
            raise ValueError(f"Bot {bot.id} carries {len(bot.values)} chips!")

        low, high = sorted(bot.values)

        if low == low_to_find and high == high_to_find:
            bot_id = bot.id

        entity_low, entity_high = bot.low_to, bot.high_to
        entity_low.values.append(low)
        entity_high.values.append(high)
        bot.values = []

        if isinstance(entity_low, Bot) and len(entity_low.values) >= 2:
            q.append(entity_low)

        if isinstance(entity_high, Bot) and len(entity_high.values) >= 2:
            q.append(entity_high)

        seen.add(bot)

    return bot_id


def part2(outputs: Outputs) -> int:
    res = 1
    for output in outputs:
        if output.id not in (0, 1, 2):
            continue
        if len(output.values) != 1:
            raise ValueError(f"More than one item in Output {output.id}")
        res *= output.values.pop()

    return res


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    bots, outputs = create_bots_and_outputs(data)

    p1 = simulate(bots, 17, 61)
    print("Part 1:", p1)

    p2 = part2(outputs)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
