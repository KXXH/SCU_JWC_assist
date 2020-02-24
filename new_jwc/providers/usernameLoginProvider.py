import hashlib
import requests
from PIL import Image
from io import BytesIO
import json
import logging
from ..config.headerConfig import header
from ..config.loginConfig import LOGIN_PAGE_URL, CAPTCHA_URL, LOGIN_URL
from ..utils.login_check import login_check


class UsernameLoginProvider:
    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.md5(password.encode()).hexdigest()

    def login(self):
        postDict = {
            'j_username': self.username,
            'j_password': self.password,
        }
        s = requests.Session()
        s.headers.update(header)
        r = s.get(CAPTCHA_URL)
        captcha_img = Image.open(BytesIO(r.content))
        captcha_img.show()
        postDict['j_captcha'] = input('请输入验证码:')
        logging.info('正在登陆教务处……')
        s.post(LOGIN_URL, data=postDict)
        login_check(s)
        return s
