from google.cloud import pubsub_v1
import time

project_id = "networkedapps-anasandy-2026"
subscription_id = "flowcontrol-sub"

# set the total number of messages expected
TOTAL_MESSAGES = 1000  # change to 10, 100, 1000 per experiment

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

message_count = 0
start_time = None

def callback(message):
    global message_count, start_time, streaming_pull_future

    if message_count == 0:
        start_time = time.time()

    message_count += 1
    message.ack()

    if message_count % 10 == 0 or message_count == TOTAL_MESSAGES:
        print(f"Received {message_count} messages")

    # stop the subscriber once all messages are received
    if message_count >= TOTAL_MESSAGES:
        streaming_pull_future.cancel()

# subscribe to the topic
streaming_pull_future = subscriber.subscribe(
    subscription_path,
    callback=callback,
)

print(f"Subscriber started, expecting {TOTAL_MESSAGES} messages...")

try:
    streaming_pull_future.result()
except Exception:
    pass  # ignore cancellation exception
finally:
    if start_time:
        total_time = time.time() - start_time
        print(f"Total time to receive {message_count} messages: {total_time:.2f} seconds")
    subscriber.close()
