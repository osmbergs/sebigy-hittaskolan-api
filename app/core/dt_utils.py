import datetime


def now():
    #    return datetime.datetime(datetime.timezone.utc)
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)


def get_quarter(dt):
    return str(dt.year) + str((dt.month - 1) // 3 + 1)


def get_current_quarter():
    dt = now()
    return get_quarter(dt)


def get_next_quarter():
    curr = get_current_quarter()
    year = int(curr[0:3])
    next_quarter = int(curr[-1]) + 1

    if next_quarter == 5:
        next_quarter = 1
        year = year + 1

    return str(year) + str(next_quarter)


def next_quarter_in_one_month() -> bool:
    curr = get_current_quarter()
    return curr[-1] == 4
