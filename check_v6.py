import aiohttp
import asyncio
import requests
import time

async def check_url(session, url):
    try:
        start_time = time.time()
        async with session.get(url, timeout=3) as response:
            elapsed_time = time.time() - start_time
            if response.status == 200:
                print(f"{url} - 响应时间：{elapsed_time:.2f}秒")
                return True
            else:
                print(f"{url} - 状态码：{response.status}")
    except asyncio.TimeoutError:
        print(f"{url} - 超时")
    except Exception as e:
        print(f"{url} - 错误：{e}")
    return False

async def main():
    url = "https://raw.githubusercontent.com/suxuang/myIPTV/main/ipv6.m3u"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        response_text = await response.text()
        response_lines = response_text.strip().split('\n')

        tasks = []
        with open('cs.txt', 'w') as f:
            for line in response_lines:
                if "http" in line:
                    task = asyncio.create_task(check_url(session, line.strip()))
                    tasks.append(task)
                    if len(tasks) >= 10:  # 限制同时进行的任务数量
                        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                        tasks = [t for t in tasks if t not in done]

            done, pending = await asyncio.wait(tasks)
            for task in done:
                if task.result():
                    f.write(task.result() + '\n')

if __name__ == "__main__":
    asyncio.run(main())
