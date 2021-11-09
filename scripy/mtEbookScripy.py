import os
import requests
import datetime
import json
import re

def date_range(date):
	timestamp_start = date.timestamp()
	timestamp_end = (date + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)).timestamp()
	return (int(timestamp_start * 1000), int(timestamp_end * 1000))

def is_partime(start_time, end_time):
	if start_time.split()[0] == end_time.split()[0]:
		return True
	return False

def date_num(start_time, end_time):
	date_from = datetime.datetime(*[int(d) for d in  start_time.split()[0].split('-')])
	date_end = datetime.datetime(*[int(d) for d in  end_time.split()[0].split('-')])
	return (date_end - date_from).days


def format_time(url):
	url = re.sub(r'(startTime=\d+)&', 'startTime={startTime}', url)
	return re.sub(r'(endTime=\d+)&', 'endTime={endTime}', url)


class MtEbookScripy:
	def __init__(self, hotels):
		self.hotels = hotels
		self.record_path = "result.txt"
		self.create_record_file()
		self.logo = " [美团] "

	def create_record_file(self):
		if not os.path.exists(self.record_path):
			with open(self.record_path, "w", encoding="utf-8") as f:
				f.write("")

	def record_order_result(self, hotel_name, order_num, score, orderId_list):
		# orderId_list # 订单id列表用于调试可以输出
		report = "{logo} {date} {hotel_name} 订单数: {order_num} 分数：{score} \n"
		report = report.format(logo=self.logo, hotel_name=hotel_name, date=self.date_str, 
							   score=score, order_num=order_num)
		self.cache.insert(1.0, report)
		if not os.path.exists(self.record_path):
			self.create_record_file()

		with open(self.record_path, "a+", encoding="utf-8") as f:
			f.write(report.encode('utf-8').decode('utf-8'))

	def record_comment_result(self, hotel_name, good_num):
		report = "{logo} {date} {hotel_name} 好评数: {good_num} \n"
		report = report.format(logo=self.logo, hotel_name=hotel_name, 
						       date=self.date_str, good_num=good_num)
		self.cache.insert(1.0, report)
		if not os.path.exists(self.record_path):
			self.create_record_file()

		with open(self.record_path, "a+", encoding="utf-8") as f:
			f.write(report.encode('utf-8').decode('utf-8'))

	def mt_scripy(self, hotel, date):
		headers = {
			'cookie': hotel['cookie'],
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
		}
		self.get_order(date, hotel, headers)
		self.get_comment(date, hotel, headers)

	def get_order(self, date, hotel, headers):
		start_time, end_time = date_range(date)
		number = 0  # 美团ebook的分页按照 0 10 20 ...
		order_url = hotel['order_url']
		order_list = []
		while True:
			url = order_url.format(startTime=start_time, endTime=end_time, number=number)
			number += 20
			r = requests.get(url, headers=headers)
			print(r.text)
			data = r.json()['data']
			order_list += data['results']
			print(data['total'], number)
			if data['total'] < number:
				break

		order_num = 0
		score = 0
		orderId_list = []
		for order in order_list:
			if order['status'] != "CONSUMED" :
				continue
			if order['orderId'] in orderId_list:
				continue
			orderId_list.append(order['orderId'])
			if is_partime(order['checkInDateString'], order['checkOutDateString']):
				order_num += 1
				score += 0.5
			else:
				order_num += 1
				score += order['roomCount'] * date_num(order['checkInDateString'], order['checkOutDateString'])
		self.record_order_result(hotel['name'], order_num, score, orderId_list)

	def get_comment(self, date, hotel, headers):
		comment_url = hotel['comment_url']
		dianpin_url =  hotel['dianpin_url']
		r = requests.get(comment_url, headers=headers)
		comment_list = r.json()['data']['commentList']
		r = requests.get(dianpin_url, headers=headers)
		comment_list += r.json()['data']['commentList']
		good_num = 0
		for comment in comment_list:
			if comment['score'] == 50:
				print(comment, "<debug>")
		for comment in comment_list:
			if comment['commentTime'] / 1000 < date.timestamp() or \
			   comment['commentTime'] / 1000 > (date + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)).timestamp():
			   continue
			if comment['score'] == 50:
				good_num += 1
		# print("好评数：", good_num)s
		self.record_comment_result(hotel['name'], good_num)

	def run(self, date=None, cache=None, selected_hotel_names=[]):
		self.cache = cache
		self.date_str = date.strftime("%Y-%m-%d")
		for hotel in self.hotels:
			if hotel['name'] in selected_hotel_names:
				self.mt_scripy(hotel, date)
		self.cache.insert(1.0, "美团抓取 运行结束\n")

