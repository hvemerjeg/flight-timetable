from datetime import datetime

def formatTime(epoch_time:str) -> str:
    datetime_obj = datetime.fromtimestamp(epoch_time)
    time_str = datetime_obj.strftime('%H:%M')
    return str(time_str)

def formatDateTime(epoch_time:str) -> str:
    datetime_obj = datetime.fromtimestamp(epoch_time)
    date_time_str = datetime_obj.strftime('%Y-%m-%d %H:%M')
    return str(date_time_str)
