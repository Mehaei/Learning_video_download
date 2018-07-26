import requests
import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
from lxml import etree
from urllib import request
import threading
from queue import Queue


# 指示进度
def schedule(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('下载进度：%.2f%%' % per, end='\r')


# 下载函数
def my_download(data_q):
    if not data_q.empty():
        url, fname = data_q.get(timeout=5)
        print()
        print('%s下载中...' % fname)
        request.urlretrieve(url, './lufei_viedo/' + fname + '.mp4', schedule)  # 下载


base_url = 'https://www.luffycity.com/classmate/play/%d'
cookie_dict = {
    'MEIQIA_EXTRA_TRACK_ID': '16XR302rgmVJlmjvU6Me4x8sh5C',
    'sessionid': 'awikx1d470kie61mwaxhd28ksu42jwxe',
    'user_key': '95064c6ae4eb5ef0e18a1538f4f105e5',
    'noticeNumber': '2',
    'degree_id': '',
    'Hm_lvt_9ccb46bca480aa352bdfe01eaa234edb': '1530198189,1530198314,1530240259,1530281215',
    'Hm_lpvt_9ccb46bca480aa352bdfe01eaa234edb': '1530281215',
    'MEIQIA_VISIT_ID': '16h7wcl9uzUAoeEVXrY57lRbIRo',
    'MEIQIA_REJECT_INVITATION': 'yes',
    'access_token': 'vm6RQvOBbaOoH4gYGSZvdXPLZIFLqC',
    'csrftoken': 'df0qkHtiBKth67ha1TEgMYoUshrDsQ6KtzbzPHQMEXpq1PlQCgHrXWxyafNmC1fj',
    'token': 'Bearer%20vm6RQvOBbaOoH4gYGSZvdXPLZIFLqC',
    'username': 'RemusMM',
    'userImg': '//hcdn1.luffycity.com/static/frontend/head_portrait/logo@2x.png',
    'shopCartNumber': '0',
    'phone': '15175391106'
}
q_list = []
for i in range(1, 30):
    full_url = base_url % i
    q_list.append(full_url)

for i in range(111, 149):
    full_url = base_url % i
    q_list.append(full_url)

for i in range(233, 281):
    full_url = base_url % i
    q_list.append(full_url)

for i in range(357, 397):
    full_url = base_url % i
    q_list.append(full_url)

driver = webdriver.Chrome(executable_path=r'/Users/remus/PycharmProjects/tools/chromedriver')

# 增加cookie
# for name, value in cookie_dict.items():
#     c1 = {
#         'domain': 'luffycity.com',
#         'name': name,
#         'value': value,
#         'expires': '',
#         'path': '/',
#         'httpOnly': False,
#         'HostOnly': False,
#         'Secure': False,
#     }
#     driver.add_cookie(c1)

driver.get('https://www.luffycity.com/classmate/play/1')
# wait = WebDriverWait(driver, 30)
time.sleep(30)

if not os.path.exists('./lufei_viedo'):
    os.makedirs('./lufei_viedo')

data_q = Queue()
for i in q_list:
    driver.get(i)
    time.sleep(5)
    html = driver.page_source
    html = etree.HTML(html)
    url = html.xpath('//video/@src')[0]  # 拿到视频的url地址
    fname = html.xpath('//small[@class="playing-sec-title"]/text()')[0]  # 视频名字
    if os.path.exists('./lufei_viedo/' + fname + '.mp4'):
        continue
    print(url)
    data_q.put((url, fname))
    print('%s下载中...' % fname)
    os.system('ffmpeg -i "' + url + '" -c copy ./lufei_viedo/' + fname + '.mp4')  # 下载
print('下载完成！')

'''
t_list = []
for i in range(4):
    t = threading.Thread(target=my_download, args=(data_q,))
    t.start()
    t_list.append(t)
mylist = [t.join() for t in t_list]

print('下载完成！')
driver.close()
'''