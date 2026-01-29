import json, time, argparse, numpy as np
from google.cloud import pubsub_v1

parser = argparse.ArgumentParser()
parser.add_argument("--project_id", required=True)
parser.add_argument("--sub_id", required=True)
args = parser.parse_args()

subscriber = pubsub_v1.SubscriberClient()
sub_path = subscriber.subscription_path(args.project_id, args.sub_id)
latencies = []

def callback(message):
    global latencies
    recv_time = time.time()
    try:
        data = json.loads(message.data.decode("utf-8"))
        latency = (recv_time - data["timestamp"]) * 1000
        latencies.append(latency)
        
        print(f"[{len(latencies)}] From {data['source']}: {latency:.2f}ms")
        
        if len(latencies) % 5 == 0:
            print(f"---> {args.sub_id} Avg: {np.mean(latencies):.2f}ms | Max: {np.max(latencies):.2f}ms")
        
        message.ack()
    except Exception as e:
        print(f"Error: {e}")

streaming_pull_future = subscriber.subscribe(sub_path, callback=callback)
print(f"Listening on {args.sub_id}...")

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()