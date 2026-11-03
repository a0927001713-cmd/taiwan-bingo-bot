
import os
import json
import urllib.request
import uuid

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

CHANNELS = list(dict.fromkeys([
    os.environ["TELEGRAM_CHAT_ID"],
    os.environ["TELEGRAM_ADS_CHAT_ID"],
]))

VIDEO_FILE = VIDEO_FILE = "telegram_video.mov"

MESSAGE = """👑森哥团队👑
💰招商代理💰
🏆888.hdna57.com/reg/CF0HV1🏆
"""

def send_video(channel):
    if not os.path.isfile(VIDEO_FILE):
        raise FileNotFoundError(VIDEO_FILE)

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

    print(f"影片發送成功：{channel}")

for channel in CHANNELS:
    send_video(channel)

