
import os
import urllib.parse
import urllib.request

token = os.environ["TELEGRAM_BOT_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]

data = urllib.parse.urlencode({
    "chat_id": chat_id,
    "text": "🎱 台灣賓果自動發文程式連線測試成功！"
}).encode("utf-8")

url = f"https://api.telegram.org/bot{token}/sendMessage"

with urllib.request.urlopen(
    urllib.request.Request(url, data=data),
    timeout=20
) as response:
    print(response.read().decode("utf-8"))
