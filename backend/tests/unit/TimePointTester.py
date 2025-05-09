from app.models import TimePoint


def test_time_point():
    time1 = TimePoint(hour=1, minute=0)
    time2 = TimePoint(hour=1, minute=0)
    time3 = TimePoint(hour=2, minute=0)

    assert time3 > time1
    assert time1 < time3
    assert time2 == time1

    time4 = TimePoint(hour=1, minute=1)
    assert time4 > time1
    assert time1 < time4
