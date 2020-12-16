# mqtt-notifysend-bridge
 Bridge between MQTT and Notify-Send. Works on Ubuntu Linux, and on Windows using [vaskovsky/notify-send](https://github.com/vaskovsky/notify-send)

## Getting Started
### Requirements
Python 3.6 and above, with pip

### Installation
Clone this directory locally, and install with `pip install .`

### Usage
```
mqtt-notifysend-bridge --server <servername>[:<port>] --topic path/to/topic
```

## Command-line options
- `--server`: Server to connect to, and optionally port number
- `--topic`: Topic to subscribe to
