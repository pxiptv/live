import socket
import requests
import time

def check_url(url):
    try:
        host = url.split("//")[-1].split("/")[0]
        addr_info = socket.getaddrinfo(host, None, socket.AF_INET6)
        if addr_info:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock.settimeout(3)
            start_time = time.time()
            result = sock.connect_ex((addr_info[0][4][0], 80)) # 假设使用80端口
            elapsed_time = time.time() - start_time
            sock.close()
            if result == 0:
                print(f"{url} - 响应时间：{elapsed_time:.2f}秒")
                return True
            else:
                print(f"{url} - 连接失败")
        else:
            print(f"{url} - 无法解析主机名")
    except Exception as e:
        print(f"{url} - 错误：{e}")
    return False

def main():
    url = "https://raw.githubusercontent.com/suxuang/myIPTV/main/ipv6.m3u"
    response = requests.get(url)
    response_lines = response.text.strip().split('\n')

    with open('cs.txt', 'w') as f:
        for line in response_lines:
            if "http" in line:
                if check_url(line.strip()):
                    f.write(line.strip() + '\n')

if __name__ == "__main__":
    main()
