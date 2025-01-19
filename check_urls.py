import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime
import os
import re
import requests
from urllib.parse import urlparse


timestart = datetime.now()

# 读取文件内容 1
def read_txt_file(file_path):
    skip_strings = ['#genre#', '127.0.0.1', '192.168', '198.168', 'php.jdshipin', '[240', 'ottrrs.hl.chinamobile', 'serv00.bkpcp.top', '122.152.202.33', '1.70.34.19:8084/udp/', '106.111.244.30:3000/rtp/', '14.145.234.231:8888/udp/', '106.111.74.38:10001/rtp/', '106.59.3.147:55555/udp/', '122.224.232.226:8888/udp/', '125.111.12.243:9999/udp/', '183.156.56.79:9999/udp/', '171.117.73.99:8082/rtp/', '60.189.61.9:9999/udp/', '/live/0701', 'ChiSheng9', 'epg.pw', '/hls/', '(576p)', '(540p)', '(360p)', '(480p)', '(180p)', '(404p)', 'r.jdshipin', 'hwltc.tv.cdn.zj.chinamobi', 'ali.hlspull.yximgs', 'generationnexxxt', 'live.goodiptv.club', 'playtv-live.ifeng']  # 定义需要跳过的字符串数组['#', '@', '#genre#'] 
    required_strings = ['://']  # 定义需要包含的字符串数组['必需字符1', '必需字符2'] 

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [
            line for line in file
            if not any(skip_str in line for skip_str in skip_strings) and all(req_str in line for req_str in required_strings)
        ]
    return lines

# 读取文件内容 2
def read_txt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.readlines()

# 读取文件内容 3
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return set(file.readlines())
        
# 追加录入 1
def append_to_file(filename, lines):
    with open(filename, 'a', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')  # 确保每行写入后有换行符
            
# 追加录入 2
def append_to_blacklist(filename, line):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(line)

# 删除空行
def remove_empty_lines(filename):
    # 读取文件内容
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 删除空行
    non_empty_lines = [line for line in lines if line.strip()]

    # 写回文件
    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(non_empty_lines)

# 去重文件内容
def remove_duplicates(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        unique_lines = set(lines)  # 使用集合去重
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(unique_lines)
    except IOError as e:
        print(f'无法读取或写入文件{filename}: {e}')
    
# 格式化频道名称
def process_name_string(input_str):
    parts = input_str.split(',')
    processed_parts = []
    for part in parts:
        processed_part = process_part(part)
        processed_parts.append(processed_part)
    result_str = ','.join(processed_parts)
    return result_str

def process_part(part_str):
    # 处理逻辑
    part_str = part_str.replace("「IPV6」", "")  # 剔除 「IPV6」
    part_str = part_str.replace("IPV6", "")  # 剔除 IPV6
    part_str = part_str.replace("「IPV4」", "")  # 剔除 「IPV4」
    part_str = part_str.replace("IPV4", "")  # 剔除 IPV4 
    part_str = part_str.replace("[V4]", "")  # 剔除 [V4]
    part_str = part_str.replace("[V6]", "")  # 剔除 [V6]
    part_str = part_str.replace("[720p]", "")  # 剔除 [720p]
    part_str = part_str.replace("[1080p]", "")  # 剔除 [1080p]
    part_str = part_str.replace("$1920x1080", "")  # 剔除 $1920x1080
    part_str = part_str.replace("台,http", ",http")  # 替换 台
    part_str = part_str.replace("高清,http", ",http")  # 替换 高清
    part_str = part_str.replace("标清,http", ",http")  # 替换 标清  
    part_str = part_str.replace("視", "视")  # 替换
    part_str = part_str.replace("聞", "闻")  # 替换
    part_str = part_str.replace("衛", "卫")  # 替换
    part_str = part_str.replace("東", "东")  # 替换
    part_str = part_str.replace("華", "华")  # 替换
    part_str = part_str.replace("電", "电")  # 替换
    part_str = part_str.replace("語", "语")  # 替换
    part_str = part_str.replace("間", "间")  # 替换
    part_str = part_str.replace("亞", "亚")  # 替换
    part_str = part_str.replace("線", "线")  # 替换
    part_str = part_str.replace("國", "国")  # 替换
    part_str = part_str.replace("灣", "湾")  # 替换
    part_str = part_str.replace("環", "环")  # 替换
    part_str = part_str.replace("蓮", "莲")  # 替换
    part_str = part_str.replace("鏡", "镜")  # 替换
    part_str = part_str.replace("財經", "财经")  # 替换
    part_str = part_str.replace("凤凰-", "凤凰")  # 替换
    part_str = part_str.replace("鳳凰", "凤凰")  # 替换
    part_str = part_str.replace("凤凰卫视", "凤凰")  # 替换
    part_str = part_str.replace("TVB", "")  # 替换
    part_str = part_str.replace("中天亚洲台", "中天亚洲")  # 替换
    part_str = part_str.replace("广东｜", "")  # 替换
    part_str = part_str.replace("湖南｜", "")  # 替换
    part_str = part_str.replace("翡翠,http", "翡翠台,http")  # 替换
    part_str = part_str.replace("明珠,http", "明珠台,http")  # 替换
    part_str = part_str.replace("频道高清,http", ",http")  # 替换
    part_str = part_str.replace("频道,http", ",http")  # 替换
    part_str = part_str.replace("資訊", "资讯")  # 替换
    part_str = part_str.replace("紀實", "纪实")  # 替换
    part_str = part_str.replace(" HD", "")  # 剔除 HD
    part_str = part_str.replace("HD", "")  # 剔除 HD
    part_str = part_str.replace("𝟘", "0")  # 替换 𝟘
    part_str = part_str.replace("𝟙", "1")  # 替换 𝟙
    part_str = part_str.replace("𝟚", "2")  # 替换 𝟚
    part_str = part_str.replace("𝟛", "3")  # 替换 𝟛
    part_str = part_str.replace("𝟜", "4")  # 替换 𝟜
    part_str = part_str.replace("𝟝", "5")  # 替换 𝟝
    part_str = part_str.replace("𝟞", "6")  # 替换 𝟞
    part_str = part_str.replace("𝟟", "7")  # 替换 𝟟
    part_str = part_str.replace("𝟠", "8")  # 替换 𝟠
    part_str = part_str.replace("𝟡", "9")  # 替换 𝟡
    part_str = part_str.replace("移动咪咕直播", "咪咕体育")  # 替换 移动咪咕直播
    part_str = part_str.replace("咪咕直播", "咪咕体育")  # 替换 咪咕直播
    part_str = part_str.replace("咪咕直播 ", "咪咕体育")  # 替换 咪咕直播
    part_str = part_str.replace("咪咕视频", "咪咕体育")  # 替换 咪咕视频
    part_str = part_str.replace("咪咕体育-", "咪咕体育")  # 替换 咪咕体育
    part_str = part_str.replace("咪咕体育_", "咪咕体育")  # 替换 咪咕体育
    part_str = part_str.replace("咪咕体育 ", "咪咕体育")  # 替换 咪咕体育
    part_str = part_str.replace("•", "")  # 先剔除 •  
    part_str = part_str.replace("_4M1080HEVC", "")  # 剔除
    part_str = part_str.replace("_2.5M1080HEVC", "")  # 剔除
    part_str = part_str.replace(" (1080p)", "")  # 替换 1080p
    part_str = part_str.replace(" (900p)", "")  # 替换 900p
    part_str = part_str.replace(" (720p)", "")  # 替换 720p
    part_str = part_str.replace(" (576p)", "")  # 替换 576p
    part_str = part_str.replace(" (540p)", "")  # 替换 540p
    part_str = part_str.replace(" (480p)", "")  # 替换 480p
    part_str = part_str.replace(" (360p)", "")  # 替换 360p
    part_str = part_str.replace(" (240p)", "")  # 替换 240p
    part_str = part_str.replace(" (180p)", "")  # 替换 180p
    part_str = part_str.replace("  [Geo-blocked]", "")  # 替换[Geo-blocked]

    if "CCTV" in part_str and "://" not in part_str:
        part_str = part_str.replace("PLUS", "+")  # 替换 PLUS
        part_str = part_str.replace("1080", "")  # 替换 1080
        filtered_str = ''.join(char for char in part_str if char.isdigit() or char == 'K' or char == '+')
        if not filtered_str.strip():  # 处理特殊情况，如果发现没有找到频道数字返回原名称
            filtered_str = part_str.replace("CCTV", "")
        if len(filtered_str) > 2 and re.search(r'4K|8K', filtered_str):  # 特殊处理CCTV中部分4K和8K名称
            # 使用正则表达式替换，删除4K或8K后面的字符，并且保留4K或8K
            filtered_str = re.sub(r'(4K|8K).*', r'\1', filtered_str)
            if len(filtered_str) > 2: 
                # 给4K或8K添加括号
                filtered_str = re.sub(r'(4K|8K)', r'(\1)', filtered_str)
        return "CCTV" + filtered_str 
    elif "卫视" in part_str:
        part_str = part_str.replace("-卫视", "卫视")  # 替换 -卫视
        # 定义正则表达式模式，匹配“卫视”后面的内容
        pattern = r'卫视「.*」'
        # 使用sub函数替换匹配的内容为空字符串
        result_str = re.sub(pattern, '卫视', part_str)
        return result_str
    return part_str

def filter_and_save_channel_names(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    processed_lines = []
    for line in lines:
        if ',' in line:
            channel_name, url = line.split(',', 1)
            processed_channel_name = process_name_string(channel_name)
            processed_line = f"{processed_channel_name},{url}"
            processed_lines.append(processed_line)
        else:
            processed_lines.append(line)
    
    with open(input_file, 'w', encoding='utf-8') as out_file:
        for line in processed_lines:
            out_file.write(line)

# 按自选频道提取待检测内容
def filter_channels(channel_file, tv_file, output_file):
	try:
		with open(channel_file, 'r', encoding='utf-8') as ch_file:
			channels = ch_file.readlines()
		
		with open(tv_file, 'r', encoding='utf-8') as tv_file:
			tv_lines = tv_file.readlines()
		
		matched_lines = []
		
		for channel in channels:
			channel = channel.strip()
			if "#genre#" in channel:
				continue  # 跳过包含 "#genre#" 的行
			for tv_line in tv_lines:
				if tv_line.startswith(channel):
					matched_lines.append(tv_line.strip())
		
		with open(output_file, 'w', encoding='utf-8') as out_file:
			for line in matched_lines:
				out_file.write(line + '\n')
				
		print(f"筛选完成，共找到 {len(matched_lines)} 行匹配的内容。")
		
	except Exception as e:
		print(f"发生错误：{e}")
        
# 写入文件内容 1
def write_txt_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n')

# 写入文件内容 2
def write_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)
        
# 写入文件
def write_list(file_path, data_list):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data_list:
            file.write(item + '\n')

# 将iptv.txt转换为iptv.m3u文件
def convert_to_m3u(iptv_file, m3u_file):
    lines = read_txt(iptv_file)
    with open(m3u_file, 'w', encoding='utf-8') as file:
        file.write("#EXTM3U\n")
        for line in lines:
            parts = line.split(',', 1)
            if len(parts) == 2:
                file.write(f"#EXTINF:-1 group-title=\"{group_name}\",{parts[0]}\n")
                file.write(f"{parts[1]}\n")
                
# 增加外部url到检测清单，同时支持检测m3u格式url
# urls里所有的源都读到这里。
def get_url_file_extension(url):
    # 解析URL
    parsed_url = urlparse(url)
    # 获取路径部分
    path = parsed_url.path
    # 提取文件扩展名
    extension = os.path.splitext(path)[1]
    return extension

def convert_m3u_to_txt(m3u_content):
    # 分行处理
    lines = m3u_content.split('\n')
    
    # 用于存储结果的列表
    txt_lines = []
    
    # 临时变量用于存储频道名称
    channel_name = ""
    
    for line in lines:
        # 过滤掉 #EXTM3U 开头的行
        if line.startswith("#EXTM3U"):
            continue
        # 处理 #EXTINF 开头的行
        if line.startswith("#EXTINF"):
            # 获取频道名称（假设频道名称在引号后）
            channel_name = line.split(',')[-1].strip()
        # 处理 URL 行
        elif line.startswith("http://") or line.startswith("https://"):
            txt_lines.append(f"{channel_name},{line.strip()}")
    
    # 将结果合并成一个字符串，以换行符分隔
    return '\n'.join(txt_lines)

def process_url(url):
    try:
        # 打开URL并读取内容
        with urllib.request.urlopen(url) as response:
            # 以二进制方式读取数据
            data = response.read()
            # 将二进制数据解码为字符串
            text = data.decode('utf-8')
            if get_url_file_extension(url) in [".m3u", ".m3u8"]:
                converted_text = convert_m3u_to_txt(text)
                urls_all_lines.extend(converted_text.split('\n'))
            elif get_url_file_extension(url) == ".txt":
                lines = text.split('\n')
                for line in lines:
                    if "#genre#" not in line and "," in line and ("http://" in line or "https://" in line):
                        # 检查并处理 "?key=txiptv" 和 "$LR•"
                        if "?key=txiptv" in line:
                            line = line.split('?key=txiptv')[0]
                        if "$LR•" in line:
                            line = line.split('$LR•')[0]
                        urls_all_lines.append(line.strip())
    
    except Exception as e:
        print(f"处理URL时发生错误：{e}")

if __name__ == "__main__":
    # 定义要访问的多个URL
    urls = [
	'https://raw.githubusercontent.com/yuanzl77/IPTV/main/live.txt',
	'https://raw.githubusercontent.com/Wirili/IPTV/main/live.txt',
	'https://raw.githubusercontent.com/qq49371114/collect-tv-txt/ec97c7ebf5b20965760b59b6a9a6818b82d008a2/live.txt',
	'https://raw.githubusercontent.com/lc529180405/caicai/8be46d9e0b399ba0ddc1b7832b3bd7a236b3c159/%E6%9E%81%E8%A7%86%E8%A7%A3%E5%AF%86.txt',
        'https://raw.githubusercontent.com/suxuang/myIPTV/main/ipv6.m3u',
	'https://raw.githubusercontent.com/iptv-js/iptv-js.github.io/main/ss_itv.m3u',
	'https://raw.githubusercontent.com/250992941/iptv/main/st1.txt',
	'https://raw.githubusercontent.com/Guovin/iptv-api/gd/output/result.txt',
        'https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/merged_output.txt',
        # 'https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/others_output.txt',
        # 'https://raw.githubusercontent.com/alonezou/yn-iptv/main/reference/MyIPTV',
        # 'https://raw.githubusercontent.com/qist/tvbox/master/tvlive.txt',
        # 'https://raw.githubusercontent.com/leyan1987/iptv/main/iptvnew.txt',
        'https://raw.githubusercontent.com/maitel2020/iptv-self-use/main/iptv.txt',
        'https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.txt',
        'https://live.fanmingming.com/tv/m3u/ipv6.m3u',
        'https://cdn.jsdelivr.net/gh/abc1763613206/myiptv@latest/utf8/merged-simple.txt',
        'https://gitlab.com/p2v5/wangtv/-/raw/main/wang-tvlive.txt',
        # 'https://gitlab.com/p2v5/wangtv/-/raw/main/lunbo.txt'
    ]

    urls_all_lines = []

    for url in urls:
        print(f"提取电视频道网址: {url}")
        process_url(url)   # 读取上面url清单中直播源存入 urls_all_lines
        print(f"新获取的电视频道网址行数: {len(urls_all_lines)}")

    # 处理单频道多网址问题
    new_lines = []
    for line in urls_all_lines:
        if '://' in line and '#' in line:
            parts = line.split(',')
            if len(parts) == 2:
                name = parts[0]
                urls = parts[1].split('#')
                for url in urls:
                    new_lines.append(f"{name},{url.strip()}\n")
        else:
            new_lines.append(line)

    print(f"单频道多网址处理后的总行数： {len(new_lines)}")
    
    # 写入 online.txt 文件
    write_txt_file('online.txt',new_lines)
    filter_and_save_channel_names('online.txt')
    remove_empty_lines('online.txt')
    remove_duplicates('online.txt')

    # 读取文件内容
    online_lines = read_file('online.txt')
    blacklist_lines = read_file('blacklist.txt')
    iptv_lines = read_file('iptv.txt')

    # 将 blacklist_lines 和 iptv_lines 转换为集合，并求并集去重
    combined_blacklist_iptv = set(blacklist_lines).union(iptv_lines)

    # 计算 online_lines 与 combined_blacklist_iptv 的差集，并去重
    unique_online_lines = list(set(online_lines) - combined_blacklist_iptv)

    # 将差集写回到 online.txt
    write_file('online.txt', unique_online_lines)
    print(f"本次新获取的网址总行数: {len(unique_online_lines)}")

    # 定义需要保留的IP地址列表
    ips = [
        "60.223.72.118", "222.130.146.175", "124.64.11.135", "118.248.218.7", "119.39.97.2", "58.248.112.205", "120.87.97.246", "27.40.16.70", "/udp/", "/rtp/", "/GD_CUCC/G_", "jxcbn.ws-cdn.gitv.tv"
    ]

    # 读取文件并筛选内容
    with open('online.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 创建一个新文件，用于保存筛选后的内容
    with open('online.txt', 'w', encoding='utf-8') as file:
        for line in lines:
            # 检查当前行是否包含 "CCTV" 或 "卫视" 并且包含至少一个指定的IP地址
            if ('CCTV' in line or '卫视' in line) and any(ip in line for ip in ips):
                file.write(line)
            elif 'CCTV' not in line and '卫视' not in line:
                file.write(line)

    # 读取输入文件内容
    lines1 = read_txt_file('online.txt')
    print(f"本次新获取网址符合筛选条件的行数为 : {len(lines1)}")
    lines2 = read_txt_file('iptv.txt')
    lines=list(set(lines1 + lines2)) #  + lines2
    print(f"与上次有效网址合并后的行数: {len(lines)}")
    write_txt_file('tv.txt',lines)
    remove_duplicates('tv.txt')

    # 按自选频道提取待检测内容到 live.txt 文件
    filter_channels('channel.txt', 'tv.txt', 'live.txt')
    # print(f"待检测文件 live.txt 总行数: {len(live_lines)}")
    # print(f"自定义收藏的频道总数: {len(channel_lines)}")

    # 定义超时时间
    timeout = 3

    # 读取live.txt文件
    try:
        with open('live.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except IOError as e:
        print(f'无法读取文件live.txt: {e}')
        exit()

    # 存储有响应的行到 whitelist.txt ，并记录无响应的行到 blacklist.txt
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
                            append_to_blacklist('blacklist.txt', line)
                except requests.exceptions.Timeout:
                    # 如果超时，打印提示信息
                    print(f'超时错误: {name},{url}')
                    append_to_blacklist('blacklist.txt', line)
                except requests.exceptions.HTTPError as e:
                    # 如果HTTP请求返回了错误的状态码
                    print(f'HTTP错误: {name},{url}, 状态码: {e.response.status_code}')
                    append_to_blacklist('blacklist.txt', line)
                except requests.exceptions.TooManyRedirects:
                    # 如果重定向次数过多
                    print(f'重定向错误: {name},{url}')
                    append_to_blacklist('blacklist.txt', line)
                except (requests.exceptions.URLRequired,
                        requests.exceptions.MissingSchema,
                        requests.exceptions.InvalidSchema):
                    # 如果URL是必须的但未提供，或者URL的方案无效
                    print(f'URL错误: {name},{url}')
                    append_to_blacklist('blacklist.txt', line)
                except requests.exceptions.RequestException as e:
                    # 打印其他异常信息
                    print(f'其他错误: {name},{url}, Error: {e}')
                    append_to_blacklist('blacklist.txt', line)
                
    except IOError as e:
        print(f'无法写入文件 whitelist.txt: {e}')
        exit()

    # 去重 blacklist.txt 文件内容
    remove_duplicates('blacklist.txt')
    # 删除空行
    remove_empty_lines('blacklist.txt')

    # 清空 iptv.txt 文件后读取 channel.txt 文件
    channel_lines = read_txt('channel.txt')
    tv_lines = read_txt_file('whitelist.txt')
    open('iptv.txt', 'w').close()

    # 处理 channel.txt 文件中的每一行
    for channel_line in channel_lines:
        if "#genre#" in channel_line:
            append_to_file('iptv.txt', [channel_line])
        else:
            channel_name = channel_line.split(",")[0].strip()
            matching_lines = [tv_line for tv_line in tv_lines if tv_line.split(",http")[0].strip() == channel_name]
            append_to_file('iptv.txt', matching_lines)

    # 删除空行
    remove_empty_lines('iptv.txt')

    # 定义替换内容
    cctv_channels = """🇨🇳央视频道🇨🇳,#genre#
CCTV1,http://223.105.252.60/PLTV/4/224/3221228581/index.m3u8?servicetype=1
CCTV1,http://223.105.252.8/PLTV/4/224/3221227725/index.m3u8
CCTV1,http://223.105.252.8/PLTV/4/224/3221228049/index.m3u8
CCTV1,http://223.105.252.8/PLTV/4/224/3221228732/index.m3u8
CCTV1,http://b.zgjok.com:35455/itv/6000000001000029752.m3u8?cdn=wasusyt&Contentid=6000000001000029752
CCTV1,http://b.zgjok.com:35455/itv/5000000004000002226.m3u8?cdn=bestzb&Contentid=5000000004000002226
CCTV1,http://b.zgjok.com:35455/itv/1000000005000265001.m3u8?cdn=ystenlive&Contentid=1000000005000265001
CCTV2,http://223.105.252.8/PLTV/4/224/3221228118/index.m3u8
CCTV2,http://b.zgjok.com:35455/itv/1000000001000023315.m3u8?cdn=ystenlive&Contentid=1000000001000023315
CCTV2,http://b.zgjok.com:35455/itv/6000000001000014161.m3u8?cdn=wasusyt&Contentid=6000000001000014161
CCTV3,http://223.105.252.59/PLTV/4/224/3221228499/index.m3u8?servicetype=1
CCTV3,http://223.105.252.8/PLTV/4/224/3221228188/index.m3u8
CCTV3,http://b.zgjok.com:35455/itv/6000000001000022313.m3u8?cdn=wasusyt&Contentid=6000000001000022313
CCTV3,http://b.zgjok.com:35455/itv/1000000005000265003.m3u8?cdn=ystenlive&Contentid=1000000005000265003
CCTV4,http://223.105.252.8/PLTV/4/224/3221227489/index.m3u8
CCTV4,http://223.105.252.8/PLTV/4/224/3221228156/index.m3u8
CCTV4,http://b.zgjok.com:35455/itv/5000000011000031102.m3u8?cdn=bestzb&Contentid=5000000011000031102
CCTV4,http://b.zgjok.com:35455/itv/1000000005000265004.m3u8?cdn=ystenlive&Contentid=1000000005000265004
CCTV5,http://223.105.252.61/PLTV/4/224/3221228502/index.m3u8?servicetype=1
CCTV5,http://223.105.252.8/PLTV/4/224/3221228173/index.m3u8
CCTV5,http://223.105.252.8/PLTV/4/224/3221228082/index.m3u8
CCTV5,http://b.zgjok.com:35455/itv/1000000005000025222.m3u8?cdn=ystenlive&Contentid=1000000005000025222
CCTV5,http://b.zgjok.com:35455/itv/1000000005000265005.m3u8?cdn=ystenlive&Contentid=1000000005000265005
CCTV5+,http://223.105.252.8/PLTV/4/224/3221228076/index.m3u8
CCTV5+,http://223.105.252.8/PLTV/4/224/3221228114/index.m3u8
CCTV5+,http://b.zgjok.com:35455/itv/6000000001000015875.m3u8?cdn=wasusyt&Contentid=6000000001000015875
CCTV5+,http://b.zgjok.com:35455/itv/1000000005000265016.m3u8?cdn=ystenlive&Contentid=1000000005000265016
CCTV6,http://223.105.252.8/PLTV/4/224/3221228185/index.m3u8
CCTV6,http://b.zgjok.com:35455/itv/1000000001000001737.m3u8?cdn=ystenlive&Contentid=1000000001000001737
CCTV6,http://b.zgjok.com:35455/itv/6000000001000004574.m3u8?cdn=wasusyt&Contentid=6000000001000004574
CCTV6,http://b.zgjok.com:35455/itv/1000000005000265006.m3u8?cdn=ystenlive&Contentid=1000000005000265006
CCTV7,http://b.zgjok.com:35455/itv/1000000001000024341.m3u8?cdn=ystenlive&Contentid=1000000001000024341
CCTV7,http://b.zgjok.com:35455/itv/6000000001000009055.m3u8?cdn=wasusyt&Contentid=6000000001000009055
CCTV7,http://b.zgjok.com:35455/itv/1000000005000265007.m3u8?cdn=ystenlive&Contentid=1000000005000265007
CCTV8,http://223.105.252.57/PLTV/3/224/3221228165/index.m3u8?servicetype=1
CCTV8,http://223.105.252.8/PLTV/4/224/3221228079/index.m3u8
CCTV8,http://b.zgjok.com:35455/itv/6000000001000001070.m3u8?cdn=wasusyt&Contentid=6000000001000001070
CCTV8,http://b.zgjok.com:35455/itv/1000000005000265008.m3u8?cdn=ystenlive&Contentid=1000000005000265008
CCTV9,http://223.105.252.8/PLTV/4/224/3221228758/index.m3u8
CCTV9,http://b.zgjok.com:35455/itv/1000000001000014583.m3u8?cdn=ystenlive&Contentid=1000000001000014583
CCTV9,http://b.zgjok.com:35455/itv/6000000001000032162.m3u8?cdn=wasusyt&Contentid=6000000001000032162
CCTV9,http://b.zgjok.com:35455/itv/1000000005000265009.m3u8?cdn=ystenlive&Contentid=1000000005000265009
CCTV10,http://b.zgjok.com:35455/itv/1000000001000023734.m3u8?cdn=ystenlive&Contentid=1000000001000023734
CCTV10,http://b.zgjok.com:35455/itv/5000000004000012827.m3u8?cdn=bestzb&Contentid=5000000004000012827
CCTV10,http://b.zgjok.com:35455/itv/1000000005000265010.m3u8?cdn=ystenlive&Contentid=1000000005000265010
CCTV11,http://b.zgjok.com:35455/itv/5000000011000031106.m3u8?cdn=bestzb&Contentid=5000000011000031106
CCTV11,http://b.zgjok.com:35455/itv/1000000005000265011.m3u8?cdn=ystenlive&Contentid=1000000005000265011
CCTV12,http://b.zgjok.com:35455/itv/1000000001000032494.m3u8?cdn=ystenlive&Contentid=1000000001000032494
CCTV12,http://b.zgjok.com:35455/itv/6000000001000022586.m3u8?cdn=wasusyt&Contentid=6000000001000022586
CCTV12,http://b.zgjok.com:35455/itv/1000000005000265012.m3u8?cdn=ystenlive&Contentid=1000000005000265012
CCTV13,http://b.zgjok.com:35455/itv/5000000011000031108.m3u8?cdn=bestzb&Contentid=5000000011000031108
CCTV13,http://b.zgjok.com:35455/itv/1000000002000021303.m3u8?cdn=ystenlive
CCTV14,http://b.zgjok.com:35455/itv/1000000001000008170.m3u8?cdn=ystenlive&Contentid=1000000001000008170
CCTV14,http://b.zgjok.com:35455/itv/5000000004000006673.m3u8?cdn=bestzb&Contentid=5000000004000006673
CCTV14,http://b.zgjok.com:35455/itv/1000000005000265013.m3u8?cdn=ystenlive&Contentid=1000000005000265013
CCTV15,http://b.zgjok.com:35455/itv/5000000011000031109.m3u8?cdn=bestzb&Contentid=5000000011000031109
CCTV15,http://b.zgjok.com:35455/itv/1000000005000265014.m3u8?cdn=ystenlive&Contentid=1000000005000265014
CCTV16,http://223.105.252.59/PLTV/4/224/3221228314/index.m3u8?servicetype=1
CCTV16,http://b.zgjok.com:35455/itv/1000000006000233002.m3u8?cdn=ystenlive&Contentid=1000000006000233002
CCTV16,http://b.zgjok.com:35455/itv/5000000008000023254.m3u8?cdn=bestzb&Contentid=5000000008000023254
CCTV17,http://223.105.252.8/PLTV/4/224/3221228642/index.m3u8
CCTV17,http://b.zgjok.com:35455/itv/1000000006000268004.m3u8?cdn=ystenlive&Contentid=1000000006000268004
CCTV17,http://b.zgjok.com:35455/itv/1000000005000265015.m3u8?cdn=ystenlive&Contentid=1000000005000265015
CCTV4K,http://223.105.252.60/PLTV/4/224/3221228472/index.m3u8?servicetype=1

CCTV1,https://www.freetv.top/migu/608807420.m3u8?migutoken=5b04cf0d91179ab2d3d71703f0a8bc3d32dd02f7d8fb55ee70e05c216b8a9d1a73d911fbde798459fb66d94934157c996f8306c0dd37917775f2ed73dcc22cf84b25ca500bff5c636ff48d6344
CCTV2,https://www.freetv.top/migu/631780532.m3u8?migutoken=11ecfe0a296dcd532df72244565e20008b5a2e6936c05e73d9c90abe54b5bbffc942f2912e3fdd518714c4a7ad984beed028d07db3d49b8d1e21c54686ebfa8546f79a57d969866753cca722cc
CCTV3,https://www.freetv.top/migu/624878271.m3u8?migutoken=380a18fe8dc81109270780918e605114ca218bcfa395aaa8682b605d1622439ffe7981dbd10f378c9c045f872d48dce39babcb012c7362dc8b21835e88fde6457bacaa4082c74879d64ad7aee4
CCTV4,https://www.freetv.top/migu/631780421.m3u8?migutoken=fefc6a44400a0dd448699ae0ce3d6e2c5a0f49b8d48adb36e747c4fbab039337eb3244f9951acbddaf26b7bf51597a7d1b43c8845e67fd5914ece875dcad325bb388200bc0f12fdff727d03e2d
CCTV4,https://www.freetv.top/migu/608807416.m3u8?migutoken=94d24df192f212e52d7c222dfab7df5ce4aad53db2766a6c4275a4c1e796cf13fb231906f792af9bc717ce1ccafa62165ebdc66b02fb0882cd5beac443921d36883a491d2b549a5509d63534e1
CCTV5,https://www.freetv.top/migu/641886683.m3u8?migutoken=3e5c01f93922de8d1c940fe15bb47349b27e8f7a2e624dde1a83dff3b2a80f58b7624151a3a4d00488edee34f202818557340903382fae02bb754084eb942bd50e59061df36fab62fb5b908903
CCTV5+,https://www.freetv.top/migu/641886773.m3u8?migutoken=03a1b82e35e58cd89a95034ecb29e77e50493397000ec2b1e4d1ce59af01e6420d6dbc068c8230ec03be3a35a20eed8714e0959e3570a08713a7a2e8d86085eabf8f1aa85744c80c38343988b2
CCTV6,https://www.freetv.top/migu/624878396.m3u8?migutoken=8e4f91b7950497f8570c74e50003b7fa23f6565c16a6b361ff855d3a969ddf7ea3826b04d20d76b6eeb472f0cb8b86284614a835429165709ec8c3055f8e9a7879e9594a4309b5d50f59f8a535
CCTV7,https://www.freetv.top/migu/673168121.m3u8?migutoken=a878b713604abd82c57cce75de174e0284d3f101e21d0c3e362670e4b5a5e75d9b42846e5e0adf92c1ad15c63d60934f3e68c25f787bc0665d12acde75a6db4761278e79b762292ed5b5a2fae3
CCTV8,https://www.freetv.top/migu/624878356.m3u8?migutoken=170b73b07e0cf0d307afea3545da5b9609d7c15461a2f4ac0f43634101df9baf391a446b91e5f84446b6a3b0934bb4730e2f3c4a32a565f904f22c8ff745a094d45dfd49c54f31b0b78156a080
CCTV9,https://www.freetv.top/migu/673168140.m3u8?migutoken=749c49cdc31bb395e0349adc81010adc8707f80e51e9d3491ad67bfa71388ad768f7b52c8064338a7ef45eb7ddb192fb4937b21681c82499a0c16653ad9a9bec98ff5ce6ab183e4029bbdf269e
CCTV10,https://www.freetv.top/migu/624878405.m3u8?migutoken=07b6e1d4124dd85ca8138b8d8dcd646323952053748d7d5ac0a2b31dcb6626c605fb05470545bd0f7e0d23e807e6909b517b2b8b5e2eaa926600edaa15d80aee9b900245924108c86040411cd4
CCTV11,https://www.freetv.top/migu/667987558.m3u8?migutoken=16827d54043eba69d051685229b1d0623c01f398f643b3a7d912c9929d6525025ef57eb61666d45bb70dfc86405aa336ca762f0bda4f0284d98eddae4042805df42661f954a1d40820829ec8c2
CCTV12,https://www.freetv.top/migu/673168185.m3u8?migutoken=37acadb43b1d7932b0a1e8a4f2d01a06b42a10c31f3ccb417bae200ac3028f30a8110509f2cd6cd130aee4b21c85693aa49817f3381e4d28e140d8db1a20b6fecea22fec17a70ff1341efe6081
CCTV13,https://www.freetv.top/migu/608807423.m3u8?migutoken=ac19a58805588401a8e818b6dd00df9b327912af3611ba95f89235e7020821668a2b6dc65ccc3904967da59d0a9742565c56ea582baf8915d068035054818ef0f369dab64705a6a7f7120529ec
CCTV14,https://www.freetv.top/migu/624878440.m3u8?migutoken=239edad94ac0bbff14f123c7f8996ed7639110bd6cf64ec8ba8cf85842224956d452ec8b683385cb27f8a7685224a03e3aa4d914b8fe33249da9df699351b105c795452d03f2be0a1f1e39adb0
CCTV15,https://www.freetv.top/migu/673168223.m3u8?migutoken=4e8d5766579c6bef231494cabd07e5b49d965804790214280c9791e4c331fd90311cb62ea43d3a1899229bfa57be4afe5a567b32a6b78153fc9a9801e28a39435e078b48c211e71d6083519be4
CCTV17,https://www.freetv.top/migu/673168256.m3u8?migutoken=11fec7586772852c5b34d75ff515080f8def9861a030c98c5861b036729d642445a7bc5b0cd43e7086ca1903346f6cbad01b639771ee3bd13e653bdb2d14f169744862c9695688b0b177bc144a

CCTV1,https://stream1.freetv.fun/2622897affd8a1c93ab36252984ab0e499d1e4a6fc76b87e6ef8039de3f2e642.ctv
CCTV1,https://stream1.freetv.fun/5bbc3404506a5bf8c5acf95d0ffb4d15166cfb11ba4ba1c3546e0c8665be81ee.m3u8
CCTV1,https://stream1.freetv.fun/0ef91c51031b7772fdb7b080bc006776d112c7d029b86cfca9bad6c4294c53bb.m3u8
CCTV1,https://stream1.freetv.fun/c1980814348616ed0068602a3398b361096544f6d026830ceb16352b979defda.ctv
CCTV1,https://stream1.freetv.fun/149d9ac1b6234f41c3e61634bbcb0508dee05c6abcb3d3d0486431e52151e0d0.m3u8
CCTV1,https://stream1.freetv.fun/607c5648b5a826285f1e94ceab76066c767e2ba5e1623b753a6ab2f4e380199d.m3u8
CCTV1,https://stream1.freetv.fun/d6bfd8367a905e4c7d8f024b5d501f81a0dec4e08379ce380ca66ca9ab5f46dd.m3u8
CCTV1,https://stream1.freetv.fun/4a250dafef7349ead704088bec3993f3cd3b2cdcb604f23bbf700da31434fa08.ctv
CCTV1,https://stream1.freetv.fun/9b729e6c878984d044d0552a24528d74fe7ef50bf62542ff952688d80f70e770.m3u8
CCTV2,https://stream1.freetv.fun/8d9a2d76a0d819bf594bd8698a0ceadca5d3ac2b1b44321ab0cc534ebd1c4cd6.ctv
CCTV2,https://stream1.freetv.fun/71e7c1e67a4283a1ec8dd3155c656c1317dc59e0fb20d7e24f63542b6028f8d7.m3u8
CCTV2,https://stream1.freetv.fun/d6c1a851f2f79d30809b9559aadfaf6c70046913a43b61cda0b653a877209d0e.m3u8
CCTV2,https://stream1.freetv.fun/13d0211c9d0e6ac956f262af910b0509c7565f9f7f3f5a674a33d40b534a7cc1.m3u8
CCTV2,https://stream1.freetv.fun/6a2c9e86b4092dcd312be0cacb94bd3806238b31997dd297385cbf984420828d.ctv
CCTV2,https://stream1.freetv.fun/9ba314c84bd36124cc9806d480d73e8809c69b0aac8ce8cd70139e74f13e2f33.m3u8
CCTV2,https://stream1.freetv.fun/0ff1a5df634b89d961ceb79e32ec6f09791aeca7014e15f5f8c6b8a92f5af3f1.ctv
CCTV2,https://stream1.freetv.fun/b1588dff37e0c4db282c42aef4ee6913d38baec2e947a471c86cd0c094f65ae3.ctv
CCTV2,https://stream1.freetv.fun/c211dc7c7e361326eeb316f377006a6121762f74c3888cffce2ca82411c5d284.m3u8
CCTV2,https://stream1.freetv.fun/b46b78534d93d0c3b6d961ef93a23b3f12e06f7fc73d8a1f622f04cae349de1c.ctv
CCTV2,https://stream1.freetv.fun/0ff1a5df634b89d961ceb79e32ec6f09791aeca7014e15f5f8c6b8a92f5af3f1.ctv
CCTV3,https://stream1.freetv.fun/1e0e775744a98d3524e67d4b4da0a9bc3c0b9cb9fbdf47fe76a0413a4089b940.m3u8
CCTV3,https://stream1.freetv.fun/67550102420f875410d82eadd06d8c5996bfe637b26fb81bc96e7bfdb4f847b5.ctv
CCTV3,https://stream1.freetv.fun/31f5ee8674a8a9d1ab3228b40633e66a0300ce8b13b8cf4c1b7afa823ec93d64.m3u8
CCTV3,https://stream1.freetv.fun/8a6cbcdb4071b1aa89939b4c6364953d72025887869a001b8a9c08e2b3357281.ctv
CCTV4,https://stream1.freetv.fun/3608077903f414206083459a194ad0afafbbc87556755b042a0d675e387be6c7.ctv
CCTV4,https://stream1.freetv.fun/073a7a20c7c82d7ceb470e74777815cfbcd8461b065c5768c30ed00ce0bc6c4a.m3u8
CCTV4,https://stream1.freetv.fun/c9637ca4bdf1ba941ba9a79046e9382a1f26782cf90b7ada3cda36be27889e82.ctv
CCTV4,https://stream1.freetv.fun/5fc5fb89a1b7aea2834688eb0fc431436d4eb0a1f34db20cc6fa40699fcd6db7.m3u8
CCTV4,https://stream1.freetv.fun/c12729822e0fe7b91e322f89dd761e03bd1ee6339eb3b1543f1adb5584f16785.m3u8
CCTV4,https://stream1.freetv.fun/a88d74532ae065bcc0328e4448f4298a0722666413689773b636d0763bdaa1db.m3u8
CCTV4,https://stream1.freetv.fun/a6c86a441e9776abf1ffde89d18beebdb98d43b7ed0d121d0ded0fc1025e22ea.ctv
CCTV4,https://stream1.freetv.fun/4d07bdd45298f5188e1e215d557f8b1703d924d4e874e864fd160d4d7f3cae16.ctv
CCTV4,https://stream1.freetv.fun/2b1c2efaf3b5bc72e41a4b652e155ee5243e8066e2a37ef2a43e2ed867c215a2.ctv
CCTV5,https://stream1.freetv.fun/2725c98e410f72e6320bdeb02aa0ef3e9bd353cc38509aaab3895aa7ed16fa45.m3u8
CCTV5,https://stream1.freetv.fun/d76272788c0a406039794e28e4c72c796d1c105fae170cd60a5ae328aa569365.ctv
CCTV5,https://stream1.freetv.fun/7d7df5cd6969d6a9fbc902e327bc66b1174986e528924abef67eb8543e99ea06.ctv
CCTV5,https://stream1.freetv.fun/5e8c1e3a97a30f74d4a12db63254feca462e6dc5d0b668092ce1315d96d67613.ctv
CCTV5,https://stream1.freetv.fun/780a35a365d4238b8d83ea1580611ed45b573caed78c7b5761d99bb1a7cff839.m3u8
CCTV5,https://stream1.freetv.fun/accbf0e5bbc0632b079adca755b64e20a1ffa9589b1ed1146aadc6e8558f7c8d.ctv
CCTV5+,https://stream1.freetv.fun/8156da2fe8060843daeeda9f71f11a274b5bca4a1e75bbd2762fac959fffce22.m3u8
CCTV5+,https://stream1.freetv.fun/a738860ec7fcaf655c7db23c3d6ef52d023e652b5486379db530287184dad292.ctv
CCTV5+,https://stream1.freetv.fun/d1d492a153f75164cbbc0fde6fd4a17844d27c977dc2c4849861b14a223df9b0.ctv
CCTV5+,https://stream1.freetv.fun/397c743d62e0d6a5e3414609c8ea6941dfb022ebb8428d51267051ad8d78ce10.m3u8
CCTV5+,https://stream1.freetv.fun/7e18319834d88b172f57a3a019b567924e6a1e301d05029af46a4f95fcf9531c.ctv
CCTV5+,https://stream1.freetv.fun/bc0a8ca1ad48fe0d260a2f54585f64e847ac6f4501cd7a1957232a4f2377ed84.m3u8
CCTV5+,https://stream1.freetv.fun/dd4ce88d00fc9b0213a1bdbef1e4e813b48cc5f109b32bd29c93b11e30dc94f7.m3u8
CCTV6,https://stream1.freetv.fun/753fe6b20478c17a39f0c17d3c8d98a74cd5890a6e40f4ce011380f2dd185285.m3u8
CCTV7,https://stream1.freetv.fun/ac01cb50d02dc19b524e493e1d65202f058f6d2061d1d137e70d84fc4b1ff86f.m3u8
CCTV7,https://stream1.freetv.fun/4a0ac0d84597cfee83015f10200c708839dd537debc156dd2281684ae77cac4f.m3u8
CCTV7,https://stream1.freetv.fun/3907d514e131537af842b16adde9cc50d9981420a474f2c524cdbfa6d7d95d72.ctv
CCTV7,https://stream1.freetv.fun/b57c61a1dd819c5be3348b18d2486223834c75750d22e1fe058f750e2584abf9.m3u8
CCTV7,https://stream1.freetv.fun/79834e11f92f2d6a40ee7474e2f8f01a88c85e5d84b33a7f0ab13d67b0604a88.m3u8
CCTV7,https://stream1.freetv.fun/7e45fbd69537e594c3083a728995574ce8ead7de2ea591354d76e1729391dd91.m3u8
CCTV7,https://stream1.freetv.fun/978492b187939ceb862410f14e3321d54e05a0bc645f85f48c426b0e522eb940.m3u8
CCTV7,https://stream1.freetv.fun/f889cdbf4d2d3a70d08b3605611400b99378b308efa1290fba013383ba456ea9.m3u8
CCTV8,https://stream1.freetv.fun/77bb0307b4fe088ef0be2ae8fa3f0c537e9e9c0454cf325c380ba9d3abef4bab.ctv
CCTV8,https://stream1.freetv.fun/b6d81e99d0954e264b98373ee10d495fb4f3dc7f99293185ee8a7470870cf323.m3u8
CCTV8,https://stream1.freetv.fun/bf04aadae6b900db1b404cc8a35789a737c58049146a4d49a9825090217ae00d.m3u8
CCTV8,https://stream1.freetv.fun/12222da81a59a4b766eebab3c8c43f4fa910637ea182be42e2affdae3ebb845c.ctv
CCTV8,https://stream1.freetv.fun/baa0d0242fdd3f96a5009fbf567de6784c786c69a2049fb78ef11f8328434414.m3u8
CCTV8,https://stream1.freetv.fun/49d41c76d6565831788110b63fa3da2da2328001e2c97f231edbe945e6c279ab.m3u8
CCTV8,https://stream1.freetv.fun/cb997f441801a5bca8c092be9816cd3915e26d24e20df6a2e511d3c750eea86e.ctv
CCTV8,https://stream1.freetv.fun/113f0eb04d33840b7642af563255df49292c8d9c7755bf498df78cb7a315f322.m3u8
CCTV8,https://stream1.freetv.fun/f93e3ef4f01e4696e90224ac98d6232c9b3e307da4eeb4309082d7df89c83049.m3u8
CCTV9,https://stream1.freetv.fun/57b417007b9bde2713ab0b6c1f25399e0da6a5fda1443d33d81fc0ba399e6bae.ctv
CCTV9,https://stream1.freetv.fun/0cd339b78afee0cc32527d165fe97eecbc28fded481d3730868ef61a6becd337.m3u8
CCTV9,https://stream1.freetv.fun/8018c16acc619fecdaec2bd0835eaf3e5150df066a7a5d39e76d036ca2ca597e.ctv
CCTV9,https://stream1.freetv.fun/51b9eb3e1828772469c7bb5bd874d966e4c8b4d3751e4a358484428961897798.m3u8
CCTV9,https://stream1.freetv.fun/d7e6e14441711b44112b694d4bd4878507bfcb184e1c00c42d88cd82cb56a875.m3u8
CCTV10,https://stream1.freetv.fun/42171068f1cd623e711b6a2434af0f7c2aa912dac5cddd30f68d737df451cd90.m3u8
CCTV10,https://stream1.freetv.fun/65a98eb1bc5fc38505f2c025c2f0c88f31429e43104486845616deb65bf9c895.m3u8
CCTV10,https://stream1.freetv.fun/fe9f2e0bdadda39351ab26f29af49cef76523ead5679d9cb408252373361a4cf.m3u8
CCTV10,https://stream1.freetv.fun/29806059eb936e2abfc8b61bd53f1b6fe901050316c0a6c9e9b03df8f6e48eda.ctv
CCTV10,https://stream1.freetv.fun/b51bbc93a0ca00331294471c9b5150211a8eb32ddcb0b0ea143091926a7c6707.ctv
CCTV10,https://stream1.freetv.fun/0dcbed2ed662304a0dfedbfd136a829adf1c5248c533627626fddff02fb1b19f.m3u8
CCTV10,https://stream1.freetv.fun/090aa26df13ffbe97fa2de0bb57f14db7049f21c8de11f570b67151987eba9b1.m3u8
CCTV11,https://stream1.freetv.fun/616b4d014e0a73846bdb9ddddfdd777f9e0f2c132b2e00e12ad171e2081b0dbb.ctv
CCTV11,https://stream1.freetv.fun/a2291aca1f34c2adb00726f287981230a15e9fe84c5350e104f7704947052e52.m3u8
CCTV11,https://stream1.freetv.fun/17d891eae505df11015721769460efb5710e894fe09b781364d6b052e6255b4e.m3u8
CCTV11,https://stream1.freetv.fun/ebd5a275ee95ecb232efa907676ef78adce2563574fb22a99c2e6ab1f6ab8aa4.m3u8
CCTV11,https://stream1.freetv.fun/222e5acc7866c0e2fe01b374b508bf8afa6dbda8c6fea5d2c777cdc26849145c.ctv
CCTV11,https://stream1.freetv.fun/3f3cbe35e4ab51d5138589e61d79f5d29e6862401940478ddfa92fb6fcd8a874.ctv
CCTV11,https://stream1.freetv.fun/8feb8630d696cc1b00fc6689b933f13c899a4326fd16df1bdba40c6acd1df63e.ctv
CCTV11,https://stream1.freetv.fun/37b1c14c3378e510bd07d553a1abcca238f13e040b5b0419b3ece2c9d4f50efd.m3u8
CCTV11,https://stream1.freetv.fun/b295e709dd85615bdf34e8da41eb11931d04f54e06fe15c04652d69725f20095.ctv
CCTV11,https://stream1.freetv.fun/5dbd245a555927b83eaaa0569010e99d401cbe9f967f1340a89d775d9fcee7c5.ctv
CCTV11,https://stream1.freetv.fun/a296e075276025c13fccaa815a2a2968db83b532e3dcdd87dea6d56e3b63152a.m3u8
CCTV12,https://stream1.freetv.fun/6f4520a649957c1068efd36c848b994de2752266a929a4f9a50dba84b9baf9b7.m3u8
CCTV12,https://stream1.freetv.fun/72ad99a6a08c58c24868d3abddb6c4f7c8ac34a49c55133b957ff50d418f183f.m3u8
CCTV12,https://stream1.freetv.fun/42b9da7874bd097fc9b95c08d837ddb299c57b1ac31f0f0a65c40e1e3754fe64.m3u8
CCTV12,https://stream1.freetv.fun/87253b3afaea039178ade58ec1a91b1e62964839905c18240f5e1ee7bb8c7e20.m3u8
CCTV12,https://stream1.freetv.fun/b73ee2b727afd85eba854a5fed7ea89a3d35e04d7bc047e3189539033a645bfa.m3u8
CCTV12,https://stream1.freetv.fun/5aee327d1fa40207dbc2d04edd97fb791aa33a91e463bdc239c264bae47c8917.ctv
CCTV13,https://stream1.freetv.fun/f2306dc938a374481649dfb8c0cd797ab83abfaf988502de3b6d40a6ce6afdb0.ctv
CCTV13,https://stream1.freetv.fun/7f6fc8f839092b3aba26e188a3942c9fe7c7f2f3b556980df52662a617cfa505.ctv
CCTV13,https://stream1.freetv.fun/1b89d8d6ae59418c102421ce1be0b4a40498dc99decb938fc29c7703155209dd.m3u8
CCTV13,https://stream1.freetv.fun/d8d86dede808358d248bad6c290eba43f63be54e467ea3865a0140b3fb9e5f25.ctv
CCTV13,https://stream1.freetv.fun/5eff6ce6035c5ed07464e6c1a9482968c86bde95d5625615c4b87c15ef745dba.m3u8
CCTV13,https://stream1.freetv.fun/74f4294d741c39834300c655a0ac349f2700bfc45ea342f606214ea5d7a9d63c.m3u8
CCTV13,https://stream1.freetv.fun/09de0a5e75b077877a760a27b04d6732e3f5656cc7b528f55f6b82e2302b6af1.m3u8
CCTV13,https://stream1.freetv.fun/8d8f5970c3388f0b49026ce8ed37a9ab37e33a9d29b7dd4152a05c1332ccc78b.ctv
CCTV14,https://stream1.freetv.fun/5d7dfa5ebfe90c78b537cdc5dd77be50a3ed19ffe163aa50de5f4d79dd2ab3db.m3u8
CCTV14,https://stream1.freetv.fun/318722914b0180a05ca32723cab95d2e8986a6a28fb451445a2c009279f230be.ctv
CCTV14,https://stream1.freetv.fun/ec6cca0d950b307badac42da39616f13a2e1bfb5665b62b3a9ee9a0468fadb01.m3u8
CCTV14,https://stream1.freetv.fun/5d7dfa5ebfe90c78b537cdc5dd77be50a3ed19ffe163aa50de5f4d79dd2ab3db.m3u8
CCTV14,https://stream1.freetv.fun/9c73daa5c22a14745357255f55b73b65ab6bab976d1309bfe949de363622e36a.ctv
CCTV14,https://stream1.freetv.fun/9464d9316b694b16079afcdf56c5088fffdb0df6370b95375beb5fec3f218f7b.ctv
CCTV14,https://stream1.freetv.fun/810e8e594bbd7f110f164ca1f3297900a5be91468d81db0d55494d7a6f79eb19.m3u8
CCTV14,https://stream1.freetv.fun/83a5ea04ac7da0fa2e3ed621143ca53103245ebfb826bd308fe842712076b7b0.ctv
CCTV15,https://stream1.freetv.fun/534a5dadcb442d7203e015924ff89c9f43a1e1715ef63652842020ac26244a9a.ctv
CCTV15,https://stream1.freetv.fun/15e51c168d37c7ad9fefc926fd97d95acb42b1d61d80f05b58514b725089a9e3.ctv
CCTV15,https://stream1.freetv.fun/ba41afeb2715156d503ae2a1166012dec7e28c1be0ae9f6bf8a726c1cc66f3bf.ctv
CCTV15,https://stream1.freetv.fun/f5c27d1a459fea9505fe0eaff71c5f8b814a01876be632f11f1251180cd55f9b.m3u8
CCTV15,https://stream1.freetv.fun/409bdf1e83ced37ad86108df4798cec0286376e4b8065d4ac68565d95a7ed498.m3u8
CCTV15,https://stream1.freetv.fun/f1a2c6adb5b41e31363de9b99423eed7f6d9e35cede0a97f43e9b93781dc5933.ctv
CCTV15,https://stream1.freetv.fun/cbe825bf5f80f456b334a01413e11a83d5e5815a60ab7ab9367b5749adb15d29.m3u8
CCTV16,https://stream1.freetv.fun/90bfaec7908423d502fc444f46d6aa727f5b5d36f67d3492d2ddaa559108372e.m3u8
CCTV16,https://stream1.freetv.fun/1efb3b3242cec8c7865bd2a0b573ed5afb6985dcd408f266521caa1129ebb33f.m3u8
CCTV16,https://stream1.freetv.fun/c5d42167537a4101cb257e27c29869facbd810e19919d6ca1da4e21abaacc375.m3u8
CCTV17,https://stream1.freetv.fun/729d6da4250333089328d271afbcba771d3f41358efcd66fb9d566bb04a5b312.m3u8
CCTV17,https://stream1.freetv.fun/7722c1e3183b440700b138ddf95cafd8a95c2f218dbb73c20e6db5e579508b94.ctv
CCTV17,https://stream1.freetv.fun/e8e291ce45145b5fdc423db3f671fb193731ce7342ee1b7a33683f37999cba3d.ctv
CCTV17,https://stream1.freetv.fun/fc81fbbacfb04b0ae81bfbc0af49b5e3fbdbf25db51c927dcf1d3b4221651cdc.m3u8"""

    satellite_channels = """🛰️卫视频道🛰️,#genre#
湖南卫视,http://b.zgjok.com:35455/itv/5000000004000006692.m3u8?cdn=bestzb&Contentid=5000000004000006692
湖南卫视,http://b.zgjok.com:35455/itv/1000000005000265024.m3u8?cdn=ystenlive&Contentid=1000000005000265024
浙江卫视,http://223.105.252.8/PLTV/4/224/3221228147/index.m3u8
北京卫视,http://223.105.252.8/PLTV/4/224/3221228115/index.m3u8
东方卫视,http://223.105.252.8/PLTV/4/224/3221228150/index.m3u8
江苏卫视,http://223.105.252.8/PLTV/4/224/3221228099/index.m3u8
江苏卫视,http://223.105.252.8/PLTV/4/224/3221228735/index.m3u8
江苏卫视,http://223.105.252.8/PLTV/4/224/3221228738/index.m3u8
江苏卫视,http://223.105.252.8/PLTV/4/224/3221228741/index.m3u8
江苏卫视,http://223.105.252.8/PLTV/4/224/3221228744/index.m3u8
江苏卫视,http://223.105.252.8/PLTV/4/224/3221228747/index.m3u8
江苏卫视,http://223.105.252.8/PLTV/4/224/3221228750/index.m3u8
江苏卫视,http://223.105.252.8/PLTV/4/224/3221228803/index.m3u8
广东卫视,http://223.105.252.8/PLTV/4/224/3221227445/index.m3u8
山东卫视,http://223.105.252.8/PLTV/4/224/3221227448/index.m3u8
北京卫视,http://b.zgjok.com:35455/itv/1000000005000265027.m3u8?cdn=ystenlive&Contentid=1000000005000265027
安徽卫视,http://b.zgjok.com:35455/itv/1000000001000030159.m3u8?cdn=ystenlive&Contentid=1000000001000030159
安徽卫视,http://b.zgjok.com:35455/itv/1000000005000265025.m3u8?cdn=ystenlive&Contentid=1000000005000265025
东南卫视,http://b.zgjok.com:35455/itv/5000000004000010584.m3u8?cdn=bestzb&Contentid=5000000004000010584
东南卫视,http://b.zgjok.com:35455/itv/1000000005000265033.m3u8?cdn=ystenlive&Contentid=1000000005000265033
甘肃卫视,http://b.zgjok.com:35455/itv/5000000011000031121.m3u8?cdn=bestzb&Contentid=5000000011000031121
广东卫视,http://b.zgjok.com:35455/itv/1000000001000014176.m3u8?cdn=ystenlive&Contentid=1000000001000014176
广东卫视,http://b.zgjok.com:35455/itv/1000000005000265034.m3u8?cdn=ystenlive&Contentid=1000000005000265034
广西卫视,http://b.zgjok.com:35455/itv/5000000011000031118.m3u8?cdn=bestzb&Contentid=5000000011000031118
贵州卫视,http://b.zgjok.com:35455/itv/5000000004000025843.m3u8?cdn=bestzb&Contentid=5000000004000025843
海南卫视,http://b.zgjok.com:35455/itv/5000000004000006211.m3u8?cdn=bestzb&Contentid=5000000004000006211
河北卫视,http://b.zgjok.com:35455/itv/5000000006000040016.m3u8?cdn=bestzb&Contentid=5000000006000040016
河南卫视,http://b.zgjok.com:35455/itv/5000000011000031119.m3u8?cdn=bestzb&Contentid=5000000011000031119
黑龙江卫视,http://b.zgjok.com:35455/itv/1000000001000001925.m3u8?cdn=ystenlive&Contentid=1000000001000001925
黑龙江卫视,http://b.zgjok.com:35455/itv/1000000005000265029.m3u8?cdn=ystenlive&Contentid=1000000005000265029
湖北卫视,http://b.zgjok.com:35455/itv/1000000001000024621.m3u8?cdn=ystenlive&Contentid=1000000001000024621
湖北卫视,http://b.zgjok.com:35455/itv/1000000005000265023.m3u8?cdn=ystenlive&Contentid=1000000005000265023
吉林卫视,http://b.zgjok.com:35455/itv/5000000011000031117.m3u8?cdn=bestzb&Contentid=5000000011000031117
江苏卫视,http://b.zgjok.com:35455/itv/1000000001000001828.m3u8?cdn=ystenlive&Contentid=1000000001000001828
江苏卫视,http://b.zgjok.com:35455/itv/1000000005000265030.m3u8?cdn=ystenlive&Contentid=1000000005000265030
江西卫视,http://b.zgjok.com:35455/itv/1000000006000268001.m3u8?cdn=ystenlive&Contentid=1000000006000268001
江西卫视,http://b.zgjok.com:35455/itv/1000000005000265032.m3u8?cdn=ystenlive&Contentid=1000000005000265032
辽宁卫视,http://b.zgjok.com:35455/itv/5000000004000011671.m3u8?cdn=bestzb&Contentid=5000000004000011671
辽宁卫视,http://b.zgjok.com:35455/itv/1000000005000265022.m3u8?cdn=ystenlive&Contentid=1000000005000265022
青海卫视,http://b.zgjok.com:35455/itv/1000000002000013359.m3u8?cdn=ystenlive&Contentid=1000000002000013359
山东卫视,http://b.zgjok.com:35455/itv/1000000005000265019.m3u8?cdn=ystenlive&Contentid=1000000005000265019
东方卫视,http://b.zgjok.com:35455/itv/5000000004000014098.m3u8?cdn=bestzb&Contentid=5000000004000014098
东方卫视,http://b.zgjok.com:35455/itv/1000000005000265018.m3u8?cdn=ystenlive&Contentid=1000000005000265018
深圳卫视,http://b.zgjok.com:35455/itv/5000000004000007410.m3u8?cdn=bestzb&Contentid=5000000004000007410
深圳卫视,http://b.zgjok.com:35455/itv/1000000005000265028.m3u8?cdn=ystenlive&Contentid=1000000005000265028
四川卫视,http://b.zgjok.com:35455/itv/5000000004000006119.m3u8?cdn=bestzb&Contentid=5000000004000006119
天津卫视,http://b.zgjok.com:35455/itv/5000000004000006827.m3u8?cdn=bestzb&Contentid=5000000004000006827
天津卫视,http://b.zgjok.com:35455/itv/1000000005000265026.m3u8?cdn=ystenlive&Contentid=1000000005000265026
云南卫视,http://b.zgjok.com:35455/itv/5000000011000031120.m3u8?cdn=bestzb&Contentid=5000000011000031120
浙江卫视,http://b.zgjok.com:35455/itv/5000000004000007275.m3u8?cdn=bestzb&Contentid=5000000004000007275
浙江卫视,http://b.zgjok.com:35455/itv/1000000001000014260.m3u8?cdn=ystenlive&Contentid=1000000001000014260
浙江卫视,http://b.zgjok.com:35455/itv/1000000005000265031.m3u8?cdn=ystenlive&Contentid=1000000005000265031
重庆卫视,http://b.zgjok.com:35455/itv/1000000001000001096.m3u8?cdn=ystenlive&Contentid=1000000001000001096
重庆卫视,http://b.zgjok.com:35455/itv/1000000005000265017.m3u8?cdn=ystenlive&Contentid=1000000005000265017
大湾区卫视,http://b.zgjok.com:35455/itv/1000000002000011619.m3u8?cdn=ystenlive&Contentid=1000000002000011619
厦门卫视,http://b.zgjok.com:35455/itv/1000000005000266006.m3u8?livemode=1&stbId=10&cdn=ystenlive&Contentid=1000000005000266006
吉林卫视,http://b.zgjok.com:35455/itv/1000000002000027730.m3u8?cdn=ystenlive&Contentid=1000000002000027730
内蒙古卫视,http://b.zgjok.com:35455/itv/1000000002000014080.m3u8?cdn=ystenlive&Contentid=1000000002000014080
宁夏卫视,http://b.zgjok.com:35455/itv/1000000002000031451.m3u8?livemode=1&stbId=10&cdn=ystenlive&Contentid=1000000002000031451
甘肃卫视,http://b.zgjok.com:35455/itv/5000000011000031121.m3u8?cdn=bestzb
山西卫视,http://b.zgjok.com:35455/itv/1000000002000021220.m3u8?cdn=ystenlive
陕西卫视,http://b.zgjok.com:35455/itv/5000000006000040017.m3u8?cdn=bestzb
新疆卫视,http://b.zgjok.com:35455/itv/1000000002000029441.m3u8?livemode=1&stbId=10&cdn=ystenlive&Contentid=1000000002000029441
新疆卫视,http://b.zgjok.com:35455/itv/1000000002000029441.m3u8?cdn=ystenlive&Contentid=1000000002000029441
西藏卫视,http://b.zgjok.com:35455/itv/1000000002000015894.m3u8?cdn=ystenlive&Contentid=1000000002000015894
兵团卫视,http://b.zgjok.com:35455/itv/1000000005000266005.m3u8?cdn=ystenlive&Contentid=1000000005000266005
安多卫视,http://b.zgjok.com:35455/itv/1000000005000266001.m3u8?cdn=ystenlive&Contentid=1000000005000266001
康巴卫视,http://b.zgjok.com:35455/itv/1000000005000266002.m3u8?cdn=ystenlive&Contentid=1000000005000266002
农林卫视,http://b.zgjok.com:35455/itv/1000000005000266003.m3u8?cdn=ystenlive&Contentid=1000000005000266003
延边卫视,http://b.zgjok.com:35455/itv/1000000005000266008.m3u8?cdn=ystenlive&Contentid=1000000005000266008
三沙卫视,http://b.zgjok.com:35455/itv/5000000011000288016.m3u8?cdn=bestzb
湖南经视,http://b.zgjok.com:35455/itv/6306119848317438256.m3u8?cdn=hnbblive&Contentid=6306119848317438256
湖南娱乐,http://b.zgjok.com:35455/itv/6427893650335440392.m3u8?cdn=hnbblive&Contentid=6427893650335440392
湖南都市,http://b.zgjok.com:35455/itv/4682579636905393407.m3u8?cdn=hnbblive&Contentid=4682579636905393407
湖南电视剧,http://b.zgjok.com:35455/itv/8765482907954673867.m3u8?cdn=hnbblive&Contentid=8765482907954673867
湖南爱晚,http://b.zgjok.com:35455/itv/6307875884530512195.m3u8?cdn=hnbblive&Contentid=6307875884530512195
湖南电影,http://b.zgjok.com:35455/itv/7884242846753128038.m3u8?cdn=hnbblive&Contentid=7884242846753128038
湖南国际,http://b.zgjok.com:35455/itv/5015828848322021526.m3u8?cdn=hnbblive&Contentid=5015828848322021526
湖南卫视,https://stream1.freetv.fun/8f9c1b950218b09e8fb1b0d6b7416bdf4a4635a03c2f67f7880010d106038137.m3u8
湖南卫视,https://stream1.freetv.fun/5a9d48cd227fc4fe61f3a29868e142e0856d2027056a79466216bad8461b778a.ctv
湖南卫视,https://stream1.freetv.fun/178c8c1ddfb1636baa0cfd16ae47ad25451c023870063fe38be74c6d43e23b19.m3u8
湖南卫视,https://stream1.freetv.fun/e2ec5b85b37a5023400b389e088d2f023026fe2aea41accb67545aa9bb0e7880.m3u8
湖南卫视,https://stream1.freetv.fun/e9661bf80886d85924f06c05608efdf21ac1f96034cba37e395d058f70629387.ctv
湖南卫视,https://stream1.freetv.fun/43a1b7e196c98f142e5afc0c9819ddac95f2eb0db96eb21e0f3438eae9ef0d7c.ctv
浙江卫视,https://stream1.freetv.fun/553f754e0c2f9380f43fe487b962b05eaa8d337c42ec0496d04b5fdd66383d5f.m3u8
东方卫视,https://stream1.freetv.fun/ddae7298b39a8eaf452f620ee2203f97e830d7e6b9726b41f9c5f1e9cb6cdbea.m3u8
东方卫视,https://stream1.freetv.fun/90cce0c94c123d472e80f144fc1920c2119fec29994ac420a4a1a2e72dba1d6b.m3u8
江苏卫视,https://stream1.freetv.fun/de9d116d4d440dc63eff556982be839c0fe91b887dff2f85bce189481adc7ab7.m3u8
江苏卫视,https://stream1.freetv.fun/af236d18c00c75749b4ecf0030d398dba80b5787616cf74b70167c8f2ccf7b3d.m3u8
广东卫视,https://stream1.freetv.fun/b5325b8597400e5edb4c00f0e5e27ae49b509e4ed0def76b535dcd3a4509a925.m3u8
湖南国际,https://stream1.freetv.fun/7c67049177ac8d070d86896c91fe647b79a5825f0d5f93bd59f7de2f37777cdd.m3u8"""

    hot_channels = """🇭🇰港澳台🇭🇰,#genre#
凤凰中文,http://223.105.252.60/PLTV/3/224/3221228527/index.m3u8
凤凰资讯,http://223.105.252.60/PLTV/3/224/3221228524/index.m3u8
凤凰香港,http://223.105.252.60/PLTV/3/224/3221228530/index.m3u8
凤凰中文,http://223.105.252.60/PLTV/3/224/3221228527/index.m3u8?servicetype=1&unionUrl=gitv%2Flive1%2F-%2FHD-10000k-1080P-fhchinese5s&icpid=88888888&from=1&hms_devid=6885
凤凰资讯,http://223.105.252.60/PLTV/3/224/3221228524/index.m3u8?servicetype=1&unionUrl=gitv%2Flive1%2F-%2FHD-10000k-1080P-fhchinese5s&icpid=88888888&from=1&hms_devid=6885
凤凰香港,http://223.105.252.60/PLTV/3/224/3221228530/index.m3u8?servicetype=1&unionUrl=gitv%2Flive1%2F-%2FHD-10000k-1080P-fhchinese5s&icpid=88888888&from=1&hms_devid=6885
凤凰中文,http://ali.hlspull.yximgs.com/live/diyp_fh2.flv
凤凰资讯,http://ali.hlspull.yximgs.com/live/diyp_fh1.flv
凤凰香港,http://ali.hlspull.yximgs.com/live/diyp_fh3.flv
凤凰中文,http://php.jdshipin.com:8880/TVOD/iptv.php?id=fhzw
凤凰资讯,http://php.jdshipin.com:8880/TVOD/iptv.php?id=fhzx
凤凰中文,http://aktv.top/AKTV/live/aktv/null-3/AKTV.m3u8
凤凰资讯,http://aktv.top/AKTV/live/aktv/null-4/AKTV.m3u8
凤凰香港,http://aktv.top/AKTV/live/aktv/null-5/AKTV.m3u8
中天新闻,http://aktv.top/AKTV/live/aktv/null-8/AKTV.m3u8
中天亚洲,http://aktv.top/AKTV/live/aktv/null-12/AKTV.m3u8
中视新闻,http://aktv.top/AKTV/live/aktv/null-10/AKTV.m3u8
寰宇新闻,http://aktv.top/AKTV/live/aktv/null-9/AKTV.m3u8
TVBS新闻,http://aktv.top/AKTV/live/aktv/tvbs-1/AKTV.m3u8
TVBS,http://aktv.top/AKTV/live/aktv/tvbs/AKTV.m3u8
中视,http://aktv.top/AKTV/live/aktv/null-10/AKTV.m3u8
华视,http://aktv.top/AKTV/live/aktv/null-11/AKTV.m3u8
HOY78,http://aktv.top/AKTV/live/aktv/hoy78/AKTV.m3u8
无线新闻台,http://aktv.top/AKTV/live/aktv/null-1/AKTV.m3u8
无线新闻台,http://aktv.top/AKTV/live/aktv2/null-1/AKTV.m3u8
娱乐新闻台,http://aktv.top/AKTV/live/aktv/hk/AKTV.m3u8
翡翠台,http://aktv.top/AKTV/live/aktv/null/AKTV.m3u8
翡翠综合台(北美),http://aktv.top/AKTV/live/aktv/null-17/AKTV.m3u8
翡翠剧集台(北美),http://aktv.top/AKTV/live/aktv/null-18/AKTV.m3u8
明珠台,http://aktv.top/AKTV/live/aktv/null-2/AKTV.m3u8
明珠剧集台(北美,http://aktv.top/AKTV/live/aktv/null-19/AKTV.m3u8
星河台,http://aktv.top/AKTV/live/aktv2/tvb/AKTV.m3u8
爆谷台,http://aktv.top/AKTV/live/aktv2/null/AKTV.m3u8
黃金翡翠台,http://aktv.top/AKTV/live/aktv/null-21/AKTV.m3u8
千禧经典台,http://aktv.top/AKTV/live/aktv/null-15/AKTV.m3u8
TVB Plus,http://aktv.top/AKTV/live/aktv/tvbplus/AKTV.m3u8
28 AI 智慧赛马,http://aktv.top/AKTV/live/aktv/28ai/AKTV.m3u8
18台,http://aktv.top/AKTV/live/aktv/mytvsuper18/AKTV.m3u8
美亚电影,http://aktv.top/AKTV/live/aktv/hk-1/AKTV.m3u8
靖天电影,http://aktv.top/AKTV/live/aktv/null-6/AKTV.m3u8
龙华日韩,http://aktv.top/AKTV/live/aktv/null-22/AKTV.m3u8
龙华经典,http://aktv.top/AKTV/live/aktv/null-7/AKTV.m3u8
龙华电影,http://aktv.top/AKTV/live/aktv/null-23/AKTV.m3u8
Now星影,http://aktv.top/AKTV/live/aktv2/now/AKTV.m3u8
PopC,http://aktv.top/AKTV/live/aktv/popc/AKTV.m3u8
ROCK Action,http://aktv.top/AKTV/live/aktv/rockaction/AKTV.m3u8
tvN,http://aktv.top/AKTV/live/aktv/tvn/AKTV.m3u8
Channel 5 HD,http://aktv.top/AKTV/live/aktv/channel5hd/AKTV.m3u8
Channel 8 HD,http://aktv.top/AKTV/live/aktv/channel8hd/AKTV.m3u8
Channel U HD,http://aktv.top/AKTV/live/aktv/channeluhd/AKTV.m3u8
日本全天新闻,http://aktv.top/AKTV/live/aktv/null-13/AKTV.m3u8

无线新闻,http://php.jdshipin.com:8880/smt.php?id=inews_twn
无线新闻,http://php.jdshipin.com:8880/TVOD/iptv.php?id=tvbxw
娱乐新闻,http://php.jdshipin.com:8880/TVOD/iptv.php?id=fct2
翡翠台,http://php.jdshipin.com/TVOD/iptv.php?id=huali2
翡翠台,http://php.jdshipin.com:8880/TVOD/iptv.php?id=fct
翡翠台,http://php.jdshipin.com/TVOD/iptv.php?id=fct3
翡翠台,http://php.jdshipin.com:8880/TVOD/iptv.php?id=fct3
明珠台,http://php.jdshipin.com:8880/PLTV/iptv.php?id=mzt2
TVB星河,http://php.jdshipin.com:8880/smt.php?id=Xinhe
TVB星河,http://php.jdshipin.com/TVOD/iptv.php?id=xinghe
TVB星河,http://php.jdshipin.com:8880/TVOD/iptv.php?id=xinghe
华丽翡翠台,http://php.jdshipin.com:8880/TVOD/iptv.php?id=huali
华丽翡翠台,http://php.jdshipin.com/TVOD/iptv.php?id=huali
TVB Plus,http://php.jdshipin.com/TVOD/iptv.php?id=j2
TVB千禧经典,http://php.jdshipin.com/TVOD/iptv.php?id=tvbc

ViuTV,http://bziyunshao.synology.me:8889/bysid/99
ViuTV,http://zsntlqj.xicp.net:8895/bysid/99.m3u8
功夫台,https://edge6a.v2h-cdn.com/asia_action/asia_action.stream/chunklist.m3u8
耀才财经,https://v3.mediacast.hk/webcast/bshdlive-pc/playlist.m3u8
面包台,https://video.bread-tv.com:8091/hls-live24/online/index.m3u8
香港C＋,http://ottproxy2.ist.ooo/livehls/MOB-U1-NO/03.m3u8
翡翠台4K,http://cdn3.1678520.xyz/live/?id=fct4k
TVB plus,http://cdn3.1678520.xyz/live/?id=tvbp
澳门Macau,http://php.jdshipin.com:8880/amlh.php

TVBS新闻,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8574/.m3u8
年代新闻,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8539/.m3u8
三立新闻,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8543/.m3u8
东森新闻,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8540/.m3u8
民视新闻,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8542/.m3u8
壹新闻,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8548/.m3u8
三立新闻,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8543/.m3u8
寰宇新闻,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8547/.m3u8
TVBS HD,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8575/.m3u8
东森超视,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8525/.m3u8
三立都会,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8522/.m3u8
三立台湾,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8521/.m3u8
中天综合,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8526/.m3u8
东森综合,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8524/.m3u8
TVBS欢乐,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8532/.m3u8
年代MUCH,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8529/.m3u8
东森财经,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8546/.m3u8
纬来日本,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8537/.m3u8
动物星球,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8512/.m3u8
好莱坞电影,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8554/.m3u8
AMC电影,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8505/.m3u8
HBO,http://tianhewan.top/ZIPP.php?url=http://211.72.65.236:8503/.m3u8

非凡新闻,http://litv.zapi.us.kg/?id=4gtv-4gtv010
镜新闻,http://litv.zapi.us.kg/?id=4gtv-4gtv075
东森新闻,http://litv.zapi.us.kg/?id=4gtv-4gtv152
东森财经新闻,http://litv.zapi.us.kg/?id=4gtv-4gtv153
寰宇新闻,http://litv.zapi.us.kg/?id=litv-longturn15
台视,http://litv.zapi.us.kg/?id=4gtv-4gtv066
台视财经,http://litv.zapi.us.kg/?id=4gtv-4gtv056
中视,http://litv.zapi.us.kg/?id=4gtv-4gtv040
华视,http://litv.zapi.us.kg/?id=4gtv-4gtv041
民视,http://litv.zapi.us.kg/?id=4gtv-4gtv002
民视,http://litv.zapi.us.kg/?id=4gtv-4gtv155
民视第一台,http://litv.zapi.us.kg/?id=4gtv-4gtv003
民视台湾,http://litv.zapi.us.kg/?id=4gtv-4gtv001
民视台湾,http://litv.zapi.us.kg/?id=4gtv-4gtv156
影迷數位電影,http://litv.zapi.us.kg/?id=4gtv-4gtv011
AMC电影,http://litv.zapi.us.kg/?id=4gtv-4gtv017
CATCHPLAY电影,http://litv.zapi.us.kg/?id=4gtv-4gtv076
靖天电影台,http://litv.zapi.us.kg/?id=4gtv-4gtv061
龙华电影,http://litv.zapi.us.kg/?id=litv-longturn03
采昌影剧,http://litv.zapi.us.kg/?id=4gtv-4gtv049
龙华经典,http://litv.zapi.us.kg/?id=litv-longturn21
中视经典,http://litv.zapi.us.kg/?id=4gtv-4gtv080
台湾戏剧,http://litv.zapi.us.kg/?id=litv-longturn22
靖洋戏剧,http://litv.zapi.us.kg/?id=4gtv-4gtv045
靖天戏剧,http://litv.zapi.us.kg/?id=4gtv-4gtv058
公视戏剧,http://litv.zapi.us.kg/?id=4gtv-4gtv042
龙华戏剧,http://litv.zapi.us.kg/?id=litv-longturn18
时尚运动X,http://litv.zapi.us.kg/?id=4gtv-4gtv014
靖天育乐,http://litv.zapi.us.kg/?id=4gtv-4gtv062
博斯魅力,http://litv.zapi.us.kg/?id=litv-longturn04
博斯高球1,http://litv.zapi.us.kg/?id=litv-longturn05
博斯高球2,http://litv.zapi.us.kg/?id=litv-longturn06
博斯运动1,http://litv.zapi.us.kg/?id=litv-longturn07
博斯运动2,http://litv.zapi.us.kg/?id=litv-longturn08
博斯网球,http://litv.zapi.us.kg/?id=litv-longturn09
博斯无限,http://litv.zapi.us.kg/?id=litv-longturn10
博斯无限2,http://litv.zapi.us.kg/?id=litv-longturn13
TRACE SPORTS STARS,http://litv.zapi.us.kg/?id=4gtv-4gtv077
視納華仁紀實頻道,http://litv.zapi.us.kg/?id=4gtv-4gtv013
中视菁采,http://litv.zapi.us.kg/?id=4gtv-4gtv064
八大精彩,http://litv.zapi.us.kg/?id=4gtv-4gtv034
八大综艺,http://litv.zapi.us.kg/?id=4gtv-4gtv039
TVBS精采,http://litv.zapi.us.kg/?id=4gtv-4gtv067
TVBS欢乐,http://litv.zapi.us.kg/?id=4gtv-4gtv068
靖天欢乐,http://litv.zapi.us.kg/?id=4gtv-4gtv054
靖天综合,http://litv.zapi.us.kg/?id=4gtv-4gtv046
靖天资讯,http://litv.zapi.us.kg/?id=4gtv-4gtv065
靖天卡通,http://litv.zapi.us.kg/?id=4gtv-4gtv044
靖天日本,http://litv.zapi.us.kg/?id=4gtv-4gtv047
靖洋卡通,http://litv.zapi.us.kg/?id=4gtv-4gtv057
靖天国际,http://litv.zapi.us.kg/?id=4gtv-4gtv063
靖天映画,http://litv.zapi.us.kg/?id=4gtv-4gtv055
爱尔达娱乐,http://litv.zapi.us.kg/?id=4gtv-4gtv070
龙华卡通,http://litv.zapi.us.kg/?id=litv-longturn01
龙华日韩,http://litv.zapi.us.kg/?id=litv-longturn11
龙华偶像,http://litv.zapi.us.kg/?id=litv-longturn12
民视综艺,http://litv.zapi.us.kg/?id=4gtv-4gtv004
亚洲旅游,http://litv.zapi.us.kg/?id=litv-longturn17
客家电视,http://litv.zapi.us.kg/?id=4gtv-4gtv043
古典音乐,http://litv.zapi.us.kg/?id=4gtv-4gtv059
猪哥亮歌厅秀,http://litv.zapi.us.kg/?id=4gtv-4gtv006
Smart知识,http://litv.zapi.us.kg/?id=litv-longturn19
达文西频道,http://litv.zapi.us.kg/?id=4gtv-4gtv018
阿里郎,http://litv.zapi.us.kg/?id=4gtv-4gtv079
生活英语,http://litv.zapi.us.kg/?id=litv-longturn20
好消息,http://litv.zapi.us.kg/?id=litv-ftv16
好消息2台,http://litv.zapi.us.kg/?id=litv-ftv17
非凡商业,http://litv.zapi.us.kg/?id=4gtv-4gtv048
韩国娱乐,http://litv.zapi.us.kg/?id=4gtv-4gtv016

台视,rtmp://f13h.mine.nu/sat/tv071
华视,rtmp://f13h.mine.nu/sat/tv111
民视,rtmp://f13h.mine.nu/sat/tv051
中视,rtmp://f13h.mine.nu/sat/tv091
纬来日本,rtmp://f13h.mine.nu/sat/tv771

耀才财经,https://v3.mediacast.hk/webcast/bshdlive-pc/chunklist_w99771165.m3u8
耀才财经,https://v3.mediacast.hk/webcast/bshdlive-pc/playlist.m3u8
耀才财经,http://202.69.67.66:443/webcast/bshdlive-pc/playlist.m3u8
点掌财经,https://wsvideo.aniu.tv/live/aniu/playlist.m3u8
GOODTV,https://dqhxk7sbp7xog.cloudfront.net/hls-live/goodtv/_definst_/liveevent/live-ch1-2.m3u8
番薯音乐,http://61.216.67.119:1935/TWHG/E1/chunklist_w705811302.m3u8
番薯音乐,http://61.216.67.119:1935/TWHG/E1/chunklist_w7058102.m3u8
番薯音乐,http://61.216.67.119:1935/TWHG/E1/chunklist_w70581102.m3u8
环球电视,http://zb.xzxwhcb.com:9999/hls/world.m3u8

CNN,https://i.mjh.nz/SamsungTVPlus/GBBD8000016N.m3u8
CNN,https://turnerlive.warnermediacdn.com/hls/live/586495/cnngo/cnn_slate/VIDEO_0_3564000.m3u8
BBC,http://cdns.jp-primehome.com:8000/zhongying/live/playlist.m3u8?cid=cs15
BBC World News,P2p://generationnexxxt.com:19806/7fa4771def7c4896b1b9ea7e022f278c
ABC News,http://ytb.csscc.cc:2086/live.m3u8?c=12
ABC News,https://lnc-abc-news.tubi.video/index.m3u8
ABC News,https://abc-iview-mediapackagestreams-2.akamaized.net/out/v1/6e1cc6d25ec0480ea099a5399d73bc4b/index_45.m3u8
ABC News Live,https://i.mjh.nz/SamsungTVPlus/USBC39000171G.m3u8
ABC Australia,https://abc-iview-mediapackagestreams-2.akamaized.net/out/v1/6e1cc6d25ec0480ea099a5399d73bc4b/index.m3u8
FOX News,https://fox-foxnewsnow-samsungus.amagi.tv/playlist720p.m3u8
Fox Weather,https://247wlive.foxweather.com/stream/index_1280x720.m3u8
CBN News,https://bcovlive-a.akamaihd.net/re8d9f611ee4a490a9bb59e52db91414d/us-east-1/734546207001/playlist.m3u8
Euronews,P2p://generationnexxxt.com:19806/43dedaf8037e43ceb06f46baa4391692
RT News,https://rt-glb.rttv.com/dvr/rtnews/playlist_4500Kb.m3u8
TRT World,https://tv-trtworld.live.trt.com.tr/master_1080.m3u8
ABC7 Bay Area,https://i.mjh.nz/SamsungTVPlus/USBC4400010RH.m3u8
CNA,https://d2e1asnsl7br7b.cloudfront.net/7782e205e72f43aeb4a48ec97f66ebbe/index_5.m3u8
NHK World,https://nhkwlive-ojp.akamaized.net/hls/live/2003459/nhkwlive-ojp-en/index.m3u8
NHK,https://cdn.skygo.mn/live/disk1/NHK_World_Premium/HLSv3-FTA/NHK_World_Premium.m3u8
半岛新闻「英文」,https://live-hls-aje-ak.getaj.net/AJE/01.m3u8?zshijd
半岛新闻「英文」,https://live-hls-web-aje.getaj.net/AJE/01.m3u8
半岛新闻「阿拉伯」,https://live-hls-aje-ak.getaj.net/AJE/02.m3u8?zshijd
半岛新闻「阿拉伯」,http://live-hls-web-aja.getaj.net/AJA/02.m3u8
AXS TV Now,https://dikcfc9915kp8.cloudfront.net/hls/1080p/playlist.m3u8
Arirang,https://amdlive-ch01-ctnd-com.akamaized.net/arirang_1ch/smil:arirang_1ch.smil/chunklist_b3256000_sleng.m3u8
Bloomberg Originals,https://i.mjh.nz/SamsungTVPlus/GBBC900012J9.m3u8
RT Documentary,https://rt-rtd.rttv.com/live/rtdoc/playlist_4500Kb.m3u8
ION Plus,https://i.mjh.nz/SamsungTVPlus/USBD300003LK.m3u8
Fight Network,https://d12a2vxqkkh1bo.cloudfront.net/hls/1080p/playlist.m3u8
Wild Earth,https://wildearth-plex.amagi.tv/masterR1080p.m3u8
Paramount Network,http://170.254.18.106/PARAMOUNT/index.m3u8
Universal Kids,http://streamsy.online:2999/coachj88/N93DPKS9pJ/252
Start TV,http://streamsy.online:2999/coachj88/N93DPKS9pJ/1467
The Weather Channel,http://streamsy.online:2999/coachj88/N93DPKS9pJ/301
WE TV,http://streamsy.online:2999/coachj88/N93DPKS9pJ/247
Me TV,http://streamsy.online:2999/coachj88/N93DPKS9pJ/744
SNY,http://streamsy.online:2999/coachj88/N93DPKS9pJ/330
News 12 New York,https://lnc-news12.tubi.video/index.m3u8
OAN,https://cdn.klowdtv.net/803B48A/n1.klowdtv.net/live1/oan_720p/playlist.m3u8
Yahoo Finance,https://d1ewctnvcwvvvu.cloudfront.net/playlist1080pl.m3u8
GITV,http://hls-igi.cdnvideo.ru/igi/igi_hq/playlist.m3u8
ASTV,http://news1.live14.com/stream/news1_hi.m3u8
Russia Today,https://rt-glb.rttv.com/live/rtnews/playlist.m3u8
TRT World,https://tv-trtworld.live.trt.com.tr/master.m3u8
VOA,https://voa-ingest.akamaized.net/hls/live/2033874/tvmc06/playlist.m3u8
KBS World,https://kbsworld-ott.akamaized.net/hls/live/2002341/kbsworld/master.m3u8
阿里郎电视,http://amdlive-ch01.ctnd.com.edgesuite.net:80/arirang_1ch/smil:arirang_1ch.smil/chunklist_b2256000_sleng.m3u8
KoreaTV,https://hlive.ktv.go.kr/live/klive_h.stream/playlist.m3u8
朝鲜新闻频道,http://119.77.96.184:1935/chn05/chn05/chunklist_w644291506.m3u8
30A Music,http://30a-tv.com/music.m3u8
AMC Music,https://amchls.wns.live/hls/stream.m3u8
Classic Arts Showcase,https://classicarts.akamaized.net/hls/live/1024257/CAS/master.m3u8
Love Stories,https://84e619480232400a842ce499d053458a.mediatailor.us-east-1.amazonaws.com/v1/manifest/04fd913bb278d8775298c26fdca9d9841f37601f/ONO_LoveStoriesTV/18a65393-ba3b-4912-90d5-7188c128ac66/3.m3u8
Nat Geo,http://streamsy.online:2999/coachj88/N93DPKS9pJ/141
NASA,https://ntv1.akamaized.net:443/hls/live/2014075/NASA-NTV1-HLS/master_2000.m3u8?
NASA TV Public,https://ntv1.akamaized.net/hls/live/2014075/NASA-NTV1-HLS/master.m3u8
台湾Plus,https://bcovlive-a.akamaihd.net/rce33d845cb9e42dfa302c7ac345f7858/ap-northeast-1/6282251407001/playlist.m3u8"""
    
    migu_channels = """🏆咪咕体育🏆,#genre#
JJ斗地主,http://tc-tct.douyucdn2.cn/dyliveflv1a/488743rAHScWyyII_2000.flv?wsAuth=fd695c444eeee99cc6122ed396c805ba&token=cpn-androidmpro-0-488743-df8b1830ef2e6ce156759645768df95bf77749da61fcc901&logo=0&expire=0&did=d010b07dcb997ada9934081c873542f0&origin=tct&vhost=play2
咪咕体育1,http://39.135.137.203/000000001000/3000000001000028638/index.m3u8
咪咕体育2,http://39.135.137.203/000000001000/3000000001000008379/index.m3u8
咪咕体育3,http://39.135.137.203/000000001000/3000000001000008001/index.m3u8
咪咕体育4,http://39.135.137.203/000000001000/3000000001000031494/index.m3u8
咪咕体育5,http://39.135.137.203/000000001000/3000000001000008176/index.m3u8
咪咕体育6,http://39.135.137.203/000000001000/3000000001000010129/index.m3u8
咪咕体育7,http://39.135.137.203/000000001000/3000000001000010948/index.m3u8
咪咕体育8,http://39.135.137.203/000000001000/3000000001000007218/index.m3u8
咪咕体育9,http://39.135.137.203/000000001000/3000000001000005308/index.m3u8
咪咕体育10,http://39.135.137.203/000000001000/3000000010000000097/index.m3u8
咪咕体育11,http://39.135.137.203/000000001000/3000000001000005969/index.m3u8
咪咕体育12,http://39.135.137.203/000000001000/3000000010000031669/index.m3u8
咪咕体育13,http://39.135.137.203/000000001000/3000000010000027691/index.m3u8
咪咕体育14,http://39.135.137.203/000000001000/3000000010000015560/index.m3u8
咪咕体育15,http://39.135.137.203/000000001000/3000000010000002809/index.m3u8
咪咕体育16,http://39.135.137.203/000000001000/3000000010000006077/index.m3u8
咪咕体育17,http://39.135.137.203/000000001000/3000000010000012558/index.m3u8
咪咕体育18,http://39.135.137.203/000000001000/3000000010000023434/index.m3u8
咪咕体育19,http://39.135.137.203/000000001000/3000000010000003915/index.m3u8
咪咕体育20,http://39.135.137.203/000000001000/3000000010000004193/index.m3u8
咪咕体育21,http://39.135.137.203/000000001000/3000000010000021904/index.m3u8
咪咕体育22,http://39.135.137.207/000000001000/3000000010000011297/index.m3u8
咪咕体育23,http://39.135.137.203/000000001000/3000000010000006658/index.m3u8
咪咕体育24,http://39.135.137.203/000000001000/3000000010000010833/index.m3u8
咪咕体育25,http://39.135.137.203/000000001000/3000000010000025380/index.m3u8
咪咕体育27,http://39.135.137.203/000000001000/3000000010000002019/index.m3u8
咪咕体育28,http://39.135.137.203/000000001000/3000000010000005837/index.m3u8
咪咕体育29,http://39.135.137.203/000000001000/3000000010000009788/index.m3u8
咪咕体育30,http://39.135.137.203/000000001000/3000000010000011518/index.m3u8
咪咕体育31,http://39.135.137.203/000000001000/3000000010000012616/index.m3u8
咪咕体育32,http://39.135.137.203/000000001000/3000000010000015470/index.m3u8
咪咕体育33,http://39.135.137.203/000000001000/3000000010000019839/index.m3u8
咪咕体育?,http://39.135.137.203/000000001000/3000000010000017678/index.m3u8
咪咕体育1,http://39.134.136.161:6610/000000001000/3000000001000028638/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000001000028638
咪咕体育2,http://39.134.136.161:6610/000000001000/3000000001000008379/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000001000008379
咪咕体育3,http://39.134.136.161:6610/000000001000/3000000001000008001/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000001000008001
咪咕体育4,http://39.134.136.161:6610/000000001000/3000000001000031494/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000001000031494
咪咕体育5,http://39.134.136.161:6610/000000001000/3000000001000008176/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000001000008176
咪咕体育6,http://39.134.136.161:6610/000000001000/3000000001000010129/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000001000010129
咪咕体育7,http://39.134.136.161:6610/000000001000/3000000001000010948/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000001000010948
咪咕体育8,http://39.134.136.161:6610/000000001000/3000000001000007218/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000001000007218
咪咕体育9,http://39.134.136.161:6610/000000001000/3000000001000005308/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000001000005308
咪咕体育10,http://39.134.136.161:6610/000000001000/3000000010000000097/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000010000000097
咪咕体育11,http://39.134.136.161:6610/000000001000/3000000001000005969/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000001000005969
咪咕体育12,http://39.134.136.161:6610/000000001000/3000000010000031669/index.m3u8?livemode=1&stbId=3&channel-id=FifastbLive&Contentid=3000000010000031669
咪咕体育13,http://39.134.136.161:6610/000000001000/3000000010000027691/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000010000027691
咪咕体育14,http://39.134.136.161:6610/000000001000/3000000010000015560/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000010000015560
咪咕体育15,http://39.134.136.161:6610/000000001000/3000000010000002809/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000010000002809
咪咕体育16,http://39.134.136.161:6610/000000001000/3000000010000006077/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000010000006077
咪咕体育17,http://39.134.136.161:6610/000000001000/3000000010000012558/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000010000012558
咪咕体育18,http://39.134.136.161:6610/000000001000/3000000010000023434/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000010000023434
咪咕体育19,http://39.134.136.161:6610/000000001000/3000000010000003915/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000010000003915
咪咕体育20,http://39.134.136.161:6610/000000001000/3000000010000004193/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000010000004193
咪咕体育21,http://39.134.136.161:6610/000000001000/3000000010000021904/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000010000021904
咪咕体育22,http://39.134.136.161:6610/000000001000/3000000010000011297/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000010000011297
咪咕体育23,http://39.134.136.161:6610/000000001000/3000000010000006658/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000010000006658
咪咕体育24,http://39.134.136.161:6610/000000001000/3000000010000010833/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000010000010833
咪咕体育25,http://39.134.136.161:6610/000000001000/3000000010000025380/index.m3u8?livemode=1&stbId=2&channel-id=FifastbLive&Contentid=3000000010000025380
咪咕体育27,http://39.134.136.161:6610/000000001000/3000000010000002019/index.m3u8?livemode=1&stbId=3&channel-id=FifastbLive&Contentid=3000000010000002019
咪咕体育28,http://39.134.136.161:6610/000000001000/3000000010000005837/index.m3u8?livemode=1&stbId=3&channel-id=FifastbLive&Contentid=3000000010000005837
咪咕体育29,http://39.134.136.161:6610/000000001000/3000000010000009788/index.m3u8?livemode=1&stbId=3&channel-id=FifastbLive&Contentid=3000000010000009788
咪咕体育30,http://39.134.136.161:6610/000000001000/3000000010000011518/index.m3u8?livemode=1&stbId=3&channel-id=FifastbLive&Contentid=3000000010000011518
咪咕体育31,http://39.134.136.161:6610/000000001000/3000000010000012616/index.m3u8?livemode=1&stbId=3&channel-id=FifastbLive&Contentid=3000000010000012616
咪咕体育32,http://39.134.136.161:6610/000000001000/3000000010000015470/index.m3u8?livemode=1&stbId=3&channel-id=FifastbLive&Contentid=3000000010000015470
咪咕体育33,http://39.134.136.161:6610/000000001000/3000000010000019839/index.m3u8?livemode=1&stbId=3&channel-id=FifastbLive&Contentid=3000000010000019839
咪咕体育38,http://39.134.136.161:6610/000000001000/3000000010000017678/index.m3u8?livemode=1&stbId=3&channel-id=FifastbLive&Contentid=3000000010000017678
咪咕体育81,http://39.134.136.161:6610/000000001000/1000000006000270004/index.m3u8?livemode=1&stbId=10&channel-id=ystenlive&Contentid=1000000006000270004
咪咕体育82,http://39.134.136.161:6610/000000001000/2000000003000000063/index.m3u8?livemode=1&stbId=10&channel-id=hnbblive&Contentid=2000000003000000063
咪咕体育83,http://39.134.136.161:6610/000000001000/3000000020000011519/index.m3u8?livemode=1&stbId=10&channel-id=FifastbLive&Contentid=3000000020000011519
咪咕体育84,http://39.134.136.161:6610/000000001000/3000000020000011520/index.m3u8?livemode=1&stbId=10&channel-id=FifastbLive&Contentid=3000000020000011520
咪咕体育85,http://39.134.136.161:6610/000000001000/3000000020000011521/index.m3u8?livemode=1&stbId=10&channel-id=FifastbLive&Contentid=3000000020000011521
咪咕体育86,http://39.134.136.161:6610/000000001000/3000000020000011522/index.m3u8?livemode=1&stbId=10&channel-id=FifastbLive&Contentid=3000000020000011522
睛彩篮球,http://39.134.136.161:6610/000000001000/3000000020000011529/index.m3u8?livemode=1&stbId=10&channel-id=FifastbLive&Contentid=3000000020000011529
睛彩篮球,http://39.134.136.161:6610/000000001000/3000000020000011531/index.m3u8?livemode=1&stbId=10&channel-id=FifastbLive&Contentid=3000000020000011531
睛彩篮球,http://39.134.136.161:6610/000000001000/2000000003000000061/index.m3u8?livemode=1&stbId=10&channel-id=hnbblive&Contentid=2000000003000000061
睛彩篮球,http://39.134.136.161:6610/000000001000/2000000003000000065/index.m3u8?livemode=1&stbId=10&channel-id=hnbblive&Contentid=2000000003000000065
睛彩竞技,http://39.134.136.161:6610/000000001000/3000000020000011528/index.m3u8?livemode=1&stbId=10&channel-id=FifastbLive&Contentid=3000000020000011528
睛彩竞技,http://39.134.136.161:6610/000000001000/3000000020000011530/index.m3u8?livemode=1&stbId=10&channel-id=FifastbLive&Contentid=3000000020000011530
睛彩竞技,http://39.134.136.161:6610/000000001000/2000000003000000060/index.m3u8?livemode=1&stbId=10&channel-id=hnbblive&Contentid=2000000003000000060
睛彩广场舞,http://39.134.136.161:6610/000000001000/1000000006000270003/index.m3u8?livemode=1&stbId=10&channel-id=ystenlive&Contentid=1000000006000270003
睛彩广场舞,http://39.134.136.161:6610/000000001000/2000000003000000062/index.m3u8?livemode=1&stbId=10&channel-id=hnbblive&Contentid=2000000003000000062
睛彩广场舞,http://39.134.136.161:6610/000000001000/2000000003000000064/index.m3u8?livemode=1&stbId=10&channel-id=hnbblive&Contentid=2000000003000000064
睛彩广场舞,http://39.134.136.161:6610/000000001000/3000000020000011523/index.m3u8?livemode=1&stbId=10&channel-id=FifastbLive&Contentid=3000000020000011523
睛彩广场舞,http://39.134.136.161:6610/000000001000/3000000020000011524/index.m3u8?livemode=1&stbId=10&channel-id=FifastbLive&Contentid=3000000020000011524
睛彩青少,http://39.134.136.161:6610/000000001000/3000000020000011525/index.m3u8?livemode=1&stbId=10&channel-id=FifastbLive&Contentid=3000000020000011525
咪咕视频,http://[2409:8087:1a0a:df::4038]/ottrrs.hl.chinamobile.com/TVOD/88888888/224/3221226398/index.m3u8
睛彩篮球,http://[2409:8087:1a0a:df::4038]/ottrrs.hl.chinamobile.com/TVOD/88888888/224/3221226469/index.m3u8
睛彩篮球,http://[2409:8087:1a0a:df::4038]/ottrrs.hl.chinamobile.com/TVOD/88888888/224/3221226147/index.m3u8
睛彩竞技,http://[2409:8087:1a0a:df::4038]/ottrrs.hl.chinamobile.com/TVOD/88888888/224/3221226124/index.m3u8
睛彩广场舞,http://[2409:8087:1a0a:df::4038]/ottrrs.hl.chinamobile.com/TVOD/88888888/224/3221226472/index.m3u8
睛彩青少,http://223.105.252.8/PLTV/4/224/3221228729/index.m3u8
咪咕体育4K Ⅰ,http://39.135.137.203/000000001000/3000000010000005180/index.m3u8
咪咕体育4K Ⅱ,http://39.135.137.203/000000001000/3000000010000015686/index.m3u8
SiTV劲爆体育,http://[2409:8087:5e01:24::16]:6610/000000001000/2000000002000000008/index.m3u8?stbId=3&livemode=1&HlsProfileId=&channel-id=hnbblive&Contentid=2000000002000000008&IASHttpSessionId=OTT19019320240419154124000281
SiTV劲爆体育,http://[2409:8087:5e08:24::11]:6610/000000001000/2000000002000000008/index.m3u8?stbId=3&livemode=1&HlsProfileId=&channel-id=hnbblive&Contentid=2000000002000000008&IASHttpSessionId=OTT19019320240419154124000281
SiTV劲爆体育,http://[2409:8087:5e01:24::16]:6610/000000001000/2000000002000000008/index.m3u8?stbId=3&livemode=1&HlsProfileId=&channel-id=hnbblive&Contentid=2000000002000000008&IAS
SiTV劲爆体育,http://[2409:8087:5e08:24::11]:6610/000000001000/5000000002000029972/1.m3u8?channel-id=bestzb&Contentid=5000000002000029972&livemode=1&stbId=3
SiTV劲爆体育,http://b.zgjok.com:35455/itv/5000000002000029972.m3u8?cdn=bestzb&Contentid=5000000002000029972
SiTV魅力足球,http://[2409:8087:5e08:24::11]:6610/000000001000/5000000011000031207/1.m3u8?channel-id=bestzb&Contentid=5000000011000031207&livemode=1&stbId=3
SiTV劲爆体育,http://z.b.bkpcp.top/m.php?id=jbty
SiTV魅力足球,http://z.b.bkpcp.top/m.php?id=mlzq
iHOT爱体育,http://[2409:8087:5e08:24::11]:6610/000000001000/6000000006000290630/1.m3u8?channel-id=wasusyt&Contentid=6000000006000290630&livemode=1&stbId=3
iHOT爱体育,http://[2409:8087:5e08:24::11]:6610/000000001000/6000000006000290630/index.m3u8?channel-id=wasusyt&Contentid=6000000006000290630&livemode=1&stbId=3
NEWTV精品体育,http://[2409:8087:5e08:24::11]:6610/000000001000/1000000004000014634/1.m3u8?channel-id=ystenlive&Contentid=1000000004000014634&livemode=1&stbId=3
NEWTV精品体育,http://[2409:8087:5e00:24::1e]:6060/000000001000/6460382139625130259/1.m3u8
NEWTV精品体育,http://[2409:8087:74d9:21::6]:80/270000001128/9900000102/index.m3u8
NEWTV精品体育,http://[2409:8087:5e00:24::1e]:6060/000000001000/1000000004000014634/1.m3u8
五星体育,http://b.zgjok.com:35455/itv/5000000010000017540.m3u8?cdn=bestzb&Contentid=5000000010000017540
五星体育,http://[2409:8087:5e08:24::11]:6610/000000001000/2000000002000000007/index.m3u8?stbId=3&livemode=1&HlsProfileId=&channel-id=hnbblive&Contentid=2000000002000000007&IASHttpSessionId=OTT19019320240419154124000281
五星体育,http://[2409:8087:5e01:24::16]:6610/000000001000/2000000002000000007/index.m3u8?stbId=3&livemode=1&HlsProfileId=&channel-id=hnbblive&Contentid=2000000002000000007&IAS
五星体育,http://[2409:8087:5e01:24::16]:6610/000000001000/2000000002000000007/index.m3u8?stbId=3&livemode=1&HlsProfileId=&channel-id=hnbblive&Contentid=2000000002000000007&IASHttpSessionId=OTT19019320240419154124000281
五星体育,http://[2409:8087:5e08:24::11]:6610/000000001000/5000000010000017540/1.m3u8?channel-id=bestzb&Contentid=5000000010000017540&livemode=1&stbId=3
超级体育,http://[2409:8087:5e00:24::1e]:6060/000000001000/1000000001000009601/1.m3u8
超级体育,http://[2409:8087:5e00:24::1e]:6060/000000001000/1000000001000009204/1.m3u8
超级体育,http://[2409:8087:5e00:24::1e]:6060/000000001000/1000000004000007755/1.m3u8
NEWTV武博世界,http://[2409:8087:5e08:24::11]:6610/000000001000/2000000003000000007/1.m3u8?channel-id=hnbblive&Contentid=2000000003000000007&livemode=1&stbId=3
快乐垂钓,http://[2409:8087:5e00:24::1e]:6060/000000001000/5000000011000031206/1.m3u8
SiTV游戏风云,http://[2409:8087:74d9:21::6]:80/000000001000PLTV/88888888/224/3221226187/index.m3u8
SiTV游戏风云,http://[2409:8087:5e08:24::11]:6610/000000001000/2000000002000000011/index.m3u8?stbId=3&livemode=1&HlsProfileId=&channel-id=hnbblive&Contentid=2000000002000000011&IASHttpSessionId=OTT19019320240419154124000281&yang-1989
SiTV游戏风云,http://[2409:8087:5e08:24::11]:6610/000000001000/5000000011000031114/1.m3u8?channel-id=bestzb&Contentid=5000000011000031114&livemode=1&stbId=3
哒啵电竞,http://[2409:8087:74d9:21::6]:80/270000001128/9900000121/index.m3u8
哒啵电竞,http://[2409:8087:5e01:24::16]:6610/000000001000/2000000003000000066/index.m3u8?stbId=3&livemode=1&HlsProfileId=&channel-id=hnbblive&Contentid=2000000003000000066&IAS
哒啵电竞,http://[2409:8087:5e01:24::16]:6610/000000001000/2000000003000000066/index.m3u8?stbId=3&livemode=1&HlsProfileId=&channel-id=hnbblive&Contentid=2000000003000000066&IASHttpSessionId=OTT19019320240419154124000281
哒啵电竞,http://[2409:8087:5e08:24::11]:6610/000000001000/1000000006000032327/1.m3u8?channel-id=ystenlive&Contentid=1000000006000032327&livemode=1&stbId=3
哒啵电竞,http://[2409:8087:5e08:24::11]:6610/000000001000/2000000003000000066/index.m3u8?stbId=3&livemode=1&HlsProfileId=&channel-id=hnbblive&Contentid=2000000003000000066&IASHttpSessionId=OTT19019320240419154124000281
哒啵赛事,http://[2409:8087:5e08:24::11]:6610/000000001000/1000000001000003775/1.m3u8?channel-id=ystenlive&Contentid=1000000001000003775&livemode=1&stbId=3
哒啵电竞,http://b.zgjok.com:35455/itv/1000000006000032327.m3u8?cdn=ystenlive&Contentid=1000000006000032327
哒啵赛事,http://b.zgjok.com:35455/itv/1000000001000003775.m3u8?cdn=ystenlive&Contentid=1000000001000003775
Trace Sports,https://lightning-tracesport-samsungau.amagi.tv/playlist1080p.m3u8
红牛体育,http://rbmn-live.akamaized.net/hls/live/590964/BoRB-AT/master_6660.m3u8
美国摔跤,https://d2p372oxiwmcn1.cloudfront.net:443/hls/1080p/playlist.m3u8
ONE Golf「高尔夫」,http://162.250.201.58:6211/pk/ONEGOLF/tracks-v1a1/mono.m3u8
魅力足球,http://dp.sxtv.top:88/live/bestv.php?id=mlzq
快乐垂钓,http://dp.sxtv.top:88/live/bestv.php?id=klcd
和平精英,http://tc-tct.douyucdn2.cn/dyliveflv1/999rx47n2pp8pKD_2000.flv?wsAuth=6c429f39afed615e842e02ad1a9b1c6e&token=cpn-androidmpro-0-999-d32d75306aab2a7980ad37445844bcccf012d2bb110b5c33&logo=0&expire=0&did=d010b07dcb997ada9934081c873542f0&origin=tct&vhost=play1
王者荣耀,http://tc-tct.douyucdn2.cn/dyliveflv1a/1863767rkpl2_2000p.flv?wsAuth=f73077d85e523eb95b6ce1ea3581b46b&token=cpn-androidmpro-0-1863767-7b520f6fe0a2b18db3c111c4e3c14350afd2dcaf43d0ef60&logo=0&expire=0&did=d010b07dcb997ada9934081c873542f0&origin=tct&vhost=play2
穿越火线,http://tc-tct.douyucdn2.cn:80/dyliveflv1/605964rzzgGEOZHr.flv?wsAuth=43ef2d796067cbec9c238c73235a1005&token=cpn-androidmpro-0-605964-b9be22700076c085e82232beb0fbe7838e28994acafb3964&logo=0&expire=0&did=d010b07dcb997ada9934081c873542f0&origin=tct&vhost=play1
穿越火线,http://112.83.136.141:80/live/605964rzzgGEOZHr.flv?302_type=cold_aggr&_session_id=2376164747.n.cn-069f7p.14re_26504&cb_retry=0&did=d010b07dcb997ada9934081c873542f0&domain=tc-tct.douyucdn2.cn&expire=0&fp_user_url=http%3A%2F%2Ftc-tct.douyucdn2.cn%2Fdyliveflv1%2F605964rzzgGEOZHr.flv%3FwsAuth%3D43ef2d796067cbec9c238c73235a1005%26token%3Dcpn-androidmpro-0-605964-b9be22700076c085e82232beb0fbe7838e28994acafb3964%26logo%3D0%26expire%3D0%26did%3Dd010b07dcb997ada9934081c873542f0%26origin%3Dtct%26vhost%3Dplay1&logo=0&manage_ip=&mir=true&node_id=&origin=tct&pro_type=http&redirect_from=pod.cn-069f7p.14re.nss&token=cpn-androidmpro-0-605964-b9be22700076c085e82232beb0fbe7838e28994acafb3964&vhost=tc-tct.douyucdn2.cn&wsAuth=43ef2d796067cbec9c238c73235a1005
跑跑卡丁车,http://tc-tct.douyucdn2.cn/dyliveflv1a/6672862r90xSwiRP_2000.flv?wsAuth=1c2c516dd80b1193241687841f128073&token=cpn-androidmpro-0-6672862-ee6297daa5d07f3494aad175947a679df4184f7934380258&logo=0&expire=0&did=d010b07dcb997ada9934081c873542f0&origin=tct&vhost=play2"""

    solid_channels = """🥝精品频道🥝,#genre#
黑莓电影,http://b.zgjok.com:35455/itv/1000000004000019624.m3u8?cdn=ystenlive&Contentid=1000000004000019624
黑莓动画,http://b.zgjok.com:35455/itv/1000000004000021734.m3u8?cdn=ystenlive&Contentid=1000000004000021734
精彩影视,http://b.zgjok.com:35455/itv/2000000004000000063.m3u8?&cdn=hnbblive
精彩影视,http://b.zgjok.com:35455/itv/2000000004000000063.m3u8?cdn=hnbblive&Contentid=2000000004000000063
精彩影视,http://b.zgjok.com:35455/itv/6000000006000320630.m3u8?cdn=wasusyt&Contentid=6000000006000320630
iHOT爱动漫,http://b.zgjok.com:35455/itv/2000000004000000059.m3u8?&cdn=hnbblive
iHOT爱历史,http://b.zgjok.com:35455/itv/2000000004000000046.m3u8?&cdn=hnbblive
iHOT爱喜剧,http://b.zgjok.com:35455/itv/2000000004000000032.m3u8?&cdn=hnbblive
iHOT爱幼教,http://b.zgjok.com:35455/itv/2000000004000000049.m3u8?&cdn=hnbblive
iHOT爱悬疑,http://b.zgjok.com:35455/itv/2000000004000000036.m3u8?&cdn=hnbblive
iHOT爱旅行,http://b.zgjok.com:35455/itv/2000000004000000056.m3u8?&cdn=hnbblive
iHOT爱浪漫,http://b.zgjok.com:35455/itv/2000000004000000035.m3u8?&cdn=hnbblive
iHOT爱玩具,http://b.zgjok.com:35455/itv/2000000004000000053.m3u8?&cdn=hnbblive
iHOT爱科学,http://b.zgjok.com:35455/itv/2000000004000000047.m3u8?&cdn=hnbblive
iHOT爱科幻,http://b.zgjok.com:35455/itv/2000000004000000033.m3u8?&cdn=hnbblive
iHOT爱谍战,http://b.zgjok.com:35455/itv/2000000004000000038.m3u8?&cdn=hnbblive
iHOT爱赛车,http://b.zgjok.com:35455/itv/2000000004000000055.m3u8?&cdn=hnbblive
iHOT爱院线,http://b.zgjok.com:35455/itv/2000000004000000034.m3u8?&cdn=hnbblive
iHOT爱奇谈,http://b.zgjok.com:35455/itv/2000000004000000058.m3u8?&cdn=hnbblive
iHOT爱体育,http://b.zgjok.com:35455/itv/2000000004000000060.m3u8?&cdn=hnbblive
iHOT爱谍战,http://b.zgjok.com:35455/itv/6000000006000070630.m3u8?cdn=wasusyt&Contentid=6000000006000070630
iHOT爱动漫,http://b.zgjok.com:35455/itv/6000000006000280630.m3u8?cdn=wasusyt&Contentid=6000000006000280630
iHOT爱科幻,http://b.zgjok.com:35455/itv/6000000006000020630.m3u8?cdn=wasusyt&Contentid=6000000006000020630
iHOT爱科学,http://b.zgjok.com:35455/itv/6000000006000160630.m3u8?cdn=wasusyt&Contentid=6000000006000160630
iHOT爱浪漫,http://b.zgjok.com:35455/itv/6000000006000040630.m3u8?cdn=wasusyt&Contentid=6000000006000040630
iHOT爱历史,http://b.zgjok.com:35455/itv/6000000006000150630.m3u8?cdn=wasusyt&Contentid=6000000006000150630
iHOT爱旅行,http://b.zgjok.com:35455/itv/6000000006000250630.m3u8?cdn=wasusyt&Contentid=6000000006000250630
iHOT爱奇谈,http://b.zgjok.com:35455/itv/6000000006000270630.m3u8?cdn=wasusyt&Contentid=6000000006000270630
iHOT爱青春,http://b.zgjok.com:35455/itv/6000000006000100630.m3u8?cdn=wasusyt&Contentid=6000000006000100630
iHOT爱赛车,http://b.zgjok.com:35455/itv/6000000006000240630.m3u8?cdn=wasusyt&Contentid=6000000006000240630
iHOT爱体育,http://b.zgjok.com:35455/itv/6000000006000290630.m3u8?cdn=wasusyt&Contentid=6000000006000290630
iHOT爱玩具,http://b.zgjok.com:35455/itv/6000000006000220630.m3u8?cdn=wasusyt&Contentid=6000000006000220630
iHOT爱喜剧,http://b.zgjok.com:35455/itv/6000000006000010630.m3u8?cdn=wasusyt&Contentid=6000000006000010630
iHOT爱悬疑,http://b.zgjok.com:35455/itv/6000000006000050630.m3u8?cdn=wasusyt&Contentid=6000000006000050630
iHOT爱幼教,http://b.zgjok.com:35455/itv/6000000006000180630.m3u8?cdn=wasusyt&Contentid=6000000006000180630
iHOT爱院线,http://b.zgjok.com:35455/itv/6000000006000030630.m3u8?cdn=wasusyt&Contentid=6000000006000030630
iHot风尚音乐,http://b.zgjok.com:35455/itv/2000000004000000004.m3u8?cdn=hnbblive&Contentid=2000000004000000004
iHot风尚音乐,http://b.zgjok.com:35455/itv/5529729098703832176.m3u8?cdn=wasusyt&Contentid=5529729098703832176
iHot精品剧场,http://b.zgjok.com:35455/itv/2000000004000000002.m3u8?cdn=hnbblive&Contentid=2000000004000000002
iHot精品剧场,http://b.zgjok.com:35455/itv/8230197131234717902.m3u8?cdn=wasusyt&Contentid=8230197131234717902
iHot欧美影院,http://b.zgjok.com:35455/itv/2000000004000000005.m3u8?cdn=hnbblive&Contentid=2000000004000000005
iHot欧美影院,http://b.zgjok.com:35455/itv/7185203501769528108.m3u8?cdn=wasusyt&Contentid=7185203501769528108
iHot亚洲影院,http://b.zgjok.com:35455/itv/2000000004000000006.m3u8?cdn=hnbblive&Contentid=2000000004000000006
iHot亚洲影院,http://b.zgjok.com:35455/itv/5841816227539527643.m3u8?cdn=wasusyt&Contentid=5841816227539527643
NEWTV精品综合,http://b.zgjok.com:35455/itv/1000000004000019008.m3u8?cdn=ystenlive&Contentid=1000000004000019008
NEWTV精品大剧,http://b.zgjok.com:35455/itv/1000000004000013968.m3u8?cdn=ystenlive&Contentid=1000000004000013968
NEWTV精品纪录,http://b.zgjok.com:35455/itv/1000000004000013730.m3u8?cdn=ystenlive&Contentid=1000000004000013730
NEWTV精品体育,http://b.zgjok.com:35455/itv/1000000004000014634.m3u8?cdn=ystenlive&Contentid=1000000004000014634
NEWTV精品萌宠,http://b.zgjok.com:35455/itv/1000000006000032328.m3u8?cdn=ystenlive&Contentid=1000000006000032328
NEWTV爱情喜剧,http://b.zgjok.com:35455/itv/2000000003000000010.m3u8?cdn=hnbblive&Contentid=2000000003000000010
NEWTV超级电视剧,http://b.zgjok.com:35455/itv/1000000006000268003.m3u8?cdn=ystenlive&Contentid=1000000006000268003
NEWTV超级电影,http://b.zgjok.com:35455/itv/1000000003000012426.m3u8?cdn=ystenlive&Contentid=1000000003000012426
NEWTV超级体育,http://b.zgjok.com:35455/itv/1000000001000009601.m3u8?cdn=ystenlive&Contentid=1000000001000009601
NEWTV超级综艺,http://b.zgjok.com:35455/itv/1000000006000268002.m3u8?cdn=ystenlive&Contentid=1000000006000268002
NEWTV潮妈辣婆,http://b.zgjok.com:35455/itv/2000000003000000018.m3u8?cdn=hnbblive&Contentid=2000000003000000018
NEWTV东北热剧,http://b.zgjok.com:35455/itv/1000000005000266013.m3u8?cdn=ystenlive&Contentid=1000000005000266013
NEWTV动作电影,http://b.zgjok.com:35455/itv/1000000004000018653.m3u8?cdn=ystenlive&Contentid=1000000004000018653
NEWTV古装剧场,http://b.zgjok.com:35455/itv/2000000003000000024.m3u8?cdn=hnbblive&Contentid=2000000003000000024
NEWTV欢乐剧场,http://b.zgjok.com:35455/itv/1000000005000266012.m3u8?cdn=ystenlive&Contentid=1000000005000266012
NEWTV家庭剧场,http://b.zgjok.com:35455/itv/1000000004000008284.m3u8?cdn=ystenlive&Contentid=1000000004000008284
NEWTV金牌综艺,http://b.zgjok.com:35455/itv/1000000004000026167.m3u8?cdn=ystenlive&Contentid=1000000004000026167
NEWTV惊悚悬疑,http://b.zgjok.com:35455/itv/1000000004000024282.m3u8?cdn=ystenlive&Contentid=1000000004000024282
NEWTV军旅剧场,http://b.zgjok.com:35455/itv/2000000003000000014.m3u8?cdn=hnbblive&Contentid=2000000003000000014
NEWTV军事评论,http://b.zgjok.com:35455/itv/2000000003000000022.m3u8?cdn=hnbblive&Contentid=2000000003000000022
NEWTV魅力潇湘,http://b.zgjok.com:35455/itv/1000000001000006197.m3u8?cdn=ystenlive&Contentid=1000000001000006197
NEWTV明星大片,http://b.zgjok.com:35455/itv/2000000003000000016.m3u8?cdn=hnbblive&Contentid=2000000003000000016
NEWTV农业致富,http://b.zgjok.com:35455/itv/2000000003000000003.m3u8?cdn=hnbblive&Contentid=2000000003000000003
NEWTV武博世界,http://b.zgjok.com:35455/itv/2000000003000000007.m3u8?cdn=hnbblive&Contentid=2000000003000000007
NEWTV炫舞未来,http://b.zgjok.com:35455/itv/1000000001000000515.m3u8?cdn=ystenlive&Contentid=1000000001000000515
NEWTV怡伴健康,http://b.zgjok.com:35455/itv/1000000005000266011.m3u8?cdn=ystenlive&Contentid=1000000005000266011
NEWTV中国功夫,http://b.zgjok.com:35455/itv/2000000003000000009.m3u8?cdn=hnbblive&Contentid=2000000003000000009
SiTV动漫秀场,http://b.zgjok.com:35455/itv/5000000011000031113.m3u8?cdn=bestzb&Contentid=5000000011000031113
SiTV都市剧场,http://b.zgjok.com:35455/itv/5000000011000031111.m3u8?cdn=bestzb&Contentid=5000000011000031111
SiTV法治天地,http://b.zgjok.com:35455/itv/9001547084732463424.m3u8?cdn=bestzb&Contentid=9001547084732463424
SiTV欢笑剧场,http://b.zgjok.com:35455/itv/5000000002000009455.m3u8?cdn=bestzb&Contentid=5000000002000009455
SiTV欢笑剧场,http://b.zgjok.com:35455/itv/5000000007000010001.m3u8?cdn=bestzb&Contentid=5000000007000010001
SiTV金色学堂,http://b.zgjok.com:35455/itv/5000000010000026105.m3u8?cdn=bestzb&Contentid=5000000010000026105
SiTV劲爆体育,http://b.zgjok.com:35455/itv/5000000002000029972.m3u8?cdn=bestzb&Contentid=5000000002000029972
SiTV乐游,http://b.zgjok.com:35455/itv/5000000011000031112.m3u8?cdn=bestzb&Contentid=5000000011000031112
SiTV魅力足球,http://b.zgjok.com:35455/itv/5000000011000031207.m3u8?cdn=bestzb&Contentid=5000000011000031207
SiTV七彩戏剧,http://b.zgjok.com:35455/itv/5000000011000031116.m3u8?cdn=bestzb&Contentid=5000000011000031116
SiTV生活时尚,http://b.zgjok.com:35455/itv/5000000002000019634.m3u8?cdn=bestzb&Contentid=5000000002000019634
SiTV游戏风云,http://b.zgjok.com:35455/itv/5000000011000031114.m3u8?cdn=bestzb&Contentid=5000000011000031114
纪实人文,http://b.zgjok.com:35455/itv/5000000004000010282.m3u8?cdn=bestzb&Contentid=5000000004000010282
纪实人文,http://b.zgjok.com:35455/itv/1000000001000010606.m3u8?cdn=ystenlive&Contentid=1000000005000265021
第一财经,http://b.zgjok.com:35455/itv/5000000010000027146.m3u8?cdn=bestzb&Contentid=5000000010000027146
东方财经,http://b.zgjok.com:35455/itv/5000000007000010003.m3u8?cdn=bestzb&Contentid=5000000007000010003
东方影视,http://b.zgjok.com:35455/itv/5000000010000032212.m3u8?cdn=bestzb&Contentid=5000000010000032212
求索动物,http://b.zgjok.com:35455/itv/2000000004000000009.m3u8?cdn=hnbblive
求索纪录,http://b.zgjok.com:35455/itv/2000000004000000010.m3u8?cdn=hnbblive
求索科学,http://b.zgjok.com:35455/itv/2000000004000000011.m3u8?cdn=hnbblive
求索生活,http://b.zgjok.com:35455/itv/2000000004000000008.m3u8?cdn=hnbblive
纪实科教,http://b.zgjok.com:35455/itv/1000000001000001910.m3u8?cdn=ystenlive&Contentid=1000000001000001910
纪实科教,http://b.zgjok.com:35455/itv/1000000005000265020.m3u8?cdn=ystenlive&Contentid=1000000005000265020
华数4K,http://b.zgjok.com:35455/itv/6000000003000004748.m3u8?cdn=wasusyt&Contentid=6000000003000004748
纯享4K,http://b.zgjok.com:35455/itv/1000000004000011651.m3u8?cdn=ystenlive&Contentid=1000000004000011651"""

    solid_channels = """🤩3D频道🤩,#genre#
3D0,https://vd2.bdstatic.com/mda-kfhr50vjwtmttwxc/v1-cae/sc/mda-kfhr50vjwtmttwxc.mp4
3D1,https://vd4.bdstatic.com/mda-mdfijn4crxseyky0/1080p/cae_h264/1618549960/mda-mdfijn4crxseyky0.mp4
3d4,https://vd2.bdstatic.com/mda-kmtfv6y5gctpa35w/sc/mda-kmtfv6y5gctpa35w.mp4
3D5,https://vd2.bdstatic.com/mda-kkfx81ffgjvk2qja/v1-cae/sc/mda-kkfx81ffgjvk2qja.mp4
3D投影1,https://vd4.bdstatic.com/mda-ncuizu4wfrjswzxp/720p/h264_delogo/1648560283895563574/mda-ncuizu4wfrjswzxp.mp4
3D投影2,https://vd4.bdstatic.com/mda-ncuiyrw7qj9x5w3z/720p/h264_delogo/1648560203494563586/mda-ncuiyrw7qj9x5w3z.mp4
AA,https://vd3.bdstatic.com/mda-mfnc43q5ngnzua6p/sc/cae_h264/1624437508830556235/mda-mfnc43q5ngnzua6p.mp4
Bicycle,https://vd2.bdstatic.com/mda-mbirabhun6n01ucc/v1-cae/1080p/mda-mbirabhun6n01ucc.mp4
Dreamcatcher,https://vd3.bdstatic.com/mda-mbiqgzsnfeyv74y6/v1-cae/1080p/mda-mbiqgzsnfeyv74y6.mp4
MV,https://vd4.bdstatic.com/mda-kmbika46ppvf7nzc/v1-cae/1080p/mda-kmbika46ppvf7nzc.mp4
X战警：黑凤凰,https://vd2.bdstatic.com/mda-jetjizur4bnmfux8/hd/mda-jetjizur4bnmfux8.mp4
变形金刚1,https://vd3.bdstatic.com/mda-khb9j4g6c25biyqj/v1-cae/1080p/mda-khb9j4g6c25biyqj.mp4
变形金刚2K,https://vd3.bdstatic.com/mda-nd6k8tnavw6sj0a5/qhd/cae_h264_delogo/1649341416716222901/mda-nd6k8tnavw6sj0a5.mp4
变形金刚4K,https://vd3.bdstatic.com/mda-nd6k8tnavw6sj0a5/uhd/cae_h264_delogo/1649341416749683469/mda-nd6k8tnavw6sj0a5.mp4
变形金刚LD,https://vd3.bdstatic.com/mda-nd6k8tnavw6sj0a5/1080p/cae_h264_delogo/1649341416696755483/mda-nd6k8tnavw6sj0a5.mp4
变形金刚UHD,https://vd3.bdstatic.com/mda-nd6k8tnavw6sj0a5/720p/h264_delogo/1649341231263414752/mda-nd6k8tnavw6sj0a5.mp4
不同国家,https://vd2.bdstatic.com/mda-ncm7bqn1fvayqcac/sc/cae_h264_delogo/1647926240143319597/mda-ncm7bqn1fvayqcac.mp4
长津湖,https://vd3.bdstatic.com/mda-mgq3kek3j2cr07w7/sc/cae_h264_nowatermark/1627180666806871183/mda-mgq3kek3j2cr07w7.mp4
大橘,https://vd4.bdstatic.com/mda-ma2gq0my4ar6a8dz/v1-cae/1080p/mda-ma2gq0my4ar6a8dz.mp4
大片3D,https://vd2.bdstatic.com/mda-ki2cvyhz79rw40wg/v1-cae/sc/mda-ki2cvyhz79rw40wg.mp4
电影,https://vd3.bdstatic.com/mda-kj0kfvyty9dk9nk0/v1-cae/sc/mda-kj0kfvyty9dk9nk0.mp4
东京-新宿,https://vd4.bdstatic.com/mda-na6metzpvv5xqh6h/1080p/cae_h264/1641623274673701803/mda-na6metzpvv5xqh6h.mp4
钢铁侠,https://vd4.bdstatic.com/mda-narbupksqbu5yyiy/sc/cae_h264_nowatermark_delogo/1643187081773112317/mda-narbupksqbu5yyiy.mp4
功夫之王,https://vdse.bdstatic.com//92bd4a8082ab3cb7e96e1d852bc0d5f4.mp4?authorization=bce-auth-v1%2F40f207e648424f47b2e3dfbb1014b1a5%2F2022-05-07T19%3A35%3A37Z%2F-1%2Fhost%2Fbac03dc21a0ea989035da20433039cdcc82efc3a5773df7c4dbcf4d6b6d62443
混剪3D,https://vd3.bdstatic.com/mda-kksk814vwc1m06av/sc/mda-kksk814vwc1m06av.mp4
精美,https://vd4.bdstatic.com/mda-mjak88esahdcpmc5/1080p/cae_h264/1633962937397290860/mda-mjak88esahdcpmc5.mp4
龙腾虎跃,https://vd2.bdstatic.com/mda-nb48vhn84vq41zf3/1080p/cae_h264_delogo/1644042257215201305/mda-nb48vhn84vq41zf3.mp4
裸眼3D,https://vd2.bdstatic.com/mda-kka520dkkf8mrujz/sc/mda-kka520dkkf8mrujz.mp4
裸眼3D2,https://vd4.bdstatic.com/mda-mdfijn4crxseyky0/sc/mda-mdfijn4crxseyky0.mp4
木叶上忍的究极对决,https://vd4.bdstatic.com/mda-mahnrqxb6xvgzyte/sc/cae_h264_nowatermark/1610957664/mda-mahnrqxb6xvgzyte.mp4
千里江山图,https://vd4.bdstatic.com/mda-ncrggyx20mz0s134/sc/cae_h264_delogo/1648294922621791952/mda-ncrggyx20mz0s134.mp4
生物多样性,https://vd3.bdstatic.com/mda-ne6irx2irbjbbr6v/sc/cae_h264/1651932935194074079/mda-ne6irx2irbjbbr6v.mp4
视觉艺术,https://vd2.bdstatic.com/mda-ncj8cwfhcr4zyrfd/sc/cae_h264_delogo/1647755833056552862/mda-ncj8cwfhcr4zyrfd.mp4
司藤,https://vd4.bdstatic.com/mda-nae2xzfan0zk06f7/sc/cae_h264_delogo/1642265942028031063/mda-nae2xzfan0zk06f7.mp4
头号玩家,https://vd2.bdstatic.com/mda-kknwdmibvdrfaavv/v1-cae/1080p/mda-kknwdmibvdrfaavv.mp4
玩家,https://vd3.bdstatic.com/mda-kbhkh7z58qvsn0a1/mda-kbhkh7z58qvsn0a1.mp4
小丑,https://vd2.bdstatic.com/mda-jkbrts1znp07ryb8/sc/mda-jkbrts1znp07ryb8.mp4"""

    # 读取文件内容
    with open('iptv.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    # 替换内容
    content = content.replace("🇨🇳央视频道🇨🇳,#genre#", cctv_channels)
    content = content.replace("🛰️卫视频道🛰️,#genre#", satellite_channels)
    content = content.replace("🇭🇰港澳台🇭🇰,#genre#", hot_channels)
    content = content.replace("🏆咪咕体育🏆,#genre#", migu_channels)
    content = content.replace("🤩3D频道🤩,#genre#", solid_channels)

    # 写回文件
    with open('iptv.txt', 'w', encoding='utf-8') as file:
        file.write(content)

    # 去重 iptv.txt 文件内容
    # remove_duplicates('iptv.txt')
    
    # 生成 iptv.m3u 文件 x-tvg-url="https://raw.githubusercontent.com/Troray/IPTV/main/tvxml.xml,https://raw.githubusercontent.com/Meroser/EPG-test/main/tvxml-test.xml.gz" catchup="append" catchup-source="?playseek=${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}"

    output_text = '#EXTM3U x-tvg-url="https://raw.githubusercontent.com/Troray/IPTV/main/tvxml.xml,https://raw.githubusercontent.com/Meroser/EPG-test/main/tvxml-test.xml.gz"\n'

    with open("iptv.txt", "r", encoding='utf-8') as file:
        input_text = file.read()

    lines = input_text.strip().split("\n")
    group_name = ""
    for line in lines:
        parts = line.split(",")
        if len(parts) == 2 and "#genre#" in line:
            group_name = parts[0]
        elif len(parts) == 2:
            output_text += f"#EXTINF:-1 group-title=\"{group_name}\",{parts[0]}\n"
            output_text += f"{parts[1]}\n"

    with open("iptv.m3u", "w", encoding='utf-8') as file:
        file.write(output_text)

    print("新增频道在线检测完毕，结果已存入 whitelist.txt 和 blacklist.txt。")
    print(f"iptv.txt iptv.m3u 文件已生成，有效频道总数为 : {len(lines)}")
