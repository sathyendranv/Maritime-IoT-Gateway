import json
import logging
import queue
import threading
from data_acquisition.modbusTcpInterface import start_modbus_client
from data_transformation.transform_data import start_data_transformer
from cloud_connector.publishToMqtt import start_mqtt_client

CONFIG_FILE = 'config.json'
def main():
    """Main to start gateway service
    """
    try:
        # Configure logging
        logging.basicConfig(
            level='INFO',  # Set the log level to DEBUG
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
        )

        logger = logging.getLogger(__name__)
        with open (CONFIG_FILE, 'r') as file:
            app_cfg = json.load(file)
            logger.setLevel(app_cfg['log_level'])
        q = queue.Queue()
        write_q = queue.Queue()
        threads = []
        if 'data_aquisition' in app_cfg:
            for item in app_cfg['data_aquisition']:
                if 'protocol' in item and item['protocol'] == 'modbus':
                    logger.info(f"Starting Modbus client for {item['host']}:{item['port']}")
                    t = threading.Thread(target=start_modbus_client, args=(item, q, logger))
                    t.start()
                    threads.append(t)
                if 'protocol' in item and item['protocol'] == 'nmea':
                    logger.info(f"Starting NMEA client for {item['host']}:{item['port']}")
                    # t = threading.Thread(target=start_nmea_client, args=(item, q, logger))
                    # t.start()
                    # threads.append(t)
                if 'protocol' in item and item['protocol'] != 'modbus' and item['protocol'] != 'nmea':
                    logger.fatal(f"Unsupported protocol {item['protocol']} for {item['host']}:{item['port']}")
        if 'transform' in app_cfg:
            logger.info("Starting data transformer")
            t = threading.Thread(target=start_data_transformer, args=(app_cfg['transform'], logger, q, write_q))
            t.start()
            threads.append(t)
        if 'mqtt' in app_cfg:
            logger.info("Starting MQTT client")
            t = threading.Thread(target=start_mqtt_client, args=(app_cfg['mqtt'], logger, write_q))
            t.start()
            threads.append(t)
                    
        else:
            logger.fatal("No data acquisition configuration found in config.json.")

            # start_modbus_client(app_cfg['data_aquisition'], q)
    except FileNotFoundError:
        logger.error(f"Configuration file {CONFIG_FILE} not found.")
        return

if __name__ == "__main__":
    main()