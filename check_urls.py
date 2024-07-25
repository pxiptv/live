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
    skip_strings = ['#genre#', '127.0.0.1', '192.168', '198.168', 'php.jdshipin', '[240', 'ottrrs.hl.chinamobile', '/live/0701', 'jxcbn.ws-cdn.gitv.tv', 'ChiSheng9', 'epg.pw', '/udp/', '/hls/', '(576p)', '(540p)', '(360p)', '(480p)', '(180p)', '(404p)', 'r.jdshipin', 'ali.hlspull.yximgs', 'generationnexxxt', 'live.goodiptv.club', 'playtv-live.ifeng']  # 定义需要跳过的字符串数组['#', '@', '#genre#'] 
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
        'https://raw.githubusercontent.com/YueChan/Live/main/IPTV.m3u',
        'https://raw.githubusercontent.com/suxuang/myIPTV/main/ipv6.m3u',
        'https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u',
        'https://raw.githubusercontent.com/Guovin/TV/gd/result.txt',
        'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/cn.m3u',
        'https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/merged_output.txt',
        'https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/others_output.txt',
        'https://raw.githubusercontent.com/Fairy8o/IPTV/main/PDX-V4.txt',
        # 'https://raw.githubusercontent.com/Fairy8o/IPTV/main/PDX-V6.txt',
        'https://raw.githubusercontent.com/alonezou/yn-iptv/main/reference/MyIPTV',
        'https://raw.githubusercontent.com/qist/tvbox/master/tvlive.txt',
        'https://raw.githubusercontent.com/leyan1987/iptv/main/iptvnew.txt',
        'https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt',
        'https://raw.githubusercontent.com/fenxp/iptv/main/live/ipv6.txt',
        'https://raw.githubusercontent.com/fenxp/iptv/main/live/tvlive.txt',
        'https://raw.githubusercontent.com/yuanzl77/IPTV/main/live.txt',
        'https://raw.githubusercontent.com/mlvjfchen/TV/main/iptv_list.txt',
        'https://raw.githubusercontent.com/maitel2020/iptv-self-use/main/iptv.txt',
        'https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.txt',
        'https://raw.githubusercontent.com/balala2oo8/iptv/main/o.m3u',
        'https://raw.githubusercontent.com/LuckyLearning/myTV/6b3cb61977fe3b3ab25383e2852d001a963e6771/result.txt',
        'https://raw.githubusercontent.com/frxz751113/AAAAA/7ed0a668bde0c5e1cb7e61c82585ee5805e742fd/IPTV/%E6%B1%87%E6%80%BB.txt',
        'https://m3u.ibert.me/txt/fmml_ipv6.txt',
        'https://m3u.ibert.me/txt/fmml_dv6.txt',
        'https://m3u.ibert.me/txt/ycl_iptv.txt',
        'https://m3u.ibert.me/txt/y_g.txt',
        'https://m3u.ibert.me/txt/j_iptv.txt',
        'https://iptv-org.github.io/iptv/countries/cn.m3u',
        'https://live.fanmingming.com/tv/m3u/ipv6.m3u',
        'https://cdn.jsdelivr.net/gh/shidahuilang/shuyuan@shuyuan/iptv.txt',
        'https://cdn.jsdelivr.net/gh/abc1763613206/myiptv@latest/utf8/merged-simple.txt',
        'https://gitlab.com/p2v5/wangtv/-/raw/main/wang-tvlive.txt',
        'https://gitlab.com/p2v5/wangtv/-/raw/main/lunbo.txt'
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

    # 计算 blacklist_lines 和 iptv_lines 的并集
    combined_blacklist_iptv = blacklist_lines | iptv_lines

    # 计算 online_lines 与 combined_blacklist_iptv 的差集
    unique_online_lines = online_lines - combined_blacklist_iptv

    # 将差集写回到 online.txt
    write_file('online.txt', unique_online_lines)
    print(f"本次新获取的网址总行数: {len(unique_online_lines)}")

    # 定义需要保留的IP地址列表
    ips = [
        "60.223.72.118", "222.130.146.175", "124.64.11.135", "118.248.218.7", "119.39.97.2", "58.248.112.205", "120.87.97.246", "27.40.16.70", "jxcbn.ws-cdn.gitv.tv", "/GD_CUCC/G_"
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
CCTV1,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226016/index.m3u8
CCTV2,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225588/index.m3u8
CCTV3,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226021/index.m3u8
CCTV4,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226428/index.m3u8
CCTV5,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226019/index.m3u8
CCTV5+,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225603/index.m3u8
CCTV6,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226010/index.m3u8
CCTV7,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225733/index.m3u8
CCTV8,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226008/index.m3u8
CCTV9,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225734/index.m3u8
CCTV10,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225730/index.m3u8
CCTV11,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225597/index.m3u8
CCTV12,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225731/index.m3u8
CCTV13,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226011/index.m3u8
CCTV14,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225732/index.m3u8
CCTV15,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225601/index.m3u8
CCTV16,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226100/index.m3u8
CCTV17,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225765/index.m3u8
CCTV1,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221226016/index.m3u8
CCTV2,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221225588/index.m3u8
CCTV3,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221226021/index.m3u8
CCTV4,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221226007/index.m3u8
CCTV5,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221226019/index.m3u8
CCTV5+,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221225603/index.m3u8
CCTV6,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221226010/index.m3u8
CCTV7,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221225733/index.m3u8
CCTV8,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221226008/index.m3u8
CCTV9,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221225734/index.m3u8
CCTV10,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221225730/index.m3u8
CCTV11,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221225597/index.m3u8
CCTV12,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221225731/index.m3u8
CCTV13,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221226011/index.m3u8
CCTV14,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221225732/index.m3u8
CCTV15,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221225601/index.m3u8
CCTV16,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221226100/index.m3u8
CCTV17,http://[2409:8087:1a01:df::4077]/ottrrs.hl.chinamobile.com/PLTV/88888888/8/3221225765/index.m3u8
CCTV1,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN111128BESTVSMGSMG/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUU6FFmRK8Hl0ytyd5e5kWGEwoDIwMxbrlyyVy9x6ZDKnldIYKOjBOUjRyoym5n7Kg0yIYstFTUfqtC14fzxhy5Y
CCTV2,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN5000036BESTVSMGSMG/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUSpr1AVNI633ampcuzdN%2BfGVSARKsxkWGZw7vFUuOj2QZHeRzosIxVbl7i2QHFATHA3k5wDWG1qHkZQAleNv%2FbI
CCTV3,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN638727c125355/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUSPTZ4CK5oLfjaEYe9dogNMUNNEYLCPUtKY62j1Wp5u04wipypKUQ1TTuR2lXvBl5YpHqBJmlA19x22TD9bUOjk
CCTV4,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN5000037BESTVSMGSMG/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUSpr1AVNI633ampcuzdN%2BfH0ZQXwaiVktPr6ILPKXqwOUC2ZXft7ZULN6h9qLQPFOTSlVTfophiKaMb8h1kPV74
CCTV5,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN638727e617ca0/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUSPTZ4CK5oLfjaEYe9dogNMSXw4ajlL%2FoUYC2RZQQDco6uQSifXBocz5ID6RePfIKQ4rFWiHjq%2FeZoDmrzW%2FKlw
CCTV5+,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN63872908d48f9/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUSBx06ZL9Bo6JOM%2BSTjxZRK254G1jtietGzDaHvFNRtjXOvFnbf%2BTao33JqYlfMYYn2z3agOn9gvNMT9KmBaR9o
CCTV6,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN638728804b1f9/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUdDh4EPdDnvGlSBkYaxFdazJhFQmuq4XUiks9ZrIlJN%2BknLs8H%2BSxcDXy%2BTesEc8Q0KCN89MjYoj85Sol1kbKI4
CCTV7,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN5000038BESTVSMGSMG/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUSpr1AVNI633ampcuzdN%2BfHYKFve4MwNzRa0jPXeHjqnBjPmzSdKDNWNHhnZSaMGCXKmdx8d%2BnYdhVK5ge22ot4
CCTV8,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN638728970aa82/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUdDh4EPdDnvGlSBkYaxFdaymid9ta2tVUW0%2FdVrFqszC1EVEkAbpip1IYxn%2Ba2aA%2BVAihIiw9D8ejUsDbfU0K68
CCTV9,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN5000039BESTVSMGSMG/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUSpr1AVNI633ampcuzdN%2BfHArfvJF2pWpm4RxcBNhZ7j9vEUeCQte%2BbQaOGNIUEEK%2B3RBE1BC9EUsM18gnb%2FyAA
CCTV10,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN3949784BESTVSMGSMG/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUXt3TPFwzzdHCkOT9AjSv5OuXozn3alq9%2BUx7ZLG1w9aOfkLjZvYj56D3xkOAtSOIoLsdw8c1%2BCwLDg1aS4esN4
CCTV11,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN6000053BESTVSMGSMG/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUTWDyIgRkFJBAHMhA2ayG0Qj2xHA4vdPGsjBbxSL3p%2FmAObVTfznR%2Fpc%2B76QYmLRMuL3Lj9iabhv8arW7kJe6%2F4
CCTV12,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN5000040BESTVSMGSMG/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUd3JM2PCgDefrKOVZLNt0QMAmpLefguRLiOPXiDRWhxHg8yim2giTBA8RILsb%2B8Y5pkFUyZBE%2FkNJAbwncEegkU
CCTV13,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN6000054BESTVSMGSMG/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUTWDyIgRkFJBAHMhA2ayG0SuXozn3alq9%2BUx7ZLG1w9awc14iEUxQ5VsTsr5pEBsmF56tXUfsukRUpygmTCKvAI
CCTV14,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN3949788BESTVSMGSMG/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUXt3TPFwzzdHCkOT9AjSv5PYKFve4MwNzRa0jPXeHjqnp7khdLaCMP6L4QpTf84Oz6DvCG1%2BJ81QvStkxO%2FoGm8
CCTV15,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN6000055BESTVSMGSMG/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUTWDyIgRkFJBAHMhA2ayG0Tdo%2FUL80msfbhDYvoWpNl31Dy7jHvMl%2FzVUrNxhL1ek1YEGVDZ7lCg0LtKJY4Ku%2B8
CCTV16,http://[2409:8087:1a01:df::7005]/ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226100/index.m3u8
CCTV17,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN638728afa13b4/index.m3u8?AuthInfo=9kOOdBn7MFF%2F2bWjKgahUdDh4EPdDnvGlSBkYaxFdaz%2FyAI9to%2FMBBt%2FivcdSfljJ1%2FqqamWUjAiBAxNssfyBlZUDSXAIMtStS86hRHFuJM"""

    satellite_channels = """🛰️卫视频道🛰️,#genre#
湖南卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225610/index.m3u8
浙江卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225612/index.m3u8
东方卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225735/index.m3u8
江苏卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225613/index.m3u8
北京卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225728/index.m3u8
广东卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226248/index.m3u8
深圳卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225739/index.m3u8
河南卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226480/index.m3u8
江西卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226344/index.m3u8
东南卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226341/index.m3u8
重庆卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226409/index.m3u8
贵州卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226474/index.m3u8
河北卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226406/index.m3u8
黑龙江卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226327/index.m3u8
湖北卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225627/index.m3u8
吉林卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226397/index.m3u8
安徽卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226391/index.m3u8
山东卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226456/index.m3u8
四川卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226338/index.m3u8
天津卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225740/index.m3u8
海南卫视,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226465/index.m3u8
湖南卫视,http://[2409:8087:5e01:34::23]:6610/ZTE_CMS/00000001000000060000000000000174/index.m3u8?IAS
浙江卫视,http://[2409:8087:5e01:34::22]:6610/ZTE_CMS/00000001000000060000000000000248/index.m3u8?IAS
东方卫视,http://[2409:8087:5e01:34::21]:6610/ZTE_CMS/00000001000000060000000000000182/index.m3u8?IAS
江苏卫视,http://[2409:8087:5e01:34::20]:6610/ZTE_CMS/00000001000000060000000000000177/index.m3u8?IAS
广东卫视,http://[2409:8087:5e01:34::22]:6610/ZTE_CMS/00000001000000060000000000000341/index.m3u8?IAS
北京卫视,http://[2409:8087:5e01:34::21]:6610/ZTE_CMS/00000001000000060000000000000173/index.m3u8?IAS
天津卫视,http://[2409:8087:5e01:34::23]:6610/ZTE_CMS/00000001000000060000000000000249/index.m3u8?IAS
安徽卫视,http://[2409:8087:5e01:34::22]:6610/ZTE_CMS/00000001000000060000000000000368/index.m3u8?IAS
山东卫视,http://[2409:8087:5e01:34::21]:6610/ZTE_CMS/00000001000000060000000000000364/index.m3u8?IAS
江西卫视,http://[2409:8087:5e01:34::23]:6610/ZTE_CMS/00000001000000060000000000000522/index.m3u8?IAS
河北卫视,http://[2409:8087:5e01:34::21]:6610/ZTE_CMS/00000001000000060000000000000487/index.m3u8?IAS
海南卫视,http://[2409:8087:5e01:34::23]:6610/ZTE_CMS/00000001000000060000000000000262/index.m3u8?IAS
湖北卫视,http://[2409:8087:5e01:34::20]:6610/ZTE_CMS/00000001000000060000000000000250/index.m3u8?IAS
东南卫视,http://[2409:8087:5e01:34::23]:6610/ZTE_CMS/00000001000000060000000000000502/index.m3u8?IAS
贵州卫视,http://[2409:8087:5e01:34::23]:6610/ZTE_CMS/00000001000000060000000000000489/index.m3u8?IAS
吉林卫视,http://[2409:8087:5e01:34::23]:6610/ZTE_CMS/00000001000000060000000000000533/index.m3u8?IAS
黑龙江卫视,http://[2409:8087:5e01:34::20]:6610/ZTE_CMS/00000001000000060000000000000175/index.m3u8?IAS"""

    hot_channels = """🇭🇰港澳台🇭🇰,#genre#
凤凰中文,http://116.162.6.192/1.v.smtcdns.net/qctv.fengshows.cn/live/0701pcc72.m3u8
凤凰中文,http://php.jdshipin.com:8880/TVOD/iptv.php?id=fhzw
凤凰中文,http://php.jdshipin.com:8880/smt.php?id=phoenixtv_hd
凤凰资讯,http://116.162.6.192/1.v.smtcdns.net/qctv.fengshows.cn/live/0701pin72.m3u8
凤凰资讯,http://php.jdshipin.com:8880/TVOD/iptv.php?id=fhzx
凤凰资讯,http://php.jdshipin.com:8880/smt.php?id=phoenixinfo_hd
凤凰香港,http://116.162.6.192/1.v.smtcdns.net/qctv.fengshows.cn/live/0701phk72.m3u8
凤凰香港,http://php.jdshipin.com:8880/TVOD/iptv.php?id=fhhk
凤凰香港,http://php.jdshipin.com:8880/smt.php?id=hkphoenix_twn
翡翠台,http://php.jdshipin.com:8880/TVOD/iptv.php?id=fct
明珠台,http://php.jdshipin.com:8880/TVOD/iptv.php?id=mzt
TVB星河,http://php.jdshipin.com:8880/TVOD/iptv.php?id=xinghe
ViuTV,http://php.jdshipin.com:8880/TVOD/iptv.php?id=viutv
RTHK31,http://php.jdshipin.com:8880/TVOD/iptv.php?id=rthk31
RTHK32,http://php.jdshipin.com:8880/TVOD/iptv.php?id=rthk32
TVB Plus,http://php.jdshipin.com:8880/TVOD/iptv.php?id=tvbp"""
    
    migu_channels = """🏆咪咕体育🏆,#genre#
咪咕综合,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226124/index.m3u8
咪咕综合,http://[2409:8087:1a01:df::404d]/ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226124/index.m3u8
咪咕综合,http://[2409:8087:1a01:df::7005]/ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226124/index.m3u8
咪咕足球,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226147/index.m3u8
咪咕足球,http://[2409:8087:1a01:df::403b]/ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226147/index.m3u8
咪咕足球,http://[2409:8087:1a01:df::7005]/ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226147/index.m3u8
咪咕CCTV5,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226469/index.m3u8
咪咕CCTV5,http://[2409:8087:1a01:df::402a]/ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226469/index.m3u8
咪咕CCTV5,http://[2409:8087:1a01:df::7005]/ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226469/index.m3u8
咪咕CCTV5,http://gslbserv.itv.cmvideo.cn:80/3000000001000010948/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000010948&livemode=1&stbId=3
咪咕CCTV5,http://gslbserv.itv.cmvideo.cn:80/3000000010000015470/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000015470&livemode=1&stbId=3
咪咕CCTV5+,http://gslbserv.itv.cmvideo.cn:80/3000000010000005837/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000005837&livemode=1&stbId=3
咪咕体育-1,http://gslbserv.itv.cmvideo.cn:80/3000000001000005308/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000005308&livemode=1&stbId=3
咪咕体育-2,http://gslbserv.itv.cmvideo.cn:80/3000000001000005969/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000005969&livemode=1&stbId=3
咪咕体育-3,http://gslbserv.itv.cmvideo.cn:80/3000000001000007218/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000007218&livemode=1&stbId=3
咪咕体育-4,http://gslbserv.itv.cmvideo.cn:80/3000000001000008001/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000008001&livemode=1&stbId=3
咪咕体育-5,http://gslbserv.itv.cmvideo.cn:80/3000000001000008176/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000008176&livemode=1&stbId=3
咪咕体育-6,http://gslbserv.itv.cmvideo.cn:80/3000000001000008379/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000008379&livemode=1&stbId=3
咪咕体育-7,http://gslbserv.itv.cmvideo.cn:80/3000000001000010129/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000010129&livemode=1&stbId=3
咪咕体育-7,http://gslbserv.itv.cmvideo.cn:80/3000000001000028638/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000028638&livemode=1&stbId=3
咪咕体育-8,http://gslbserv.itv.cmvideo.cn:80/3000000010000031669/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000031669&livemode=1&stbId=3
咪咕体育-9,http://gslbserv.itv.cmvideo.cn:80/3000000001000031494/index.m3u8?channel-id=FifastbLive&Contentid=3000000001000031494&livemode=1&stbId=3
咪咕体育-10,http://gslbserv.itv.cmvideo.cn:80/3000000010000000097/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000000097&livemode=1&stbId=3
咪咕体育-11,http://gslbserv.itv.cmvideo.cn:80/3000000010000002019/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000002019&livemode=1&stbId=3
咪咕体育-12,http://gslbserv.itv.cmvideo.cn:80/3000000010000027691/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000027691&livemode=1&stbId=3
咪咕体育-13,http://gslbserv.itv.cmvideo.cn:80/3000000010000002809/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000002809&livemode=1&stbId=3
咪咕体育-14,http://gslbserv.itv.cmvideo.cn:80/3000000010000003915/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000003915&livemode=1&stbId=3
咪咕体育-15,http://gslbserv.itv.cmvideo.cn:80/3000000010000004193/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000004193&livemode=1&stbId=3
咪咕体育-16,http://gslbserv.itv.cmvideo.cn:80/3000000010000006077/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000006077&livemode=1&stbId=3
咪咕体育-17,http://gslbserv.itv.cmvideo.cn:80/3000000010000006658/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000006658&livemode=1&stbId=3
咪咕体育-18,http://gslbserv.itv.cmvideo.cn:80/3000000010000023434/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000023434&livemode=1&stbId=3
咪咕体育-19,http://gslbserv.itv.cmvideo.cn:80/3000000010000021904/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000021904&livemode=1&stbId=3
咪咕体育-20,http://gslbserv.itv.cmvideo.cn:80/3000000010000009788/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000009788&livemode=1&stbId=3
咪咕体育-21,http://gslbserv.itv.cmvideo.cn:80/3000000010000010833/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000010833&livemode=1&stbId=3
咪咕体育-22,http://gslbserv.itv.cmvideo.cn:80/3000000010000015560/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000015560&livemode=1&stbId=3
咪咕体育-23,http://gslbserv.itv.cmvideo.cn:80/3000000010000011297/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000011297&livemode=1&stbId=3
咪咕体育-24,http://gslbserv.itv.cmvideo.cn:80/3000000010000011518/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000011518&livemode=1&stbId=3
咪咕体育-25,http://gslbserv.itv.cmvideo.cn:80/3000000010000019839/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000019839&livemode=1&stbId=3
咪咕体育-26,http://gslbserv.itv.cmvideo.cn:80/3000000010000012558/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000012558&livemode=1&stbId=3
咪咕体育-27,http://gslbserv.itv.cmvideo.cn:80/3000000010000012616/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000012616&livemode=1&stbId=3
咪咕体育-28,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226472/index.m3u8
咪咕体育-28,http://[2409:8087:1a01:df::4046]/ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226472/index.m3u8
咪咕体育-28,http://[2409:8087:1a01:df::7005]/ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226472/index.m3u8
咪咕体育-29,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226398/index.m3u8
咪咕体育-29,http://[2409:8087:1a01:df::4033]/ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226398/index.m3u8
咪咕体育-29,http://[2409:8087:1a01:df::7005]/ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226398/index.m3u8
咪咕全民热练,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226508/index.m3u8
咪咕全民热练,http://[2409:8087:1a01:df::7005]/ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226508/index.m3u8
咪咕体育4K-1,http://gslbserv.itv.cmvideo.cn:80/3000000010000005180/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000005180&livemode=1&stbId=3
咪咕体育4K-2,http://gslbserv.itv.cmvideo.cn:80/3000000010000015686/index.m3u8?channel-id=FifastbLive&Contentid=3000000010000015686&livemode=1&stbId=3"""

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
小丑,https://vd2.bdstatic.com/mda-jkbrts1znp07ryb8/sc/mda-jkbrts1znp07ryb8.mp4
星球大战9,https://vd3.bdstatic.com/mda-ndfj480755j9juhe/cae_h264_delogo/1650116825326935651/mda-ndfj480755j9juhe.mp4
艺术科技感,https://vd3.bdstatic.com/mda-ncrw9pciw60jymyd/sc/cae_h264_delogo/1648329992682771558/mda-ncrw9pciw60jymyd.mp4
终结者,https://vd3.bdstatic.com/mda-jk1hupziz0524rq1/mda-jk1hupziz0524rq1.mp4"""

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
