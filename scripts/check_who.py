import requests
import os

def get_who_updates():
    url = "https://www.who.int/api/pages/outbreaks/disease-outbreak-news"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # Extract top 1 outbreak
            if "value" in data and len(data["value"]) > 0:
                first = data["value"][0]
                title = first.get("title", "WHO outbreak alert")
                link = first.get("url", "https://www.who.int/emergencies/disease-outbreak-news")
                return f"🚨 WHO Outbreak Update:\n{title}\n{link}"
            else:
                return "No current outbreak alerts found from WHO."
        else:
            return f"WHO API error {resp.status_code}. Using fallback alert."
    except Exception as e:
        print("Error contacting WHO API:", e)
        return "🚨 WHO Outbreak Update:\nDemo outbreak alert – Stay safe and wash hands regularly."

text = get_who_updates()

# Send to Telegram
TELE_TOKEN = os.getenv("8348093242:AAFrDbmkWpEkm0cRwZl8oyrKVWmzPySf2r4")
CHAT_ID = os.getenv("8348093242")

if TELE_TOKEN and CHAT_ID:
    send_url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    try:
        requests.get(send_url, params={"chat_id": CHAT_ID, "text": text})
    except Exception as e:
        print("Error sending Telegram message:", e)
else:
    print("Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID environment variables.")
