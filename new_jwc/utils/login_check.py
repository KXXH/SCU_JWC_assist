import json
from ..config.connectionConfig import TEST_URL
from ..exceptions.loginException import LoginException


def login_check(s):
    r = s.get(TEST_URL)
    try:
        r.json()
    except json.decoder.JSONDecodeError:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text)
        res = soup.find_all(lambda tag: "alert" in tag.get("class", []))
        if not res:
            raise LoginException("未知错误!")
        else:
            raise LoginException(list(res[0].children[-1]).strip())
    return True
