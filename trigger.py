import requests

url = "https://us-central1-pii-goldset-9023.cloudfunctions.net/process_chunks"

response = requests.post(url)

print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")
