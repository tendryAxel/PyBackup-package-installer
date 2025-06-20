import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

from pybackup.utils import TemporarySetLocal


# Todo: better handling for size
# Todo: update to python 3.11 to use the new StrEnum
class SizeUnit(str, Enum):
    bytes = "bytes"
    KB = "KB"
    MB = "MB"
    GB = "GB"
    TB = "TB"


@dataclass
class Size:
    value: float
    unit: SizeUnit

    def __init__(self, value: float | str, unit: SizeUnit = SizeUnit.bytes):
        self.value = value if isinstance(value, float) else float(value)
        self.unit = unit

    def __eq__(self, other):
        if not isinstance(other, Size):
            return False
        return self.to_bytes() == other.to_bytes()

    def to_bytes(self) -> float:
        """Convert the size to bytes for comparison"""
        multipliers = {
            SizeUnit.bytes: 1,
            SizeUnit.KB: 1024,
            SizeUnit.MB: 1024**2,
            SizeUnit.GB: 1024**3,
            SizeUnit.TB: 1024**4,
        }
        return self.value * multipliers[self.unit]


class Increment:
    def __init__(self, time: datetime, size: Size, cumulative_size: Size):
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
            (
                r"(\w{3} \w{3}\s+\d+ \d{2}:\d{2}:\d{2} \d{4})\s+"  # Date
                r"(\d+)\s*(bytes|B|KB|MB|GB|TB|kilobytes|megabytes|gigabytes|terabytes)?\s+"  # Size
                r"(\d+)\s*(bytes|B|KB|MB|GB|TB|kilobytes|megabytes|gigabytes|terabytes)?"  # Cumulative size
            ),
            line,
            re.IGNORECASE,
        )
        if match:
            time_str, size_str, size_unit, cum_size_str, cum_size_unit = match.groups()
            size_unit = SizeUnit[size_unit] if size_unit else SizeUnit.bytes
            cum_size_unit = SizeUnit[cum_size_unit] if cum_size_unit else SizeUnit.bytes
            with TemporarySetLocal():
                dt = datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y")
            increments.append(
                Increment(
                    dt, Size(size_str, size_unit), Size(cum_size_str, cum_size_unit)
                )
            )

    return increments
