import requests
import json
import time

council_id = "eaca8cd3-5388-4cf6-a0db-25d0e89cb7a2"
print(f"Using council ID: {council_id}")
print(f"Council title: Clean Test v2")

# Step 2: POST message
print()
print("=== Step 2: POST message ===")
payload = {"content": "what is tomorrow's date?", "role": "human"}
headers = {"Content-Type": "application/json"}
r = requests.post(
    f"http://localhost:8000/api/councils/{council_id}/messages",
    json=payload,
    headers=headers
)
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:2000]}")

# Step 3: Wait 20 seconds
print()
print("=== Step 3: Waiting 20 seconds for agents to respond ===")
time.sleep(20)
print("Done waiting.")

# Step 4: GET messages
print()
print("=== Step 4: GET messages ===")
r2 = requests.get(f"http://localhost:8000/api/councils/{council_id}/messages?limit=30")
print(f"Status: {r2.status_code}")
data = r2.json()
print(json.dumps(data, indent=2))
