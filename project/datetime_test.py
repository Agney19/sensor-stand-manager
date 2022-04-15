import datetime
from datetime import timedelta

class Reservation:
    def __init__(self, start_datetime, end_datetime):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime


def get_free_time(start, end, reservations, result):
    if start >= end:
        return result
    if len(reservations) == 0:
        result.append([start, end])
        return result
    first_reservation = reservations.pop(0)
    r_start = first_reservation.start_datetime
    r_end = first_reservation.end_datetime
    if r_end < start:
        return get_free_time(start, end, reservations, result)
    if r_start > start:
        result.append([start, r_start])
        if r_end < end:
            return get_free_time(r_end, end, reservations, result)
        return result
    return get_free_time(r_end, end, reservations, result)

def get_time_slots(intervals, result):
    if len(intervals) == 0:
        return result
    interval = intervals.pop(0)
    slot_start = interval[0]
    slot_duration = timedelta(minutes=23)
    slot_end = slot_start + slot_duration
    while slot_end < interval[1]:
        result.append([slot_start, slot_end])
        slot_start = slot_end
        slot_end = slot_end + slot_duration
    result.append([slot_start, interval[1]])
    return get_time_slots(intervals, result)

cur_time = datetime.datetime(1, 1, 1, 1, 1, 1)
latest_time = datetime.datetime(1, 1, 1, 10, 1, 1)
intervals = get_free_time(cur_time, latest_time, [
    Reservation(datetime.datetime(1, 1, 1, 0, 1, 1), datetime.datetime(1, 1, 1, 6, 1, 1)),
    Reservation(datetime.datetime(1, 1, 1, 4, 1, 1), datetime.datetime(1, 1, 1, 5, 1, 1)),
    Reservation(datetime.datetime(1, 1, 1, 7, 1, 1), datetime.datetime(1, 1, 1, 13, 1, 1))
], [])
print(intervals)
print(get_time_slots(intervals, []))
