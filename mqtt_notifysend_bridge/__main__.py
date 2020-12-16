#!/usr/bin/env python3
"""Listens on an MQTT topic, and calls notify-send when a message is recieved."""

import paho.mqtt.client as mqtt
import subprocess
import argparse
from shlex import quote

VERSION = "0.1.0"

def on_connect(client, userdata, flags, rc):
    """Subscribe to the topic specified in the userdata."""
    print("Connected with result code %s, subscribing to topic: %s" % (str(rc), userdata["topic"]))
    client.subscribe(userdata["topic"])


def on_disconnect(client, userdata, rc):
    """Print result code following broker disconnect."""
    print("Disconnected with result code %s" % str(rc))


def on_message(client, userdata, msg):
    """Process incoming messages from broker on subscribed topic."""
    payload = msg.payload.decode("utf-8")
    print("Processing recieved message: %s" % payload)
    subprocess.Popen(["notify-send", "-i", "info", "MQTT Message", quote(payload)])


def app(args):
    """Check provided arguments and start the MQTT client."""
    # Default values
    server = "localhost"
    port = 1883
    topic = "notification"

    # Check if a server has been provided
    if args.server is None:
        print("Warning: Server not specified, using %s" % server)
    else:
        # Split the server hostname and port number
        server_hostname_port = args.server.split(":", 1)
        server = server_hostname_port[0]
        if len(server_hostname_port) > 1:
            try:
                port = int(server_hostname_port[1])
            except ValueError:
                print("Error: Port provided is not a number")
                exit(1)

    # Check if a topic has been provided
    if args.topic is None or args.topic is not None and len(args.topic) < 1:
        print("Warning: Topic not specified, listening on default topic: %s" % topic)
    else:
        topic = args.topic

    # Start the client
    print("Starting, version %s" % VERSION)
    client = mqtt.Client(userdata={"topic": topic})
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    print("Connecting to %s:%s" % (server, port))
    client.connect(server, port, 60)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Exiting");
        exit(0);


def main():
    """Parse provided arguments and start the app."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", help="MQTT server to connect to", metavar="localhost:1883")
    parser.add_argument("-t", "--topic", help="Topic to listen for messages", metavar="path/to/topic")
    app(parser.parse_args())


if __name__ == "__main__":
    main()
