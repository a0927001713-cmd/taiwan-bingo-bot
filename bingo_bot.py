import urllib.request
import urllib.parse
import urllib.error
import json
from datetime import datetime
from zoneinfo import ZoneInfo

today = datetime.now(
    ZoneInfo("Asia/Taipei")
).strftime("%Y-%m-%d")

base = base = "https://api.taiwanlottery.com/TLCAPIWeB"

params = urllib.parse.urlencode({
    "openDate": today,
    "pageNum": 1,
    "pageSize": 10
})

url = base + "/Lottery/BingoResult?" + params

print("查詢日期:", today)
print("測試官方開獎資料")

req = urllib.request.Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
)

try:
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode(
            "utf-8", errors="replace"
        )
        print("HTTP 狀態:", r.status)
        print("資料類型:", r.headers.get("Content-Type"))
        print("回傳內容:")
        print(body[:4000])

        try:
            data = json.loads(body)
            print("JSON 解析成功")
        except json.JSONDecodeError:
            print("回傳內容不是 JSON")

except urllib.error.HTTPError as e:
    print("HTTP 錯誤:", e.code)
    print(e.read().decode(
        "utf-8", errors="replace"
    )[:1000])

except Exception as e:
    print("連線錯誤:", str(e))
