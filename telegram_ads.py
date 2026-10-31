
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
    "IMG_2415.jpeg",
    "IMG_2419.jpeg",
]

MESSAGE = """🏆 GA黄金甲｜暖心11月・热血献礼 🏆

🔥 精彩赛事 · 彩票娱乐 · 十一月专属福利 🔥

🎉 台湾宾果 BINGO BINGO
🏀 体育竞彩｜熊猫｜AI｜FB
🎰 彩票娱乐｜百家｜电子竞技

━━━━━━━━━━━━━━

🎁 十一月限定福利活动

📅 活动时间：2026/11/01—2026/11/30

💰 福利一｜平台首存

首次充值符合活动条件，即可申请对应奖励。

✨ 平台首存奖励最高 5,888 元
✨ 首存豪礼大方送，最高额外 6,888 元
✨ 指定 USDT 及电子钱包渠道另有加码

🎁 福利二｜周周复存

每周符合充值条件，即可申请复存奖励。

💎 复存奖励最高 5,888 元
💎 指定充值渠道享额外加码
💎 充值金额及奖励等级依官方活动表为准

🚀 福利三｜复存加码

达到钻石达人或以上等级，当月复存次数达到 4 次，可依活动规则申请额外 1 次复存机会。

📌 活动彩金须符合指定流水、申请期限及领取条件，详细规则请以官方公告为准。

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
https://9zax.ga2ghf.news/B51019
https://7ydkf.ga2ghf.news/B51019
https://iz2k.ga2l8l.news/B51019
https://lntd.ga27951.news/B51019
https://g9th.ga28577.news/B51019
https://ga8.sk/B51019

💬 Telegram 联系方式
https://t.me/the_shattered_dreams

━━━━━━━━━━━━━━

🎊 GA黄金甲｜十一月活动详情请查看官方公告。

⚠️ 活动彩金并非保证收益，申请资格、流水要求、提款及领取限制以完整活动规则为准。请理性娱乐，量力而为。"""

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
