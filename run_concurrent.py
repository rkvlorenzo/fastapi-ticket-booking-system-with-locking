import threading
import requests
import uuid
import time

# Ticket UUID you're trying to reserve
TICKET_ID = "bf2af413-dd2f-4dd2-a0e1-13def2abe020"

# Number of users/threads to simulate
NUM_USERS = 10

# URL of your endpoint
URL = "http://localhost:8000/tickets/reserve"

# Thread function to send the PATCH request
def reserve_ticket(user_id):
    payload = {
        "user_id": user_id,
        "ticket_id": TICKET_ID
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.patch(URL, json=payload, headers=headers)
        print(f"[User {user_id}] Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"[User {user_id}] Error: {e}")

# Create and start threads
threads = []

for i in range(NUM_USERS):
    t = threading.Thread(target=reserve_ticket, args=(i+1,))
    threads.append(t)
    t.start()
    time.sleep(0.05)  # Optional: small stagger to better simulate race conditions

# Wait for all threads to complete
for t in threads:
    t.join()

print("All requests completed.")
