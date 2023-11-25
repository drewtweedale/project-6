"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""
import arrow
from mongo_file import get_brev, insert_brev
import nose    # Testing framework
import logging


logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

test_brevet = (200,
              "2021-01-01T00:00", 
                    [{"km": 120, "open": '2021-01-01T03:32', "close": '2021-01-01T08:00'},
                    {"km": 150, "open": '2021-01-01T04:25', "close": '2021-01-01T10:00'},
                    {"km": 160, "open": '2021-01-01T04:42', "close": '2021-01-01T10:40'}])


def test_get_brev():
    # Test fetching a certain brevet
    out = get_brev()
    assert out


def test_insert_brev():
    # Test insertion of brevet.
    out = insert_brev(200, "2021-01-01T00:00", {"km": 120, "open": '2021-01-01T03:32', "close": '2021-01-01T08:00'})
    assert out