import urllib.request
import urllib.error

url = "https://apislb.taiwanlottery.com/lotto/result/bingo_bingo/?searchData=true"

request = urllib.request.Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json,text/html,*/*"
    }
)

try:
    with urllib.request.urlopen(request, timeout=20) as response:
        content = response.read().decode("utf-8", errors="replace")
        print("HTTP 狀態:", response.status)
        print("資料類型:", response.headers.get("Content-Type"))
        print("回傳資料前 1500 字:")
        print(content[:1500])
except urllib.error.HTTPError as error:
    print("HTTP 錯誤:", error.code)
    print(error.read().decode("utf-8", errors="replace")[:500])
except Exception as error:
    print("連線錯誤:", type(error).__name__, str(error))

