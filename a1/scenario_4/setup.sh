gcloud compute instances create pubsub-flow-control \
    --zone=europe-north1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2404-lts-amd64 \
    --image-project=ubuntu-os-cloud \
    --network=my-pubsub-net \
    --scopes=https://www.googleapis.com/auth/cloud-platform


# ----------  Within VM -------------
sudo apt update
sudo apt install -y python3-pip iproute2
sudo apt install -y python3-full
python3 -m venv venv
source venv/bin/activate
pip install --upgrade google-cloud-pubsub
gcloud auth application-default login

gcloud config set project networkedapps-anasandy-2026
gcloud pubsub topics create flowcontrol-topic
gcloud pubsub subscriptions create flowcontrol-sub \
  --topic=flowcontrol-topic \
  --ack-deadline=10

# Network Delay
ip addr show
sudo tc qdisc add dev ens4 root netem delay 100ms 50ms distribution normal
python3 subscriber.py 
python3 publisher.py # Another terminal

# Cleanup
sudo tc qdisc del dev ens4 root netem


# --------------------- CASE B -------------------
tc qdisc show dev ens4
python3 subscriber.py 
python3 publisher_b.py # Another terminal

# Cleanup
sudo tc qdisc del dev ens4 root netem

# --------------------- CASE C -------------------
sudo tc qdisc del dev ens4 root netem



