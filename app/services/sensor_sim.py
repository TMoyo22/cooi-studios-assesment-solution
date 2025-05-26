import time
import random
import json
import paho.mqtt.client as mqtt


MQTT_BROKER = "localhost"  # broker address
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60


NUM_SENSORS = 5
TOPIC_PATTERN = "building/room{}/temperature"  # format string for MQTT topic


def simulate_temperature():
    """Random temperature between 15 and 35 degrees Celsius."""
    return round(random.uniform(15, 35), 2)


def main():
    client = mqtt.Client()

    client.connect(
        MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE
    )  # establish connection to the MQTT broker

    print("Starting temperature sensor simulation...")

    try:
        while True:
            for room_id in range(1, NUM_SENSORS + 1):
                temperature = simulate_temperature()
                topic = TOPIC_PATTERN.format(room_id)
                payload = json.dumps(
                    {"room": room_id, "temperature": temperature, "unit": "C"}
                )

                client.publish(topic, payload)  # temp reading publish to broker
                print(f"Published to {topic}: {payload}")

            time.sleep(5)  # Delay beforthe next reading

    except KeyboardInterrupt:
        print("Simulation stopped.")

    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
