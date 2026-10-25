import urllib.request
import re

base = "https://apislb.taiwanlottery.com"

req = urllib.request.Request(
    base + "/lotto/result/bingo_bingo/?searchData=true",
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=30) as r:
    html = r.read().decode("utf-8", errors="replace")

scripts = re.findall(
    r'(?:src|href)="([^"]*bingo_bingo[^"]*\.js)"',
    html
)

print("找到賓果程式檔:", len(scripts))

for path in scripts[:3]:
    url = path if path.startswith("http") else base + path
    print("程式檔:", url)

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as r:
        js = r.read().decode("utf-8", errors="replace")

    print("程式檔長度:", len(js))

    for word in ["latestBingoResult", "bingoBingo", "api/"]:
        pos = js.find(word)
        if pos >= 0:
            print("找到關鍵字:", word)
            print(js[max(0, pos-250):pos+500])

print("檢查完成")

