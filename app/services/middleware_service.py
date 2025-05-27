import json
import logging
import requests
from paho.mqtt import client as mqtt_client
from app.utils.logger import logger

# MQTT and API config
broker = "localhost"
port = 1883
topic = "building/+/temperature"
client_id = "middleware_service"
legacy_api_base_url = "http://localhost:5000/api/hvac"


def send_hvac_command(command):
    url = f"{legacy_api_base_url}/command"
    payload = {"command": command}
    auth = ("COOiLabs", "123456")  # Same credentials as in the legacy API
    try:
        response = requests.post(url, json=payload, auth=auth)
        response.raise_for_status()
        logger.info(f"Sent HVAC command: {command}")
    except requests.RequestException as e:
        logger.error(f"Failed to send HVAC command '{command}': {e}")


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        temperature = float(payload)
        topic_parts = msg.topic.split("/")
        room = topic_parts[1]

        logger.info(f"Received temperature {temperature}°C from {room}")

        if temperature > 30:
            logger.info(
                f"Temperature {temperature}°C in {room} exceeds threshold. Activating HVAC."
            )
            send_hvac_command("activate")
        else:
            logger.info(
                f"Temperature {temperature}°C in {room} below threshold. Deactivating HVAC."
            )
            send_hvac_command("deactivate")

    except Exception as e:
        logger.error(f"Error processing message from topic {msg.topic}: {e}")


def connect_mqtt():
    client = mqtt_client.Client(client_id=client_id, callback_api_version=1)
    client.connect(broker, port)
    return client


def run():
    client = connect_mqtt()
    client.subscribe(topic)
    client.on_message = on_message
    logger.info("Middleware service started and subscribed to temperature topics.")
    client.loop_forever()


if __name__ == "__main__":
    run()
