import sys
import io
import urllib.request
import http.cookiejar
import json


class Aikuai(object):
    
    def __init__(self, user, password):

        self.user = user
        self.password = password

    def get_opener(self, login_url, headers):

        data = {'user': self.user, 'pass': self.password }
        post_data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(login_url, headers = headers, data = post_data)
        cookie = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
        resp = opener.open(req)
        return {"opener": opener, "headers": headers}

    def get_api_info(self, url, post_data, opener, headers):

        req = urllib.request.Request(url, headers = headers, data = post_data)
        resp = opener.open(req)
        return resp




if __name__ == '__main__':

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

    instance = Aikuai('yeyanbo', 'admin@123')
    login_url = 'http://192.168.102.1/login/x'
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
    opener =  instance.get_opener(login_url, headers)

    api_url = 'http://192.168.102.1/api.php'
    data = {'ac': 'top', 'type': 'home'}
    post_data = urllib.parse.urlencode(data).encode('utf-8')
    resp = instance.get_api_info(api_url, post_data, opener["opener"], opener["headers"])
   # print(resp.read().decode('utf-8'))

    ac_url = 'http://192.168.102.1/Ac/ac_config/getList'
    data = { 'cur_page': '1',
             'per_page':'100',
             'kwd':'MAC/备注' }
    post_data = urllib.parse.urlencode(data).encode('utf-8')
    resp = instance.get_api_info(ac_url, post_data, opener["opener"], opener["headers"])
    ac_dict = json.loads(resp.read().decode('utf-8'))
#    print(ac_dict["data"])
    for i in ac_dict["data"]:
        info = i["ip_addr"]+"-->" + i["mac"] + "-->" + i["state"]
        print(info)
