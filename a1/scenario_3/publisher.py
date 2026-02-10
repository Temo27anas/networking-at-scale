from google.cloud import pubsub_v1
import json, time

PROJECT_ID = "networkedapps-anasandy-2026"
TOPIC_ID = "scenario3-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

message = {
    "payload": "Mammamia!",
    "timestamp": time.time()
}

future = publisher.publish( # returns a Future
    topic_path,
    json.dumps(message).encode("utf-8")  
)

print("published message:", future.result()) # waits for the publish call to complete