import os
from paho.mqtt import client as mqtt_client
from google.cloud import pubsub_v1

broker = 'localhost'
port = 1883
topic = "/sensor/data"
project_id = "phyton-quickstart"
pubsub_topic = "projects/phyton-quickstart/topics/falldetectiontopic"

publisher = pubsub_v1.PublisherClient()
pubsub_topic_path = publisher.topic_path(project_id, pubsub_topic)

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        publisher.publish(pubsub_topic_path, msg.payload)
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
