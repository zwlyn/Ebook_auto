from tkinter import *
import hashlib
import threading
import json
import time
from scripy.xcEbookScripy import XcEbookScripy
from scripy.mtEbookScripy import MtEbookScripy
import datetime
import requests
import re

LOG_LINE_NUM = 0

def format_time(url):
    url = re.sub(r'startTime=\d+&', 'startTime={startTime}&', url)
    return re.sub(r'endTime=\d+&', 'endTime={endTime}&', url)

def format_mt_cookie(mt_cookies):
    for hotel in mt_cookies:
        hotel['order_url'] = hotel['order_url'].replace('offset=0', "offset={number}").replace('limit=10', "limit=20")
        hotel['order_url'] = format_time(hotel['order_url'])
        hotel['comment_url'] = re.sub(r'limit=\d+&', 'limit=100&', hotel['comment_url'])
        hotel['dianpin_url'] = re.sub(r'limit=\d+&', 'limit=100&', hotel['dianpin_url'])


class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
        self.load_cookies()
        print(self.mt_cookies)
        self.hotel_names = self.get_hotel_names()

    def load_cookies(self):
        with open("mt_cookie.json", "r", encoding="utf-8") as f:
            self.mt_cookies = json.load(f)
            format_mt_cookie(self.mt_cookies)

        with open("xc_cookie.json", "r", encoding="utf-8") as f:
            self.xc_cookies = json.load(f)

    def get_hotel_names(self):
        hotel_names = []
        for cookie in self.mt_cookies:
            hotel_names.append(cookie['name'])

        for cookie in self.xc_cookies:
            hotel_names.append(cookie['name'])
        return list(set(hotel_names))

    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("携程订单、评论抓取工具")           #窗口名
        self.init_window_name.geometry('1068x681+10+10')
                       #虚化，值越小虚化程度越高
        #标签
        self.init_data_label = Label(self.init_window_name, text="输入数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=12, column=0)

        #文本框
        self.hotel_select_frame = Frame(self.init_window_name, width=67, height=17)
        self.hotel_select_frame.grid(row=2, column=2, rowspan=5, columnspan=5)

        self.init_data_frame = Frame(self.init_window_name, width=67, height=17)  #原始数据录入框
        self.init_data_frame.grid(row=4, column=0, rowspan=5, columnspan=5)

        self.init_data_frame2 = Frame(self.init_window_name, width=67, height=17)
        self.init_data_frame2.grid(row=8, column=0, rowspan=5, columnspan=5)


        Label(self.hotel_select_frame, text="酒店选择").pack()
        self.hotel_var_map = {hotel_name: IntVar() for hotel_name in self.hotel_names}
        for hotel_name in self.hotel_names:
            self.hotel_var_map[hotel_name].set(1)
            bt = Checkbutton(self.hotel_select_frame, text=hotel_name, variable=self.hotel_var_map[hotel_name], \
                        onvalue=1, offvalue=0, height=2, width=20)
            bt.pack()
            

        Label(self.init_data_frame, text="日期选择").pack()
        self.date = StringVar()
        self.date.set("昨天") 
        Radiobutton(self.init_data_frame, text="昨天", variable=self.date, value="昨天").pack(anchor=W)
        Radiobutton(self.init_data_frame, text="前天", variable=self.date, value="前天").pack(anchor=W)

        Label(self.init_data_frame2, text="目标选择").pack()
        self.target = StringVar()
        self.target.set("携程") 
        Radiobutton(self.init_data_frame2, text="携程", variable=self.target, value="携程").pack(anchor=W)
        Radiobutton(self.init_data_frame2, text="美团", variable=self.target, value="美团").pack(anchor=W)
        Radiobutton(self.init_data_frame2, text="飞猪", variable=self.target, value="飞猪").pack(anchor=W)


        self.result_data_Text = Text(self.init_window_name, width=70, height=49)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        #按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="启动", bg="lightblue", width=10,command=self.start_scripy)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=1, column=11)


    def dateFromat(self, date_select: str) -> datetime.datetime:
        today = datetime.datetime.now()
        if date_select == "昨天":
            return datetime.datetime(today.year, today.month, today.day) - datetime.timedelta(days=1)
        elif date_select == "前天":
            return datetime.datetime(today.year, today.month, today.day) - datetime.timedelta(days=2)

    def test_network(self):
        try:
            r = requests.get("https://www.baidu.com", timeout=3)
            self.write_log_to_Text("INFO:网络连接测试成功")
            return True
        except Exception:
            self.write_log_to_Text("ERROR:网络连接测试失败")
            return False


    #功能函数
    def start_scripy(self):
        if not self.test_network():
            return None
        self.write_log_to_Text("INFO:启动成功")
        date = self.date.get()
        target = self.target.get()
        selected_hotel_names = [hotel_name for hotel_name in self.hotel_var_map if self.hotel_var_map[hotel_name].get()]
        if target == "携程":
            inputData = "输入数据：{date} {target} \n".format(date=self.date.get(), target=self.target.get())
            self.result_data_Text.insert(1.0, inputData)
            xcEbookScripy = XcEbookScripy(self.xc_cookies)
            threading.Thread(target=xcEbookScripy.run, args=(self.dateFromat(date), self.result_data_Text, selected_hotel_names)).start()

        elif target == "美团":
            inputData = "输入数据：{date} {target} \n".format(date=self.date.get(), target=self.target.get())
            self.result_data_Text.insert(1.0, inputData)
            mtEbookScripy = MtEbookScripy(self.mt_cookies)
            threading.Thread(target=mtEbookScripy.run, args=(self.dateFromat(date), self.result_data_Text, selected_hotel_names)).start()
        
        else: 
            self.write_log_to_Text("INFO:尚未制作，敬请期待")


   
    def get_current_time(self):
        """
        获取当前时间
        """
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time


    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


if __name__ == '__main__':
    gui_start()