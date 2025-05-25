import requests
import time

WEBHOOK_URL = "https://discord.com/api/webhooks/1376142225213493298/GN5BRUsAb4GLdqRcv8mI3Nb95nDw28hn5isJarYYjcJEKA_LZSHle7_QdfCEJbMmaBbI"
USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_hour.geojson"

last_eq_time = None

def fetch_earthquakes():
    response = requests.get(USGS_URL)
    data = response.json()

    if not data["features"]:
        return None

    latest = data["features"][0]
    props = latest["properties"]

    return {
        "title": props["title"],
        "time": props["time"],
        "url": props["url"],
        "mag": props["mag"],
        "place": props["place"]
    }

def send_to_discord(earthquake):
    embed = {
        "embeds": [{
            "title": f"🌍 Yeni Deprem: {earthquake['title']}",
            "description": f"📍 Yer: {earthquake['place']}\n📏 Büyüklük: {earthquake['mag']}",
            "url": earthquake["url"],
            "color": 0xff0000,
            "footer": {
                "text": "Veri: USGS Earthquake Feed"
            }
        }]
    }
    r = requests.post(WEBHOOK_URL, json=embed)
    print("✅ Webhook gönderildi." if r.status_code == 204 else f"❌ Hata: {r.status_code}")

def main():
    global last_eq_time
    print("📡 Deprem Botu Başlatıldı (USGS)")
    while True:
        try:
            eq = fetch_earthquakes()
            if eq and eq["time"] != last_eq_time:
                send_to_discord(eq)
                last_eq_time = eq["time"]
            else:
                print("🔁 Yeni deprem yok.")
        except Exception as e:
            print(f"❗ Hata: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main()
