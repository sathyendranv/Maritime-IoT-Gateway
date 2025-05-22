import asyncio
import sys
import os

# Add the top-level directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.common import generate_valid_timestamp, DataTransfer

class NMEASocketClient:
    def __init__(self, host, port, logger, q, topic, unit):
        self.host = host
        self.port = port
        self.logger = logger
        self.q = q
        self.topic = topic
        self.unit = unit

    async def tcp_client(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)

        while True:
            data = await reader.read(100)
            if not data:
                break
            self.logger.debug(f'Received: {data.decode()}')
            self.parse_custom_nmea_sentence(data.decode())

        writer.close()
        await writer.wait_closed()

    def parse_custom_nmea_sentence(self, sentence):
        if not sentence.startswith('$'):
            raise ValueError("Invalid NMEA sentence")

        parts = sentence.split(',')

        sentence_type = parts[0][1:]
        data_value = parts[1]
        status = parts[2].split('*')[0]
        checksum = parts[2].split('*')[1]

        self.logger.debug(f"Sentence Type: {sentence_type}")
        self.logger.debug(f"Data Value: {data_value}")
        self.logger.debug(f"Status: {status}")
        self.logger.debug(f"Checksum: {checksum}")

        obj = DataTransfer(data_value, generate_valid_timestamp(), self.topic, self.unit, status)  
        self.logger.debug(f"Publishing data: {obj.__dict__}")
        self.q.put(obj) 

def start_nmea_client(config,  q, logger):
    nmea_client = NMEASocketClient(config['host'], config['port'], logger, q, config['publishtopic'], config['unit'])
    asyncio.run(nmea_client.tcp_client())
