# Useragent Fake 
> Based on https://www.whatismybrowser.com latest User-Agent
> 
## Install
`pip install git+https://github.com/sharmankin/useragent_fake.git`

## Usage
### Update User-Agent database
```python
from ua_fake import UserAgent

agent = UserAgent()
agent.update()
# Reading User-Agent entries source: 100%|██████████| 12/12 [00:02<00:00,  4.17it/s]
```
### Get random User-Agent
```python
from ua_fake import UserAgent

agent = UserAgent()

for _ in range(3):
    print(
        agent()
    )
# Mozilla/5.0 (X11; Linux i686; rv:106.0) Gecko/20100101 Firefox/106.0
# Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.105 Mobile Safari/537.36 EdgA/107.0.1418.28
# Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0

```
### Get random User-Agent with specified Browser
```python
from ua_fake import UserAgent

agent = UserAgent()

for _ in range(3):
    print(
        agent.yandex_browser
    )
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 YaBrowser/22.11.0 Yowser/2.5 Safari/537.36
# Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 YaBrowser/22.11.2.463 Mobile/15E148 Safari/604.1
# Mozilla/5.0 (iPod touch; CPU iPhone 16_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 YaBrowser/22.11.2.463 Mobile/15E148 Safari/605.1
```
