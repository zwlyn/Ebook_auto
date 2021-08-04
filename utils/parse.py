from bs4 import BeautifulSoup
import re
import datetime

def parse_order(page, date):
    """
    page是订单界面的html, byte格式
    """
    soup = BeautifulSoup(page, 'lxml')
    orderList = soup.find_all(class_='ordersSyn-list')[0]
    score = 0
    order_num = 0
    for order in orderList:
        # print(order, i, type(soup))
        night_num = re.findall(r'''<strong data-bind="text: LiveDays&gt;0\? LiveDays: '-'">(\d+)</strong>''', str(order))
        room_num = re.findall(r'''<strong data-bind=" text: Quantity">(\d+)</strong>''', str(order))
        order_id = re.findall(r'''<span data-bind="text: OrderID">(\d+)</span>''', str(order))
        order_date = re.findall(r'''<span data-bind="text: ArrivalAndDepartureDomestic">(\d+/\d+) - \d+/\d+</span>''', str(order))
        if not night_num or not room_num or not order_id or not order_date:
            continue
        if not ('已入住' in str(order) or '已接单' in str(order)) or "无效" in str(order):
            continue
        order_date = order_date[0]
        if int(order_date.split("/")[0]) != date.month or int(order_date.split("/")[1]) != date.day:  # 入住日期必须是昨天
            continue
        score += int(night_num[0]) * int(room_num[0])
        order_num += 1
        print("晚数：", night_num[0], "间数：", room_num[0], "订单号：", order_id, "日期：", order_date)

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


def need_next_page(last_date, date):
    if (last_date - date).total_seconds() < 0:
        return False
    return True


def parse_comment(page, date):
    # with open("comment.html", "rb") as f:
    #     page = f.read()
    soup = BeautifulSoup(page, 'lxml')
    commendList = soup.find_all(class_='cmt-item')
    last_date = last_comment_date(commendList)
    need_next = need_next_page(last_date, date)
    grades = []
    good_commend_num = 0 
    for commend in commendList:
        grade = commend.find_all(class_='mr5 txt26 ebk-c-Blue')
        order_date = re.findall(r'发表于 : <span>(\d+-\d+-\d+)', str(commend.getText))
        if not grade or not order_date:
            continue
        order_date = order_date[0]
        if int(order_date.split("-")[1]) != date.month or int(order_date.split("-")[2]) != date.day:
            continue
        grade = grade[0].text
        if float(grade) == 5.0:
            good_commend_num += 1
        grades.append(float(grade))
    print(grades, good_commend_num)
    return grades, good_commend_num, need_next
