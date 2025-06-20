import datetime
import locale


from pybackup.type import parse_increments, Increment, Size, SizeUnit
from tests.utils import get_random_locale, repeat_test


def test_parse_increments():
    input_text = """
          Time                 Size         Cumulative size 
------------------------ ----------------- -----------------
Sat Jun  7 07:27:44 2025          92 bytes         178 bytes
Sat Jun  7 07:27:45 2025          91 KB            177 KB
Sat Jun  7 07:37:38 2025          86 bytes          86 bytes  (current mirror)
"""

    increments = parse_increments(input_text)
    assert (
        Increment(
            time=datetime.datetime(2025, 6, 7, 7, 27, 44),
            size=Size(92),
            cumulative_size=Size(178),
        )
        == increments[0]
    )
    assert (
        Increment(
            time=datetime.datetime(2025, 6, 7, 7, 27, 45),
            size=Size(91, SizeUnit.KB),
            cumulative_size=Size(177, SizeUnit.KB),
        )
        == increments[1]
    )
    assert (
        Increment(
            time=datetime.datetime(2025, 6, 7, 7, 37, 38),
            size=Size(86),
            cumulative_size=Size(86),
        )
        == increments[2]
    )


@repeat_test(10)
def test_parse_increments_with_any_locale_work(iteration):
    locale.setlocale(locale.LC_TIME, get_random_locale())
    input_text = """
          Time                 Size         Cumulative size 
------------------------ ----------------- -----------------
Sat Jun  7 07:37:38 2025          86 bytes          86 bytes  (current mirror)
"""
    increments = parse_increments(input_text)
    assert (
        Increment(
            time=datetime.datetime(2025, 6, 7, 7, 37, 38),
            size=Size(86),
            cumulative_size=Size(86),
        )
        == increments[0]
    )
