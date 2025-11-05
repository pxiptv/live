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
    part_str = part_str.replace("-4K", " 4K")  # 替换
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
	'https://raw.githubusercontent.com/luoye20230624/hndxzb/main/iptv_list.txt',	
	'https://d.kstore.dev/download/15366/6988.txt'
	#'https://raw.bgithub.xyz/Guovin/iptv-api/gd/output/result.txt',
	#'https://fy.iptv1.ggff.net/?url=http://www.douzhicloud.site:35455',
	#'https://raw.bgithub.xyz/qq49371114/collect-tv-txt/main/live_lite.txt',
		
	#'https://xcz.funly.us/live.txt',
	#'https://raw.bgithub.xyz/yuanzl77/IPTV/main/live.txt',
	#'https://raw.bgithub.xyz/Wirili/IPTV/main/live.txt',
	#'https://raw.bgithub.xyz/lc529180405/caicai/main/%E6%9E%81%E8%A7%86%E8%A7%A3%E5%AF%86.txt',
    #'https://raw.bgithub.xyz/suxuang/myIPTV/main/ipv6.m3u',
	#'https://raw.bgithub.xyz/iptv-js/iptv-js.github.io/main/ss_itv.m3u',
	#'https://raw.bgithub.xyz/250992941/iptv/main/st1.txt',
    #'https://raw.bgithub.xyz/alonezou/yn-iptv/main/reference/MyIPTV',
    #'https://raw.bgithub.xyz/qist/tvbox/master/tvlive.txt',
    #'https://raw.bgithub.xyz/leyan1987/iptv/main/iptvnew.txt',
    #'https://raw.bgithub.xyz/maitel2020/iptv-self-use/main/iptv.txt', 
    #'https://gitlab.com/p2v5/wangtv/-/raw/main/wang-tvlive.txt'
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
CCTV1,https://migu.188766.xyz/?migutoken=50b17da85782ad968983c2746a3ecf59&id=CCTV1&type=yy
CCTV2,https://migu.188766.xyz/?migutoken=7841b8adc4bcfdcca35794067f014d25&id=CCTV2&type=yy
CCTV3,https://migu.188766.xyz/?migutoken=c6891ddd9767e0c9f9b0f9a3aaf90c8b&id=CCTV3&type=yy
CCTV4,https://migu.188766.xyz/?migutoken=e6a7be05ac76970c85926ce47a4d9c16&id=CCTV4&type=yy
CCTV5,https://migu.188766.xyz/?migutoken=8c596235c383b8d21a8db06fa3a6341f&id=CCTV5&type=yy
CCTV5+,https://migu.188766.xyz/?migutoken=c079a5251fc80c1d24fc1dcc7fd22857&id=CCTV5p&type=yy
CCTV6,https://migu.188766.xyz/?migutoken=095457749dc05a731a395617ab04949c&id=CCTV6&type=yy
CCTV7,https://migu.188766.xyz/?migutoken=5d5172943342247b1cb222a9ac5fc466&id=CCTV7&type=yy
CCTV8,https://migu.188766.xyz/?migutoken=bf7c0c509e507d01741102d404b99746&id=CCTV8&type=yy
CCTV9,https://migu.188766.xyz/?migutoken=e25de42a224e642a3594b1e93cf3ed1b&id=CCTV9&type=yy
CCTV10,https://migu.188766.xyz/?migutoken=8b89795de1cc74318bf5c6293a4d6fa0&id=CCTV10&type=yy
CCTV11,https://migu.188766.xyz/?migutoken=928b715caf282de3d57af8064343951d&id=CCTV11&type=yy
CCTV12,https://migu.188766.xyz/?migutoken=ed40b34faedf6d9fa8120a05c837f693&id=CCTV12&type=yy
CCTV13,https://migu.188766.xyz/?migutoken=f2da258e6735fdb1f0c223b11149efa1&id=CCTV13&type=yy
CCTV14,https://migu.188766.xyz/?migutoken=fad1feedb99d17fc8ec110df724186d3&id=CCTV14&type=yy
CCTV15,https://migu.188766.xyz/?migutoken=0d9a225defe44aff2149561898573a77&id=CCTV15&type=yy
CCTV17,https://migu.188766.xyz/?migutoken=2f35c22bcc0bf8ec4d5df35fda777766&id=CCTV17&type=yy
CCTV1,https://migu.188766.xyz/?migutoken=058116fbb26e8951fe2155c9a751d905&id=CCTV1&type=yy
CCTV2,https://migu.188766.xyz/?migutoken=579981f6c852e250e5d5ff746e20c1da&id=CCTV2&type=yy
CCTV4,https://migu.188766.xyz/?migutoken=c228696a8c2f743d3ef216f344a98977&id=CCTV4&type=yy
CCTV5,https://migu.188766.xyz/?migutoken=27cb71aa8c5613fa445122fc0f66fa66&id=CCTV5&type=yy
CCTV5+,https://migu.188766.xyz/?migutoken=d2cd1916deb6f266df065efa10cb9dc4&id=CCTV5p&type=yy
CCTV8,https://migu.188766.xyz/?migutoken=8a0286a4ddfe3a0094414176b502c024&id=CCTV8&type=yy
CCTV9,https://migu.188766.xyz/?migutoken=9152adb8c108dfd57350f0155411384d&id=CCTV9&type=yy
CCTV10,https://migu.188766.xyz/?migutoken=a6ea9919efff70e8b58dbf6352764b65&id=CCTV10&type=yy
CCTV13,https://migu.188766.xyz/?migutoken=18533d4d908fc58c106315210042a966&id=CCTV13&type=yy
CCTV14,https://migu.188766.xyz/?migutoken=feb129122007256f7d5c543638f3c2bb&id=CCTV14&type=yy
CCTV17,https://migu.188766.xyz/?migutoken=2d1bdb0dad80b47e7c90052c3df56b35&id=CCTV17&type=yy"""

    satellite_channels = """🛰️卫视频道🛰️,#genre#
湖南卫视,https://migu.188766.xyz/?migutoken=ae73ef66bd109f114cf569d2220a3797&id=hnws&type=sz
浙江卫视,https://migu.188766.xyz/?migutoken=59e99918a255463297aa2b79d8c52ff6&id=%E6%B5%99%E6%B1%9F%E5%8D%AB%E8%A7%86&pp=1
浙江卫视,https://ali-m-l.cztv.com/channels/lantian/channel001/1080p.m3u8
江苏卫视,https://migu.188766.xyz/?migutoken=32b6e40243e3018caba1eece9824470d&id=%E6%B1%9F%E8%8B%8F%E5%8D%AB%E8%A7%86&type=yy
东方卫视,https://migu.188766.xyz/?migutoken=ee72e71131bb44ca0cb5afb0de13fed4&id=%E4%B8%9C%E6%96%B9%E5%8D%AB%E8%A7%86&type=yy
广东卫视,https://migu.188766.xyz/?migutoken=57a4d59310e507a243a9e1faa1d7c83e&id=%E5%B9%BF%E4%B8%9C%E5%8D%AB%E8%A7%86&type=yy
河南卫视,https://migu.188766.xyz/?migutoken=5c56f9fe9f7d7cefdf261569960c940b&id=%E6%B2%B3%E5%8D%97%E5%8D%AB%E8%A7%86%E9%AB%98%E6%B8%85&type=yy
海南卫视,https://migu.188766.xyz/?migutoken=14faabef39292696f0a771e42955d81a&id=hn_hnws&type=sz
湖北卫视,https://migu.188766.xyz/?migutoken=288b192300b89db840e4c9928a5de8b4&id=%E6%B9%96%E5%8C%97%E5%8D%AB%E8%A7%86&type=yy
江西卫视,https://migu.188766.xyz/?migutoken=8e7e43f88dc06a1f0d9667b237b7c60e&id=%E6%B1%9F%E8%A5%BF%E5%8D%AB%E8%A7%86&type=yy
辽宁卫视,https://migu.188766.xyz/?migutoken=ab330788c285a4cf92446a7e0a05fcc2&id=%E8%BE%BD%E5%AE%81%E5%8D%AB%E8%A7%86&type=yy
陕西卫视,https://migu.188766.xyz/?migutoken=7db4ee466ac1acc7ca548fef57495403&id=%E9%99%95%E8%A5%BF%E5%8D%AB%E8%A7%86&type=yy
三沙卫视,https://migu.188766.xyz/?migutoken=94d4cba38ba093b91ba52809e0b8eb46&id=hn_ssws&type=sz
吉林卫视,https://migu.188766.xyz/?migutoken=51534e92696fee1c1f11a88f42af3e2d&id=%E5%90%89%E6%9E%97%E5%8D%AB%E8%A7%86&type=yy
青海卫视,https://migu.188766.xyz/?migutoken=055934c46e0598815d09fce07b763bd0&id=%E9%9D%92%E6%B5%B7%E5%8D%AB%E8%A7%86&type=yy
海南卫视,https://migu.188766.xyz/?migutoken=9e2e9770c38fd57761d105d3603a9ed1&id=%E6%B5%B7%E5%8D%97%E5%8D%AB%E8%A7%86&type=yy
农林卫视,https://migu.188766.xyz/?migutoken=b30d111cb1949ba27d8adc029e22b764&id=%E4%B8%AD%E5%9B%BD%E5%86%9C%E6%9E%97%E5%8D%AB%E8%A7%86&type=yy
内蒙古卫视,https://migu.188766.xyz/?migutoken=df2081409752001dae3bff9d4c3ecd73&id=%E5%86%85%E8%92%99%E5%8F%A4%E5%8D%AB%E8%A7%86&pp=1
兵团卫视,https://migu.188766.xyz/?migutoken=a30c3a7d0e33e403ebf88caf1f7be5e9&id=%E5%85%B5%E5%9B%A2%E5%8D%AB%E8%A7%86&type=yy
大湾区卫视,https://migu.188766.xyz/?migutoken=6d6f3724c8dd08f1956dbfe524d4c2d0&id=%E5%A4%A7%E6%B9%BE%E5%8C%BA%E5%8D%AB%E8%A7%86&type=yy
湖南卫视,https://migu.188766.xyz/?migutoken=3ea0edb779e16d47b7c19af71f68b8d6&id=hnws&type=sz
浙江卫视,https://migu.188766.xyz/?migutoken=1e4b588eba92db60c24f8d458cf44f79&id=%E6%B5%99%E6%B1%9F%E5%8D%AB%E8%A7%86&pp=1
浙江卫视,https://ali-m-l.cztv.com/channels/lantian/channel001/1080p.m3u8
江苏卫视,https://migu.188766.xyz/?migutoken=23acff0ff0ecaef3d340a1a4e7d9ef67&id=%E6%B1%9F%E8%8B%8F%E5%8D%AB%E8%A7%86&type=yy
东方卫视,https://migu.188766.xyz/?migutoken=b4f30afa875eb7c3050026c2f5668021&id=%E4%B8%9C%E6%96%B9%E5%8D%AB%E8%A7%86&type=yy
广东卫视,https://migu.188766.xyz/?migutoken=6f089ea86b898d859145b20935c97f9a&id=%E5%B9%BF%E4%B8%9C%E5%8D%AB%E8%A7%86&type=yy
湖北卫视,https://migu.188766.xyz/?migutoken=8406a166fcb56b8ddf84e2efc0a5db82&id=%E6%B9%96%E5%8C%97%E5%8D%AB%E8%A7%86&type=yy
江西卫视,https://migu.188766.xyz/?migutoken=8e783e5cf54c7552bb4c7aecbeae7d40&id=%E6%B1%9F%E8%A5%BF%E5%8D%AB%E8%A7%86&type=yy
河南卫视,https://migu.188766.xyz/?migutoken=28652f0b3fb8db15e81f1b23084b9edf&id=%E6%B2%B3%E5%8D%97%E5%8D%AB%E8%A7%86&type=yy
陕西卫视,https://migu.188766.xyz/?migutoken=348346c58b70eb6b07e01732b72d7213&id=%E9%99%95%E8%A5%BF%E5%8D%AB%E8%A7%86&type=yy
内蒙古卫视,https://migu.188766.xyz/?migutoken=b5858e0646147a6473f2d100c4c3eb88&id=%E5%86%85%E8%92%99%E5%8F%A4%E5%8D%AB%E8%A7%86&pp=1
大湾区卫视,https://migu.188766.xyz/?migutoken=81d06edbda25811f07fc2923a024fddf&id=%E5%A4%A7%E6%B9%BE%E5%8C%BA%E5%8D%AB%E8%A7%86&type=yy
湖南都市,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000099000000195952/main.m3u8?stbid=
湖南经视,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000099000000194900/main.m3u8?stbid=
湖南电视剧,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000099000000196987/main.m3u8?stbid=
湖南电影,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000099000000197673/main.m3u8?stbid=
湖南娱乐,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000099000000197674/main.m3u8?stbid=
金鹰纪实,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000099000000197675/main.m3u8?stbid=
湖南爱晚,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000099000000197676/main.m3u8?stbid=
湖南国际,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000099000000197677/main.m3u8?stbid=
金鹰卡通,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000099000000197678/main.m3u8?stbid=
湖南教育,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000023000000196697/main.m3u8?stbid=
茶频道,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000025000000316196/main.m3u8?stbid=
深圳都市,http://rfx2018.55555.io:2345/udp/239.77.1.176:5146
深圳财经生活,http://rfx2018.55555.io:2345/udp/239.77.1.242:5146
深圳少儿,http://rfx2018.55555.io:2345/udp/239.77.1.244:5146
深圳宝安,http://rfx2018.55555.io:2345/udp/239.77.1.67:5146
深圳龙岗,http://rfx2018.55555.io:2345/udp/239.77.1.223:5146
深圳都市,http://sub.mtoo.vip:8333/udp/239.77.1.176:5146
深圳财经生活,http://sub.mtoo.vip:8333/udp/239.77.1.242:5146
深圳少儿,http://sub.mtoo.vip:8333/udp/239.77.1.244:5146
深圳都市,http://ha.m-too.top:8333/udp/239.77.1.176:5146
深圳财经生活,http://ha.m-too.top:8333/udp/239.77.1.242:5146
深圳少儿,http://ha.m-too.top:8333/udp/239.77.1.244:5146"""

    hot_channels = """🇭🇰港澳台🇭🇰,#genre#
凤凰中文,http://43.152.143.193:80/1.v.smtcdns.net/tvlive.fengshows.cn/live/0701pcc72.flv
凤凰资讯,http://43.152.143.193:80/1.v.smtcdns.net/tvlive.fengshows.cn/live/0701pin72.flv
凤凰香港,http://43.152.143.193:80/1.v.smtcdns.net/tvlive.fengshows.cn/live/0701phk72.flv
凤凰中文,https://migu.188766.xyz/?migutoken=dafea9a89f8759bcd04edfafc63b435d&id=fhzw&pp=1
凤凰中文,https://migu.188766.xyz/?migutoken=bf161ac290d85d4778ebc36e83daeb42&id=phoenixtv_hd&type=dy
凤凰资讯,https://migu.188766.xyz/?migutoken=9b308c31f6f659e7ee7bc6bb4b3cfff9&id=fhzx&pp=1
凤凰资讯,https://migu.188766.xyz/?migutoken=5a850debc67f6090a63d625e8a4b9764&id=phoenixinfo_hd&type=dy
凤凰香港,https://migu.188766.xyz/?migutoken=407dc0f7365332e4297cc4be4e80ab8b&id=fhhk&pp=1
凤凰香港,https://migu.188766.xyz/?migutoken=8ea86101844c05d6675be46a790325aa&id=hkphoenix_twn&type=dy
凤凰中文,https://mgev.188766.xyz/?migutoken=3267cd6151f58a4919b93c0e63f69337&id=fhzw&pp=1
凤凰中文,https://migu.188766.xyz/?migutoken=866341f35ab82e48dea654d12b6e5881&id=hk_fhzw&type=dy
凤凰资讯,https://mgev.188766.xyz/?migutoken=85fccb710060e734ed36c45940532bff&id=fhzx&pp=1
凤凰资讯,https://migu.188766.xyz/?migutoken=902dd46104f7da4e91108d392b281213&id=hk_fhzx&type=dy
凤凰香港,https://mgev.188766.xyz/?migutoken=0c151f885334200f0142117a9e167f8c&id=fhhk&pp=1
凤凰香港,https://migu.188766.xyz/?migutoken=d88da94088e229852fad7e3b27e37c04&id=hk_fhhk&type=dy
翡翠台,https://migu.188766.xyz/?migutoken=6ff40ca6e9a458a448fdb09a33919405&id=%E7%BF%A1%E7%BF%A0%E5%8F%B0&pp=1
翡翠台,https://migu.188766.xyz/?migutoken=af18bef2634b43fa854485eefdd5a91d&id=jade_twn&type=dy
无线新闻,https://migu.188766.xyz/?migutoken=38eea02778765b91accfcc9b762c37a5&id=inews_twn&type=dy
明珠台,https://migu.188766.xyz/?migutoken=2cd4c549faf4bb0b9d50f4547a25aa13&id=pearl_twn&type=dy
翡翠台,https://migu.188766.xyz/?migutoken=04145df78ef83eef5b830ef166351e04&id=hk_fct&type=dy
翡翠台4K,https://migu.188766.xyz/?migutoken=f5d3ddc45a607cb46f85565d6002e6fe&id=hk_fct4k&type=dy
无线新闻,https://migu.188766.xyz/?migutoken=6d40ea4a8dd9f18c5bfbddaf30a8e3b9&id=hk_wxxw&type=dy
Now新闻台,https://migu.188766.xyz/?migutoken=c279dda66e730c35558e092884fdb1dc&id=hk_now&type=dy
TVB Plus,https://migu.188766.xyz/?migutoken=16d671d8ea4bb37c1ccc5450cfce72d2&id=hk_tvbp&type=dy
明珠台,https://migu.188766.xyz/?migutoken=bc0f802ab684ad9377fe77a79c51de79&id=hk_mzt&type=dy
TVB星河,https://migu.188766.xyz/?migutoken=fa5509d3453723e42e49f4187e199f7c&id=hk_tvbxh&type=dy
TVB功夫,https://migu.188766.xyz/?migutoken=8a398d2b6b543d4e99df237897cfd4bf&id=hk_yzwx&type=dy
八度空间,https://migu.188766.xyz/?migutoken=dabecf5b3f67ce286f4c60ac66b74f89&id=hk_8tv&type=dy
CHU,https://migu.188766.xyz/?migutoken=6e8e543491f6cced998cf2447e869807&id=hk_chu&type=dy
CH5,https://migu.188766.xyz/?migutoken=743ae3a1579b552141abb1ec825c5f86&id=hk_ch5&type=dy
CH8,https://migu.188766.xyz/?migutoken=b4beafba7f583f9f6bf135f83cabfb39&id=hk_ch8&type=dy
澳视澳门,https://migu.188766.xyz/?migutoken=ce19ac7ba26536bfb8a71fa37e934d32&id=hk_asam&type=dy
HOY77,https://migu.188766.xyz/?migutoken=9cd32ab08eaf1f9ab6155d8342a6c0b3&id=hk_hoy&type=dy
中天新闻,https://smt.858.qzz.io/Smart.php?id=ctinews
中视新闻,https://smt.858.qzz.io/Smart.php?id=zhongshinews_twn
东森新闻,https://smt.858.qzz.io/Smart.php?id=ettvnews
三立综合,https://smt.858.qzz.io/Smart.php?id=sanlizhonghe
台视新闻,https://smt.858.qzz.io/Smart.php?id=ttvnews_twn
民视新闻,https://smt.858.qzz.io/Smart.php?id=ftvnew_taiwan
寰宇新闻,https://smt.858.qzz.io/Smart.php?id=huanyuxinwen_twn
非凡新闻,https://smt.858.qzz.io/Smart.php?id=feifannews_twn
年代新闻,https://smt.858.qzz.io/Smart.php?id=niandainews_twn
TVBS新闻,https://smt.858.qzz.io/Smart.php?id=tvbs_n
中天亚洲,https://smt.858.qzz.io/Smart.php?id=ctiasia_twn
AXN电影,https://smt.858.qzz.io/Smart.php?id=axn_twn
AstroMTV,https://smt.858.qzz.io/Smart.php?id=AstroMTV
EYE-旅游,https://smt.858.qzz.io/Smart.php?id=eyetvtravel_twn
EYE-戏剧,https://smt.858.qzz.io/Smart.php?id=eyetvxiju_twn
HitsMovie,https://smt.858.qzz.io/Smart.php?id=Hitsmovie
StarMovies,https://smt.858.qzz.io/Smart.php?id=starmovies_raj
StarmaaMovies,https://smt.858.qzz.io/Smart.php?id=starmaamovies_raj
TVBAsia,https://smt.858.qzz.io/Smart.php?id=Tvbasia
八大第一,https://smt.858.qzz.io/Smart.php?id=badafirst
八大戏剧,https://smt.858.qzz.io/Smart.php?id=badadrama
八大娱乐,https://smt.858.qzz.io/Smart.php?id=badaentertain
八大综合,https://smt.858.qzz.io/Smart.php?id=badazhonghe
大爱贰台,https://smt.858.qzz.io/Smart.php?id=daai2_twn
大爱壹台,https://smt.858.qzz.io/Smart.php?id=daai_twn
东森财经,https://smt.858.qzz.io/Smart.php?id=ettvcaijing_twn
东森电影,https://smt.858.qzz.io/Smart.php?id=ettvmovie
东森戏剧,https://smt.858.qzz.io/Smart.php?id=ettvdrama
东森洋片,https://smt.858.qzz.io/Smart.php?id=ettvwestern
东森幼幼,https://smt.858.qzz.io/Smart.php?id=yoyo_twn
东森综合,https://smt.858.qzz.io/Smart.php?id=ettvzhonghe
公视台语,https://smt.858.qzz.io/Smart.php?id=ctv2_twn
华视闽南,https://smt.858.qzz.io/Smart.php?id=ctshd_twn
寰宇财经,https://smt.858.qzz.io/Smart.php?id=huanyutaiwan_twn
龙祥电影,https://smt.858.qzz.io/Smart.php?id=lungxiangtime_twn
美亚电影,https://smt.858.qzz.io/Smart.php?id=meiyamovie_twn
民视第一,https://smt.858.qzz.io/Smart.php?id=lunghuajingdian_twn
民视闽南,https://smt.858.qzz.io/Smart.php?id=ftvhd_taiwan
三立闽南,https://smt.858.qzz.io/Smart.php?id=sanlitaiwan
三立戏剧,https://smt.858.qzz.io/Smart.php?id=sanlixiju_twn
三立综合,https://smt.858.qzz.io/Smart.php?id=sanlizhonghe
探索亚洲,https://smt.858.qzz.io/Smart.php?id=discoverytwn_twn
天映国特,https://smt.858.qzz.io/Smart.php?id=Celestial
天映经典,https://smt.858.qzz.io/Smart.php?id=Celestial2
天映闽特,https://smt.858.qzz.io/Smart.php?id=Celestialindo
天映粤特,https://smt.858.qzz.io/Smart.php?id=ctv18_twn
tvNMovie,https://smt.858.qzz.io/Smart.php?id=Tvnmovie
纬来电影,https://smt.858.qzz.io/Smart.php?id=videolandmovie
纬来日本,https://smt.858.qzz.io/Smart.php?id=videolandjapan
纬来体育,https://smt.858.qzz.io/Smart.php?id=videolandsport
纬来综合,https://smt.858.qzz.io/Smart.php?id=videolandzonghe
无线翡翠,https://smt.858.qzz.io/Smart.php?id=Tvbjade
无线翡翠,https://smt.858.qzz.io/Smart.php?id=jade_twn
无线娱乐,https://smt.858.qzz.io/Smart.php?id=Tvbentertainment
亚洲旅游,https://smt.858.qzz.io/Smart.php?id=asiatravel_twn
有线新闻,https://smt.858.qzz.io/Smart.php?id=hoycaijing_twn
中视经典,https://smt.858.qzz.io/Smart.php?id=zhongshi_twn
中视闽南,https://smt.858.qzz.io/Smart.php?id=zhongshihd_twn
中天娱乐,https://smt.858.qzz.io/Smart.php?id=ctient
中天综合,https://smt.858.qzz.io/Smart.php?id=ctizhonghe"""
    
    migu_channels = """🏆咪咕体育🏆,#genre#
咪咕直播 1,http://gslbserv.itv.cmvideo.cn:80/3000000001000005308/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000005308&livemode=1&stbId=BingCha
咪咕直播 2,http://gslbserv.itv.cmvideo.cn:80/3000000001000005969/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000005969&livemode=1&stbId=BingCha
咪咕直播 3,http://gslbserv.itv.cmvideo.cn:80/3000000001000007218/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000007218&livemode=1&stbId=BingCha
咪咕直播 4,http://gslbserv.itv.cmvideo.cn:80/3000000001000008001/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000008001&livemode=1&stbId=BingCha
咪咕直播 5,http://gslbserv.itv.cmvideo.cn:80/3000000001000008176/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000008176&livemode=1&stbId=BingCha
咪咕直播 6,http://gslbserv.itv.cmvideo.cn:80/3000000001000008379/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000008379&livemode=1&stbId=BingCha
咪咕直播 7,http://gslbserv.itv.cmvideo.cn:80/3000000001000010129/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000010129&livemode=1&stbId=BingCha
咪咕直播 8,http://gslbserv.itv.cmvideo.cn:80/3000000001000010948/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000010948&livemode=1&stbId=BingCha
咪咕直播 9,http://gslbserv.itv.cmvideo.cn:80/3000000001000028638/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000028638&livemode=1&stbId=BingCha
咪咕直播 10,http://gslbserv.itv.cmvideo.cn:80/3000000001000031494/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000031494&livemode=1&stbId=BingCha
咪咕直播 11,http://gslbserv.itv.cmvideo.cn:80/3000000010000000097/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000000097&livemode=1&stbId=BingCha
咪咕直播 12,http://gslbserv.itv.cmvideo.cn:80/3000000010000002019/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000002019&livemode=1&stbId=BingCha
咪咕直播 13,http://gslbserv.itv.cmvideo.cn:80/3000000010000002809/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000002809&livemode=1&stbId=BingCha
咪咕直播 14,http://gslbserv.itv.cmvideo.cn:80/3000000010000003915/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000003915&livemode=1&stbId=BingCha
咪咕直播 15,http://gslbserv.itv.cmvideo.cn:80/3000000010000004193/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000004193&livemode=1&stbId=BingCha
咪咕直播 16,http://gslbserv.itv.cmvideo.cn:80/3000000010000005837/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000005837&livemode=1&stbId=BingCha
咪咕直播 17,http://gslbserv.itv.cmvideo.cn:80/3000000010000006077/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000006077&livemode=1&stbId=BingCha
咪咕直播 18,http://gslbserv.itv.cmvideo.cn:80/3000000010000006658/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000006658&livemode=1&stbId=BingCha
咪咕直播 19,http://gslbserv.itv.cmvideo.cn:80/3000000010000009788/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000009788&livemode=1&stbId=BingCha
咪咕直播 20,http://gslbserv.itv.cmvideo.cn:80/3000000010000010833/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000010833&livemode=1&stbId=BingCha
咪咕直播 21,http://gslbserv.itv.cmvideo.cn:80/3000000010000011297/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000011297&livemode=1&stbId=BingCha
咪咕直播 22,http://gslbserv.itv.cmvideo.cn:80/3000000010000011518/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000011518&livemode=1&stbId=BingCha
咪咕直播 23,http://gslbserv.itv.cmvideo.cn:80/3000000010000012558/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000012558&livemode=1&stbId=BingCha
咪咕直播 24,http://gslbserv.itv.cmvideo.cn:80/3000000010000012616/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000012616&livemode=1&stbId=BingCha
咪咕直播 25,http://gslbserv.itv.cmvideo.cn:80/3000000010000015470/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000015470&livemode=1&stbId=BingCha
咪咕直播 26,http://gslbserv.itv.cmvideo.cn:80/3000000010000015560/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000015560&livemode=1&stbId=BingCha
咪咕直播 27,http://gslbserv.itv.cmvideo.cn:80/3000000010000017678/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000017678&livemode=1&stbId=BingCha
咪咕直播 28,http://gslbserv.itv.cmvideo.cn:80/3000000010000019839/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000019839&livemode=1&stbId=BingCha
咪咕直播 29,http://gslbserv.itv.cmvideo.cn:80/3000000010000021904/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000021904&livemode=1&stbId=BingCha
咪咕直播 30,http://gslbserv.itv.cmvideo.cn:80/3000000010000023434/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000023434&livemode=1&stbId=BingCha
咪咕直播 31,http://gslbserv.itv.cmvideo.cn:80/3000000010000025380/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000025380&livemode=1&stbId=BingCha
咪咕直播 32,http://gslbserv.itv.cmvideo.cn:80/3000000010000027691/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000027691&livemode=1&stbId=BingCha
咪咕直播 33,http://gslbserv.itv.cmvideo.cn:80/3000000010000031669/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000031669&livemode=1&stbId=BingCha
咪咕直播 34,http://gslbserv.itv.cmvideo.cn:80/3000000020000011518/index.m3u8?channel-id=FifastbLive&Contentid=3000000020000011518&livemode=1&stbId=BingCha
咪咕直播 35,http://gslbserv.itv.cmvideo.cn:80/3000000020000011519/index.m3u8?channel-id=FifastbLive&Contentid=3000000020000011519&livemode=1&stbId=BingCha
咪咕直播 36,http://gslbserv.itv.cmvideo.cn:80/3000000020000011520/index.m3u8?channel-id=FifastbLive&Contentid=3000000020000011520&livemode=1&stbId=BingCha
咪咕直播 37,http://gslbserv.itv.cmvideo.cn:80/3000000020000011521/index.m3u8?channel-id=FifastbLive&Contentid=3000000020000011521&livemode=1&stbId=BingCha
咪咕直播 38,http://gslbserv.itv.cmvideo.cn:80/3000000020000011522/index.m3u8?channel-id=FifastbLive&Contentid=3000000020000011522&livemode=1&stbId=BingCha
睛彩竞技,http://gslbserv.itv.cmvideo.cn:80/3000000020000011528/index.m3u8?channel-id=FifastbLive&Contentid=3000000020000011528&livemode=1&stbId=BingCha
睛彩篮球,http://gslbserv.itv.cmvideo.cn:80/3000000020000011529/index.m3u8?channel-id=FifastbLive&Contentid=3000000020000011529&livemode=1&stbId=BingCha
睛彩青少,http://gslbserv.itv.cmvideo.cn:80/3000000020000011525/index.m3u8?channel-id=FifastbLive&Contentid=3000000020000011525&livemode=1&stbId=BingCha
睛彩广场舞,http://gslbserv.itv.cmvideo.cn:80/3000000020000011523/index.m3u8?channel-id=FifastbLive&Contentid=3000000020000011523&livemode=1&stbId=BingCha
咪咕直播4K-1,http://gslbserv.itv.cmvideo.cn:80/3000000010000005180/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000005180&livemode=1&stbId=BingCha
咪咕直播4K-2,http://gslbserv.itv.cmvideo.cn:80/3000000010000015686/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000015686&livemode=1&stbId=BingCha
咪咕直播 1,http://gslbserv.itv.cmvideo.cn:80/3000000001000005308/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000005308&livemode=1&stbId=YanG-1989
咪咕直播 2,http://gslbserv.itv.cmvideo.cn:80/3000000001000005969/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000005969&livemode=1&stbId=YanG-1989
咪咕直播 3,http://gslbserv.itv.cmvideo.cn:80/3000000001000007218/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000007218&livemode=1&stbId=YanG-1989
咪咕直播 4,http://gslbserv.itv.cmvideo.cn:80/3000000001000008001/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000008001&livemode=1&stbId=YanG-1989
咪咕直播 5,http://gslbserv.itv.cmvideo.cn:80/3000000001000008176/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000008176&livemode=1&stbId=YanG-1989
咪咕直播 6,http://gslbserv.itv.cmvideo.cn:80/3000000001000008379/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000008379&livemode=1&stbId=YanG-1989
咪咕直播 7,http://gslbserv.itv.cmvideo.cn:80/3000000001000010129/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000010129&livemode=1&stbId=YanG-1989
咪咕直播 8,http://gslbserv.itv.cmvideo.cn:80/3000000001000010948/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000010948&livemode=1&stbId=YanG-1989
咪咕直播 9,http://gslbserv.itv.cmvideo.cn:80/3000000001000028638/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000028638&livemode=1&stbId=YanG-1989
咪咕直播 10,http://gslbserv.itv.cmvideo.cn:80/3000000001000031494/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000031494&livemode=1&stbId=YanG-1989
咪咕直播 11,http://gslbserv.itv.cmvideo.cn:80/3000000010000000097/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000000097&livemode=1&stbId=YanG-1989
咪咕直播 12,http://gslbserv.itv.cmvideo.cn:80/3000000010000002019/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000002019&livemode=1&stbId=YanG-1989
咪咕直播 13,http://gslbserv.itv.cmvideo.cn:80/3000000010000002809/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000002809&livemode=1&stbId=YanG-1989
咪咕直播 14,http://gslbserv.itv.cmvideo.cn:80/3000000010000003915/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000003915&livemode=1&stbId=YanG-1989
咪咕直播 15,http://gslbserv.itv.cmvideo.cn:80/3000000010000004193/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000004193&livemode=1&stbId=YanG-1989
咪咕直播 16,http://gslbserv.itv.cmvideo.cn:80/3000000010000005837/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000005837&livemode=1&stbId=YanG-1989
咪咕直播 17,http://gslbserv.itv.cmvideo.cn:80/3000000010000006077/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000006077&livemode=1&stbId=YanG-1989
咪咕直播 18,http://gslbserv.itv.cmvideo.cn:80/3000000010000006658/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000006658&livemode=1&stbId=YanG-1989
咪咕直播 19,http://gslbserv.itv.cmvideo.cn:80/3000000010000009788/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000009788&livemode=1&stbId=YanG-1989
咪咕直播 20,http://gslbserv.itv.cmvideo.cn:80/3000000010000010833/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000010833&livemode=1&stbId=YanG-1989
咪咕直播 21,http://gslbserv.itv.cmvideo.cn:80/3000000010000011297/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000011297&livemode=1&stbId=YanG-1989
咪咕直播 22,http://gslbserv.itv.cmvideo.cn:80/3000000010000011518/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000011518&livemode=1&stbId=YanG-1989
咪咕直播 23,http://gslbserv.itv.cmvideo.cn:80/3000000010000012558/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000012558&livemode=1&stbId=YanG-1989
咪咕直播 24,http://gslbserv.itv.cmvideo.cn:80/3000000010000012616/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000012616&livemode=1&stbId=YanG-1989
咪咕直播 25,http://gslbserv.itv.cmvideo.cn:80/3000000010000015470/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000015470&livemode=1&stbId=YanG-1989
咪咕直播 26,http://gslbserv.itv.cmvideo.cn:80/3000000010000015560/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000015560&livemode=1&stbId=YanG-1989
咪咕直播 27,http://gslbserv.itv.cmvideo.cn:80/3000000010000017678/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000017678&livemode=1&stbId=YanG-1989
咪咕直播 28,http://gslbserv.itv.cmvideo.cn:80/3000000010000019839/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000019839&livemode=1&stbId=YanG-1989
咪咕直播 29,http://gslbserv.itv.cmvideo.cn:80/3000000010000021904/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000021904&livemode=1&stbId=YanG-1989
咪咕直播 30,http://gslbserv.itv.cmvideo.cn:80/3000000010000023434/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000023434&livemode=1&stbId=YanG-1989
咪咕直播 31,http://gslbserv.itv.cmvideo.cn:80/3000000010000025380/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000025380&livemode=1&stbId=YanG-1989
咪咕直播 32,http://gslbserv.itv.cmvideo.cn:80/3000000010000027691/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000027691&livemode=1&stbId=YanG-1989
咪咕直播 33,http://gslbserv.itv.cmvideo.cn:80/3000000010000031669/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000031669&livemode=1&stbId=YanG-1989
咪咕直播 34,http://gslbserv.itv.cmvideo.cn:80/3000000020000011518/index.m3u8?channel-id=FifastbLive&Contentid=3000000020000011518&livemode=1&stbId=YanG-1989
咪咕直播 35,http://gslbserv.itv.cmvideo.cn:80/3000000020000011519/index.m3u8?channel-id=FifastbLive&Contentid=3000000020000011519&livemode=1&stbId=YanG-1989
咪咕直播 36,http://gslbserv.itv.cmvideo.cn:80/3000000020000011520/index.m3u8?channel-id=FifastbLive&Contentid=3000000020000011520&livemode=1&stbId=YanG-1989
咪咕直播 37,http://gslbserv.itv.cmvideo.cn:80/3000000020000011521/index.m3u8?channel-id=FifastbLive&Contentid=3000000020000011521&livemode=1&stbId=YanG-1989
咪咕直播 38,http://gslbserv.itv.cmvideo.cn:80/3000000020000011522/index.m3u8?channel-id=FifastbLive&Contentid=3000000020000011522&livemode=1&stbId=YanG-1989
咪咕直播 4K-1,http://gslbserv.itv.cmvideo.cn:80/3000000010000005180/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000005180&livemode=1&stbId=YanG-1989
咪咕直播 4K-2,http://gslbserv.itv.cmvideo.cn:80/3000000010000015686/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000015686&livemode=1&stbId=YanG-1989
JJ斗地主,http://huanqiuzhibo.cn/manifest/douyu.php?id=488743
JJ斗地主,http://zzy789.xyz/douyu1.php?id=488743
五星体育,https://migu.188766.xyz/?migutoken=f044e1c97db7c6da6135c112a2f5b2e3&id=%E4%BA%94%E6%98%9F%E4%BD%93%E8%82%B2&pp=1
广东体育,https://mgev.188766.xyz/?migutoken=adc89b1e857930955cba95be68079f7d&id=gd_gdty&type=sz
体坛名栏汇,https://migu.188766.xyz/?migutoken=d61bc9415bae5920e5eadbc2b582e4ce&id=%E4%BD%93%E5%9D%9B%E5%90%8D%E6%A0%8F%E6%B1%87&type=yy
24小时全运会轮播台,https://migu.188766.xyz/?migutoken=390092c18ab2663c01bd3673f0e7b57e&id=24%E5%B0%8F%E6%97%B6%E5%85%A8%E8%BF%90%E4%BC%9A%E8%BD%AE%E6%92%AD%E5%8F%B0&type=yy
24小时城市联赛轮播台,https://migu.188766.xyz/?migutoken=66bbfae74c62c2f889831e58abef93e6&id=24%E5%B0%8F%E6%97%B6%E5%9F%8E%E5%B8%82%E8%81%94%E8%B5%9B%E8%BD%AE%E6%92%AD%E5%8F%B0&type=yy
武术世界,https://migu.188766.xyz/?migutoken=2590a054b1130b84a770f6d2603454a7&id=%E6%AD%A6%E6%9C%AF%E4%B8%96%E7%95%8C&type=yy
四海钓鱼,https://migu.188766.xyz/?migutoken=64aecbd48db04e8f2a4f8deb72b131fc&id=%E5%9B%9B%E6%B5%B7%E9%92%93%E9%B1%BC&type=yy
广东体育,http://rfx2018.55555.io:2345/udp/239.77.0.168:5146
广东体育,http://sub.mtoo.vip:8333/udp/239.77.0.168:5146
广东体育,http://ha.m-too.top:8333/udp/239.77.0.168:5146
广东体育,http://php.jdshipin.com:8880/TVOD/iptv.php?id=gdty"""

    solid_channels = """🥝精品频道🥝,#genre#
CHC家庭影院,https://migu.188766.xyz/?migutoken=abd713c982c6ee90d0424319ff22764c&id=CHC%E5%AE%B6%E5%BA%AD%E5%BD%B1%E9%99%A2&type=yy
CHC动作电影,https://migu.188766.xyz/?migutoken=417ec01f22421c2f2e6fe69f827344bc&id=CHC%E5%8A%A8%E4%BD%9C%E7%94%B5%E5%BD%B1&type=yy
CHC影迷电影,https://migu.188766.xyz/?migutoken=28e6d0259793e1baba822b369d222863&id=CHC%E5%BD%B1%E8%BF%B7%E7%94%B5%E5%BD%B1&type=yy
新片放映厅,https://migu.188766.xyz/?migutoken=be02baa5bf0ccc971fafc7b5026f60c2&id=%E6%96%B0%E7%89%87%E6%94%BE%E6%98%A0%E5%8E%85&type=yy
高清大片,https://migu.188766.xyz/?migutoken=0fecbdcfcc98ab8378934150dda80835&id=%E9%AB%98%E6%B8%85%E5%A4%A7%E7%89%87&type=yy
经典香港电影,https://migu.188766.xyz/?migutoken=2f1289a2d2489e81419c56689bd682df&id=%E7%BB%8F%E5%85%B8%E9%A6%99%E6%B8%AF%E7%94%B5%E5%BD%B1&type=yy
抗战经典影片,https://migu.188766.xyz/?migutoken=93e7653f5fffd0c4cdcec651bac1fd05&id=%E6%8A%97%E6%88%98%E7%BB%8F%E5%85%B8%E5%BD%B1%E7%89%87&type=yy
环球旅游,https://migu.188766.xyz/?migutoken=a43031f2e58ed9005461fa7fc33150e9&id=%E7%8E%AF%E7%90%83%E6%97%85%E6%B8%B8&type=yy
最强综艺趴,https://migu.188766.xyz/?migutoken=1ad7b608f123603cded8b3fb3089132b&id=%E6%9C%80%E5%BC%BA%E7%BB%BC%E8%89%BA%E8%B6%B4&type=yy
嘉佳卡通,https://migu.188766.xyz/?migutoken=df60baf9d9b6c5c1810143fd7b0f7997&id=%E5%98%89%E4%BD%B3%E5%8D%A1%E9%80%9A&type=yy
经典动画大集合,https://migu.188766.xyz/?migutoken=5f1b2c6e6b2d6068fddb8d8df236cd7c&id=%E7%BB%8F%E5%85%B8%E5%8A%A8%E7%94%BB%E5%A4%A7%E9%9B%86%E5%90%88&type=yy
优漫卡通,https://migu.188766.xyz/?migutoken=212b88146a7936f067db27cd9827d7e6&id=%E4%BC%98%E6%BC%AB%E5%8D%A1%E9%80%9A%E9%A2%91%E9%81%93&type=yy
财富天下,https://migu.188766.xyz/?migutoken=f7c82f129e8a7e0ca61e32d793b9fd92&id=%E8%B4%A2%E5%AF%8C%E5%A4%A9%E4%B8%8B&type=yy
中学生,https://migu.188766.xyz/?migutoken=f5ecf5e0289cc3fe993cfc48669975a8&id=%E4%B8%AD%E5%AD%A6%E7%94%9F&type=yy
老故事,https://migu.188766.xyz/?migutoken=658d11e1cf292405ba6aa4c67df1e2fe&id=%E8%80%81%E6%95%85%E4%BA%8B&type=yy
新动力量创一流,https://migu.188766.xyz/?migutoken=51f310c33bf5dcd8ebaf02c65e4c02b3&id=%E6%96%B0%E5%8A%A8%E5%8A%9B%E9%87%8F%E5%88%9B%E4%B8%80%E6%B5%81&type=yy
NewTV超级电视剧,http://gslbserv.itv.cmvideo.cn/1000000006000268003/1.m3u8?channel-id=ystenlive&Contentid=1000000006000268003&livemode=1&stbId=3
NewTV超级电影,http://gslbserv.itv.cmvideo.cn/1000000003000012426/1.m3u8?channel-id=ystenlive&Contentid=1000000003000012426&livemode=1&stbId=3
NewTV超级体育,http://gslbserv.itv.cmvideo.cn/1000000001000009601/1.m3u8?channel-id=ystenlive&Contentid=1000000001000009601&livemode=1&stbId=3
NewTV超级综艺,http://gslbserv.itv.cmvideo.cn/1000000006000268002/1.m3u8?channel-id=ystenlive&Contentid=1000000006000268002&livemode=1&stbId=3
NewTV哒啵赛事,http://gslbserv.itv.cmvideo.cn/1000000001000003775/1.m3u8?channel-id=ystenlive&Contentid=1000000001000003775&livemode=1&stbId=3
NewTV东北热剧,http://gslbserv.itv.cmvideo.cn/1000000005000266013/1.m3u8?channel-id=ystenlive&Contentid=1000000005000266013&livemode=1&stbId=3
NewTV动作电影,http://gslbserv.itv.cmvideo.cn/1000000004000018653/1.m3u8?channel-id=ystenlive&Contentid=1000000004000018653&livemode=1&stbId=3
NewTV黑莓电影,http://gslbserv.itv.cmvideo.cn/1000000004000019624/1.m3u8?channel-id=ystenlive&Contentid=1000000004000019624&livemode=1&stbId=3
NewTV黑莓动画,http://gslbserv.itv.cmvideo.cn/1000000004000021734/1.m3u8?channel-id=ystenlive&Contentid=1000000004000021734&livemode=1&stbId=3
NewTV欢乐剧场,http://gslbserv.itv.cmvideo.cn/1000000005000266012/1.m3u8?channel-id=ystenlive&Contentid=1000000005000266012&livemode=1&stbId=3
NewTV精品萌宠,http://gslbserv.itv.cmvideo.cn/1000000006000032328/1.m3u8?channel-id=ystenlive&Contentid=1000000006000032328&livemode=1&stbId=3
NewTV精品综合,http://gslbserv.itv.cmvideo.cn/1000000004000019008/1.m3u8?channel-id=ystenlive&Contentid=1000000004000019008&livemode=1&stbId=3
NewTV魅力潇湘,http://gslbserv.itv.cmvideo.cn/1000000001000006197/1.m3u8?channel-id=ystenlive&Contentid=1000000001000006197&livemode=1&stbId=3
NewTV炫舞未来,http://gslbserv.itv.cmvideo.cn/1000000001000000515/1.m3u8?channel-id=ystenlive&Contentid=1000000001000000515&livemode=1&stbId=3
NewTV怡伴健康,http://gslbserv.itv.cmvideo.cn/1000000005000266011/1.m3u8?channel-id=ystenlive&Contentid=1000000005000266011&livemode=1&stbId=3
天元围棋,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000010000000040365/main.m3u8?stbid=
梨园,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000064000000308847/main.m3u8?stbid=
四海钓鱼,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000010000000040367/main.m3u8?stbid=
快乐垂钓,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000010000000040368/main.m3u8?stbid=
文物宝库,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000064000000308848/main.m3u8?stbid=
武术世界,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000064000000308859/main.m3u8?stbid=
家庭影院,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000050000000448840/main.m3u8?stbid=
高清电影,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000050000000448841/main.m3u8?stbid=
动作电影,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000050000000448842/main.m3u8?stbid=
环球旅游,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000064000000308870/main.m3u8?stbid=
第一剧场,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000091000000244808/main.m3u8?stbid=
风云剧场,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000091000000244807/main.m3u8?stbid=
风云音乐,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000091000000244809/main.m3u8?stbid=
风云足球,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000091000000244800/main.m3u8?stbid=
怀旧剧场,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000091000000244806/main.m3u8?stbid=
央视文化精品,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000091000000244810/main.m3u8?stbid=
世界地理,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000091000000244805/main.m3u8?stbid=
央视台球,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000091000000244803/main.m3u8?stbid=
兵器科技,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000091000000244796/main.m3u8?stbid=
电视指南,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000091000000244797/main.m3u8?stbid=
高尔夫网球,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000091000000244801/main.m3u8?stbid=
早期教育,http://tvgslb.hn.chinamobile.com:8089/180000001002/32023060222354368427501888132813/main.m3u8?stbid=
中国天气,http://tvgslb.hn.chinamobile.com:8089/180000001002/00000001000000000004000000182438/main.m3u8?stbid="""

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
    
    # 生成 iptv.m3u 文件 x-tvg-url="https://raw.bgithub.xyz/Troray/IPTV/main/tvxml.xml,https://raw.bgithub.xyz/Meroser/EPG-test/main/tvxml-test.xml.gz" catchup="append" catchup-source="?playseek=${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}"

    output_text = '#EXTM3U x-tvg-url="https://raw.bgithub.xyz/Troray/IPTV/main/tvxml.xml,https://raw.bgithub.xyz/Meroser/EPG-test/main/tvxml-test.xml.gz"\n'

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
