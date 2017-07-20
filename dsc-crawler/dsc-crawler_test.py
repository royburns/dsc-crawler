# -*- coding: utf-8 -*-

import ujson
import requests

# test for Githook    

URL = 'https://dscapp.dscun.com'
HOST = 'dscapp.dscun.com'
token = "30d9ce9660dbe362b25f7bdabdb31e40"

def get_user_info(user_id):

    print '111'
    url_api = 'api/user'
    headers = {
        'Host': "dscapp.dscun.com",
        'meet-token': '0ccbe9212e7640a904d41ee477076227',
        'Proxy-Connection': 'keep-alive',
        'client-version': '3.4.6.1',
        'Connection': 'keep-alive',
        'os-type': 'iOS',
        'User-Agent': '单身村 3.4.6 rv:3.4.6.1 (iPhone; iOS 10.2; zh_CN)',
        'app-version': '2.0.1',
        'Accept-Encoding': 'gzip'
    }

    data = {'login': '******',
            'pass': '******'
            }

    s = '{}/{}/{}'.format(URL, url_api, user_id)
    # print s
    # 'https://dscapp.dscun.com/api/user/86052'
    r = requests.get(s, headers=headers, json=data)

    print(r.status_code)
    print(r.reason)
    # print(r.text)
    decoded = ujson.decode(r.text)['data']
    for x in decoded:
        print u'{}: {} -- type: {}'.format(x, decoded[x], type(decoded[x]))

    print(decoded['id'])

    pass

if __name__ == "__main__":

    user_id = 107162
    get_user_info(user_id)

    pass
