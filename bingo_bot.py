import urllib.request
import re

url = "https://apislb.taiwanlottery.com/_nuxt/bingo_bingo.1_0_8_7.js"

req = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=30) as r:
    js = r.read().decode("utf-8", errors="replace")

print("程式檔讀取成功:", len(js))

# 找出可能的資料路徑
patterns = [
    r'["\']([^"\']{1,200}(?:bingo|Bingo|lotto|Lotto|result|Result)[^"\']{0,200})["\']',
    r'["\']([^"\']{1,200}/api/[^"\']{1,200})["\']'
]

found = set()

for pattern in patterns:
    for match in re.findall(pattern, js):
        found.add(match)

print("找到相關字串:", len(found))

for item in sorted(found):
    print("線索:", item[:300])

print("搜尋完成")


