from datetime import datetime, timezone

def generate_valid_timestamp():
    # Get the current time in UTC
    now_utc = datetime.now(timezone.utc)

    # Format the date and time
    formatted_time = now_utc.strftime("%Y-%m-%d at %H:%M UTC")

    return formatted_time

class DataTransfer:
    def __init__(self, data,timestamp, publich_topic, unit,status):
        self.data = data
        self.timestamp = timestamp
        self.publich_topic = publich_topic
        self.unit = unit
        self.status = status

class MsgTransfer:
    def __init__(self, protocol ,msg,topic):
        self.protocol = protocol
        self.msg = msg
        self.topic = topic