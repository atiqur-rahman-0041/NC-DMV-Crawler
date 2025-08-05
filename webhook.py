import requests

def notify_discord(message, webhook_url):
    data = {"content": message}
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            pass
            # print("✅ Notification sent to Discord")
        else:
            print(f"⚠️ Failed to send Discord notification: {response.status_code} {response.text}")
    except Exception as e:
        print(f"❌ Error sending Discord notification: {e}")


