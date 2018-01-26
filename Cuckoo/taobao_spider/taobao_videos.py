import requests

url = 'https://cloud.video.taobao.com/play/u/108727117/p/1/e/6/t/1/50047688890.mp4'
res = requests.get(url).content
with open("shipin.mp4", 'wb') as f:
    f.write(res)