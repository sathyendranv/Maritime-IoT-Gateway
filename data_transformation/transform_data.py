import time
import queue
import sys
import os

# Add the top-level directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.common import MsgTransfer

class DataTransformer:
    def __init__(self, logger, q, write_q):
        self.data_published = {}
        self.logger = logger
        self.q = q
        self.write_q = write_q

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
    def worker(self):
        while True:
            try:
                # Get an item from the queue
                item = self.q.get(timeout=3)  # Wait for 3 seconds for an item
                msg = self.generate_publish_msg(item.data, item.status, item.unit, item.timestamp)

                obj = MsgTransfer("", msg, item.publich_topic)
                self.write_q.put(obj)
                self.logger.debug(f"Transformed data: {obj.__dict__}")

                # Simulate processing time
                time.sleep(0.1)
                self.logger.debug(f"Finished processing item: {item}")
                # Mark the task as done
                self.q.task_done()
            except queue.Empty:
                print("No more items to process, worker is exiting.")
                time.sleep(1)
                continue
                

def start_data_transformer(config, logger, read_q, write_q):
    transformer = DataTransformer(logger, read_q, write_q)
    transformer.worker()
