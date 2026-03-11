from google.cloud import pubsub_v1
from concurrent import futures
import json
import time

project_id = "networkedapps-anasandy-2026"
topic_id = "flowcontrol-topic"

# publisher flow control
publisher_flow_control = pubsub_v1.types.PublishFlowControl(
    message_limit=10,
    limit_exceeded_behavior=pubsub_v1.types.LimitExceededBehavior.ERROR,
)

publisher = pubsub_v1.PublisherClient(
    publisher_options=pubsub_v1.types.PublisherOptions(
        flow_control=publisher_flow_control
    )
)

topic_path = publisher.topic_path(project_id, topic_id)

publish_futures = []

start_time = time.time()

# publish messages
for i in range(100):
    data = json.dumps({"count": i}).encode("utf-8")
    try:
        future = publisher.publish(topic_path, data)
        publish_futures.append(future)
        print(f"Publish requested: {i}")
    except Exception as e:
        print(f"Immediate error publishing message {i}: {e}")

# wait for all futures and catch errors
for i, future in enumerate(publish_futures):
    try:
        future.result()  # raise exceptions for failed publishes
    except Exception as e:
        print(f"Message {i} failed: {e}")

end_time = time.time()
print(f"Publishing finished in {end_time - start_time:.2f} seconds")
