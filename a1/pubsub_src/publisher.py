import json
import time
import argparse
from google.cloud import pubsub_v1

parser = argparse.ArgumentParser()
parser.add_argument("--project_id", required=True)
parser.add_argument("--topic_id", default="fanout-topic")
args = parser.parse_args()

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(args.project_id, args.topic_id)

for i in range(1, 101):
    data = {
        "source": "publisher-finland",
        "timestamp": time.time(),
        "count": i
    }
    message_bytes = json.dumps(data).encode("utf-8")
    publisher.publish(topic_path, message_bytes)
    print(f"Published message {i}")
    time.sleep(1)