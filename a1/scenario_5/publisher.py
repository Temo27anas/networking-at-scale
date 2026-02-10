from google.cloud import pubsub_v1
from concurrent import futures
import json
import time

project_id = "networkedapps-anasandy-2026"
topic_id = "flowcontrol-topic"

batch_settings = pubsub_v1.types.BatchSettings(
    max_bytes=1,       # 1 byte
    max_messages=1,    # 1 message
    max_latency=0      # 0 seconds
)

publisher = pubsub_v1.PublisherClient(
    batch_settings=batch_settings
)

topic_path = publisher.topic_path(project_id, topic_id)

num_messages = 100  # change to 10, 100, 1000 per experiment

publish_futures = []
start_time = time.time()

for i in range(num_messages):
    data = json.dumps({"count": i}).encode("utf-8")
    future = publisher.publish(topic_path, data)
    publish_futures.append(future)

futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)
end_time = time.time()
print(f"Publishing {num_messages} messages finished in {end_time - start_time:.2f} seconds")
