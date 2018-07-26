'''
用于下载路飞学城7天培训的python视频
'''


# 请求头和cookie
header = {

    "accept" : "application/json, text/plain, */*",
    "accept-encoding" : "gzip, deflate, br",
    "referer" : "https://www.luffycity.com/study/chapter/8947/2/%E7%AC%AC%E4%B8%80%E6%A8%A1%E5%9D%97/Python%E5%85%A5%E9%97%A87%E5%A4%A9%E7%89%B9%E8%AE%AD%E8%90%A5",
    "user-agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    "cookie": "MEIQIA_EXTRA_TRACK_ID=16dbYkHS7qG2kjTCd6KcfYG1pKT; user_key=e2a53781cb03666fe4edf73effc2e340; isDegreeCourse=1; source=shop_course; sessionid=36wlgr908aifhuxkoihn3uixpeicocoo; courseId=3; validPeriodId=30; purchase_course=[{%22courseId%22:%223%22%2C%22validPeriodId%22:30%2C%22price%22:0%2C%22courseUrl%22:%22%22}]; purchase_course_price_sum=0; degree_id=5; module_course_id=35; Hm_lvt_9ccb46bca480aa352bdfe01eaa234edb=1532093153,1532094320,1532157958,1532162284; MEIQIA_VISIT_ID=17ijzaBI1KxIj6glQTUeDsWQDM4; access_token=oj70nOYnqDjodpsLZf56FnI6f8OJlG; csrftoken=D8ezJP9oOfdM361bpC8muuTrAd6ELO3TR5oBQHwiuYaZPrjTsBUk9QP5JfD5s5Aj; token=Bearer%20oj70nOYnqDjodpsLZf56FnI6f8OJlG; username=MrMeng; userImg=//hcdn1.luffycity.com/static/frontend/head_portrait/logo@2x.png; shopCartNumber=0; noticeNumber=7; phone=18510131010; Hm_lpvt_9ccb46bca480aa352bdfe01eaa234edb=1532230309",
    "x-requested-with" : "XMLHttpRequest",
}

# 导入模块
# 自带模块
import os
import time
import random
# 第三名模块
import requests
from queue import  Queue
from selenium import webdriver
from lxml import etree
from urllib import request
from threading import Thread

# 请求数据页
data_url = "https://www.luffycity.com/api/v1/user/module/8947/"
response = requests.get(data_url,headers = header)
# 直接将获取的json数据转化为字典格式，方便操作
text_json = response.json()
# 请求播放视频地址列表
url_list = []
url = "https://www.luffycity.com/micro/play/%d"

# 获取的数据是json格式的
for data in text_json['data']:
    for url_id in data['coursesections']:
        base_url = url % url_id['id']
        url_list.append(base_url)

# 下载函数
def schedule(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('\r下载进度：%.2f%%' % per, end=' ')

#下载视频，暂时没用
def download_video(download_list):
    print('123')
    if not download_list.empty():
        m_name, m_url = download_list.get()
        print('%s下载中...' % m_name)
        request.urlretrieve(m_url, './lufei_video/' + m_name + '.mp4', schedule)  # 下载

# 初始化浏览器
browers = webdriver.Chrome(executable_path=r'E:\reptile\software\chromedriver.exe')

# 请求地址 用于登录
browers.get("https://www.luffycity.com/study/chapter/8947/2/%E7%AC%AC%E4%B8%80%E6%A8%A1%E5%9D%97/Python%E5%85%A5%E9%97%A87%E5%A4%A9%E7%89%B9%E8%AE%AD%E8%90%A5")

# 这个时间是用来输入账号密码登录的
time.sleep(20)
download_list = Queue()

# 创建文件夹
if not os.path.exists('./lufei_video'):
    os.makedirs('./lufei_video')

# 遍历视频地址
for video_url in url_list:

    # 请求地址
    browers.get(video_url)
    # time.sleep()
    # 随机停几秒
    time.sleep(random.randint(5,10))
    # 获取网页源码
    html = etree.HTML(browers.page_source)
    m_url = html.xpath('//video/@src')[0]
    m_name = html.xpath('//small/text()')[0]
    # 直接调用 不使用队列
    # print('%s..下载中，稍安勿躁...' % m_name)
    request.urlretrieve(m_url, './lufei_video/' + m_name + '.mp4', schedule)
    # 如果这个路径存在 则证明正在下载中
    if not os.path.exists('./lufei_video/' + m_name + '.mp4'):
        continue
    print('%s...下载中' % m_name)

    # 还不会使
    # os.system('ffmpeg -i "' + url + '" -c copy ./lufei_video/' + m_name + '.mp4')


    # 使用队列 调用函数
    # download_video(download_list)
    # 将下载路径和文件名放入队列中
    # download_list.put((m_name,m_url))
    # 如果这个路径存在 则证明正在下载中

    # if not os.path.exists('./lufei_video/' + m_name + '.mp4'):
    #     continue
    # print('%s...下载中' % m_name)
'''
# 使用多线程，但是呢 需要上面的循环全部跑完，但是呢 上面的循环跑完需要很久，
# 但是呢 如果将多线程放到循环上面，则下载队列是空的，还要阻塞主线程，那么队列就永远时空的
# 所以暂时就不用了，反正这个月也没流量了
t_list = []
for i in range(5):
    t = Thread(target=download_video, args=(download_list,))
    t.start()
    t_list.append(t)

for v in t_list:
    v.join()

print('视频下载完成')
browers.close()
'''