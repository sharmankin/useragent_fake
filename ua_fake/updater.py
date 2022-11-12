from bs4 import BeautifulSoup as Soup
import requests
from requests.adapters import HTTPAdapter, Retry
from tqdm import tqdm
from urllib3.util import Timeout
from bs4.element import Tag
import re


bl = [
    'firefox',
    'internet-explorer',
    'opera',
    'safari',
    'chrome',
    'edge',
    'vivaldi',
    'yandex-browser',
    'android',
    'windows',
    'ios',
    'macos'
]

s = requests.Session()

'https://developers.whatismybrowser.com/useragents/explore/software_name/android-webview/'

s.mount(
    'https://',
    HTTPAdapter(
        max_retries=Retry(
            connect=3,
            redirect=3,
            total=5,
            backoff_factor=.0005
        )
    )
)


def get_content(tagret_item: str):
    response = s.get(
        f'https://www.whatismybrowser.com/guides/the-latest-user-agent/{tagret_item}',
        timeout=Timeout(connect=60, read=120, total=180)
    )

    soup = Soup(response.content, 'html.parser')

    data = [tr for t in soup.find_all(
        'table', {'class': 'listing-of-useragents'}
    ) for tr in t.find('tbody').find_all('tr')]

    def row_parse(row: Tag):
        target, u_agents_tag = row.find_all('td')

        *_, os = [*target.stripped_strings]

        *_, os = re.findall(r'\w+', os)

        ua_items = [*u_agents_tag.stripped_strings]

        # _, *p, useragent = row.stripped_strings
        # os, *_ = p or ['Standart', '']
        for item in ua_items:
            yield {
                'browser': tagret_item,
                'os': os.removeprefix('on').strip(),
                'useragent': item
            }

    # return [*map(row_parse, data)]
    return [item for elem in data for item in row_parse(elem)]


agents = [elem for item in tqdm(bl) for elem in get_content(item)]
