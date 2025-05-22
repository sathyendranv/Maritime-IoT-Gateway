# Maritime-IoT-Gateway
## Overview

Maritime-IoT-Gateway is a solution designed to facilitate secure and reliable data exchange between maritime IoT devices and cloud or on-premises systems. It acts as a bridge, enabling real-time monitoring, control, and analytics for maritime operations.

## Getting Started

### Prerequisites

- Python 3.10+
- Git

### Installation

```bash
git clone https://github.com/your-org/Maritime-IoT-Gateway.git
cd Maritime-IoT-Gateway
pip install -r requirements.txt
```

### Running the Gateway

```bash
python main.py
```

> Note: Data Acquisition depends on simulation script on Github: https://github.com/ChiquiTi2/CraneIoT


## Configuration

Edit the [config.json](config.json) file to set up device connections, protocols, and cloud endpoints.

**config.json**:

- `log_level` - Set the Log Level for Gateway can be set to `INFO`, `DEBUG`, `WARN`. 
- Data Acquisition: 
    - `protocol`: Set to `nmea` for NMEA Rate of Turn Sensor and `modbus` for Modbus
    - `host`, `port`: ip and port of server where it is running 
    -  `publishtopic`: Topic to which the data to be published. Global for `nmea` and for `modbus` each register needs an topic update. 
    - `unit`: unit of the data read. Support `celsius` or `fahrenheit`
    - `interval`: sensor measurements have an update frequency in secs. Optional for `nmea`
    - `timeout`: connection timeout interval. 
    - `register`: JSON Object with key value pair of each registry containing (only for `modbus`)
        - `address`: Modbus Register address 
        - `name`: Name or Description
        - `publishtopic`: Topic to which the data to be published
        - `unit`: unit of the data read. Support `celsius` or `fahrenheit`

    > _**Note:**_
    >
    > - _Only `Holding Register` is supported in `modbus`_
    > - _Default assumption for `Holding Register` is `address` start from 0 and total count is based on number of item in array._

- Data Transformation:
    - `syncInterval`: Interval to sync data when no change has occurred in last x duration.
    - `offset`: Offset value to publish the data.
    - `publish`: Protocol to publish the data to North bound. Supported Protocol is `mqtt`

- MQTT (North bound):
    - `host`: IP or URL of mqtt broker
    - `port`: Port of mqtt broker
    - `enable_lwt`: enable LWT (Last Will & Testament) send message to each topic with the content: "connection lost"
    - `username`: username of authentication.
    - `password`: password of authentication.
    - `keepalive`:  kept alive duration for connection.


## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

This project is licensed under the MIT License.