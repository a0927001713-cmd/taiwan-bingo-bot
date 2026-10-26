
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

MESSAGE =
MESSAGE = """🏆 GA黄金甲｜十月豪礼盛大开启 🏆

🔥 精彩赛事 · 彩票娱乐 · 多重活动福利 🔥

🎉 台湾宾果 BINGO BINGO
🏀 体育竞彩｜熊猫｜AI｜FB
🎰 彩票娱乐｜百家｜电子竞技

━━━━━━━━━━━━━━

🎁 十月限定福利活动

📅 活动时间：2026/10/01—2026/10/31

💰 福利一｜平台首存奖励

首次充值符合条件，即可申请对应奖励！

✨ 首存奖励最高 5,888
✨ 首存豪礼大方送，最高额外 6,888
✨ 指定钱包及 USDT 渠道另有加码

🎁 福利二｜周周复存奖励

每周符合充值条件，即可申请复存奖励。

💎 复存奖励最高 5,888
💎 指定充值渠道享额外加码

🚀 福利三｜复存加码

达到指定会员等级，当月符合复存次数条件，还可申请额外复存机会！

📌 详细申请资格、奖励条件、流水要求及领取限制，请以官方活动规则为准。

━━━━━━━━━━━━━━

🌟 平台服务资讯

💳 支持多种存取款方式：

▪️ USDT
▪️ 微信支付
▪️ 支付宝
▪️ 银行卡
▪️ 多种电子钱包

━━━━━━━━━━━━━━

🌐 彩票注册网址
http://888.hdna57.com/reg/CF0HV1

⚽ 体育竞彩入口
https://ga9.sk/B51019

💬 Telegram 联系方式
https://t.me/bingomaster0

━━━━━━━━━━━━━━

🎊 更多十月活动，欢迎查看官方公告！

⚠️ 请确认规定及参与资格，理性娱乐，量力而为。活动奖金并非保证收益，实际领取以平台公布的规则为准。"""

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
