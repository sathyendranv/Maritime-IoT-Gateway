import time
import queue
import sys
import os
import threading

# Add the top-level directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.common import MsgTransfer, DataTransfer

class DataBackup(DataTransfer):
    def __init__(self, item, timestamp):
        super().__init__(item.data, timestamp, item.publich_topic, item.unit, item.status)
        self.timestamp = timestamp


class DataTransformer:
    def __init__(self, logger, q, write_q, syncInterval, offset):
        self.data_published = {}
        self.last_published = {}
        self.logger = logger
        self.q = q
        self.write_q = write_q
        self.syncInterval = syncInterval
        self.offset = offset

    def generate_publish_msg(self, data, status, unit,timestamp):
        status_msg = "Invalid"
        if status == "A":
            status_msg = "Valid"

        if unit == "celsius":
            unit_str = "°C"
        elif unit == "fahrenheit":
            unit_str = "°F"
        else:
            unit_str = "(Unknown)"

        payload = str(data) + unit_str + ", " + status_msg + ", "+ timestamp
        return payload
    def check_if_data_published(self, item, topic):
        if self.offset == 0:
            return True
        if topic not in self.data_published:
            self.data_published[topic] = item.data
            obj = DataBackup(item, time.time())
            self.last_published[topic] = obj
            return True
        if abs(float(item.data) - float(self.data_published[topic])) > self.offset:
            self.data_published[topic] = item.data
            obj = DataBackup(item, time.time())
            self.last_published[topic] = obj
            return True
        return False


    def worker(self):
        while True:
            try:
                # Get an item from the queue
                item = self.q.get(timeout=3)  # Wait for 3 seconds for an item
                msg = self.generate_publish_msg(item.data, item.status, item.unit, item.timestamp)
                if self.check_if_data_published(item, item.publich_topic):
                    obj = MsgTransfer("", msg, item.publich_topic)
                    self.write_q.put(obj)
                    self.logger.debug(f"Transformed data: {obj.__dict__}")
                else:
                    self.logger.info(f"Data not published due to offset: {item.data} - {self.data_published[item.publich_topic]} topic: {item.publich_topic}")
                # Simulate processing time
                time.sleep(0.1)
                self.logger.debug(f"Finished processing item: {item}")
                # Mark the task as done
                self.q.task_done()
            except queue.Empty:
                print("No more items to process, worker is exiting.")
                time.sleep(1)
                continue

def sync_data_publisher(transformer_obj):
    while True:
        current_time = time.time()
        for topic, item in transformer_obj.last_published.items():
            if current_time - item.timestamp > transformer_obj.syncInterval:
                msg = transformer_obj.generate_publish_msg(item.data, item.status, item.unit, item.timestamp)
                obj = MsgTransfer("", msg, topic)
                transformer_obj.write_q.put(obj)
                transformer_obj.logger.debug(f"Sync published data: {obj.__dict__}")
        time.sleep(transformer_obj.syncInterval)
               

def start_data_transformer(config, logger, read_q, write_q):
    transformer = DataTransformer(logger, read_q, write_q, config['syncInterval'], config['offset'])
    t = threading.Thread(target=sync_data_publisher, args=(transformer,))
    t.start()     
    transformer.worker()
