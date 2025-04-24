import asyncio
import aiohttp
import argparse
import logging
from urllib.parse import urlparse

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def check_website(session, url, keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }

    logging.info(f"开始检查 URL: {url}")
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            content = await response.text()
            if keyword.lower() in content.lower():
                logging.info(f"URL {url} 包含关键词 '{keyword}'")
                return url
            else:
                logging.info(f"URL {url} 不包含关键词 '{keyword}'")
    except aiohttp.ClientError as client_error:
        logging.error(f"访问 {url} 时发生客户端错误: {client_error}")
    except Exception as e:
        logging.error(f"访问 {url} 时发生未知错误: {e}")
    return None


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


async def process_urls(urls, keyword):
    valid_urls = [url for url in urls if is_valid_url(url)]
    logging.info(f"从输入文件中筛选出 {len(valid_urls)} 个有效 URL")
    async with aiohttp.ClientSession() as session:
        tasks = [check_website(session, url, keyword) for url in valid_urls]
        results = await asyncio.gather(*tasks)
        valid_results = [url for url in results if url]
        logging.info(f"在 {len(valid_urls)} 个有效 URL 中，有 {len(valid_results)} 个包含关键词 '{keyword}'")
        return valid_results


def main():
    parser = argparse.ArgumentParser(description="检查网页是否包含指定关键词")
    parser.add_argument("input_file", type=str, help="包含网址的文本文件路径")
    parser.add_argument("output_file", type=str, help="用于保存包含指定关键词的网址的文件路径")
    parser.add_argument("keyword", type=str, help="要查找的关键词")
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file.readlines() if line.strip()]
        logging.info(f"从文件 {args.input_file} 中读取到 {len(urls)} 个 URL")

        loop = asyncio.get_event_loop()
        valid_urls = loop.run_until_complete(process_urls(urls, args.keyword))

        with open(args.output_file, 'w', encoding='utf-8') as output_file:
            for url in valid_urls:
                output_file.write(url + '\n')
        logging.info(f"已将包含 '{args.keyword}' 关键词的 {len(valid_urls)} 个网址保存到 {args.output_file}")
    except FileNotFoundError:
        logging.error(f"错误: 未找到文件 {args.input_file}")
    except Exception as e:
        logging.error(f"发生未知错误: {e}")


if __name__ == "__main__":
    main()


