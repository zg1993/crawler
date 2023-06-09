# -*-coding: utf-8 -*-

import pytz



def timestamp_to_str(timestamp):
    tz = pytz.timezone('Asia/Macau')
    return pytz.datetime.datetime.fromtimestamp(timestamp,tz).strftime('%Y-%m-%d %H:%M')
    