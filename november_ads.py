
import os
import json
import urllib.request
import urllib.error

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

CHAT_IDS = list(dict.fromkeys(
    x.strip()
    for x in [
        os.getenv("TELEGRAM_CHAT_ID", ""),
        os.getenv("TELEGRAM_ADS_CHAT_ID", "")
    ]
    if x.strip()
))

TITLE = """🏆 GA黄金甲｜11月新人专属福利

🎉 新人免费开局，38元体验金自由选！

📅 活动时间
2026/11/01 — 2026/11/30

🎁 福利一｜新人免费体验金

🔴 体育电竞体验金：38元
体育／电竞完成3倍流水

🔵 全馆体验金：38元
全场馆完成8倍流水（不含彩票）

⚠️ 两种体验金仅可选择一种。

💰 福利二｜新人首存送彩金

首存200元 ➜ 赠送68元
首存500元 ➜ 赠送168元
首存1000元 ➜ 赠送328元
首存3000元 ➜ 赠送968元
首存5000元 ➜ 赠送1688元
首存10000元 ➜ 赠送3088元

🔥 首存彩金最高3088元！

📢 森哥团队｜台湾宾果・赛事资讯
🔗 https://t.me/bingomaster0

⚠️ 活动须符合平台规则及适用地区法律。
"""

API = f"https://api.telegram.org/bot{TOKEN}"

def send(chat_id):
    photo_path = "november_poster.jpg"

    if os.path.isfile(photo_path):
        boundary = "TelegramPhotoBoundary"
        with open(photo_path, "rb") as f:
            photo = f.read()

        body = (
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="chat_id"\r\n\r\n'
            f"{chat_id}\r\n"
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="photo"; filename="poster.jpg"\r\n'
            "Content-Type: image/jpeg\r\n\r\n"
        ).encode() + photo + (
            f"\r\n--{boundary}--\r\n"
        ).encode()

        req = urllib.request.Request(
            API + "/sendPhoto",
            data=body,
            headers={
                "Content-Type":
                f"multipart/form-data; boundary={boundary}"
            }
        )
        with urllib.request.urlopen(req, timeout=40) as r:
            result = json.load(r)
            if not result.get("ok"):
                raise RuntimeError(str(result))
    else:
        print("Poster missing: sending text only")

    data = json.dumps({
        "chat_id": chat_id,
        "text": TITLE,
        "disable_web_page_preview": True
    }).encode("utf-8")

    req = urllib.request.Request(
        API + "/sendMessage",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req, timeout=40) as r:
        result = json.load(r)
        if not result.get("ok"):
            raise RuntimeError(str(result))

    print(f"Successfully sent to {chat_id}")

if not CHAT_IDS:
    raise RuntimeError("No Telegram chat IDs configured")

for chat_id in CHAT_IDS:
    send(chat_id)

