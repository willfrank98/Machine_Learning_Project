from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


f = open("business_news.csv", 'w', encoding="utf-8")
f.write("Timestamp,Headline,Summary\n")
for i in range(1, 2000):
    raw_html = simple_get("https://www.reuters.com/news/archive/businessNews?view=page&page=" + str(i) + "&pageSize=10")
    html = BeautifulSoup(raw_html, "html.parser")

    new_rows = [[] for i in range(10)]
    j = 0
    for time in html.select('.news-headline-list .timestamp'):
        time = time.text.replace(',', '_')
        new_rows[j].append(time)
        j += 1

    j = 0
    for headline in html.select('.news-headline-list h3.story-title')[:10]:
        text = headline.text.strip().replace(',', '_')
        new_rows[j].append(text)
        j += 1

    j = 0
    for summary in html.select('.news-headline-list .story-content p')[:10]:
        text = summary.text.replace('\n', ' ').replace(',', '_')
        new_rows[j].append(text)
        j += 1

    for row in new_rows:
        f.write(str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + '\n')

    print("done page " + str(i))

