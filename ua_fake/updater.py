def update_database():
    import re
    from .db import connect

    import requests
    from bs4 import BeautifulSoup as Soup
    from bs4.element import Tag
    from requests.adapters import HTTPAdapter, Retry
    from tqdm import tqdm
    from urllib3.util import Timeout

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

    agents = [elem for item in tqdm(bl, desc='Reading User-Agent entries source') for elem in get_content(item)]

    with connect() as cn:
        cr = cn.cursor()
        cr.executemany(
            # """
            # insert into useragent (app, os, user_agent) values (:browser, :os, :useragent) on conflict do nothing
            # """
            """
                with ex(id) as (select coalesce(c.id, b.id)
                        from (select null as id) b
                                 left join (select id
                                            from useragent
                                            where app = :browser
                                              and user_agent = :useragent) c)
        
                    insert
                    into useragent (app, os, user_agent)
                    select :browser, :os, :useragent
                    from ex
                    where ex.id is null
                    on conflict do nothing;
            """
            ,
            agents
        )

        cr.close()
        cn.commit()
