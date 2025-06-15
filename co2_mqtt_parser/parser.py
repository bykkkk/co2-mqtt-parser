
import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPIC_SUB = "ew11/recv"
TOPIC_PUB = "home/sensors/indoor_co2"
DISCOVERY_TOPIC = "homeassistant/sensor/indoor_co2/config"

def publish_discovery(client):
    discovery_payload = {
        "name": "Indoor CO2",
        "state_topic": TOPIC_PUB,
        "unit_of_measurement": "ppm",
        "device_class": "carbon_dioxide",
        "unique_id": "indoor_co2_001",
        "icon": "mdi:molecule-co2"
    }
    client.publish(DISCOVERY_TOPIC, json.dumps(discovery_payload), retain=True)
    print("Published MQTT discovery payload.")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC_SUB)
    publish_discovery(client)

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8').upper()
    if payload.startswith("F7A001") and len(payload) >= 16:
        try:
            co2_str = payload[12:16]
            co2_val = int(co2_str)
            print(f"CO₂: {co2_val} ppm")
            client.publish(TOPIC_PUB, str(co2_val))
        except ValueError:
            print("Invalid CO₂ value in payload:", payload)

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_forever()
