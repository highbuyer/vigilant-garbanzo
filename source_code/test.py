import multiprocessing as mp
import time
from urllib.request import urlopen, urljoin
from bs4 import BeautifulSoup
import re

# base_url = "http://127.0.0.1:4000/"
base_url = 'https://morvanzhou.github.io/'


def crawl(url):
    response = urlopen(url)
    time.sleep(0.1)  # slightly delay for downloading
    print(url)
    return response.read().decode()


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.find_all('a', {"href": re.compile('^/.+?/$')})
    title = soup.find('h1').get_text().strip()
    page_urls = set([urljoin(base_url, url['href']) for url in urls])  # 去重
    url = soup.find('meta', {'property': "og:url"})['content']
    return title, page_urls, url


if __name__ == '__main__':
    unseen = set([base_url,])
    seen = set()
    # count = 0
    # while len(unseen) != 0:
    #
    #     htmls = [crawl(url) for url in unseen]
    #     results = [parse(html) for html in htmls]
    #     seen.update(unseen)
    #     unseen.clear()
    #     count += 1
    #     print("第%d遍" % (count))
    #
    #     for title, page_urls, url in results:
    #         unseen.update(page_urls - seen)
    #         # print(title, page_urls, url)

    pool = mp.Pool()
    count, t1 = 1, time.time()
    while len(unseen) != 0:
        if len(seen) >= 20:
            break
        print('\nDistributed Crawling...')
        crawl_jobs = [pool.apply_async(crawl, args=(url,)) for url in unseen]
        htmls = [j.get() for j in crawl_jobs]

        print('\nDistributed Crawling...')
        parse_jobs = [pool.apply_async(parse, args=(html,)) for html in htmls]
        results = [k.get() for k in parse_jobs]

        print('\nDistributed Crawling...')
        seen.update(unseen)
        unseen.clear()

        print("第%d遍" % (count))

        for title, page_urls, url in results:
            unseen.update(page_urls - seen)
            print(count, title, url)
            count += 1
    print('Total time: %.1f s' % (time.time() - t1,))
