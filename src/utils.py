from datetime import date, datetime
from dateutil.relativedelta import relativedelta

DATE_FMT='%d/%m/%Y'
KM_PER_MI = 1.60934

def time_str_to_secs(time_str:str)->int:
    secs_mins_hours = time_str.split(':')[::-1]
    total_secs = 0
    for i_part, part in enumerate(secs_mins_hours):
        part_int = int(part)
        if part_int < 0 or part_int > 59:
            raise ValueError(f'{time_str} is not a valid time')
        total_secs += part_int*(60**i_part)
    return total_secs

def secs_to_time_str(secs:int):
    hh = secs // 3600
    rem = secs % 3600
    mm = rem // 60
    ss = rem % 60
    hh_str = f'{hh}:' if hh else ''
    return f'{hh_str}{mm:02d}:{ss:02d}'

def date_from_str(date_str:str)->date:
    return datetime.strptime(date_str, DATE_FMT).date()

def date_to_str(date_:date)->str:
    return date_.strftime(DATE_FMT)

def years_since(dob:date, other_date:date=date.today())->int:
    return relativedelta(other_date, dob).years

def distance_in_kms(distance:str)->float:
    distance_val, distance_units = distance.split()
    
    if distance_units.lower().startswith('km'):
        distance_km = float(distance_val)
    elif distance_units.lower().startswith('mi'):
        distance_km = float(distance_val)*KM_PER_MI
    else:
        raise ValueError(f'Distance {distance} not valid')
    return distance_km