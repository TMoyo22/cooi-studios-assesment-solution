# Smart Building IoT Middleware Service

## Overview

This project implements a middleware service for a smart building IoT system that:

- Runs a **legacy HVAC REST API** built with Flask.
- Listens to **temperature data from an MQTT broker**.
- Automatically triggers HVAC commands via the legacy API when room temperatures exceed 30°C.
- Logs all actions and errors for traceability.

---

## Project Structure

The project is set up to separate the api handling, services and middleware into modules under the app/ dir.

---

## Setup & Running

### 1. Install dependencies

pip install -r requirements.txt

### 2. Run the legacy HVAC API

python run.py

- The API will be available at: `http://127.0.0.1:5000`
- Basic Authentication is enabled with credentials:
  - Username: `COOiLabs`
  - Password: `123456`

## CREDENTIALS ARE HARDCODED TO MAINTAIN SIMPLICITY, HOWEVER A .ENV CAN BE IMPLEMENTED FOR ADDITIONAL SECUIRTY

### 3. Run the middleware service

python -m app.services.middleware_service

- The middleware subscribes to MQTT topics like `building/room1/temperature`.
- It triggers HVAC commands based on temperature thresholds.

### 4. Simulate temperature sensor data

Using Mosquitto MQTT client:
Open your command prompt: after installing the mosquitto client(https://mosquitto.org/download/)
To open CMD:

1. Windows + R
2. Click Enter

### Run the following (CMD)

mosquitto_pub -h localhost -t building/room1/temperature -m 40

---

## Testing the API

### With authentication
In Powershell:
curl.exe -u COOiLabs:123456 http://localhost:5000/api/hvac/status

### Without authentication (should fail if you don't add the authentication properly)

curl.exe http://localhost:5000/api/hvac/status

---

## Design Choices

- The first choice I made was to choose Python, my main reason for choosing python in this project and others in its quicker to build with and quickly prototype core features. The other reason is the really large communnity across, stack overflow, discord, reddit, there always people who would faced the same problems you are facing even if the implementation is not exactly the same the concept will be.

Python is also very popular in IoT and coupled with paho-mqtt client library, you cant go wrong

- Why MQTT? => MQTT is a lightweight protocol that is designed for low-bandwidth networks making it suitable for this type of IoT enviroment, I chose Mosquitto beacuse it is open source and it manages its messaging well between IoT nodes. Messaging via MQTT allows for near real-time delivery which is important for this use-case of controlling an HVAC system from temperature readings. Since it can run on a physical board (e.g microcontroller) locally and not only on server it allows us to have decision making occur at the edge for real-time feedback without sending data to the cloud first for it to be processed there, which would introduce greater latency.

- REST APIs are stateless making them ideal for this use case. Stateless refers to a request sent from the client side to the server is independent and holds all the neccesary information required for the server to act on the request. No information on previous request is stored at the server. Allowing for scalability. REST APIs also allow for a number of authentication methods.

- Breaking up the app into modules to follow best practices and it makes debugging much easier than trying to find an issue in a single code base with 1000 lines of code. Its easier to scale and maintain as well.

- Error handling and Retires all done in the middleware, easier debugging.

- I tried to focus on scalability which I feel is crucial for IoT systems as nodes can be increased as the system is upgraded so ensuring you have a scalable architecture will future proof your system and allow for easier integration of devices later.

## Challenges I faced

- One of the challenges I faced was how to ensure that the the simulation will be able to simulate all temperatures at the same time , then I ran into a silution to use threading which will separate each actuator into its "own thread" and the it will communicate with its sensor independently.

- Most of the other challenges were python imports and could be resolved, especially the middleware service. Soultin: To make sure that python resolves package imports you need to use the -m flag from project root.

---

## References

- [paho-mqtt Python client](https://pypi.org/project/paho-mqtt/)
- [Mosquitto MQTT Broker](https://mosquitto.org/download/)
- [Flask MQTT Documentation](https://flask-mqtt.readthedocs.io/en/latest/index.html)
- [YouTube MQTT Tutorial](https://www.youtube.com/watch?v=z3YMz-Gocmw)

---

## Future Improvements

- Beautiful Dashboard !

# My Journey

## This section was just out of interest on milestones I set for myself after breaking the project down. In no particular order...My project checkpoints :)

1. Actuators Are Live
   Shows the actuator simulators connecting to the MQTT broker and subscribing to control topics.

![Image](https://github.com/user-attachments/assets/329a3d5a-14b2-4f9e-bd7b-979121584ee8)

Actuators Communicating with the Broker
This screenshot shows the actuators sending PINGREQ and receiving PINGRESP messages, confirming active communication with the MQTT broker.

![Image](https://github.com/user-attachments/assets/0e461440-fb2e-4857-98b0-cc427cb4faa9)

2. Data Being Sent to the Broker
   Demonstrates simulated temperature data being published to the MQTT broker and received by the system.

![Image](https://github.com/user-attachments/assets/a9f56d8e-b8d2-4920-a61c-b609e3f9cde7)

3.Broker Running
Shows the Mosquitto MQTT broker running locally and ready to accept connections.

![Image](https://github.com/user-attachments/assets/61a9e6ac-5dec-4094-b57a-c4f44c4bb523)

Mosquitto MQTT Broker Running and Publishing/Receiving Data
This image demonstrates the Mosquitto broker running, with successful subscription and message publishing using the mosquitto_pub and mosquitto_sub commands.

![Image](https://github.com/user-attachments/assets/74b79c8b-3cae-4cfb-bd10-254c3a87c60d)

4. Temperature Data Received by Middleware
   Demonstrates temperature data being sent to the middleware and the middleware logging the received values and actions.

![Image](https://github.com/user-attachments/assets/63bd7b49-e01d-4571-98fd-cd3c495b7f46)
![Image](https://github.com/user-attachments/assets/e21b368b-dbfb-4149-809b-5e8fa5fac033)

5. Testing API Endpoint via curl
   This screenshot shows a successful GET request to the HVAC status endpoint using curl, confirming the API is running and accessible.

![Image](https://github.com/user-attachments/assets/720a2fd0-0625-4359-a9dd-3225b66b4057)

Testing the POST Endpoint

Here, you can see attempts to activate the HVAC via the POST endpoint, including an example of a malformed request and a successful activation.

![Image](https://github.com/user-attachments/assets/2c5d7bd4-cf37-4a6c-ad78-1f78bb24a6e2)

## Logs

![Image](https://github.com/user-attachments/assets/7fff46b6-4660-4191-9b11-b68530e414ae)
