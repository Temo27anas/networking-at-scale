from google.cloud import pubsub_v1
import json, time,  datetime

PROJECT_ID = "networkedapps-anasandy-2026"
SUBSCRIPTION_ID = "scenario3-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID,
                                                 SUBSCRIPTION_ID)


last_receive_time = None
retry_intervals = []

def callback(message: pubsub_v1.subscriber.message.Message):
    global last_receive_time
    now = time.time()
    receive_time = datetime.datetime.utcnow().isoformat()

    if last_receive_time is not None:
        interval = now - last_receive_time
        retry_intervals.append(interval)
        print(f"last retry interval: {interval:.2f}s")

    last_receive_time = now

    print("message ID:", message.message_id)
    print("receive time:", receive_time)

    message.nack()    # Always nack
    print("NACK sent\n")

# Listen to subscription
subscriber.subscribe(subscription_path, callback=callback)

print("listening...")
while True:
    time.sleep(60)
