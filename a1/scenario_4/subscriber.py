from google.cloud import pubsub_v1
import time

project_id = "networkedapps-anasandy-2026"
subscription_id = "flowcontrol-sub"

subscriber = pubsub_v1.SubscriberClient()

flow_control = pubsub_v1.types.FlowControl(
    max_messages=1000,
)

subscription_path = subscriber.subscription_path(
    project_id, subscription_id
)

def callback(message):
    print(f"Received message {message.message_id}")
    time.sleep(0.2)  # simulate processing
    message.ack()

streaming_pull_future = subscriber.subscribe(
    subscription_path,
    callback=callback,
    flow_control=flow_control,
)

print("Subscriber started...")

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
    subscriber.close()
