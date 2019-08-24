from bs4 import BeautifulSoup
import urllib.request
import random
import time
import re

user_agent_list = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]
re_non_word = re.compile(r'[\W]+')


def get_html(url):
    wait()

    print("Opening {}".format(url))
    user_agent = random.choice(user_agent_list)
    request = urllib.request.Request(url, headers={'User-Agent': user_agent})
    response = urllib.request.urlopen(request)
    return response.read()


def wait():
    t = random.uniform(1, 5)
    print("Waiting {} seconds…".format(t))
    time.sleep(t)


def list_pages(url, domain):
    while True:
        soup = BeautifulSoup(get_html(url), 'html.parser')
        yield soup

        a = soup.find('a', {'rel': 'next'})
        if a is None:
            return
        else:
            url = domain + a.attrs['href']


def sermon_pages(soup, domain):
    for a in soup.find_all('a', {'class': 'card__shadow'}):
        yield BeautifulSoup(get_html(domain + a.attrs['href']), 'html.parser')


def find_mp3(soup):
    m = soup.select('a[href$=mp3]')
    return m[0].attrs['href']


def safe_title(unsafe_title):
    """
    Take a title and make it safe for use in filenames.

    >>> safe_title(' Word of Promise, Spirit of God, Hope of Man\\n')
    'word-of-promise-spirit-of-god-hope-of-man'
    >>> safe_title('What Does It Mean to Fulfill the Law in Romans 8:3–4?')
    'what-does-it-mean-to-fulfill-the-law-in-romans-8-3-4'
    """
    sub = re_non_word.sub(' ', unsafe_title)
    return '-'.join(sub.split()).strip().lower()
