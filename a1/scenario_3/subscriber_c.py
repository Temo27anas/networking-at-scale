from google.cloud import pubsub_v1
import json, datetime, os,time

PROJECT_ID = "networkedapps-anasandy-2026"
SUBSCRIPTION_ID = "scenario3-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

def callback(message):
    # simulate  crash
        print(f"subscriber crashed for msg {message.message_id}!")
        raise Exception("crash!")

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"listening for msg on {subscription_path}...")

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
