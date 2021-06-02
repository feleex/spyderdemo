# 发送多种类型的邮件
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
from lxml import etree
from threading import Timer
import time
from datetime import datetime

last_update_time=datetime.strptime('2021-05-29','%Y-%m-%d')
timearray=[]
timearray.append(last_update_time);
#发送邮件

def sendmessage():
    msg_from = '1106367854@qq.com'  # 发送方邮箱
    passwd = 'rvyyxwyfrkznibee'  # 就是上面的授权码

    to = ['1482525192@qq.com']  # 接受方邮箱

    # 设置邮件内容
    # MIMEMultipart类可以放任何内容
    msg = MIMEMultipart()
    conntent = "内容有更新"
    # 把内容加进去

    msg.attach(MIMEText(conntent, 'plain', 'utf-8'))

    # 设置邮件主题
    msg['Subject'] = "这个是邮件主题"

    # 发送方信息
    msg['From'] = msg_from

    # 开始发送

    # 通过SSL方式发送，服务器地址和端口
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    # 登录邮箱
    s.login(msg_from, passwd)
    # 开始发送
    s.sendmail(msg_from, to, msg.as_string())
    print("邮件发送成功")


# 监控网页
firstelement_xpath='//*[@id="waterfall"]/div[1]'
firstelement_date_xpath='/html/body/div[4]/div/div[3]/div/div[1]/a/div[2]/span/date[2]'
date_xpath='//*[@id="waterfall"]/div[1]/a/div[2]/span/date[2]'
front_url='https://www.seedmm.life/'
chrome_header={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
def getifupdate_by_monitoring ():
    response = requests.get(front_url,chrome_header)
    # print(response.text)
    html=etree.HTML(response.text)

    html_data = html.xpath(date_xpath)
    for i in html_data:
        print('当前更新时间为:'+i.text)
        if is_update(i.text,last_update_time):
            print('last_update_time:'+str(last_update_time))
            print(True)
            sendmessage()
            return
    print(False)
    return

def is_update(text, last_update_time):
    update_time=datetime.strptime(text,'%Y-%m-%d')
    print('上次更新时间为:'+last_update_time.strftime('%Y-%m-%d'))
    # today_time=datetime.strptime(datetime.now().strftime('%Y-%m-%d'),'%Y-%m-%d')
    # print(today_time)
    result=update_time>timearray[0]
    if result:
        timearray[0]=update_time
    return result
# 定时任务
def schedual_monitor():
    getifupdate_by_monitoring()
    t=Timer(60*60*6,schedual_monitor)
    t.start()
    return
    # s=sched.scheduler(time.time, time.sleep)
    # s.enter(0,0,getifupdate_by_monitoring(),(5,))
    # s.run()
schedual_monitor()
# def printa():
#     print('hallo')
#     t=Timer(2,printa)
#     t.start()
# printa()