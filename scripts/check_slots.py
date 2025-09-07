import requests
from datetime import datetime
import os

# Step 1: Read PIN code (use env variable or default)
PIN = os.getenv("PIN", "110001")

# Step 2: Today’s date in DD-MM-YYYY format
DATE = datetime.today().strftime("%d-%m-%Y")

# Step 3: CoWIN public API endpoint
url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PIN}&date={DATE}"
headers = {"User-Agent": "Mozilla/5.0"}  # required to avoid blocking

# Step 4: Call API
resp = requests.get(url, headers=headers)
data = resp.json()

# Step 5: Extract available slots
available = []
for center in data.get('centers', []):
    for sess in center.get('sessions', []):
        if sess.get('available_capacity', 0) > 0:
            available.append(
                f"{center['name']} ({center['pincode']}) on {sess['date']} "
                f"slots:{sess['available_capacity']} vaccine:{sess['vaccine']}"
            )

# Step 6: Prepare message
if available:
    text = "💉 Vaccine slots available:\n" + "\n".join(available)
else:
    text = f"No slots found for {PIN} on {DATE}."

# Step 7: Send message to Telegram
TELE_TOKEN = os.getenv("8348093242:AAFrDbmkWpEkm0cRwZl8oyrKVWmzPySf2r4")
CHAT_ID = os.getenv("8348093242")
send_url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
requests.get(send_url, params={"chat_id": CHAT_ID, "text": text})
