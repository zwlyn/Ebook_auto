from bs4 import BeautifulSoup
import re
import datetime


today = datetime.datetime.now()
yesterday =  datetime.datetime(today.year, today.month, today.day) - datetime.timedelta(days=1)
def parse_order(page):
    """
    page是订单界面的html
    """
    global yesterday
    soup = BeautifulSoup(page, 'lxml')
    orderList = soup.find_all(class_='ordersSyn-list')[0]
    score = 0
    order_num = 0
    for order in orderList:
        night_num = re.findall(r'''<strong data-bind="text: LiveDays&gt;0\? LiveDays: '-'">(\d+)</strong>''', str(order))
        room_num = re.findall(r'''<strong data-bind=" text: Quantity">(\d+)</strong>''', str(order))
        order_id = re.findall(r'''<span data-bind="text: OrderID">(\d+)</span>''', str(order))
        date = re.findall(r'''<span data-bind="text: ArrivalAndDepartureDomestic">(\d+/\d+) - \d+/\d+</span>''', str(order))
        if not night_num or not room_num or not order_id or not date:
            continue
        if not ('已入住' in str(order) or '已接单' in str(order)):
            continue
        date = date[0]
        if int(date.split("/")[0]) != yesterday.month or int(date.split("/")[1]) != yesterday.day:  # 入住日期必须是昨天
            continue
        score += int(night_num[0]) * int(room_num[0])
        order_num += 1
        print("晚数：", night_num[0], "间数：", room_num[0], "订单号：", order_id, "日期：", date)

    print("分数", score, "单数:", order_num)
    return score, order_num

def last_comment_date(commendList):
    last_comment = commendList[-1]
    date = re.findall(r'发表于 : <span>(\d+-\d+-\d+)', str(last_comment.getText))
    if not date:
        return None
    ret = datetime.datetime(*[int(n) for n in date[0].split('-')])
    print(ret)
    return ret


def need_next_page(last_date):
    if (last_date - yesterday).total_seconds() < 0:
        return False
    return True


def parse_comment(page):
    global yesterday
    soup = BeautifulSoup(page, 'lxml')
    commendList = soup.find_all(class_='cmt-item')
    last_date = last_comment_date(commendList)
    need_next = need_next_page(last_date)
    grades = []
    good_commend_num = 0 
    for commend in commendList:
        grade = commend.find_all(class_='mr5 txt26 ebk-c-Blue')
        date = re.findall(r'发表于 : <span>(\d+-\d+-\d+)', str(commend.getText))
        if not grade or not date:
            continue
        date = date[0]
        if int(date.split("-")[1]) != yesterday.month or int(date.split("-")[2]) != yesterday.day:
            continue
        grade = grade[0].text
        if float(grade) == 5.0:
            good_commend_num += 1
        grades.append(float(grade))
    print(grades, good_commend_num)
    return grades, good_commend_num, need_next
