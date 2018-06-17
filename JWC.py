import re
import http.cookiejar
import urllib
import time
import getpass

class JWC:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def getOpener(self, head):
        httpHandler = urllib.request.HTTPHandler(debuglevel=0)
        cj = http.cookiejar.CookieJar()
        pro = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(httpHandler,pro)
        header = []
        for key, value in head.items():
            elem = (key, value)
            header.append(elem)
        opener.addheaders = header
        return opener

    def login(self):
        url = 'http://202.115.47.141/loginAction.do'
        postDict = {
            'zjh': self.__username,
            'mm': self.__password,
        }
        header = {'Connection': 'Keep-Alive',
                  'Accept': 'text/html, application/xhtml+xml, */*',
                  'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
                  }
        self.__opener = self.getOpener(header)
        postData = urllib.parse.urlencode(postDict).encode(encoding='GBK')
        op = self.__opener.open(url, postData)
        print('正在登陆教务处……')
        data = op.read()
        html1 = data.decode('GBK')
        print(html1)

    def rateAll(self):
        url = 'http://202.115.47.141/jxpgXsAction.do?oper=listWj'
        op = self.__opener.open(url)
        data = op.read()
        html = data.decode('GBK')

        print('正在获取评教清单……')
        # print(html)
        s=r"共(\d+)项"
        self.__listTotalCount = re.search(s, html).groups()[0]
        #time.sleep(5)
        postDict = {
            'pageSize' :int(self.__listTotalCount),
            'totalrows':int(self.__listTotalCount),
        }
        postData = urllib.parse.urlencode(postDict).encode(encoding='GBK')
        url = 'http://202.115.47.141/jxpgXsAction.do'
        req = urllib.request.Request(url, postData)
        op = self.__opener.open(req)
        data = op.read()
        html = data.decode('GBK')
        print(html)
        # 找到课堂教学问卷

        # 评价课堂教学
        for item in re.findall(r'<img name="0000000068#@(.*?)" style="cursor: hand;" title="评估"', html):
            infomationList = item.split("#@")
            postDict = {
                'wjbm':'0000000068',
                'bpr':infomationList[0],
                'pgnr':infomationList[-1],
                'oper':'wjShow',
                'wjmc':infomationList[2],
                'bprm':infomationList[1],
                'pgnrm':infomationList[-2],
                'wjmc':infomationList[3],
                '0000000036' :"10_1",
                '0000000037' :"10_1",
                '0000000038' :"10_1",
                '0000000039' :"10_1",
                '0000000040' :"10_1",
                '0000000041' :"10_1",
                '0000000042' :"10_1",
                'zgpj':'Good!',
            }
            postData = urllib.parse.urlencode(postDict).encode(encoding='GBK')
            self.__opener.open(url, postData)
            url1 = 'http://202.115.47.141/jxpgXsAction.do?oper=wjpg'
            headers = {'Connection': 'Keep-Alive',
                      'Accept': 'text/html, application/xhtml+xml, */*',
                      'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                      'Host':'202.115.47.141',
                      'Referer':'http://202.115.47.141/jxpgXsAction.do?oper=listWj',
                      'Method':'POST',
                      }
            postData = urllib.parse.urlencode(postDict).encode(encoding='GBK')
            req = urllib.request.Request(url1, postData, headers)
            op = self.__opener.open(req)
            print("正在评价%s课程..." % infomationList[3])
            print(postDict)
            data = op.read()
            html1 = data.decode('GBK')
            print(html1)
        # 评价实践教学
        for item in re.findall(r'<img name="0000000069#@(.*?)" style="cursor: hand;" title="评估"', html):
            infomationList = item.split("#@")
            postDict = {
                'wjbm':'0000000069',
                'bpr':infomationList[0],
                'pgnr':infomationList[-1],
                'oper':'wjShow',
                'wjmc':infomationList[2],
                'bprm':infomationList[1],
                'pgnrm':infomationList[-2],
                'wjmc':infomationList[3],
                '0000000089' :"10_1",
                '0000000090' :"10_1",
                '0000000091' :"10_1",
                '0000000092' :"10_1",
                '0000000093' :"10_1",
                '0000000094' :"10_1",
                '0000000095' :"10_1",
                'zgpj':'Good!',
            }
            postData = urllib.parse.urlencode(postDict).encode(encoding='GBK')
            self.__opener.open(url, postData)
            url1 = 'http://202.115.47.141/jxpgXsAction.do?oper=wjpg'
            headers = {'Connection': 'Keep-Alive',
                      'Accept': 'text/html, application/xhtml+xml, */*',
                      'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                      'Host':'202.115.47.141',
                      'Referer':'http://202.115.47.141/jxpgXsAction.do?oper=listWj',
                      'Method':'POST',
                      }
            postData = urllib.parse.urlencode(postDict).encode(encoding='GBK')
            req = urllib.request.Request(url1, postData, headers)
            op = self.__opener.open(req)
            print("正在评价%s课程..." % infomationList[3])
            print(postDict)
            data = op.read()
            html1 = data.decode('GBK')
            print(html1)
        # 评价实验教学
        for item in re.findall(r'<img name="0000000070#@(.*?)" style="cursor: hand;" title="评估"', html):
            infomationList = item.split("#@")
            postDict = {
                'wjbm':'0000000070',
                'bpr':infomationList[0],
                'pgnr':infomationList[-1],
                'oper':'wjShow',
                'wjmc':infomationList[2],
                'bprm':infomationList[1],
                'pgnrm':infomationList[-2],
                'wjmc':infomationList[3],
                '0000000082' :"10_1",
                '0000000083' :"10_1",
                '0000000084' :"10_1",
                '0000000085' :"10_1",
                '0000000086' :"10_1",
                '0000000087' :"10_1",
                '0000000088' :"10_1",
                'zgpj':'Good!',
            }
            postData = urllib.parse.urlencode(postDict).encode(encoding='GBK')
            self.__opener.open(url, postData)
            url1 = 'http://202.115.47.141/jxpgXsAction.do?oper=wjpg'
            headers = {'Connection': 'Keep-Alive',
                      'Accept': 'text/html, application/xhtml+xml, */*',
                      'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                      'Host':'202.115.47.141',
                      'Referer':'http://202.115.47.141/jxpgXsAction.do?oper=listWj',
                      'Method':'POST',
                      }
            postData = urllib.parse.urlencode(postDict).encode(encoding='GBK')
            req = urllib.request.Request(url1, postData, headers)
            op = self.__opener.open(req)
            print("正在评价%s课程..." % infomationList[3])
            print(postDict)
            data = op.read()
            html1 = data.decode('GBK')
            print(html1)
        # 评价体育教学
        for item in re.findall(r'<img name="0000000071#@(.*?)" style="cursor: hand;" title="评估"', html):
            infomationList = item.split("#@")
            postDict = {
                'wjbm':'0000000071',
                'bpr':infomationList[0],
                'pgnr':infomationList[-1],
                'oper':'wjShow',
                'wjmc':infomationList[2],
                'bprm':infomationList[1],
                'pgnrm':infomationList[-2],
                'wjmc':infomationList[3],
                '0000000096' :"10_1",
                '0000000097' :"10_1",
                '0000000098' :"10_1",
                '0000000099' :"10_1",
                '0000000100' :"10_1",
                '0000000101' :"10_1",
                '0000000102' :"10_1",
                'zgpj':'Good!',
            }
            postData = urllib.parse.urlencode(postDict).encode(encoding='GBK')
            self.__opener.open(url, postData)
            url1 = 'http://202.115.47.141/jxpgXsAction.do?oper=wjpg'
            headers = {'Connection': 'Keep-Alive',
                      'Accept': 'text/html, application/xhtml+xml, */*',
                      'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                      'Host':'202.115.47.141',
                      'Referer':'http://202.115.47.141/jxpgXsAction.do?oper=listWj',
                      'Method':'POST',
                      }
            postData = urllib.parse.urlencode(postDict).encode(encoding='GBK')
            req = urllib.request.Request(url1, postData, headers)
            op = self.__opener.open(req)
            print("正在评价%s课程..." % infomationList[3])
            print(postDict)
            data = op.read()
            html1 = data.decode('GBK')
            print(html1)
        # 评价助教
        for item in re.findall(r'<img name="0000000072#@(.*?)" style="cursor: hand;" title="评估"', html):
            infomationList = item.split("#@")
            postDict = {
                'wjbm':'0000000072',
                'bpr':infomationList[0],
                'pgnr':infomationList[-1],
                'oper':'wjShow',
                'wjmc':infomationList[2],
                'bprm':infomationList[1],
                'pgnrm':infomationList[-2],
                'wjmc':infomationList[3],
                '0000000028' :"10_1",
                '0000000029' :"10_1",
                '0000000030' :"10_1",
                '0000000031' :"10_1",
                '0000000032' :"10_1",
                '0000000033' :"10_1",
                'zgpj':'Good!',
            }
            postData = urllib.parse.urlencode(postDict).encode(encoding='GBK')
            self.__opener.open(url, postData)
            url1 = 'http://202.115.47.141/jxpgXsAction.do?oper=wjpg'
            headers = {'Connection': 'Keep-Alive',
                      'Accept': 'text/html, application/xhtml+xml, */*',
                      'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                      'Host':'202.115.47.141',
                      'Referer':'http://202.115.47.141/jxpgXsAction.do?oper=listWj',
                      'Method':'POST',
                      }
            postData = urllib.parse.urlencode(postDict).encode(encoding='GBK')
            req = urllib.request.Request(url1, postData, headers)
            op = self.__opener.open(req)
            print("正在评价%s课程..." % infomationList[3])
            print(postDict)
            data = op.read()
            html1 = data.decode('GBK')
            print(html1)

if __name__ == '__main__':
    username = input("请输入用户名：")
    password = getpass.getpass("请输入密码：")
    j = JWC(username, password)
    j.login()
    j.rateAll()
