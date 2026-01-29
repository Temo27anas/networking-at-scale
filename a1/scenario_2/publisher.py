import json, time, argparse
from google.cloud import pubsub_v1

parser = argparse.ArgumentParser()
parser.add_argument("--project_id", required=True)
parser.add_argument("--pub_id", required=True)
args = parser.parse_args()

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(args.project_id, "scenario2-topic")

for i in range(1, 101):
    data = {"source": args.pub_id, "timestamp": time.time(), "count": i}
    publisher.publish(topic_path, json.dumps(data).encode("utf-8"))
    print(f"{args.pub_id} sent msg {i}")
    time.sleep(1)
