def less_than_four(stat):
    if stat.Off_Wrist.lower() != "nan" and stat.Interval_Type == "DAILY":
        return float(stat.Off_Wrist) < 240
    return False

def parse_time(str_time):
    str_time,tod = str_time.split(" ")
    h, m, s = [int(t) for t in str_time.split(":")]
    return  (h if h != 12 else 0) + m/60 + s/3600 + (0 if tod == "PM" else 12)

def hours_to_intervals(hours):
    return hours * 120