import os
import json
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from bs4 import BeautifulSoup
from parse import parse_order, parse_comment
import datetime

with open("cookie_storage.json", "r", encoding="utf-8") as f:
	cookie_list = json.load(f)

class EbookScripy:
	def __init__(self):
		self.yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
		self.record_path = "result.txt"
		self.create_record_file()

	def create_driver(self):
		chrome_options = webdriver.ChromeOptions()
		# chrome_options.add_argument("--headless")
		chrome_options.add_experimental_option('useAutomationExtension',False)
		chrome_options.add_argument("disable-blink-features")
		chrome_options.add_argument("disable-blink-features=AutomationControlled")  
		self.driver = webdriver.Chrome(chrome_options =chrome_options)

	def create_record_file(self):
		if not os.path.exists(self.record_path):
			with open(self.record_path, "w", encoding="utf-8") as f:
				f.write("")

	def record_order_result(self, hotel_name, order_num, score):
		report = self.yesterday + " " + hotel_name + " 订单数：" + str(order_num) + " 分数：" + str(score) + "\n"
		if not os.path.exists(self.record_path):
			self.create_record_file()

		with open(self.record_path, "a+", encoding="utf-8") as f:
			f.write(report.encode('utf-8').decode('utf-8'))
		
	def delete_all_cookies(self):
		self.driver.delete_all_cookies()

	def login(self, cookie):
		self.create_driver()
		self.delete_all_cookies()
		self.driver.get('https://ebooking.ctrip.com/ebkfinance/settlement/homePage')
		for k, v in cookie.items():
			self.driver.add_cookie({'name': k, 'value': v, 'Domain': 'ebooking.ctrip.com'})
		self.driver.refresh()

	def scripy_order(self, hotel_name):
		time.sleep(0.5)
		self.driver.find_element_by_link_text('财务结算').click()
		time.sleep(1)
		self.driver.find_element_by_link_text('订单处理').click()
		time.sleep(1)
		self.driver.find_element_by_link_text('订单查询').click()
		time.sleep(1)
		self.driver.find_element_by_xpath("//button[@id='btnDateType']/em").click()
		time.sleep(0.5)
		self.driver.find_element_by_xpath("//div[@id='divDateType']/ul/li[3]").click()
		time.sleep(0.5)
		self.driver.find_element_by_xpath("//div[@id='divordersearchcontrol']/div[2]/button[2]").click()
		time.sleep(1)
		target_element = self.driver.find_element_by_xpath("//div[@id='orderListDiv']/div[3]/ul/li/div/div")
		time.sleep(0.5)
		js = """
		var element = document.getElementsByClassName('order-side ebk-scroll');
		var orderList = element.orderListDiv;
		orderList.scrollTo(0, orderList.scrollHeight);
		"""
		self.driver.execute_script(js)
		time.sleep(1)
		self.driver.execute_script(js)
		time.sleep(1)
		self.driver.execute_script(js)
		time.sleep(1)
		self.driver.execute_script(js)
		time.sleep(0.5)
		page = self.driver.page_source.encode('utf-8')
		score, order_num = parse_order(page)
		print(hotel_name, "分数：", score, "单数", order_num)
		self.record_order_result(hotel_name, order_num, score)

	def comment_page_worker(self, page):
		need_next = True
		page_num = 1
		while need_next:
			page_grades, page_good_comment_num, need_next = parse_comment(page)
			self.grades.extend(page_grades)
			self.good_comment_num += page_good_comment_num
			if need_next:
				page_num += 1
				self.driver.find_element_by_link_text(str(page_num)).click()
				time.sleep(5)
				page = self.driver.page_source.encode('utf-8') 

	def record_comment_result(self, hotel_name):
		report = self.yesterday + " " + hotel_name + " 点评：" + str(self.grades) + " 好评数：" + str(self.good_comment_num) + "\n"
		if not os.path.exists(self.record_path):
			self.create_record_file()

		with open(self.record_path, "a+", encoding="utf-8") as f:
			f.write(report.encode('utf-8').decode('utf-8'))


	def scripy_comment(self, hotel_name):
		time.sleep(0.5)
		self.driver.find_element_by_link_text('订单处理').click()
		time.sleep(1)
		self.driver.find_element_by_link_text('点评问答').click()
		time.sleep(1)
		self.driver.find_element_by_link_text('订单点评').click()
		time.sleep(1)
		self.grades = []
		self.good_comment_num = 0
		wc_page = self.driver.page_source.encode('utf-8')
		self.comment_page_worker(wc_page)
		time.sleep(1)

		self.driver.find_element_by_xpath("//span[contains(.,' 去哪儿')]").click()
		time.sleep(1)
		qne_page = self.driver.page_source.encode('utf-8')
		self.comment_page_worker(qne_page)
		time.sleep(1)

		self.driver.find_element_by_xpath("//span[contains(.,' 同程旅行')]").click()
		time.sleep(1)
		qne_page = self.driver.page_source.encode('utf-8')
		self.comment_page_worker(qne_page)
		time.sleep(1)

		self.record_comment_result(hotel_name)

	def close_dirver(self):
		self.driver.close()

	def run(self):
		for cookie in cookie_list:
			self.login(cookie['cookie'])
			self.scripy_order(cookie['name'])
			self.scripy_comment(cookie['name'])
			self.close_dirver()

ebookScripy = EbookScripy()
ebookScripy.run()




