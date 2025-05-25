import feedparser
import requests
import time

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/WEBHOOK_ID/WEBHOOK_TOKEN"
RSS_URL = "https://www.koeri.boun.edu.tr/sismo/zeqmap/rss/latest.rss"
last_earthquake = None

def send_discord_webhook(title, link, summary):
    data = {
        "embeds": [{
            "title": title,
            "url": link,
            "description": summary,
            "color": 0xFF0000,
            "footer": {
                "text": "Deprem Bilgisi • Kandilli Rasathanesi"
            }
        }]
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("✅ Bildirim gönderildi.")
    else:
        print(f"❌ Webhook hatası: {response.status_code} - {response.text}")

def check_earthquakes():
    global last_earthquake
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        print("⚠️ Veri alınamadı.")
        return

    latest = feed.entries[0]
    title = latest.title
    link = latest.link
    summary = latest.summary

    if last_earthquake != title:
        print(f"🌍 Yeni deprem: {title}")
        send_discord_webhook(title, link, summary)
        last_earthquake = title
    else:
        print("🔁 Yeni deprem yok.")

if __name__ == "__main__":
    print("📡 Bot çalışıyor...")
    while True:
        try:
            check_earthquakes()
        except Exception as e:
            print(f"❗ Hata: {e}")
        time.sleep(60)
