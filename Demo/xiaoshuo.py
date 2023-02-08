import os
import requests
from bs4 import BeautifulSoup

global save_path
save_path = 'D:/Demo/PythonDemo/wetest/pic/'
if os.path.exists(save_path) is False:
    os.makedirs(save_path)

global headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/54.0.2840.99 Safari/537.36'}
server = 'http://www.xbiquge.la/'

# 星辰变地址
book = 'http://www.xbiquge.la/5/5623/'


# 获取章节内容
def get_content(chapter_url):
    req = requests.get(url=chapter_url);
    html_req = req.content
    html_req_utf8 = str(html_req, 'utf8')
    chapter_req = BeautifulSoup(html_req_utf8, 'html.parser')
    texts = chapter_req.find_all('div', id="content")
    print(texts)
    # 获取div标签id属性content的内容 \xa0 是不间断空白符 &nbsp;
    content = texts[0].contents.replace('\xa0' * 4, '\t')
    print(content)
    return content


def main():
    res = requests.get(book, headers=headers)
    html_res = res.content
    # print(html_res)
    html_res_utf8 = str(html_res, 'utf8')
    # print(html_res_utf8)
    # 使用自带的html.parser解析
    soup = BeautifulSoup(html_res_utf8, 'html.parser')
    # print(soup)
    a = soup.find('div', id='list').find_all('a')
    # print(a)
    for href in a:
        try:
            chapter = server + href.get("href")
            content = get_content(chapter)
            print(content)
            chapter = save_path + href.string.replace("?", "") + ".txt"
            print(chapter)
        except Exception as e:
            print(e)

    pass


if __name__ == '__main__':
    main()
