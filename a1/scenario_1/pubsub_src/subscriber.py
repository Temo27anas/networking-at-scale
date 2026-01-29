import json
import time
import argparse
import numpy as np
from google.cloud import pubsub_v1

parser = argparse.ArgumentParser()
parser.add_argument("--project_id", required=True)
parser.add_argument("--sub_id", required=True)
args = parser.parse_args()

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(args.project_id, args.sub_id)
latencies = []

def callback(message):
    recv_time = time.time()
    data = json.loads(message.data.decode("utf-8"))
    latency = (recv_time - data["timestamp"]) * 1000
    latencies.append(latency)
    message.ack()
    
    if len(latencies) == 100:
        print(f"\n--- Results for {args.sub_id} ---")
        print(f"Avg: {np.mean(latencies):.2f}ms | Max: {np.max(latencies):.2f}ms | Min: {np.min(latencies):.2f}ms")
        print(f"p50: {np.percentile(latencies, 50):.2f}ms | p95: {np.percentile(latencies, 95):.2f}ms")
        print("Experiment Complete. Press Ctrl+C to exit.")

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Subscriber active on {args.sub_id}...")

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()