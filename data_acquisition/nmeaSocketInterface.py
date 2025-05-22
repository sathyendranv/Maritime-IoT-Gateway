import asyncio
import sys
import os

# Add the top-level directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class NMEASocketClient:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    async def tcp_client(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)

        while True:
            data = await reader.read(100)
            if not data:
                break
            print(f'Received: {data.decode()}')
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

        print(f"Sentence Type: {sentence_type}")
        print(f"Data Value: {data_value}")
        print(f"Status: {status}")
        print(f"Checksum: {checksum}")
