import time
import json
import random
from paho.mqtt import client as mqtt_client

MQTT_BROKER = "localhost"  # Change if needed
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

NUM_ACTUATORS = 5
TOPIC_PATTERN = "building/room{}/hvac_control"  # MQTT topic pattern for actuators


def generate_client_id(room_id):
    return f"hvac_actuator_{room_id}_{random.randint(0, 1000)}"


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected to MQTT Broker! Topis:")

        client.subscribe(userdata["topic"])
        print(f"Subscribed to topic: {userdata['topic']}")
    else:
        print(f"Failed to connect, return code ({reason_code})")


def on_message(client, userdata, msg):
    try:
        message = msg.payload.decode()
        print(f"Actuator for room {userdata['room_id']} received command: {message}")

        if message.upper() == "ON":
            print(f"Room {userdata['room_id']} HVAC turned ON")
        elif message.upper() == "OFF":
            print(f"Room {userdata['room_id']} HVAC turned OFF")
        else:
            print(f"Room {userdata['room_id']} received unknown command: {message}")
    except Exception as e:
        print(f"Error processing message: {e}")


def run_actuator(room_id):
    topic = TOPIC_PATTERN.format(room_id)
    client_id = generate_client_id(room_id)
    client = client = mqtt_client.Client(
        client_id=client_id, userdata={"room_id": room_id, "topic": topic}
    )

    client.user_data_set({"room_id": room_id, "topic": topic})
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
    client.loop_start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"Actuator for room {room_id} stopping...")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    import threading

    threads = []
for room_id in range(1, NUM_ACTUATORS + 1):
    t = threading.Thread(target=run_actuator, args=(room_id,), daemon=True)
    t.start()
    threads.append(t)

print(f"Started {NUM_ACTUATORS} HVAC actuator simulators. Press Ctrl+C to exit.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping all actuators...")
