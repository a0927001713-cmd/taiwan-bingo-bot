import urllib.request
import re

url = "https://apislb.taiwanlottery.com/lotto/result/bingo_bingo/?searchData=true"

req = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=30) as response:
    html = response.read().decode("utf-8", errors="replace")

print("網頁讀取成功")
print("網頁長度:", len(html))

match = re.search(
    r'<script[^>]*id="__NUXT_DATA__"[^>]*>(.*?)</script>',
    html,
    re.S
)

if match:
    print("找到網頁資料區塊")
    print(match.group(1)[:3000])
else:
    print("未找到預載資料區塊")
    print("需要繼續尋找開獎 API")
