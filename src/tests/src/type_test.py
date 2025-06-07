import datetime

from pybackup.type import parse_increments, Increment


def test_parse_increments():
    input_text = """
          Time                 Size         Cumulative size 
------------------------ ----------------- -----------------
Sat Jun  7 07:27:44 2025          91 bytes         177 bytes
Sat Jun  7 07:37:38 2025          86 bytes          86 bytes  (current mirror)
"""

    increments = parse_increments(input_text)
    assert (
        Increment(
            time=datetime.datetime(2025, 6, 7, 7, 27, 44), size=91, cumulative_size=177
        )
        == increments[0]
    )
    assert (
        Increment(
            time=datetime.datetime(2025, 6, 7, 7, 37, 38), size=86, cumulative_size=86
        )
        == increments[1]
    )
