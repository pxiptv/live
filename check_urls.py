import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime
import os
import re #正则
import requests
from urllib.parse import urlparse


timestart = datetime.now()

# 读取文件内容 1
def read_txt_file(file_path):
    skip_strings = ['#genre#', '127.0.0.1', '192.168', '198.168', 'ChiSheng9', 'epg.pw', '/udp/', '(576p)', '(540p)', '(360p)', '(480p)', '(180p)', '(404p)', 'r.jdshipin', 'ali.hlspull.yximgs', 'generationnexxxt', 'live.goodiptv.club', 'playtv-live.ifeng']  # 定义需要跳过的字符串数组['#', '@', '#genre#'] 
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

import re

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
    part_str = part_str.replace("TVB", "")  # 替换
    part_str = part_str.replace("中天亚洲台", "中天亚洲")  # 替换
    part_str = part_str.replace("广东｜", "")  # 替换
    part_str = part_str.replace("湖南｜", "")  # 替换
    part_str = part_str.replace("翡翠,http", "翡翠台,http")  # 替换
    part_str = part_str.replace("明珠,http", "明珠台,http")  # 替换
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
    
    # 删除 "?key=txiptv" 及其之后的字符
    part_str = part_str.split('?key=txiptv')[0] + '\n'
    part_str = part_str.split('$LR•')[0] + '\n'

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
urls_all_lines = []

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
        elif line.startswith("http"):
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
            if get_url_file_extension(url)==".m3u" or get_url_file_extension(url)==".m3u8":
                urls_all_lines.append(convert_m3u_to_txt(text))
            elif get_url_file_extension(url)==".txt":
                lines = text.split('\n')
                for line in lines:
                    if  "#genre#" not in line and "," in line and "://" in line:
                        #channel_name=line.split(',')[0].strip()
                        #channel_address=line.split(',')[1].strip()
                        urls_all_lines.append(line.strip())
    
    except Exception as e:
        print(f"处理URL时发生错误：{e}")
        
if __name__ == "__main__":
    # 定义要访问的多个URL
    urls = [
        'https://raw.githubusercontent.com/YueChan/Live/main/IPTV.m3u',
        'https://raw.githubusercontent.com/suxuang/myIPTV/main/ipv6.m3u',
        'https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u',
        'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/cn.m3u',
        'https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/merged_output.txt',
        'https://raw.githubusercontent.com/alonezou/yn-iptv/main/reference/MyIPTV',
        'https://raw.githubusercontent.com/qist/tvbox/master/tvlive.txt',
        'https://raw.githubusercontent.com/leyan1987/iptv/main/iptvnew.txt',
        'https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt',
        'https://raw.githubusercontent.com/fenxp/iptv/main/live/ipv6.txt',
        'https://raw.githubusercontent.com/yuanzl77/IPTV/main/live.txt',
        'https://raw.githubusercontent.com/mlvjfchen/TV/main/iptv_list.txt',
        'https://raw.githubusercontent.com/maitel2020/iptv-self-use/main/iptv.txt',
        'https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.txt',
        'https://raw.githubusercontent.com/zjykfy/ykfy/main/all.m3u',
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
    for url in urls:
        print(f"提取电视频道网址: {url}")
        process_url(url)   #读取上面url清单中直播源存入urls_all_lines

    # 写入 online.txt 文件
    write_txt_file('online.txt',urls_all_lines)
    filter_and_save_channel_names('online.txt')
    lines = read_txt_file('online.txt')

    with open('others.txt', 'w') as others_file, open('online_temp.txt', 'w') as online_file:
        for line in lines:
            if '#' in line and not any(exclude in line for exclude in ["#EXTM3U", "#EXTINF", "#genre#"]):
                name = line.split(',')[0]
                modified_line = line.replace('#', f'\n{name},')
                others_file.write(modified_line)
            else:
                online_file.write(line)
    
    # 合并 online_temp.txt 和 others.txt 为 online.txt
    with open('online.txt', 'w') as final_online_file:
        with open('online_temp.txt', 'r') as online_temp_file:
            final_online_file.write(online_temp_file.read())
        with open('others.txt', 'r') as others_file:
            final_online_file.write(others_file.read())
            
    # 删除临时文件
    import os
    os.remove('online_temp.txt')
    os.remove('others.txt')

    print("一个频道多个网址的行已处理并合并为 online.txt。")

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

    # 读取输入文件内容
    lines1 = read_txt_file('online.txt')
    lines2 = read_txt_file('iptv.txt')
    lines=list(set(lines1 + lines2))
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
            print(f"正在过滤自选频道: {channel_name}")  # 调试信息
            matching_lines = [tv_line for tv_line in tv_lines if tv_line.split(",")[0].strip() == channel_name]
            if not matching_lines:
                print(f"没有找到匹配的频道: {channel_name}")
            append_to_file('live.txt', matching_lines)

    live_lines = read_txt('live.txt')
    remove_empty_lines('live.txt')
    print("待检测文件 live.txt 已生成。")

    print(f"channel.txt 行数: {len(channel_lines)}")
    print(f"live.txt 行数: {len(live_lines)}")

    write_txt_file('whitelist.txt',live_lines)  # 测试

    # 去重 blacklist.txt 文件内容
    remove_duplicates('blacklist.txt')

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
    print(f"iptv.txt iptv.m3u 文件已生成。")
