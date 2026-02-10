from google.cloud import pubsub_v1
import time

project_id = "networkedapps-anasandy-2026"
subscription_id = "flowcontrol-sub"

subscriber = pubsub_v1.SubscriberClient()

max_messages = 1  # changed to 1, 10, or 100 for each experiment

flow_control = pubsub_v1.types.FlowControl(
    max_messages=max_messages,
)

subscription_path = subscriber.subscription_path(project_id, subscription_id)

message_count = 0
start_time = None

def callback(message):
    global message_count, start_time
    if message_count == 0:
        start_time = time.time()
    message_count += 1
    message.ack()
    if message_count % 10 == 0:
        print(f"Received {message_count} messages")

streaming_pull_future = subscriber.subscribe(
    subscription_path,
    callback=callback,
    flow_control=flow_control,
)

print(f"Subscriber started with max_messages={max_messages}...")

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
    subscriber.close()
finally:
    if start_time:
        total_time = time.time() - start_time
        print(f"Total time to receive {message_count} messages: {total_time:.2f} seconds")
