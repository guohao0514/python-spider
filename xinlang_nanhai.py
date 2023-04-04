# -*- coding:utf-8 -*-
"""
作者: guohao
日期: 2023年03月06日
"""
import requests
from lxml import etree
import os

if __name__ == "__main__":
    for page in range(1, 6):
        url = f'https://mil.news.sina.com.cn/roll/index.d.html?cid=234400&page={page}'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        # page = 1
        # param = {
        #     'cid' : 234400,
        #     'page' : page
        # }
        page_text = requests.get(url=url, headers=headers).text
        with open('./nanhai.html', 'w', encoding='utf-8') as fp:
            fp.write(page_text)
        page_tree = etree.HTML(page_text)
        herfs = page_tree.xpath("//div[@class='fixList']//a/@href")
        for herf in herfs:
            myUrl = herf
            dheaders = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
            }
            dpage_text = requests.get(url=myUrl, headers=dheaders)
            dpage_text.encoding = "utf-8"
            dpage_tree = etree.HTML(dpage_text.text)
            try:
                title = dpage_tree.xpath("//h1[@class='main-title']/text()")[0]
                character = '\/:*?？"<>|'
                for s in character:
                    if s in title:
                        title = title.replace(s, '')
                path = f"D:\wenjian\code\pythonProject3\pro\{title}\文字"

                content = dpage_tree.xpath("//p[@cms-style='font-L']/text()")
                if len(content) == 0:
                    content = dpage_tree.xpath("//p/text()")
                time = dpage_tree.xpath("//span[@class='date']/text()")[0]
                time = int(time[:4])
                imgSrcs = dpage_tree.xpath("//div[@class='img_wrapper']/img/@src")

                if 2022 >= time >= 2020:
                    if not os.path.exists(path):
                        os.makedirs(path)
                    with open(f"{path}\{title}.txt", mode="w", encoding="utf-8") as f:
                        for i in content:
                            if len(content) != 1:
                                f.write(i + "\n")
                            else:
                                f.write(i)
                    ipath = f"D:\wenjian\code\pythonProject3\pro\{title}\图片"
                    if not os.path.exists(ipath):
                        os.makedirs(ipath)
                    count = len(imgSrcs)
                    for imgSrc in imgSrcs:
                        imgSrc = 'http:' + imgSrc
                        photo = requests.get(imgSrc, dheaders).content
                        rpath = f"{ipath}\{str(count)+'-'+str(title)}.jpg"
                        with open(rpath, 'wb') as fp:
                            fp.write(photo)
                        count -= 1

                        # print(count)
            except IndexError:
                pass
