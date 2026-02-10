# Setup script for Scenario 3
# Case A
gcloud pubsub topics create scenario3-topic

gcloud pubsub subscriptions create scenario3-sub \
  --topic=scenario3-topic \
  --ack-deadline=10

gcloud pubsub subscriptions delete scenario3-sub


## Case B
gcloud pubsub subscriptions create scenario3-sub \
  --topic=scenario3-topic \
  --ack-deadline=10 \
  --min-retry-delay=1s \
  --max-retry-delay=300s

gcloud pubsub subscriptions update scenario3-sub \
  --min-retry-delay=0s

gcloud pubsub subscriptions delete scenario3-sub

# Case C

gcloud pubsub topics create scenario3-topic

gcloud pubsub topics create dlq-topic

gcloud pubsub subscriptions create scenario3-sub \
    --topic=scenario3-topic \
    --ack-deadline=10 \
    --max-delivery-attempts=5 \
    --dead-letter-topic=dlq-topic


gcloud pubsub subscriptions create dlq-sub \
    --topic=dlq-topic

gcloud pubsub subscriptions pull dlq-sub --limit=10 --auto-ack


gcloud pubsub topics delete scenario3-topic