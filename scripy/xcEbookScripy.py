import os
import json
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from bs4 import BeautifulSoup
from utils.parse import parse_order, parse_comment
from utils import move_to_gap, get_track
import datetime
from selenium.webdriver.common.action_chains import ActionChains


class XcEbookScripy:
	def __init__(self, cookies):
		self.cookies = cookies
		self.date_str = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
		self.record_path = "result.txt"
		self.create_record_file()
		self.logo = " [携程] "

	def create_driver(self):
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_experimental_option('useAutomationExtension',False)
		chrome_options.add_argument("disable-blink-features")
		chrome_options.add_argument("disable-blink-features=AutomationControlled")  
		self.driver = webdriver.Chrome(chrome_options =chrome_options)

	def create_record_file(self):
		if not os.path.exists(self.record_path):
			with open(self.record_path, "w", encoding="utf-8") as f:
				f.write("")

	def record_order_result(self, hotel_name, order_num, score):
		report = self.logo + self.date_str + " " + hotel_name + " 订单数：" + str(order_num) + " 分数：" + str(score) + "\n"
		self.cache.insert(1.0, report)
		if not os.path.exists(self.record_path):
			self.create_record_file()

		with open(self.record_path, "a+", encoding="utf-8") as f:
			f.write(report.encode('utf-8').decode('utf-8'))
		
	def delete_all_cookies(self):
		self.driver.delete_all_cookies()

	def login(self, username, password):
		self.create_driver()
		self.delete_all_cookies()
		self.driver.maximize_window()
		self.driver.get("https://ebooking.ctrip.com/ebkovsassembly/Login")
		username_element = self.driver.find_element_by_id("loginName")
		username_element.clear()
		username_element.send_keys(username);
		time.sleep(0.5)
		password_element = self.driver.find_element_by_id("password")
		password_element.clear()
		password_element.send_keys(password);
		time.sleep(0.5)
		self.driver.find_element_by_xpath("//button[contains(.,'登录')]").click()
		time.sleep(1)
		self.cross_check()
		self.wait_when_word()

	def wait_when_word(self):
		try:
			print("有文字校验")
			while True:
				self.driver.find_element_by_xpath("//div[@id='verification-code-choose']/div[2]/div")
				time.sleep(1)

		except Exception as e:
			print(e, "没有文字校验")

	def cross_check(self):
		try:
			check_element = self.driver.find_element_by_xpath("//div[@id='verification-code']/div/div[2]/div/i")
			move_to_gap(self.driver, check_element, get_track(1000))
		except Exception as e:
			print(e)

	def refresh_cookie(self, name):
		time.sleep(2)
		cookie_json=self.driver.get_cookies()
		def format_cookie(cookies):
			result = {}
			for item in cookies:
				result[item['name']] = item['value']
			return result

		new_cookie = format_cookie(cookie_json)
		print(new_cookie, '------1')
		for cookie in self.cookies:
			if cookie['name'] == name:
				print(cookie['cookie'], '------2')
				cookie['cookie'] = new_cookie
				break

		with open("xc_cookie.json", 'w', encoding='utf-8') as f:
			f.write(json.dumps(self.cookies, indent=4, ensure_ascii=False))

	def scripy_order(self, hotel_name, date):
		while True:
			try:
				time.sleep(0.5)
				self.driver.find_element_by_link_text('财务结算').click()
				break
			except Exception:
				self.driver.find_element_by_xpath("/html/body").click() # 鼠标左键点击， 200为x坐标， 100为y坐标
				time.sleep(1)
		
		time.sleep(1)
		self.driver.find_element_by_link_text('订单处理').click()
		time.sleep(1)
		self.driver.find_element_by_link_text('订单查询').click()
		time.sleep(1)
		self.driver.find_element_by_xpath("//span[contains(.,'过去7天')]").click()
		time.sleep(2)
		target_element = self.driver.find_element_by_xpath("//div[@id='orderListDiv']")
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
		score, order_num = parse_order(page, date)
		print(hotel_name, "分数：", score, "单数", order_num)
		self.record_order_result(hotel_name, order_num, score)

	def comment_page_worker(self, page, date):
		need_next = True
		page_num = 1
		while need_next:
			page_grades, page_good_comment_num, need_next = parse_comment(page, date)
			self.grades.extend(page_grades)
			self.good_comment_num += page_good_comment_num
			if need_next:
				page_num += 1
				self.driver.find_element_by_link_text(str(page_num)).click()
				time.sleep(5)
				page = self.driver.page_source.encode('utf-8') 

	def record_comment_result(self, hotel_name):
		report = self.logo + self.date_str + " " + hotel_name + " 点评：" + str(self.grades) + " 好评数：" + str(self.good_comment_num) + "\n"
		self.cache.insert(1.0, report)
		if not os.path.exists(self.record_path):
			self.create_record_file()

		with open(self.record_path, "a+", encoding="utf-8") as f:
			f.write(report.encode('utf-8').decode('utf-8'))


	def scripy_comment(self, hotel_name, date):
		time.sleep(0.5)
		self.driver.find_element_by_link_text('订单处理').click()
		time.sleep(1)
		self.driver.find_element_by_link_text('点评问答').click()
		time.sleep(1)
		self.driver.find_element_by_link_text('订单点评').click()
		time.sleep(2)
		self.grades = []
		self.good_comment_num = 0
		wc_page = self.driver.page_source.encode('utf-8')
		self.comment_page_worker(wc_page, date)
		time.sleep(1)

		self.driver.find_element_by_xpath("//span[contains(.,' 去哪儿')]").click()
		time.sleep(1)
		qne_page = self.driver.page_source.encode('utf-8')
		self.comment_page_worker(qne_page, date)
		time.sleep(1)

		self.driver.find_element_by_xpath("//span[contains(.,' 同程旅行')]").click()
		time.sleep(1)
		qne_page = self.driver.page_source.encode('utf-8')
		self.comment_page_worker(qne_page, date)
		time.sleep(1)

		self.record_comment_result(hotel_name)

	def close_dirver(self):
		self.driver.close()
		self.driver.quit()

	def yesterday_date(self) -> datetime.datetime:
		today = datetime.datetime.now()
		return datetime.datetime(today.year, today.month, today.day) - datetime.timedelta(days=1)

	def run(self, date=None, cache=None, selected_hotel_names=[]):
		self.cache = cache
		if date:
			self.date_str = date.strftime("%Y-%m-%d")
		if not date:
			date = self.yesterday_date()
		for cookie in self.cookies:
			if cookie['name'] in selected_hotel_names:
				self.login(cookie['username'], cookie['password'])
				self.scripy_order(cookie['name'], date)
				self.scripy_comment(cookie['name'], date)
				self.close_dirver()

		self.cache.insert(1.0, "携程抓取 运行结束\n")

if __name__ == '__main__':
	ebookScripy = EbookScripy()
	ebookScripy.run()




