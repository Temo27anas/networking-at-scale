from google.cloud import pubsub_v1
import json, time, datetime

PROJECT_ID = "networkedapps-anasandy-2026"
SUBSCRIPTION_ID = "scenario3-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID,
                                                 SUBSCRIPTION_ID)

# case A: always NACK
def callback(message: pubsub_v1.subscriber.message.Message):
    receive_time = datetime.datetime.utcnow().isoformat()
    payload = json.loads(message.data.decode("utf-8"))

    print("message ID:", message.message_id)

    message.nack()     # Always nack
    print("NACK is sent\n")

# Listen to subscription
subscriber.subscribe(subscription_path, callback=callback)

print("listening...")
while True:
    time.sleep(60)
