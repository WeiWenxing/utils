import argparse
import requests
from bs4 import BeautifulSoup


def get_meta_keywords(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            keywords = meta_keywords.get('content')
            return keywords
        return None

    except requests.RequestException as e:
        print(f"请求出错: {e}")
    except Exception as e:
        print(f"发生错误: {e}")
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='从指定 URL 提取 meta 关键词信息')
    parser.add_argument('--url', type=str, required=True, help='要提取关键词的目标 URL')
    args = parser.parse_args()

    url = args.url
    keywords = get_meta_keywords(url)
    if keywords:
        print(f"提取到的关键词信息: {keywords}")
    else:
        print("未找到关键词信息。")

