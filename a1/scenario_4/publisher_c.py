from google.cloud import pubsub_v1
from concurrent import futures
import json
import time

project_id = "networkedapps-anasandy-2026"
topic_id = "flowcontrol-topic"

# publisher flow control: defaults
publisher_flow_control = pubsub_v1.types.PublishFlowControl(
    message_limit=1000,
    limit_exceeded_behavior=pubsub_v1.types.LimitExceededBehavior.BLOCK,
)

publisher = pubsub_v1.PublisherClient(
    publisher_options=pubsub_v1.types.PublisherOptions(
        flow_control=publisher_flow_control
    )
)

topic_path = publisher.topic_path(project_id, topic_id)

publish_futures = []

start_time = time.time()

for i in range(100):
    data = json.dumps({"count": i}).encode("utf-8")
    future = publisher.publish(topic_path, data)
    publish_futures.append(future)
    print(f"Publish requested: {i}")

# wait for all messages to finish publishing
futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

end_time = time.time()
print(f"Publishing finished in {end_time - start_time:.2f} seconds")
