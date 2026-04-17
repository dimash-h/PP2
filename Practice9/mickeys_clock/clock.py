import datetime

def get_angles():
    time = datetime.datetime.now()

    sec_angle = -(time.second * 6) + 90
    min_angle = -(time.minute * 6) + 90
    return min_angle, sec_angle