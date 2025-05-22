from pymodbus.client import ModbusTcpClient
import time
import sys
import os

# Add the top-level directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.common import generate_valid_timestamp, DataTransfer

class ModbusTcpInterface:
    def __init__(self, ip, port, timeout, queue,logger):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.client = ModbusTcpClient(host=self.ip, port=self.port, timeout=self.timeout)
        self.queue = queue
        self.logger = logger

    def connect(self):
        return self.client.connect()

    def close(self):
        self.client.close()

    def read_holding_registers(self, start_address, count):
        if not self.connect():
            self.logger.error("Unable to connect to Modbus server.")
            return None

        result = self.client.read_holding_registers(address=start_address, count=count)
        if result.isError():
            self.logger.error("Error reading holding registers:", result)
            self.close()
            return None

        self.logger.debug(f"Holding Registers {start_address} to {start_address + count - 1}: {result.registers}")
        self.close()
        return result.registers

def start_modbus_client(config, q, logger):
    modbus_client = ModbusTcpInterface(config['host'], config['port'], config['timeout'], q, logger)
    if 'register' in config and 'holding_register' in config['register']:
        pass
    else:
        logger.fatal("Only holding register configuration is supported.")
    while True:
        timestamp = generate_valid_timestamp()
        data = modbus_client.read_holding_registers(0, len(config['register']['holding_register']))
        
        for i in range(len(config['register']['holding_register'])):
            if data != None:
                obj = DataTransfer(data[i], timestamp, config['register']['holding_register'][i]['publishtopic'], config['register']['holding_register'][i]['unit'], "A")   
            else:
                obj = DataTransfer(-1, timestamp, config['register']['holding_register'][i]['publishtopic'], config['register']['holding_register'][i]['unit'],"V")
            logger.debug(f"Publishing data: {obj.__dict__}")
            q.put(obj)
        time.sleep(config['interval'])