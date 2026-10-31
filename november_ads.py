
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
2026/11/01 00:00 — 2026/11/30 23:59
🎁 福利一｜新人免费体验金
新会员可任选一种体验金：
🔴 体育电竞体验金
免费领取 38 元
体育／电竞完成 3 倍流水
🔵 全馆体验金
免费领取 38 元
全场馆完成 8 倍流水（不含彩票）
⚠️ 两种体验金仅可选择一种，申请成功后不可更换。
💰 福利二｜新人首存送彩金
首次充值.     额外彩金
200 元.          68 元

500 元.          168 元

1,000 元.       328 元

3,000 元.      968 元

5,000 元.     1,688 元

10,000 元.    3,088 元

🔥 首存彩金最高 3,088 元！
首存彩金需完成全场馆 6 倍流水（不含彩票）。
📌 活动重点须知
✅ 仅限活动前未有成功充值记录的新会员申请。
✅ 体验金与首存彩金均须联系专属经理申请。
✅ 累计有效充值满 200 元，才可申请解锁出款功能。
✅ 首存彩金须在解锁出款功能时一并申请，事后不可补领。
✅ 申请成功后，彩金预计 24 小时内发放。
✅ 彩金发放后，须在 7 天内领取。
✅ 首存活动不可与其他首存优惠共享。
━━━━━━━━━━━━━━
🎯 新人双重福利，免费体验金＋首存送彩金！
📢 活动详情及申请方式，请联系专属经理。
⚠️ 活动彩金及提款条件以官方完整规则为准，请留意流水要求。
https://9zax.ga2ghf.news/B51019
https://7ydkf.ga2ghf.news/B51019
https://iz2k.ga2l8l.news/B51019
https://lntd.ga27951.news/B51019
https://g9th.ga28577.news/B51019
https://ga8.sk/B51019
"""

API = f"https://api.telegram.org/bot{TOKEN}"

def send(chat_id):
    photo_path = "IMG_2417.jpeg"

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

