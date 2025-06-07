import re
from datetime import datetime
from typing import List


class Increment:
    def __init__(self, time: datetime, size: int, cumulative_size: int):
        self.time = time
        self.size = size
        self.cumulative_size = cumulative_size

    def __repr__(self):
        return f"Increment(time={self.time}, size={self.size}, cumulative_size={self.cumulative_size})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Increment):
            return False
        return (
            self.size == other.size
            and self.cumulative_size == other.cumulative_size
            and self.time == other.time
        )


def parse_increments(text: str) -> List[Increment]:
    lines = text.strip().split("\n")
    increments = []

    for line in lines:
        if not line or line.startswith("-") or "Time" in line:
            continue  # Skip headers and separators

        # Match line using regex
        match = re.match(
            r"(\w{3} \w{3}\s+\d+ \d{2}:\d{2}:\d{2} \d{4})\s+(\d+) bytes\s+(\d+) bytes",
            line,
        )
        if match:
            time_str, size_str, cum_size_str = match.groups()
            dt = datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y")
            increments.append(Increment(dt, int(size_str), int(cum_size_str)))

    return increments
