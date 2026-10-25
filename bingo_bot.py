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

bingo = data[32]
result_index = bingo["latestBingoResult"]

print("最新賓果資料位置:", result_index)
print("最新賓果資料內容:")
print(json.dumps(
    data[result_index],
    ensure_ascii=False,
    indent=2
))

print("檢查完成")
