import urllib.request
import re
import json

url = "https://apislb.taiwanlottery.com/lotto/result/bingo_bingo/?searchData=true"

req = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=30) as response:
    html = response.read().decode("utf-8", errors="replace")

match = re.search(
    r'<script[^>]*id="__NUXT_DATA__"[^>]*>(.*?)</script>',
    html,
    re.S
)

if not match:
    raise Exception("找不到資料區塊")

data = json.loads(match.group(1))

print("資料項目總數:", len(data))

for i, item in enumerate(data):
    if isinstance(item, dict):
        if any("bingo" in str(k).lower() for k in item):
            print("位置:", i)
            print("內容:", str(item)[:2000])

print("資料檢查完成")

