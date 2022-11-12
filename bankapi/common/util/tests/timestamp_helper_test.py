import time
from datetime import datetime
from datetime import date
from time import struct_time
from common.util.timestamp_helper import *

if __name__ == '__main__':
    print(datetime.utcnow())

    print(convert_epoch_to_str(get_timestamp()))



    print(convert_epoch_to_str(get_n_hrs_ago(-2)))


    print(get_timestamp())

    print(format_epoch_time(2020, 8, 12, 11, 20, 0))

    print(convert_epoch_to_str(get_date()))

    print(convert_epoch_to_str(get_timestamp()))

    for i in range(4):
        o = get_now_and_then(get_timestamp(), 30)

        print(convert_epoch_to_str(o))
        time.sleep(2)

    print(convert_epoch_to_str(get_yesterday()))
    print(convert_epoch_to_str(get_tomorrow()))
    print(convert_epoch_to_str(get_n_days_ago(2)))
    print(convert_epoch_to_str(get_n_hrs_ago(2)))
    print(convert_epoch_to_str(get_one_min_ago()))
    print(convert_epoch_to_str(get_ten_sec_ago()))
