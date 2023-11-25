"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""
import arrow
from acp_times import open_time, close_time
import nose    # Testing framework
import logging
from unittest.mock import MagicMock
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

def test_control_0km():
    # Test when the control distance is 0 km.
    assert open_time(0, 200, arrow.get("2021-01-01T00:00")).format("YYYY-MM-DDTHH:mm") == arrow.get("2021-01-01T00:00").format("YYYY-MM-DDTHH:mm")
    assert close_time(0, 200, arrow.get("2021-01-01T00:00")).format("YYYY-MM-DDTHH:mm") == arrow.get("2021-01-01T01:00").format("YYYY-MM-DDTHH:mm")

def test_control_eq_brev():
    # Test for if the control distance equals the brevet distance.
    assert open_time(200, 200, arrow.get("2021-01-01T00:00")).format("YYYY-MM-DDTHH:mm") == arrow.get("2021-01-01T05:53").format("YYYY-MM-DDTHH:mm")
    assert close_time(200, 200, arrow.get("2021-01-01T00:00")).format("YYYY-MM-DDTHH:mm") == arrow.get("2021-01-01T13:30").format("YYYY-MM-DDTHH:mm")

def test_change_y_m_d():
    # Test when the date changes (end of the year, month, and day).
    assert open_time(100, 200, arrow.get("2021-12-31T21:00")).format("YYYY-MM-DDTHH:mm") == arrow.get("2021-12-31T23:56").format("YYYY-MM-DDTHH:mm")
    assert close_time(100, 200, arrow.get("2021-12-31T21:00")).format("YYYY-MM-DDTHH:mm") == arrow.get("2022-01-01T03:40").format("YYYY-MM-DDTHH:mm")

def test_control_gre_brev():
    # Test when the controle time is greater than the brevet length (but not by more than 20 percent)
    assert open_time(620, 600, arrow.get("2021-01-01T00:00")).format("YYYY-MM-DDTHH:mm") == arrow.get("2021-01-01T19:31").format("YYYY-MM-DDTHH:mm")
    assert close_time(620, 600, arrow.get("2021-01-01T00:00")).format("YYYY-MM-DDTHH:mm") == arrow.get("2021-01-02T16:00").format("YYYY-MM-DDTHH:mm")

def test_gen_case():
    # Test for a general case (200km brev, with controles at 60km, 120km, 175km, and 205km).
    assert open_time(60, 200, arrow.get("2021-01-01T00:00")).format("YYYY-MM-DDTHH:mm") == arrow.get("2021-01-01T01:46").format("YYYY-MM-DDTHH:mm")
    assert close_time(60, 200, arrow.get("2021-01-01T00:00")).format("YYYY-MM-DDTHH:mm") == arrow.get("2021-01-01T04:00").format("YYYY-MM-DDTHH:mm")
    assert open_time(120, 200, arrow.get("2021-01-01T00:00")).format("YYYY-MM-DDTHH:mm") == arrow.get("2021-01-01T03:32").format("YYYY-MM-DDTHH:mm")
    assert close_time(120, 200, arrow.get("2021-01-01T00:00")).format("YYYY-MM-DDTHH:mm") == arrow.get("2021-01-01T08:00").format("YYYY-MM-DDTHH:mm")
    assert open_time(175, 200, arrow.get("2021-01-01T00:00")).format("YYYY-MM-DDTHH:mm") == arrow.get("2021-01-01T05:09").format("YYYY-MM-DDTHH:mm")
    assert close_time(175, 200, arrow.get("2021-01-01T00:00")).format("YYYY-MM-DDTHH:mm") == arrow.get("2021-01-01T11:40").format("YYYY-MM-DDTHH:mm")