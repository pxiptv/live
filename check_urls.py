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
    skip_strings = ['#genre#', '127.0.0.1', '192.168', '198.168', '[240', 'ottrrs.hl.chinamobile', 'php.jdshipin', '/live/0701', 'jxcbn.ws-cdn.gitv.tv', 'ChiSheng9', 'epg.pw', '/GD_CUCC/G_', '/udp/', '/hls/', '(576p)', '(540p)', '(360p)', '(480p)', '(180p)', '(404p)', 'r.jdshipin', 'ali.hlspull.yximgs', 'generationnexxxt', 'live.goodiptv.club', 'playtv-live.ifeng']  # 定义需要跳过的字符串数组['#', '@', '#genre#'] 
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
        "60.223.72.118", "222.130.146.175", "124.64.11.135", "118.248.218.7", "119.39.97.2", "58.248.112.205", "120.87.97.246", "27.40.16.70", "jxcbn.ws-cdn.gitv.tv"
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

    # 清空 live.txt 文件后读取 channel.txt 文件
    open('live.txt', 'w').close()
    channel_lines = read_txt('channel.txt')
    tv_lines = read_txt_file('tv.txt')

    # 处理 channel.txt 文件中的每一行
    for channel_line in channel_lines:
        if "#genre#" in channel_line:
            append_to_file('live.txt', [channel_line])
        else:
            channel_name = channel_line.split(",")[0].strip()
            print(f"正在筛选自选频道: {channel_name}")  # 调试信息
            matching_lines = [tv_line for tv_line in tv_lines if tv_line.split(",")[0].strip() == channel_name]
            if not matching_lines:
                print(f"未匹配的频道: {channel_name}")
            append_to_file('live.txt', matching_lines)

    live_lines = read_txt('live.txt')
    remove_empty_lines('live.txt')
    print(f"待检测文件 live.txt 总行数: {len(live_lines)}")
    print(f"自定义收藏的频道总数: {len(channel_lines)}")

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
CCTV1,http://58.248.112.205:8006/GD_CUCC/G_CCTV-1-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHZMxCRWp3HWsIw2YA4WN0gZ4ZwGH0TEaahnmJ3AUk9g%2B&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV2,http://58.248.112.205:8006/GD_CUCC/G_CCTV-2-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHYpSLOWx8KnbAEA%2FNlMdpMt4ZwGH0TEaahnmJ3AUk9g%2B&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV3,http://58.248.112.205:8006/GD_CUCC/G_CCTV-3-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHTZfkz7RIpdfIwJsxT6gQaB4ZwGH0TEaahnmJ3AUk9g%2B&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV4,http://58.248.112.205:8006/GD_CUCC/G_CCTV-4-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHe5MfrWrjPe5q06p5LAS8TUtN86kueV3HZoMvTL28BOV&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV5,http://58.248.112.205:8006/GD_CUCC/G_CCTV-5-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHfjI6wzwX5YlP5VGDtCFYEotN86kueV3HZoMvTL28BOV&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV5+,http://58.248.112.205:8006/GD_CUCC/G_CCTV-5PLUS-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHYdR%2FXUke9cnQAha7YFSVSdY6KJ0YlTSaKwh%2FkUorJB0&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV6,http://58.248.112.205:8006/GD_CUCC/G_CCTV-6-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHaquAvgVGCBNc5yICXxWYNYtN86kueV3HZoMvTL28BOV&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV7,http://58.248.112.205:8006/GD_CUCC/G_CCTV-7-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHWhwnULjlEBfSKy1l8wbijAtN86kueV3HZoMvTL28BOV&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV8,http://58.248.112.205:8006/GD_CUCC/G_CCTV-8-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHW6PrfWRPRPmGe%2BdNGyl5jItN86kueV3HZoMvTL28BOV&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV9,http://58.248.112.205:8006/GD_CUCC/G_CCTV-9-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHXltvbyel90%2BujQX9sEOc7AtN86kueV3HZoMvTL28BOV&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV10,http://58.248.112.205:8006/GD_CUCC/G_CCTV-10-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHUsd9mij0JyOcibqYTdmWtKVHtMQrYKMhXfF9Bgs%2FQgY&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV11,http://58.248.112.205:8006/GD_CUCC/G_CCTV-11-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHQtjk7PDi4fkN2nvO2gK27uVHtMQrYKMhXfF9Bgs%2FQgY&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV12,http://58.248.112.205:8006/GD_CUCC/G_CCTV-12-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHRtFGgShYCQQqFHAFhzmleqVHtMQrYKMhXfF9Bgs%2FQgY&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV13,http://58.248.112.205:8006/GD_CUCC/G_CCTV-13-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHeUi4Thb7vkXG9wotcNmK%2FSVHtMQrYKMhXfF9Bgs%2FQgY&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV14,http://58.248.112.205:8006/GD_CUCC/G_CCTV-14-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHc44kHEGXWPeTdip0KbSgbeVHtMQrYKMhXfF9Bgs%2FQgY&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV15,http://58.248.112.205:8006/GD_CUCC/G_CCTV-15-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHYyPYgkCWBSIT3aCcBdsAjuVHtMQrYKMhXfF9Bgs%2FQgY&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV16,http://58.248.112.205:8006/GD_CUCC/G_CCTV-16-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHVSIaGkZ%2BPhCYgvTlbbof9eVHtMQrYKMhXfF9Bgs%2FQgY&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV17,http://58.248.112.205:8006/GD_CUCC/G_CCTV-17-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHflsNSUvoRXJq9Dxabd45ukMgMwyeTsEM4M617I3YR8P&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
CCTV1,http://120.87.97.246:8114/GD_CUCC/G_CCTV-1-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBVJJZNDYjNTYW0xrj2atp5krmovGfhet3wgtKVBhIbxM&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714141158688&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515e96acf29ccb8a&FvSeid=88fe5578aee15bbe&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4298&Fsv_chan_hls_se_idx=60&Fsv_TBt=8468056&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-1-CQ&Fsv_CMSID=GD_CUCC
CCTV2,http://221.4.143.69:8114/GD_CUCC/G_CCTV-2-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBa03tuFR%2Fdsya1OSO0Z1VDEEWNg5ICoftLE%2FdS9%2BOGL0&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714141587490&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515e9a069bf67e38&FvSeid=88fe5578aee2f1ef&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=9874&Fsv_chan_hls_se_idx=60&Fsv_TBt=8466752&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-2-CQ&Fsv_CMSID=GD_CUCC
CCTV3,http://221.4.143.70:8114/GD_CUCC/G_CCTV-3-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBewnOI0Q0FnH0j6ix%2FEuEE%2FlrAcxI6a6K3gCsE%2F0xqwv&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714141713143&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515e9b01de7422d3&FvSeid=88fe5578aee4ebd2&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=9873&Fsv_chan_hls_se_idx=59&Fsv_TBt=8465136&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-3-CQ&Fsv_CMSID=GD_CUCC
CCTV4,http://58.248.112.229:8114/GD_CUCC/G_CCTV-4-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBRab8%2B23dyjcWftcVGhPU%2BNGwbxMCOQz1LvVoHJF7Vi%2F&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714141890962&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515e9c65870a689b&FvSeid=88fe5578aeeccb46&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18136&Fsv_chan_hls_se_idx=59&Fsv_TBt=8467576&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-4-CQ&Fsv_CMSID=GD_CUCC
CCTV5,http://58.248.112.230:8114/GD_CUCC/G_CCTV-5-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBSH%2Fdcga0ub9HyjSFJq4wMsikb7ADOVlWhn49oiB6V%2FG&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714141993662&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515e9d32fa20cc6a&FvSeid=88fe5578aeee6593&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18135&Fsv_chan_hls_se_idx=58&Fsv_TBt=8468304&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-5-CQ&Fsv_CMSID=GD_CUCC
CCTV5+,http://58.248.112.229:8114/GD_CUCC/G_CCTV-5PLUS-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBYdR%2FXUke9cnQAha7YFSVSe71iqwQ7l064%2Fcza9NPPzC&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714142067736&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515e9dc7161f6f45&FvSeid=88fe5578aeef8e53&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18140&Fsv_chan_hls_se_idx=58&Fsv_TBt=8466448&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-5PLUS-CQ&Fsv_CMSID=GD_CUCC
CCTV6,http://58.248.112.230:8114/GD_CUCC/G_CCTV-6-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBdDMxs6M4VqBOY3wzfYh5Zn70IXSXFRQUc4GqtZY1Coe&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714142154017&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515e9e73ad37b261&FvSeid=88fe5578aef0e784&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18133&Fsv_chan_hls_se_idx=57&Fsv_TBt=8464824&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-6-CQ&Fsv_CMSID=GD_CUCC
CCTV7,http://120.87.97.245:8114/GD_CUCC/G_CCTV-7-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBbnOCQoNESV2qWsAYbhnlDiyPV4eph4rJWQgnDXisMTe&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714142251011&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515e9f359e8a15a7&FvSeid=88fe5578aef26916&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4291&Fsv_chan_hls_se_idx=57&Fsv_TBt=8467648&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-7-CQ&Fsv_CMSID=GD_CUCC
CCTV8,http://58.248.112.230:8114/GD_CUCC/G_CCTV-8-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBYZxg8b1eRG7LTk8x07GrI44Cftlba08rT1Q6udDNxyt&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714142312998&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515e9fb1a10697de&FvSeid=88fe5578aef360be&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18131&Fsv_chan_hls_se_idx=56&Fsv_TBt=8466856&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-8-CQ&Fsv_CMSID=GD_CUCC
CCTV9,http://221.4.143.69:8114/GD_CUCC/G_CCTV-9-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBZc7OJ1GFY%2FDpyULoLmfNSfAKtWnnk8cjSV9zSUfQpeh&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714142362100&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515ea013cefbd9a1&FvSeid=88fe5578aeef086a&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=9866&Fsv_chan_hls_se_idx=56&Fsv_TBt=8466328&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-9-CQ&Fsv_CMSID=GD_CUCC
CCTV10,http://120.87.97.246:8114/GD_CUCC/G_CCTV-10-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBUsd9mij0JyOcibqYTdmWtJRAbL1Z1y%2FbfEZUJlg3Wvj&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714142432333&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515ea0a05b529be9&FvSeid=88fe5578aef54285&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4288&Fsv_chan_hls_se_idx=55&Fsv_TBt=8467232&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-10-CQ&Fsv_CMSID=GD_CUCC
CCTV11,http://58.248.112.229:8114/GD_CUCC/G_CCTV-11-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBQtjk7PDi4fkN2nvO2gK27vcQcFLN2lXJ4FdJoL4kLn0&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714142503836&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515ea12f4d9ddde5&FvSeid=88fe5578aef65e1f&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18128&Fsv_chan_hls_se_idx=55&Fsv_TBt=4356104&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-11-CQ&Fsv_CMSID=GD_CUCC
CCTV12,http://58.248.112.230:8114/GD_CUCC/G_CCTV-12-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBRtFGgShYCQQqFHAFhzmleoLMq0KIThiOUWH4ztNrd0k&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714142580867&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515ea1c95f2a805f&FvSeid=88fe5578aef792b7&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18127&Fsv_chan_hls_se_idx=54&Fsv_TBt=8466896&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-12-CQ&Fsv_CMSID=GD_CUCC
CCTV13,http://58.248.112.229:8114/GD_CUCC/G_CCTV-13-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBeUi4Thb7vkXG9wotcNmK%2FSEqT0xBi9U3gvduQFenMFz&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714142684111&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515ea297dbe86391&FvSeid=88fe5578aef92c0e&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18126&Fsv_chan_hls_se_idx=54&Fsv_TBt=8467928&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-13-CQ&Fsv_CMSID=GD_CUCC
CCTV13,http://27.40.16.69:8114/GD_CUCC/G_CCTV-NEWS.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKtFFYII9SK6P1IL3s11GhJ1pf5JnC9Eg4rDEpIRMhpPS&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715183857978&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e67e539b6e818&FvSeid=77fd5578ee83ca61&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=1034&Fsv_chan_hls_se_idx=11&Fsv_TBt=2287152&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-NEWS&Fsv_CMSID=GD_CUCC
CCTV14,http://120.87.97.246:8114/GD_CUCC/G_CCTV-14-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBc44kHEGXWPeTdip0KbSgbcUS47HSY0WGvdsrttpfOO6&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714142761082&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515ea331cc7525f8&FvSeid=88fe5578aefa65da&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4284&Fsv_chan_hls_se_idx=53&Fsv_TBt=8467848&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-14-CQ&Fsv_CMSID=GD_CUCC
CCTV15,http://27.40.16.69:8114/GD_CUCC/G_CCTV-15-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBYyPYgkCWBSIT3aCcBdsAjsuu6MyRrRs1cAsik3e8WER&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714142830484&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515ea3bca60188e9&FvSeid=88fe5578aefb7ba7&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4261&Fsv_chan_hls_se_idx=53&Fsv_TBt=8467296&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-15-CQ&Fsv_CMSID=GD_CUCC
CCTV16,http://221.4.143.70:8114/GD_CUCC/G_CCTV-16-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBVSIaGkZ%2BPhCYgvTlbbof9ehJWpxNEs6VzmrJ5uWaaFf&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714142879377&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515ea41e722a0a58&FvSeid=88fe5578aef71f1f&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=9859&Fsv_chan_hls_se_idx=52&Fsv_TBt=8468280&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-16-CQ&Fsv_CMSID=GD_CUCC
CCTV17,http://58.248.112.229:8114/GD_CUCC/G_CCTV-17-CQ.m3u8?Authinfo=56fbZo0WT6rfM%2FXuA%2B6zBflsNSUvoRXJq9Dxabd45ul6sEw7jHEWykLtxlHY3hJu&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.19&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4219&gAppVersionName=4.2.19&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1714142953661&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=0&gCityCode=DEFAULT&verType=0&Fsv_Tgid=515ea4b3041d0be6&FvSeid=88fe5578aefd65ce&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18122&Fsv_chan_hls_se_idx=52&Fsv_TBt=8466808&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CCTV-17-CQ&Fsv_CMSID=GD_CUCC
CCTV1,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV1HD/index.m3u8?gMac=unknown&livodToken=bb800ae03c2a2601e027d128dbd1b82006eadafaf3c87df367dfbc39b38e217c_1720507748_604800&fromCDN=ws
CCTV1,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV1HD/index.m3u8?gMac=unknown&livodToken=3f76fa247855b9f1507e08620e857dda1b4424839963e7074fc1ee72310d6023_1720504514_604800&fromCDN=ws
CCTV2,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV2HD/index.m3u8?gMac=unknown&livodToken=3c65cf8c046f4fa02293a900a4fb002a1581aa92702ef56b1b4b66d7c9d5dcd3_1720507803_604800&fromCDN=ws
CCTV3,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV3_HD/index.m3u8?gMac=unknown&livodToken=5c5d27dfa6b308e64237c7af856d43276f42c5fa0da49c14c8f267c3f853f277_1720507841_604800&fromCDN=ws
CCTV3,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV3_HD/index.m3u8?gMac=unknown&livodToken=f62fb091a195ebe647b1222ede2e69841a9077e00d7164564988bff3361446f2_1720504551_604800&fromCDN=ws
CCTV4,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV4HD/index.m3u8?gMac=unknown&livodToken=a2076a91d4ab3e3a8d96df561854b17563ddc027aec6e893eac3be4e11830fb7_1720507863_604800&fromCDN=ws
CCTV4,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV4HD/index.m3u8?gMac=unknown&livodToken=d26bda0b501044353fe102fbe85cb45a6dfdaca26f4a7522f2b693761325ad82_1720504557_604800&fromCDN=ws
CCTV5,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV5_HD/index.m3u8?gMac=unknown&livodToken=aa173201e6b845bbee67f1b26f1a348b9e154cf79c6d52eef85063a55d21c61b_1720504563_604800&fromCDN=ws
CCTV5,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV5_HD/index.m3u8?gMac=unknown&livodToken=0a8daf617d4530fe59311611a96dcccfd6a7c054c880e8d1cef242c8da5f0a32_1720507885_604800&fromCDN=ws
CCTV6,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV6_HD/index.m3u8?gMac=unknown&livodToken=86f8139ff3260e367086c8b1e4760a54b14301be0d4152d8f47fe1940086b3ae_1720507946_604800&fromCDN=ws
CCTV8,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV8_HD/index.m3u8?gMac=unknown&livodToken=a262d6f91c91f1b3b9970ca0005377026a37645dbb4150a3131badc4e3a5ad2f_1720508010_604800&fromCDN=ws
CCTV8,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV8_HD/index.m3u8?gMac=unknown&livodToken=5054faa27b50dbbb99bd1082115e5860f6edb52038a9e0f954d26199625c8810_1720504606_604800&fromCDN=ws
CCTV9,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV9HD/index.m3u8?gMac=unknown&livodToken=827790a3c97b2ec4d8db29f865f4a76f6ee666e7dd6f7d8d79c95ff19569c406_1720508034_604800&fromCDN=ws
CCTV9,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV9HD/index.m3u8?gMac=unknown&livodToken=7962fd0fc672036d700e4e49a432622a74e060a23f1b55b1cc1e2ee7ee13b4a9_1720504614_604800&fromCDN=ws
CCTV10,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV10HD/index.m3u8?gMac=unknown&livodToken=3372eeac7f52075d36d0edd66eab703b95c8eb3ddf8502186f235a1d890717d9_1720508080_604800&fromCDN=ws
CCTV10,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV10HD/index.m3u8?gMac=unknown&livodToken=fabd3816e5335ddba8d1d88c9536a13c2675337479957dee07e669564a88f4e7_1720504638_604800&fromCDN=ws
CCTV11,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV11HD/index.m3u8?gMac=unknown&livodToken=0034ae2fe24df5a14eb68b5de40ac5b36ab49542913cb5b015ae64ff49312f97_1720504669_604800&fromCDN=ws
CCTV11,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV11HD/index.m3u8?gMac=unknown&livodToken=b7b4308467a66538e5a370fdfe90b3be8c54fa72c5cb958e5f43f4f56e036d2e_1720508128_604800&fromCDN=ws
CCTV12,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV12HD/index.m3u8?gMac=unknown&livodToken=580c20b986086596a03afb85524d28a7b1255fd045cc29e549830abd92eab828_1720508158_604800&fromCDN=ws
CCTV12,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV12HD/index.m3u8?gMac=unknown&livodToken=2c98acaa80392eb7cfc5167a9a71482882518255259852ee6387715d5104fd23_1720504686_604800&fromCDN=ws
CCTV13,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV13HD/index.m3u8?gMac=unknown&livodToken=f4be577234c226bfecf00f96b626bcca106a9d4eaeeaae331b860678bd3f60e7_1720508191_604800&fromCDN=ws
CCTV13,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV13HD/index.m3u8?gMac=unknown&livodToken=7ff060443836507a41a5214026042c9626a11fbff401291700ce35d59c3e6293_1720504703_604800&fromCDN=ws
CCTV14,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV14HD/index.m3u8?gMac=unknown&livodToken=c1f72c79ee7857898e80e822b3768418b14d710294fb16dc503997f9bce0adda_1720508238_604800&fromCDN=ws
CCTV14,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV14HD/index.m3u8?gMac=unknown&livodToken=0d96180497a13efbadc909954e682aae4e63affa0ef1823b5c6dc5a73b461db4_1720504729_604800&fromCDN=ws
CCTV15,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV15/index.m3u8?gMac=unknown&livodToken=b714fc4aa91983a115cdc86176cd98542fc7be2916c39a626ef88fe721f90859_1720504745_604800&fromCDN=ws
CCTV15,http://jxcbn.ws-cdn.gitv.tv/hls/CCTV15/index.m3u8?gMac=unknown&livodToken=bde6e809b30a2e9d5be77b50b95f7634e4524e2a06f94bbcec4356d0f5b54ae3_1720508275_604800&fromCDN=ws
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
北京卫视,http://58.248.112.205:8006/GD_CUCC/G_BEIJING-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHX6pFJlsKFX2elUkY7G9WuYMgMwyeTsEM4M617I3YR8P&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
东方卫视,http://58.248.112.205:8006/GD_CUCC/G_DONGFANG-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHfFI8ayEeoekFD8P08%2F7EXF4NHMHVaPey3ntJx7niV8g&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
湖南卫视,http://58.248.112.205:8006/GD_CUCC/G_HUNAN-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHRo9Db0sT8QFSkrF29I7qMlTsBzPp9x%2Bi0NFonroQm9c&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
江苏卫视,http://58.248.112.205:8006/GD_CUCC/G_JIANGSU-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHe%2BuH8HDFS0PtokY11nWnf4MgMwyeTsEM4M617I3YR8P&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
浙江卫视,http://58.248.112.205:8006/GD_CUCC/G_ZHEJIANG-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHdr3tmmw%2BL49D6e6Yw0TfYx4NHMHVaPey3ntJx7niV8g&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
黑龙江卫视,http://58.248.112.205:8006/GD_CUCC/G_HEILONGJIANG-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHYGO4sBlEXR27vS0rpENy%2BBCfQjfKrVAhZ7nyqv5N0cI&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
吉林卫视,http://58.248.112.205:8006/GD_CUCC/G_JILIN-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHSKeM%2FnJizcqZgRu5kTtQyRSM%2B19aM2hw2IMIRHBBV72&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
辽宁卫视,http://58.248.112.205:8006/GD_CUCC/G_LIAONING-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHURqeVO49Tnq6K%2BWCd0TWOt4NHMHVaPey3ntJx7niV8g&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
河北卫视,http://58.248.112.205:8006/GD_CUCC/G_HEBEI-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHQcq7ejyAAXuDG88sZCpS0RSM%2B19aM2hw2IMIRHBBV72&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
天津卫视,http://58.248.112.205:8006/GD_CUCC/G_TIANJIN-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHaessbbY33u5MnZnHCFZZTIMgMwyeTsEM4M617I3YR8P&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
山东卫视,http://58.248.112.205:8006/GD_CUCC/G_SHANDONG-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHY%2BfIJoJ9xhIZtB7lTaNNRJ4NHMHVaPey3ntJx7niV8g&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
安徽卫视,http://58.248.112.205:8006/GD_CUCC/G_ANHUI-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHfKoKW8pLH0L%2FBk2FrKutcNTsBzPp9x%2Bi0NFonroQm9c&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
河南卫视,http://58.248.112.205:8006/GD_CUCC/G_HENAN-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHWZ%2Fm7n7CVTCrcobp4nZ6sZSM%2B19aM2hw2IMIRHBBV72&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
湖北卫视,http://58.248.112.205:8006/GD_CUCC/G_HUBEI-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHc%2FzOJ%2F44TR7mqGS1%2Bw8V7hSM%2B19aM2hw2IMIRHBBV72&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
江西卫视,http://58.248.112.205:8006/GD_CUCC/G_JIANGXI-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHSFtNLUdun4aiq6hb34UOKeRQN%2BYLDq5f9pmexwERDLi&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
东南卫视,http://58.248.112.205:8006/GD_CUCC/G_DONGNAN-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHQ3sVbVN1ZTQKUpnK8xcf7yRQN%2BYLDq5f9pmexwERDLi&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
广东卫视,http://58.248.112.205:8006/GD_CUCC/G_GUANGDONG-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHfgbSbSCTYnboG1IAsnN%2B8QE6B7fY0qM5PCisIiFJCnl&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
深圳卫视,http://58.248.112.205:8006/GD_CUCC/G_SHENZHEN-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHdBPUZJQRNJB5bOiIhhUc3d4NHMHVaPey3ntJx7niV8g&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
广西卫视,http://58.248.112.205:8006/GD_CUCC/G_GUANGXI-HQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHUIecLjXoLUiOhb4XqRrxOuRQN%2BYLDq5f9pmexwERDLi&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
海南卫视,http://58.248.112.205:8006/GD_CUCC/G_HAINAN-HQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHTh7JGAu1YMGJ6XT%2FnqLPsRZEJK%2BpW4Fs700noHhVlGc&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
四川卫视,http://58.248.112.205:8006/GD_CUCC/G_SICHUAN-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHShysHnFVsdNiy%2FnVMuA%2F2ui53pLIt5xLZYRaSNohMBM&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
重庆卫视,http://58.248.112.205:8006/GD_CUCC/G_CHONGQING-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHS5XA1hsd3RREgysPiqqJeTFDuOvLs1zu4981Mqid2sx&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
贵州卫视,http://58.248.112.205:8006/GD_CUCC/G_GUIZHOU-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHWs5lc8HFQLTI9VPV%2F62TTuRQN%2BYLDq5f9pmexwERDLi&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
云南卫视,http://58.248.112.205:8006/GD_CUCC/G_YUNNAN-CQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHcpOXbCYIiVElKHA3dFAzTD1BWtWU81eWqPvN0PhI2pD&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
陕西卫视,http://58.248.112.205:8006/GD_CUCC/G_SHANXI-HQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHe8cMCaTgpWWUaOfH%2BZI9az1BWtWU81eWqPvN0PhI2pD&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
甘肃卫视,http://58.248.112.205:8006/GD_CUCC/G_GANSU-HQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHQqvE61CmV4kFMWXpFeskG1SM%2B19aM2hw2IMIRHBBV72&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
三沙卫视,http://58.248.112.205:8006/GD_CUCC/G_SANSHA-HQ.m3u8?Authinfo=3iRp8RZG1d3hGsaPmj%2FtHVaHhm7EfB24tSDTA%2B4ZUJz1BWtWU81eWqPvN0PhI2pD&p=GITV&area=GD_CUCC&mac=d4:38:44:a5:72:8b
广东卫视,http://120.87.97.246:8114/GD_CUCC/G_GUANGDONG-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKvgbSbSCTYnboG1IAsnN%2B8SqEfgQMFPe4ummH0FzRlHZ&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715177814221&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e38ada34b4c42&FvSeid=77fd5578ee255a62&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4280&Fsv_chan_hls_se_idx=51&Fsv_TBt=8467184&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_GUANGDONG-CQ&Fsv_CMSID=GD_CUCC
江苏卫视,http://58.248.112.229:8114/GD_CUCC/G_JIANGSU-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKu%2BuH8HDFS0PtokY11nWnf4qV6vyu%2BOKjQBSSKsQUVYE&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715178500503&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e3e0a43cf17e8&FvSeid=77fd5578ee3014e1&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18120&Fsv_chan_hls_se_idx=51&Fsv_TBt=8465688&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_JIANGSU-CQ&Fsv_CMSID=GD_CUCC
浙江卫视,http://221.4.143.70:8114/GD_CUCC/G_ZHEJIANG-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKtr3tmmw%2BL49D6e6Yw0TfYxu1Rs%2FVoWmP1ObIwtTG9QM&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715178633727&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e3f14af0e6062&FvSeid=77fd5578ee322b51&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=9855&Fsv_chan_hls_se_idx=50&Fsv_TBt=8466712&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_ZHEJIANG-CQ&Fsv_CMSID=GD_CUCC
湖南卫视,http://27.40.16.69:8114/GD_CUCC/G_HUNAN-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKn6FShWeUnbW0LuGMY6sAL8C%2BfCULxR%2FAC5HDljJd9K3&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715178682174&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e3f7588ed2416&FvSeid=77fd5578ee32eac5&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4255&Fsv_chan_hls_se_idx=50&Fsv_TBt=8472328&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_HUNAN-CQ&Fsv_CMSID=GD_CUCC
东方卫视,http://27.40.16.70:8114/GD_CUCC/G_DONGFANG-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKvFI8ayEeoekFD8P08%2F7EXHQHvoSr2x4xkdtxQfHt6cg&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715178761860&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e4014f3eb28dc&FvSeid=77fd5578ee342bde&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4254&Fsv_chan_hls_se_idx=49&Fsv_TBt=8467904&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_DONGFANG-CQ&Fsv_CMSID=GD_CUCC
北京卫视,http://58.248.112.229:8114/GD_CUCC/G_BEIJING-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKn6pFJlsKFX2elUkY7G9Wuaj1MVb5sXKFIg1u28lIJn0&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715178807747&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e4070b83a8b8c&FvSeid=77fd5578ee34e2cf&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18116&Fsv_chan_hls_se_idx=49&Fsv_TBt=8466128&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_BEIJING-CQ&Fsv_CMSID=GD_CUCC
深圳卫视,http://27.40.16.70:8114/GD_CUCC/G_SHENZHEN-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKtBPUZJQRNJB5bOiIhhUc3e2OqQ5ejG4cfAiuU8Ka%2FSr&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715178863654&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e40e08c51af02&FvSeid=77fd5578ee35c10a&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4252&Fsv_chan_hls_se_idx=48&Fsv_TBt=8467296&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_SHENZHEN-CQ&Fsv_CMSID=GD_CUCC
辽宁卫视,http://27.40.16.69:8114/GD_CUCC/G_LIAONING-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKkRqeVO49Tnq6K%2BWCd0TWOv%2FGe21maMcczv29zbhzU5i&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715178917390&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e414c0b1d923b&FvSeid=77fd5578ee3699e0&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4251&Fsv_chan_hls_se_idx=48&Fsv_TBt=8467984&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_LIAONING-CQ&Fsv_CMSID=GD_CUCC
安徽卫视,http://221.4.143.70:8114/GD_CUCC/G_ANHUI-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKpi6kJCQCoMejZ%2FjmEq59ETBeFztV3v%2BtvhPvprhMbo3&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715178966803&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e41aed47214b9&FvSeid=77fd5578ee375ce2&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=9849&Fsv_chan_hls_se_idx=47&Fsv_TBt=8467952&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_ANHUI-CQ&Fsv_CMSID=GD_CUCC
山东卫视,http://120.87.97.245:8114/GD_CUCC/G_SHANDONG-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKo%2BfIJoJ9xhIZtB7lTaNNRKhgu973cupNzXqrFaHpa4m&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715179016159&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e421184ec77bb&FvSeid=77fd5578ee382291&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4271&Fsv_chan_hls_se_idx=47&Fsv_TBt=8467296&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_SHANDONG-CQ&Fsv_CMSID=GD_CUCC
黑龙江卫视,http://27.40.16.70:8114/GD_CUCC/G_HEILONGJIANG-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKoGO4sBlEXR27vS0rpENy%2BC90wzLcBzAblH7tEMBexot&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715179089553&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e42a45c04fbd0&FvSeid=77fd5578ee3948ee&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4247&Fsv_chan_hls_se_idx=46&Fsv_TBt=8467816&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_HEILONGJIANG-CQ&Fsv_CMSID=GD_CUCC
天津卫视,http://221.4.143.69:8114/GD_CUCC/G_TIANJIN-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKqessbbY33u5MnZnHCFZZTKedVHdYk5kh2CdQP7Xn4%2B6&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715179130392&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e42f60faa9dd1&FvSeid=77fd5578ee39ecbe&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=9847&Fsv_chan_hls_se_idx=46&Fsv_TBt=8468032&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_TIANJIN-CQ&Fsv_CMSID=GD_CUCC
广西卫视,http://120.87.97.245:8114/GD_CUCC/G_GUANGXI-HQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKkIecLjXoLUiOhb4XqRrxOuvJ2bhovth1ZiNfRiDsRl0&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715179210822&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e4396f49e6225&FvSeid=77fd5578ee3b2d07&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=1039&Fsv_chan_hls_se_idx=18&Fsv_TBt=4356480&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_GUANGXI-HQ&Fsv_CMSID=GD_CUCC
东南卫视,http://58.248.112.230:8114/GD_CUCC/G_DONGNAN-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKg3sVbVN1ZTQKUpnK8xcf7x%2FCQE0V52YypyihQhUfLY5&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715179246299&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e43ddc7fdc49c&FvSeid=77fd5578ee3bb97c&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18108&Fsv_chan_hls_se_idx=45&Fsv_TBt=4356280&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_DONGNAN-CQ&Fsv_CMSID=GD_CUCC
甘肃卫视,http://120.87.97.245:8114/GD_CUCC/G_GANSU-HQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKu8%2BHz6yr4RTNfYc5PxP2EiHpodLfG71p5gfWMpex5u%2B&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715179903515&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e49004ccec872&FvSeid=77fd5578ee460191&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=1041&Fsv_chan_hls_se_idx=19&Fsv_TBt=4355528&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_GANSU-HQ&Fsv_CMSID=GD_CUCC
贵州卫视,http://58.248.112.229:8114/GD_CUCC/G_GUIZHOU-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKms5lc8HFQLTI9VPV%2F62TTvoUIVS7GXMM5XnqjLoqMGn&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715180048627&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e4a2287e30f84&FvSeid=77fd5578ee48469c&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18107&Fsv_chan_hls_se_idx=45&Fsv_TBt=8466792&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_GUIZHOU-CQ&Fsv_CMSID=GD_CUCC
海南卫视,http://58.248.112.229:8114/GD_CUCC/G_HAINAN-HQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKuHFzyLGvmSMltQzCpEgABbzTx6xqsUWMTeDo0%2FrycmR&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182081651&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e5a049b2f5521&FvSeid=77fd5578ee68091a&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4380&Fsv_chan_hls_se_idx=20&Fsv_TBt=4357088&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_HAINAN-HQ&Fsv_CMSID=GD_CUCC
河北卫视,http://120.87.97.246:8114/GD_CUCC/G_HEBEI-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKhpKSI6s6OLBtormwyqxqXAWWbd7WiLqjR4vnvi9bRwf&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182193047&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e5ae354947b12&FvSeid=77fd5578ee69c553&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4265&Fsv_chan_hls_se_idx=44&Fsv_TBt=8455624&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_HEBEI-CQ&Fsv_CMSID=GD_CUCC
河南卫视,http://221.4.143.69:8114/GD_CUCC/G_HENAN-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKpdyyWmwPpo0%2BOlJpyKTryJEbtG%2Bests7yU1uk2fPQyg&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182227040&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e5b2758477c9d&FvSeid=77fd5578ee6a4d8f&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=9841&Fsv_chan_hls_se_idx=44&Fsv_TBt=8467296&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_HENAN-CQ&Fsv_CMSID=GD_CUCC
湖北卫视,http://58.248.112.230:8114/GD_CUCC/G_HUBEI-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKrg071ENwYSAZcO2GiGH9lI2lGOSb3j5CN1iPWx2HIq9&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182267095&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e5b7775947e97&FvSeid=77fd5578ee6aec3c&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18104&Fsv_chan_hls_se_idx=43&Fsv_TBt=8467728&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_HUBEI-CQ&Fsv_CMSID=GD_CUCC
吉林卫视,http://27.40.16.69:8114/GD_CUCC/G_JILIN-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKqq%2B26rAMzWWYsNVrLLNbHmaARITnQlrumEMUf7cXEvC&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182300069&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e5bb964898020&FvSeid=77fd5578ee6b7111&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4240&Fsv_chan_hls_se_idx=43&Fsv_TBt=8467304&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_JILIN-CQ&Fsv_CMSID=GD_CUCC
江西卫视,http://120.87.97.245:8114/GD_CUCC/G_JIANGXI-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKiFtNLUdun4aiq6hb34UOKdnmvR2PbgsfQI1rMAHU0ky&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182357590&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e5c2c769d42ff&FvSeid=77fd5578ee6c5a9f&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=3156&Fsv_chan_hls_se_idx=1&Fsv_TBt=8478384&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_JIANGXI-CQ&Fsv_CMSID=GD_CUCC
康巴卫视,http://58.248.112.229:8114/GD_CUCC/G_KANGBA.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKlpsS8rdezc18%2BPeYiFzXoVrRQBIQrDCRq9p3SLjrAfL&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182426981&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e5cb735f166c6&FvSeid=77fd5578ee6d6e50&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4389&Fsv_chan_hls_se_idx=23&Fsv_TBt=2287296&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_KANGBA&Fsv_CMSID=GD_CUCC
安多卫视,http://58.248.112.230:8114/GD_CUCC/G_ANDUO.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKuTMtq2yEd8i%2BDTKa8BIczckWD8oWllCoqw4dlcl9k1z&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182463188&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e5cff98ddc89d&FvSeid=77fd5578ee6dfea6&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4390&Fsv_chan_hls_se_idx=23&Fsv_TBt=2287440&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_ANDUO&Fsv_CMSID=GD_CUCC
兵团卫视,http://58.248.112.229:8114/GD_CUCC/G_BINGTUAN.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKg%2BHicnPfeizG3y0NUSJ2dRq2eA%2FYw6jIuuTgXuLMwo%2B&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182594140&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e5e05840acf03&FvSeid=77fd5578ee7008c3&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4391&Fsv_chan_hls_se_idx=24&Fsv_TBt=2284520&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_BINGTUAN&Fsv_CMSID=GD_CUCC
大湾区卫视,http://58.248.112.229:8114/GD_CUCC/G_NANFANG.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKpcF6cxV02%2F2vamAvq3NTjZdp1PqnpHZJhFc1mqvBHwl&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182632351&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e5e52029fd0c6&FvSeid=77fd5578ee70a687&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4393&Fsv_chan_hls_se_idx=25&Fsv_TBt=2287792&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_NANFANG&Fsv_CMSID=GD_CUCC
内蒙古卫视,http://120.87.97.246:8114/GD_CUCC/G_NEIMENGGU.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKtadjOJg8CbeqsqTgzJiG7FM7k1u027nYSb3VMtNVHOm&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182669897&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e5e9d43853283&FvSeid=77fd5578ee7139f9&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=3106&Fsv_chan_hls_se_idx=24&Fsv_TBt=2287296&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_NEIMENGGU&Fsv_CMSID=GD_CUCC
宁夏卫视,http://120.87.97.246:8114/GD_CUCC/G_NINGXIA.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKrEoOVZkTXPRpyu8Fec9vdCdoyO018NO14G7CqFI6mAm&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182701912&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e5edd129ab3fd&FvSeid=77fd5578ee71bb73&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=3108&Fsv_chan_hls_se_idx=25&Fsv_TBt=2287296&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_NINGXIA&Fsv_CMSID=GD_CUCC
农林卫视,http://58.248.112.229:8114/GD_CUCC/G_NONGLIN.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKmcvhGCzk9vaPOy1KwX%2F%2Bt%2Bt8%2BGzw88wCH0ODAqMBq60&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182732724&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e5f1ab8c1956e&FvSeid=77fd5578ee723749&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4395&Fsv_chan_hls_se_idx=26&Fsv_TBt=2287344&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_NONGLIN&Fsv_CMSID=GD_CUCC
三沙卫视,http://221.4.143.70:8114/GD_CUCC/G_SANSHA-HQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKn28G%2BWQkLi7Q1Mh845gzlZpk5pTBlduEA6C0mU%2FOMOo&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182782124&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e5f7d8db637b1&FvSeid=77fd5578ee72f88e&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=8693&Fsv_chan_hls_se_idx=26&Fsv_TBt=4355976&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_SANSHA-HQ&Fsv_CMSID=GD_CUCC
陕西卫视,http://120.87.97.245:8114/GD_CUCC/G_SHANXI-HQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKvTKKoI90D6zih8EBEVuISOoNd58%2BpeLvDCVqfR%2Bz2zC&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182821604&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e5fcc899b5974&FvSeid=77fd5578ee739987&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=3141&Fsv_chan_hls_se_idx=28&Fsv_TBt=4357096&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_SHANXI-HQ&Fsv_CMSID=GD_CUCC
四川卫视,http://58.248.112.230:8114/GD_CUCC/G_SICHUAN-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKihysHnFVsdNiy%2FnVMuA%2F2uEYXiVeRF%2BucKv3Z40C7o4&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182969797&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e60f4e1f02053&FvSeid=77fd5578ee75ea0c&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18102&Fsv_chan_hls_se_idx=42&Fsv_TBt=8468784&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_SICHUAN-CQ&Fsv_CMSID=GD_CUCC
西藏卫视,http://120.87.97.246:8114/GD_CUCC/G_XIZANG.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKmxx5kvhKVtAPfH0qKl14uc0OofWCn8X%2F8yyIACfIeA3&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715183009371&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e61441141c1fd&FvSeid=77fd5578ee768a7f&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=3143&Fsv_chan_hls_se_idx=28&Fsv_TBt=2287296&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_XIZANG&Fsv_CMSID=GD_CUCC
新疆卫视,http://58.248.112.230:8114/GD_CUCC/G_XINJIANG.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKi6FcStVNDiOP%2F2OqxiETIMcXVZrQaEXpNcm6hl5lagk&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715183048966&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e61932f7943b8&FvSeid=77fd5578ee77266d&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=16959&Fsv_chan_hls_se_idx=28&Fsv_TBt=2287296&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_XINJIANG&Fsv_CMSID=GD_CUCC
延边卫视,http://58.248.112.230:8114/GD_CUCC/G_YANBIAN.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKsDHE1G9dncbxrpdCy9LpiOqFDsEdX4qrobuTeLEDWHs&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715183083445&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e61d8353d2539&FvSeid=77fd5578ee77b3ef&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=16969&Fsv_chan_hls_se_idx=10&Fsv_TBt=2284640&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_YANBIAN&Fsv_CMSID=GD_CUCC
云南卫视,http://120.87.97.245:8114/GD_CUCC/G_YUNNAN-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKsw5gpVWcejjhE1KHstDaBG5txDdXzjGOGT72Bx9wXfe&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715183112723&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e6212b9f22693&FvSeid=77fd5578ee78247b&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4260&Fsv_chan_hls_se_idx=42&Fsv_TBt=4356528&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_YUNNAN-CQ&Fsv_CMSID=GD_CUCC
重庆卫视,http://120.87.97.246:8114/GD_CUCC/G_CHONGQING-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKi5XA1hsd3RREgysPiqqJeQsy8aM7T7T6yS2xeSLQCNX&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715183188119&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e62a9bf6c0a15&FvSeid=77fd5578ee79524c&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=4259&Fsv_chan_hls_se_idx=41&Fsv_TBt=8466936&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_CHONGQING-CQ&Fsv_CMSID=GD_CUCC
青海卫视,http://58.248.112.229:8114/GD_CUCC/G_QINGHAI.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKtPONYs6QtaHPseT96s%2FID0CJK8A3PYAgbxQETLpGrgj&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715183368940&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e641325baf208&FvSeid=77fd5578ee7c278e&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18141&Fsv_chan_hls_se_idx=61&Fsv_TBt=2287408&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_QINGHAI&Fsv_CMSID=GD_CUCC
厦门卫视,http://58.248.112.230:8114/GD_CUCC/G_XIAMEN.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKqGN1tBE%2F%2B5MsxIjF3XUVlNwwU2%2BP7Se%2BeLJsHpsPerh&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715183457815&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e64c4e841b5c2&FvSeid=77fd5578ee7d88ff&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18142&Fsv_chan_hls_se_idx=61&Fsv_TBt=2287232&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_XIAMEN&Fsv_CMSID=GD_CUCC
北京奥运纪实,http://58.248.112.229:8114/GD_CUCC/G_BEIJINGJS-CQ.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKlqqd8HLKWN9yv5NoaCSBtwn5c8oDbwHIxF8FZNpmYbI&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715183248846&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e6322fbc94cd8&FvSeid=77fd5578ee7a4621&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=18099&Fsv_chan_hls_se_idx=41&Fsv_TBt=8467416&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_BEIJINGJS-CQ&Fsv_CMSID=GD_CUCC
上海纪实,http://221.4.143.69:8114/GD_CUCC/G_SHANGHAIJS-HD.m3u8?Authinfo=F8UQ%2BEevMmd%2FnekE5YOOKj2XjEQPCgsjHTwYM82OKTALPIQT5K8kr81olsEefKQX&p=GITV&area=GD_CUCC&partnerCode=GD_CUCC&token=0C760427464F16BC52147D30B20FE4AFCF076375187B56B35E8BDB02A2F6902DE9292062EA71D873A44BBEEB2412BDB1EC6FB05780A8EA269429663960F75A0E38AD629F8C7EE56B792DC687DBB007AA5A7E6BA759697151C58F0015A49D684681688F54CF181FEA9885C669F98E6157C28D65F01F79AD703ABEC36AB5501CEAAAA270038E8B9D34B33962FE84B6D2A996DBE32DF2BA88F913DE2ED98DD12A30&version=0.0.0.0&apkVersion=4.2.33&mac=fc:57:03:56:49:16&multicast=0&platform=LIVE&gAreaId=CHN&gAppChannel=DEFAULT&gSoftTermId=TERMINAL&gManufacturer=Hisense&gModel=IP108H&gMac=fc:57:03:56:49:16&gStbId=00000444000710800001FC5703564916&gOsType=android&gOsVersion=4.4.2&gApiLevel=19&gAppVersionCode=4233&gAppVersionName=4.2.33&gDowngrade=EMERGENCY&gProductLineCode=LIVOD&gRomVersion=3.17.2.4602&gTimestamp=1715182933379&gRequests=1&gThirdPartyCDN=0&gGroupCode=&gUserId=002040101532912&isIty=1&gCityCode=DEFAULT&verType=0&Fsv_Tgid=517e60ac13fb7eb3&FvSeid=77fd5578ee755b9a&Fsv_filetype=1&Fsv_ctype=LIVES&Fsv_cid=8739&Fsv_chan_hls_se_idx=32&Fsv_TBt=5380312&Fsv_ShiftEnable=1&Fsv_ShiftTsp=120&Fsv_SV_PARAM1=0&Fsv_otype=0&Provider_id=GD_CUCC&Pcontent_id=G_SHANGHAIJS-HD&Fsv_CMSID=GD_CUCC
北京卫视,http://jxcbn.ws-cdn.gitv.tv/hls/BEIJHD/index.m3u8?gMac=unknown&livodToken=a03d2d8d7e5995cc88771669d9afacef2c4fd34206978b97b7f462f360cbde7c_1720504784_604800&fromCDN=ws
东方卫视,http://jxcbn.ws-cdn.gitv.tv/hls/DONGFHD/index.m3u8?gMac=unknown&livodToken=b7bb48fb65bb7bd0e2ce4de6309c40e502d1cc91787b4b7c85cea02bf3d22638_1720504796_604800&fromCDN=ws
天津卫视,http://jxcbn.ws-cdn.gitv.tv/hls/TIANJHD/index.m3u8?gMac=unknown&livodToken=977e71eed63ad14d681dbd5962343cae48fe3599170fe630e0e7aba01dfde99a_1720504813_604800&fromCDN=ws
黑龙江卫视,http://jxcbn.ws-cdn.gitv.tv/hls/HEILJHD/index.m3u8?gMac=unknown&livodToken=c5b025ddc821b9f62c0a17f301104df2af76e892f429b4636fa8c0f7e52d6506_1720504847_604800&fromCDN=ws
吉林卫视,http://jxcbn.ws-cdn.gitv.tv/hls/JILHD/index.m3u8?gMac=unknown&livodToken=e3a5aac0b06b66cea1848a32750983dbca3a2b898dc6c5dbaf20e082eaa2120b_1720504879_604800&fromCDN=ws
辽宁卫视,http://jxcbn.ws-cdn.gitv.tv/hls/LIAONHD/index.m3u8?gMac=unknown&livodToken=8414e5e18ad89ea3c4592c9e0f82126f60694cbeec6ffe588614efa7dabe7ec8_1720504896_604800&fromCDN=ws
甘肃卫视,http://jxcbn.ws-cdn.gitv.tv/hls/GSWS/index.m3u8?gMac=unknown&livodToken=abae7cfdc425438c30f02fcfa56c8547560a619eefb5dc5e583cc0d3c225a6c3_1720504927_604800&fromCDN=ws
河北卫视,http://jxcbn.ws-cdn.gitv.tv/hls/HAIBHD/index.m3u8?gMac=unknown&livodToken=1496955be2e3c85f6ec35e2080cb5e644170c44157b6171095181e215cb2b392_1720504953_604800&fromCDN=ws
安徽卫视,http://jxcbn.ws-cdn.gitv.tv/hls/ANHUIHD/index.m3u8?gMac=unknown&livodToken=2923444bead95427f28e1d92e80a38244cbaaaebd9e9a136112147831ad676e1_1720505005_604800&fromCDN=ws
河南卫视,http://jxcbn.ws-cdn.gitv.tv/hls/HENHD/index.m3u8?gMac=unknown&livodToken=8f3df88626853460a1d54ef589218045fdcfe63877800445b4cd7b0b39f8b9f6_1720505022_604800&fromCDN=ws
湖北卫视,http://jxcbn.ws-cdn.gitv.tv/hls/HUBEIHD/index.m3u8?gMac=unknown&livodToken=1176edf6948f37e79509982269638c9a3d831651cf925626072c7d35c59ab30d_1720505040_604800&fromCDN=ws
湖南卫视,http://jxcbn.ws-cdn.gitv.tv/hls/HUNANHD/index.m3u8?gMac=unknown&livodToken=dac077f2344d86f6499d547255e452bc95ce6bc8399a6338d4b3c67eee105aea_1720505056_604800&fromCDN=ws
江西卫视,http://jxcbn.ws-cdn.gitv.tv/hls/JXWSHD/index.m3u8?gMac=unknown&livodToken=474c90d882097b2d562398658075287e1e21930013b659af3a1922509cd4bbd1_1720505073_604800&fromCDN=ws
江苏卫视,http://jxcbn.ws-cdn.gitv.tv/hls/JIANGSHD/index.m3u8?gMac=unknown&livodToken=9f2a7ee1dceb8fb0de4c36b3c04903e7e66e2b6428eedbbc68925456ffa75296_1720505091_604800&fromCDN=ws
东南卫视,http://jxcbn.ws-cdn.gitv.tv/hls/DONGNHD/index.m3u8?gMac=unknown&livodToken=91f83145199e758c3ee0a369998a5cbe0e996afbeddd6593a0b69e0b6917bde9_1720505126_604800&fromCDN=ws
广东卫视,http://jxcbn.ws-cdn.gitv.tv/hls/GUANGDHD/index.m3u8?gMac=unknown&livodToken=851dc3367c77a462130bed174d80940abd5a1763eaf3d6f9084d213c49bb0fda_1720505150_604800&fromCDN=ws
深圳卫视,http://jxcbn.ws-cdn.gitv.tv/hls/SHENZHD/index.m3u8?gMac=unknown&livodToken=710c541291228ce0cb2543d93616abf4d2906b24f5fd712fe1e4332d5e31a7f3_1720505175_604800&fromCDN=ws
广西卫视,http://jxcbn.ws-cdn.gitv.tv/hls/GUANGXHD/index.m3u8?gMac=unknown&livodToken=86a5fed20a305cd10cb1e1f3d81ca473de518a45b7e630fa7b7e66dcf2c2e316_1720505191_604800&fromCDN=ws
云南卫视,http://jxcbn.ws-cdn.gitv.tv/hls/YUNNHD/index.m3u8?gMac=unknown&livodToken=4316b96111a2f4a0180625ace771506581add44ed643625ac56fa682704b4af4_1720505208_604800&fromCDN=ws
贵州卫视,http://jxcbn.ws-cdn.gitv.tv/hls/GUIZHD/index.m3u8?gMac=unknown&livodToken=6a5915a95f060a962a33247245c37399e22ab840d24f185001a19bada4f32095_1720505218_604800&fromCDN=ws
四川卫视,http://jxcbn.ws-cdn.gitv.tv/hls/SICHD/index.m3u8?gMac=unknown&livodToken=aae3b7d3f710cb95ac50e10fd1c8915cbd473aa1d627861a4e331b6470420b14_1720505236_604800&fromCDN=ws
新疆卫视,http://jxcbn.ws-cdn.gitv.tv/hls/XJWS/index.m3u8?gMac=unknown&livodToken=f414ce81db6d621fc92644857018571bcc9907b3b71b57e830db6f4be32d0294_1720505252_604800&fromCDN=ws
海南卫视,http://jxcbn.ws-cdn.gitv.tv/hls/HAINHD/index.m3u8?gMac=unknown&livodToken=2b30d57372713ae10ee004113d8ce4b737f5bd7631a1bd4bf19aa667cd535f27_1720505278_604800&fromCDN=ws
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
