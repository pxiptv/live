import urllib.request
import requests

def fetch_file(url):
    try:
        response = urllib.request.urlopen(url)
        return response.read().decode('utf-8')
    except Exception as e:
        print(f"无法获取文件：{e}")
        return None

def check_url(url, timeout=3):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return True
    except requests.RequestException as e:
        print(f"URL 检测失败：{e}")
    return False

def main():
    urls = [
        'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/cn.m3u'
    ]

    online_urls = []

    for url in urls:
        print(f"获取文件：{url}")
        content = fetch_file(url)
        if content:
            lines = content.splitlines()
            for line in lines:
                if line.startswith("http://") or line.startswith("https://"):
                    print(f"检测网址：{line}")
                    if check_url(line):
                        online_urls.append(line)
                        print(f"在线：{line}")
                    else:
                        print(f"离线：{line}")

    with open('cs.txt', 'w', encoding='utf-8') as file:
        for online_url in online_urls:
            file.write(online_url + '\n')

if __name__ == "__main__":
    main()
