# -*- coding: utf-8 -*-

import datetime
import os
import os.path
# import random
import sqlite3
import threading
import time
import ujson

# import numpy as np
import requests

import sys
reload(sys)
sys.setdefaultencoding('utf8')

URL = 'https://dscapp.dscun.com'
HOST = 'dscapp.dscun.com'
token = "30d9ce9660dbe362b25f7bdabdb31e40"


class Crawler:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.csv_path = "./db/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        os.makedirs(self.csv_path)
        self.csv_name = self.csv_path + "/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.csv'
        self.db_name = "./temp.db"
        self.lock = threading.Lock()
        # self.proxyProvider = ProxyProvider()
        self.total = 0
        self.done = 0
        self.emptyuser = [] #用来存储无效用户

    def get_user_info(self, user_id):

        if((user_id % 600) == 0): #为了防止网站反爬虫，读600次数据sleep30秒，这个两个数据也是随便设置的。
            time.sleep(30)
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

        print(user_id)
        s = '{}/{}/{}'.format(URL, url_api, user_id)
        try:
            r = requests.get(s, headers=headers, json=data)

            # print(r.status_code)
            # print(r.reason)
            # print(r.text)
            assert r.status_code == 200 or r.status_code == 202
            decoded = ujson.decode(r.text)['data']

            if len(decoded) > 12:
                with sqlite3.connect(self.db_name) as c:
                    try:
                        c.execute("INSERT INTO user VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',"
                                  "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',"
                                  "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',"
                                  "'%s','%s','%s','%s','%s',%d,%d,%d,'%s',%d,'%s','%s')" % (
                                    decoded['id'], decoded['type'], decoded['name'], decoded['os_type'], decoded['birthday'],
                                    decoded['city'], decoded['sex'], decoded['seed'], decoded['flower'], decoded['trumpet'],
                                    '|'.join(decoded['key_info'].split(',')), decoded['avatar'], decoded['education'], decoded['university'], decoded['hometown'],
                                    decoded['height'], decoded['weight'], decoded['characters'], decoded['station'], decoded['company'],
                                    decoded['star_sign'], decoded['ideal_mate'], decoded['nationality'], decoded['update_time'], decoded['birthpet'],
                                    decoded['hobby'], decoded['marriage'], decoded['city_index'], decoded['recommend_num'], decoded['receive_hearts'],
                                    decoded['interest_me_num'], decoded['crush_me_num'], decoded['referee_id'], decoded['referee_name'], decoded['heart_count'],
                                    decoded['is_profile'], decoded['is_crush'], decoded['is_interest'], decoded['heart_dir'], decoded['show_info'],
                                    decoded['hometown'].split(' ')[0], decoded['hometown'].split(' ')[1]))
                    except Exception as ex:
                        print('Line 90: ', ex.message)
            else:
                print('User ID: ', user_id, '无效用户(假数据，或者是被删除用户)！')
                print('Line 92: ', decoded)
                self.emptyuser.append(user_id)
                id, type, name, os_type, birthday, \
                city, sex, seed, flower, trumpet, \
                key_info, avatar, education, university, \
                hometown, height, weight, characters, \
                station, company, star_sign, ideal_mate, nationality, \
                update_time, birthpet, hobby, marriage, city_index, \
                recommend_num, receive_hearts, interest_me_num, crush_me_num, \
                referee_id, referee_name, heart_count, \
                is_profile, is_crush, is_interest, heart_dir, show_info, ht_province, ht_city = \
                    user_id, '-1', '未名', 'ios', '2017-09-01', \
                    '深圳', 'female', '50', '5', '5', \
                    'hometown,birthday,education', '', '本科', '武汉理工大学', \
                    '湖北 武汉', '171', '60', '啦啦啦', \
                    'CEO', '食物与艺术', '处女座', '啦啦啦', '1', \
                    '2017-03-18 17:49:58', '5', '啦啦啦', '1', '1', \
                    '0', '0', '0', '0', \
                    '1', '杨村长', '0', \
                    False, False, False, 0, False, '湖北', '武汉'
                with sqlite3.connect(self.db_name) as c:
                    try:
                        # print(decoded)
                        c.execute("INSERT INTO user VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',"
                                  "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',"
                                  "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',"
                                  "'%s','%s','%s','%s','%s',%d,%d,%d,'%s',%d,'%s','%s')" % (
                                    id, type, name, os_type, birthday,
                                    city, sex, seed, flower, trumpet,
                                    key_info, avatar, education, university,
                                    hometown, height, weight, characters,
                                    station, company, star_sign, ideal_mate, nationality,
                                    update_time, birthpet, hobby, marriage, city_index,
                                    recommend_num, receive_hearts, interest_me_num, crush_me_num,
                                    referee_id, referee_name, heart_count,
                                    is_profile, is_crush, is_interest, heart_dir, show_info, ht_province, ht_city))
                    except Exception as ex:
                        print('Line 91: ', ex.message)
        except Exception as ex:
            print('Line 94: ', ex)

        pass

    def start(self):

        if os.path.isfile(self.db_name):
            os.remove(self.db_name)

        try:
            with sqlite3.connect(self.db_name) as c:
                c.execute('''CREATE TABLE user
                    (id INTEGER, type TINYINT, name VARCHAR(12), os_type VARCHAR(10), birthday DATETIME,
                    city VARCHAR(24), sex VARCHAR(6), seed TINYINT, flower TINYINT, trumpet TINYINT,
                    key_info VARCHAR(120), avatar VARCHAR(1024), education VARCHAR(10), university VARCHAR(56),
                    hometown VARCHAR(56), height TINYINT, weight TINYINT, characters VARCHAR(1024),
                    station VARCHAR(24), company VARCHAR(24), star_sign VARCHAR(24), ideal_mate VARCHAR(1024),
                    nationality TINYINT,
                    update_time DATETIME, birthpet TINYINT, hobby VARCHAR(120), marriage TINYINT, city_index TINYINT,
                    recommend_num TINYINT, receive_hearts TINYINT, interest_me_num TINYINT, crush_me_num TINYINT,
                    referee_id INTEGER, referee_name VARCHAR(12), heart_count TINYINT,
                    is_profile BOOLEAN, is_crush BOOLEAN, is_interest BOOLEAN, heart_dir TINYINT, show_info BOOLEAN,
                    ht_province VARCHAR(12), ht_city VARCHAR(12))''')
        except Exception as ex:
            print('Line 118: ', ex)
            pass

        # for i in range(1, 107075):
        # 1～86482: 79874个无效账户
        # 86483～107170: 10个无效账户
        # 最新人数：107166;
        for i in range(86483, 107170):
            self.get_user_info(i)

        self.group_data()

    def group_data(self):
        print("Creating group data")
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        f = open(self.csv_name, "w")
        f.write("id, type, name, os_type, birthday, \
                city, sex, seed, flower, trumpet, \
                key_info, avatar, education, university, \
                hometown, height, weight, characters, \
                station, company, star_sign, ideal_mate, nationality, \
                update_time, birthpet, hobby, marriage, city_index, \
                recommend_num, receive_hearts, interest_me_num, crush_me_num, \
                referee_id, referee_name, heart_count, \
                is_profile, is_crush, is_interest, heart_dir, show_info, \
                ht_province, ht_city\n")
        for row in cursor.execute('''SELECT * FROM user'''):
            # print(row)
            id, type, name, os_type, birthday, \
            city, sex, seed, flower, trumpet, \
            key_info, avatar, education, university, \
            hometown, height, weight, characters, \
            station, company, star_sign, ideal_mate, nationality, \
            update_time, birthpet, hobby, marriage, city_index, \
            recommend_num, receive_hearts, interest_me_num, crush_me_num, \
            referee_id, referee_name, heart_count, \
            is_profile, is_crush, is_interest, heart_dir, show_info, ht_province, ht_city = row

            f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," #'%s','%s','%s','%s','%s',%d,%d,%d,'%s',%d,'%s','%s'
                    "%s,%s\n" % (
                id, type, name, os_type, birthday,
                city, sex, seed, flower, trumpet,
                key_info, avatar, education, university,
                hometown, height, weight, characters,
                station, company, star_sign, ideal_mate, nationality,
                update_time, birthpet, hobby, marriage, city_index,
                recommend_num, receive_hearts, interest_me_num, crush_me_num,
                referee_id, referee_name, heart_count,
                is_profile, is_crush, is_interest, heart_dir, show_info,
                ht_province, ht_city))
        f.flush()
        f.close()

        os.system("gzip -9 " + self.csv_name)

        print('All empty user ids: ', self.emptyuser)
        print('All empty user count: ', len(self.emptyuser))

if __name__ == "__main__":

    Crawler().start()

    pass
