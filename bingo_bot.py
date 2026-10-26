import os
import json
import urllib.request
import urllib.parse
from datetime import datetime
from zoneinfo import ZoneInfo

API = "https://api.taiwanlottery.com/TLCAPIWeB/Lottery/BingoResult"
TZ = ZoneInfo("Asia/Taipei")

def get_results():
    today = datetime.now(TZ).strftime("%Y-%m-%d")
    query = urllib.parse.urlencode({
        "openDate": today,
        "pageNum": 1,
        "pageSize": 10
    })
    req = urllib.request.Request(
        API + "?" + query,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.load(response)

    if not isinstance(data, dict):
        raise ValueError("API 格式不正確")
    print("API 最外層欄位：", list(data.keys()))
    print("API 資料預覽：")
    print(json.dumps(data, ensure_ascii=False)[:2500])

    records = data.get("content", {}).get("bingoQueryResult")

    if not isinstance(records, list) or not records:
        raise ValueError("找不到開獎資料，請查看上方預覽")

    return records

def parse_numbers(value):
    if isinstance(value, str):
        import re
        numbers = [
            int(x) for x in re.findall(r"\d+", value)
        ]
    elif isinstance(value, list):
        numbers = [int(x) for x in value]
    else:
        raise ValueError("號碼格式不正確")

    if (len(numbers) != 20
            or len(set(numbers)) != 20
            or not all(1 <= n <= 80 for n in numbers)):
        raise ValueError("開獎號碼未通過驗證")

    return sorted(numbers)

def send_message(message):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message
    }).encode()

    request = urllib.request.Request(
        url, data=payload, method="POST"
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)

    if not result.get("ok"):
        raise RuntimeError("Telegram 發送失敗")

def main():
    records = get_results()
    latest = records[0]

    period = str(latest.get("drawTerm", "")).strip()
    print("最新一期完整欄位：", json.dumps(latest, ensure_ascii=False))
    draw_time = str(latest.get("drawDate", "")).strip()
    numbers = parse_numbers(latest.get("bigShowOrder"))

    if not period:
        raise ValueError("缺少開獎期數")

    lines = [
        "🎱 台灣賓果 BINGO BINGO",
        f"🎯 開獎期數：{period}",
        "⏰ 開獎時間：待確認",
        "",
        "📢 本期開獎號碼"
    ]

    for i in range(0, 20, 5):
        lines.append(
            " ".join(f"{n:02d}" for n in numbers[i:i+5])
        )

    message = "\n".join(lines)

    # 安全測試：先只顯示，不發送
    print(message)
    send_message("🧪 賓果機器人測試訊息\n\n" + message)

if __name__ == "__main__":
    main()
