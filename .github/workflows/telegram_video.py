
import os
import json
import urllib.request
import uuid

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

CHANNELS = [
    os.environ["TELEGRAM_CHAT_ID"],
    os.environ["TELEGRAM_ADS_CHAT_ID"],
]

VIDEO_FILE = VIDEO_FILE = "VID_20261028191318132.mp4"

MESSAGE = """👑森哥团队👑
💰招商代理💰
🏆888.hdna57.com/reg/CF0HV1🏆
"""

def send_video(channel):
    boundary = "----Telegram" + uuid.uuid4().hex
    parts = []

    def add_field(name, value):
        parts.append(
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
                f"{value}\r\n"
            ).encode("utf-8")
        )

    add_field("chat_id", channel)
    add_field("caption", MESSAGE)
    add_field("supports_streaming", "true")

    parts.append(
        (
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="video"; '
            'filename="telegram_video.mp4"\r\n'
            "Content-Type: video/mp4\r\n\r\n"
        ).encode("utf-8")
    )

    with open(VIDEO_FILE, "rb") as f:
        parts.append(f.read())

    parts.append(b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))

    request = urllib.request.Request(
        f"https://api.telegram.org/bot{TOKEN}/sendVideo",
        data=b"".join(parts),
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.load(response)

    if not result.get("ok"):
        raise RuntimeError(str(result))

    print("影片發送成功")

for channel in dict.fromkeys(CHANNELS):
    send_video(channel)
