
import os
import json
import urllib.request

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

CHANNELS = [
    os.environ["TELEGRAM_CHAT_ID"],
    os.environ["TELEGRAM_ADS_CHAT_ID"],
]

MESSAGE = """🏆 GA黄金甲｜十月活动资讯 🏆

🎉 台湾宾果 BINGO BINGO
🏀 体育竞彩｜熊猫｜AI｜FB
🎰 彩票娱乐｜体育赛事｜电子竞技

🎁 十月限定活动
📅 2026/10/01—2026/10/31

💰 平台首存活动
💎 周周复存活动
🚀 会员专属活动

📌 具体资格、条件及限制，请以官方活动规则为准。

🌐 彩票注册网址
http://888.hdna57.com/reg/CF0HV1

⚽ 体育竞彩入口
https://ga9.sk/B51019

💬 Telegram 联系方式
https://t.me/bingomaster0

⚠️ 请遵守当地法律，理性娱乐，量力而为。
"""

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

for channel in dict.fromkeys(CHANNELS):
    data = json.dumps({
        "chat_id": channel,
        "text": MESSAGE
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)

    if not result.get("ok"):
        raise RuntimeError(f"發送失敗：{channel}")

    print(f"發送成功：{channel}")
