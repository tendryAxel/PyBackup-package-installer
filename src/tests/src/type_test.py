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


def test_parse_increments_with_equality():
    text = """
          Time                 Size         Cumulative size 
------------------------ ----------------- -----------------
Sat Jun 14 09:14:26 2025          97 bytes           19.0 MB
Sat Jun 14 09:47:12 2025         104 bytes           19.0 MB
Sat Jun 14 09:48:09 2025           0 bytes           19.0 MB
Sat Jun 14 09:49:35 2025           79.3 KB           19.0 MB
Sat Jun 14 09:53:44 2025           0 bytes           18.9 MB
Fri Jun 20 21:29:05 2025           51.4 KB           18.9 MB
Fri Jun 20 21:29:23 2025           0 bytes           18.9 MB
Fri Jun 20 21:30:58 2025           18.9 MB           18.9 MB
Fri Jun 20 21:31:14 2025          92 bytes          92 bytes  (current mirror)
"""
    increments = parse_increments(text)

    expected_increments = [
        Increment(
            time=datetime.datetime(2025, 6, 14, 9, 14, 26),
            size=Size(97, SizeUnit.bytes),
            cumulative_size=Size(19.0, SizeUnit.MB),
        ),
        Increment(
            time=datetime.datetime(2025, 6, 14, 9, 47, 12),
            size=Size(104, SizeUnit.bytes),
            cumulative_size=Size(19.0, SizeUnit.MB),
        ),
        Increment(
            time=datetime.datetime(2025, 6, 14, 9, 48, 9),
            size=Size(0, SizeUnit.bytes),
            cumulative_size=Size(19.0, SizeUnit.MB),
        ),
        Increment(
            time=datetime.datetime(2025, 6, 14, 9, 49, 35),
            size=Size(79.3, SizeUnit.KB),
            cumulative_size=Size(19.0, SizeUnit.MB),
        ),
        Increment(
            time=datetime.datetime(2025, 6, 14, 9, 53, 44),
            size=Size(0, SizeUnit.bytes),
            cumulative_size=Size(18.9, SizeUnit.MB),
        ),
        Increment(
            time=datetime.datetime(2025, 6, 20, 21, 29, 5),
            size=Size(51.4, SizeUnit.KB),
            cumulative_size=Size(18.9, SizeUnit.MB),
        ),
        Increment(
            time=datetime.datetime(2025, 6, 20, 21, 29, 23),
            size=Size(0, SizeUnit.bytes),
            cumulative_size=Size(18.9, SizeUnit.MB),
        ),
        Increment(
            time=datetime.datetime(2025, 6, 20, 21, 30, 58),
            size=Size(18.9, SizeUnit.MB),
            cumulative_size=Size(18.9, SizeUnit.MB),
        ),
        Increment(
            time=datetime.datetime(2025, 6, 20, 21, 31, 14),
            size=Size(92, SizeUnit.bytes),
            cumulative_size=Size(92, SizeUnit.bytes),
        ),
    ]

    assert len(increments) == len(expected_increments)

    for actual, expected in zip(increments, expected_increments):
        assert actual == expected, f"Échec de comparaison pour {expected}"
