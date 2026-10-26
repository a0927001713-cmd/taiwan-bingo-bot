import urllib.request

url = "https://apislb.taiwanlottery.com/_nuxt/bingo_bingo.1_0_8_7.js"

req = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=30) as response:
    js = response.read().decode("utf-8", errors="replace")

keywords = [
    "/Lottery/BingoResult",
    "openDate",
    "dataPerPage"
]

for word in keywords:
    print("\n===== 搜尋:", word, "=====")

    start = 0
    count = 0

    while count < 3:
        pos = js.find(word, start)

        if pos == -1:
            break

        print("位置:", pos)
        print(js[max(0, pos-600):pos+600])
        print("----------------")

        start = pos + len(word)
        count += 1

print("檢查完成")
