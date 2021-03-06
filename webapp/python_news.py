from datetime import datetime

import requests
from bs4 import BeautifulSoup

from webapp.model import db, News


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_python_news():
    html = get_html('https://www.python.org/blogs/')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_='list-recent-posts').findAll('li')
        result_news = []
        for news in all_news:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time').text
            try:
                published = datetime.strptime(published, "%B %d, %Y")
            except(ValueError):
                published = datetime.now()
            save_news(title, url, published)
            # return(published())
            # print(title)
            # print(url)
            # print(published)
    #     result_news.append({
    #         'title': title,
    #         'url': url,
    #         'published': published
    #     })
        return result_news
    return False


def save_news(title, url, published):
    news_exist = News.query.filter(News.url == url).count()
    print(news_exist)
    if not news_exist:
        new_news = News(title=title, url=url, published=published)
        db.session.add(new_news)
        db.session.commit()
# if __name__ == '__main__':
# if __name__ == '__main__':
#     html = get_html('https://www.python.org/blogs/')
#     if html:
#         get_python_news(html)
# if __name__ == '__main__':
#     # if html:
#     #     # with open('python.org.html', 'w', encoding='utf8') as f:
#     #     #     f.write(html)
# #     #     news = get_python_news(html)
# print(get_python_news)
