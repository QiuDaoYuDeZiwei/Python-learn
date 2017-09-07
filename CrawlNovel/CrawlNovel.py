#coding= utf-8
import re
import requests
import time
from SaveData import SaveNovelData


def CrawlNovelList(url, header, proxy):
    """
    input url
    return nextpageurl --string
    """
    source_code = requests.get(
        url,  headers=header, proxies=proxy, timeout=10).text

    p = re.compile(r'''onclick="ys.common.jumpurl\('t','(\d*?)'\)''', re.S)
    NextNovelListUrl = re.findall(p, source_code)[0]
    NextNovelListUrl = r'http://www.yousuu.com/booklist?t=' + \
        str(NextNovelListUrl)

    p2 = re.compile('data-listid="(.*?)"', re.S)
    NovelListUrl = re.findall(p2, source_code)
    NovelListUrl = [r'http://www.yousuu.com/booklist/' +
                    str(i) for i in NovelListUrl]

    a = SaveNovelData()
    for i in NovelListUrl:
        a.InsertTablePageNovel((url, NextNovelListUrl, i))
    a.CloseCon()
    return NextNovelListUrl


def CrawlNovel(url, header, proxy):
    source_code = requests.get(
        url,  headers=header, proxies=proxy, timeout=10).text
    p = re.compile(r'''onclick="ys.common.jumpurl\('page',(\d*?)\)"''', re.S)
    pages = re.findall(p, source_code)
    if pages:
        urlpages = [url + r'?page=' + str(i) for i in set(pages)]
    else:
        urlpages = [url]
    for urlpage in urlpages:
        source_code = requests.get(
            urlpage,  headers=header, proxies=proxy, timeout=10).text
        p = re.compile(r'a href="/book/(\d*?)"', re.S)
        NovelUrl = re.findall(p, source_code)
        NovelUrl = [r'http://www.yousuu.com/book/' + str(i) for i in NovelUrl]
        a = SaveNovelData()
        for novelurl in NovelUrl:
            a.InsertTableNovelUrl((urlpage, novelurl))
        a.CloseCon()


p_novelname = re.compile(
    r'''<span style="font-size:18px;font-weight:bold;">(.*?)</span>''', re.S)
p_novel_orgurl = re.compile(
    r'''<div class="media"><a href="(.*?)"''', re.S)
p_tag_category = re.compile(r'''class="tag category">(.*?)</a>''', re.S)
p_author = re.compile(r'''<a href="/search/(.*?)\?type=author"''',
                      re.S)  # 作者介绍 "/search/(.*?)?type=author
p_novelrank = re.compile(
    r'''<i class="fa fa-star-o"></i>&nbsp;(.*?)</span>''', re.S)
p_detail = re.compile(
    r'<div class="media-body ys-bookmain"><ul class="list-unstyled list-sm">(.*?)</li></ul></div></div></div>', re.S)
p_detail2 = re.compile(r'<.*?>', re.S)


def CrawlNovelData(url, header, proxy):

    source_code = requests.get(
        url,  headers=header, proxies=proxy, timeout=10).text

    novelname = re.findall(p_novelname, source_code)[0]
    novel_orgurl = re.findall(p_novel_orgurl, source_code)[0]
    tag_category = re.findall(p_tag_category, source_code)[0]
    author = re.findall(p_author, source_code)[0]
    novelrank = re.findall(p_novelrank, source_code)[0]
    detail = [re.sub(p_detail2, ' ', i)
              for i in re.findall(p_detail, source_code)][0]
    a = SaveNovelData()
    a.InsertTableNovelData(
        (url,novelname, novel_orgurl, tag_category, author, novelrank, detail))
    a.CloseCon()
