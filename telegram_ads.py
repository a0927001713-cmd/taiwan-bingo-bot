
import os
import json
import uuid
import urllib.request

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

CHANNELS = [
    os.environ["TELEGRAM_CHAT_ID"],
    os.environ["TELEGRAM_ADS_CHAT_ID"],
]

IMAGES = [
    "6300EBDF-5640-425C-BA16-FFAFFEE02D0E.jpeg",
    "32B2BE67-80D9-4825-9899-3B516928B5F5.jpeg",
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

def send_album(channel):
    boundary = uuid.uuid4().hex

    media = [
        {
            "type": "photo",
            "media": f"attach://photo{i}",
            **({"caption": MESSAGE} if i == 0 else {}),
        }
        for i in range(len(IMAGES))
    ]

    parts = []

    def add_part(name, content, filename=None, content_type=None):
        header = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{name}"'
        )

        if filename:
            header += f'; filename="{filename}"'

        header += "\r\n"

        if content_type:
            header += f"Content-Type: {content_type}\r\n"

        header += "\r\n"

        parts.append(header.encode("utf-8"))
        parts.append(content)
        parts.append(b"\r\n")

    add_part("chat_id", channel.encode("utf-8"))
    add_part("media", json.dumps(media).encode("utf-8"))

    for i, filename in enumerate(IMAGES):
        with open(filename, "rb") as image:
            add_part(
                f"photo{i}",
                image.read(),
                filename,
                "image/jpeg"
            )

    body = b"".join(parts) + f"--{boundary}--\r\n".encode()

    request = urllib.request.Request(
        f"https://api.telegram.org/bot{TOKEN}/sendMediaGroup",
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        },
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        result = json.load(response)

    if not result.get("ok"):
        raise RuntimeError(f"發送失敗：{channel}")

    print(f"圖片與文字發送成功：{channel}")


for channel in dict.fromkeys(CHANNELS):
    send_album(channel)
