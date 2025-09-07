import requests, os

TELE_TOKEN = os.getenv("8348093242:AAFrDbmkWpEkm0cRwZl8oyrKVWmzPySf2r4")
CHAT_ID = os.getenv("8348093242")

# WHO Disease Outbreak News API
url = "https://www.who.int/api/news/diseaseoutbreaknews"

resp = requests.get(url)
if resp.status_code == 200:
    items = resp.json().get('value', [])
    if items:
        latest = items[0]  # latest outbreak
        title = latest.get('title', 'WHO Update')
        link = "https://www.who.int" + latest.get('url', '/')
        text = f"🚨 WHO Outbreak Update:\n{title}\n{link}"
        send_url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
        requests.get(send_url, params={"chat_id": CHAT_ID, "text": text})
