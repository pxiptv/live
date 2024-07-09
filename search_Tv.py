import requests
import time

# 定义超时时间
timeout = 5

# 追加录入
def append_to_file(filename, line):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(line)

# 读取live.txt文件
try:
    with open('live.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
except IOError as e:
    print(f'无法读取文件live.txt: {e}')
    exit()

# 存储有响应的行到whitelist.txt，并记录无响应的行到blacklist.txt
try:
    with open('whitelist.txt', 'w', encoding='utf-8') as output_file:
        for line in lines:
            # 找到","后的内容，即网址，并分割字符串为name和url
            parts = line.split(',', 1)  # 限制分割一次
            if len(parts) < 2:
                continue  # 如果没有找到","，跳过当前行

            name = parts[0].strip()  # 去除可能的空白字符
            url = parts[1].strip()

            try:
                if "://" in url:
                    # 发送HTTP请求前记录时间
                    start_time = time.time()
                    response = requests.get(url, timeout=timeout, stream=True)
                    # 计算响应时间
                    elapsed_time = (time.time() - start_time) * 1000
                    # 如果响应状态码为200，即网站在线，则写入whitelist.txt
                    if response.status_code == 200:
                        print(f'检测正常: {name},{url}, 响应时间: {elapsed_time:.2f}ms')
                        output_file.write(line)
                    else:
                        print(f'检测失败: {name},{url}')
                        append_to_file('blacklist.txt', line)
            except requests.exceptions.Timeout:
                # 如果超时，打印提示信息
                print(f'超时错误: {name},{url}')
                append_to_file('blacklist.txt', line)
            except requests.exceptions.HTTPError as e:
                # 如果HTTP请求返回了错误的状态码
                print(f'HTTP错误: {name},{url}, 状态码: {e.response.status_code}')
                append_to_file('blacklist.txt', line)
            except requests.exceptions.TooManyRedirects:
                # 如果重定向次数过多
                print(f'重定向错误: {name},{url}')
                append_to_file('blacklist.txt', line)
            except (requests.exceptions.URLRequired,
                    requests.exceptions.MissingSchema,
                    requests.exceptions.InvalidSchema):
                # 如果URL是必须的但未提供，或者URL的方案无效
                print(f'URL错误: {name},{url}')
                append_to_file('blacklist.txt', line)
            except requests.exceptions.RequestException as e:
                # 打印其他异常信息
                print(f'其他错误: {name},{url}, Error: {e}')
                append_to_file('blacklist.txt', line)
                
except IOError as e:
    print(f'无法写入文件whitelist.txt: {e}')
    exit()

print("新增频道在线检测完毕，结果已存入 whitelist.txt 和 blacklist.txt。")
