import requests
import datetime
import json

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

hotels = {
"德清三店": {
	"cookie": "_lxsdk_cuid=173e0b49834c8-060a40b66c27e5-3323765-295d29-173e0b49835c8; _lxsdk=173e0b49834c8-060a40b66c27e5-3323765-295d29-173e0b49835c8; uuid=429f9d86e4343e66d5b2.1627351247.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; e_u_id_3299326472=49d9033674ec32820fdea3ef727d9a75; ebbsid=G1rAdBWKwYVQRaQIOpZPKmE35zqa5qbbnvcYtGKDWE2qH1m3YMmFo-Xsz8ER0Dt2xp1BUNkvbhctco_AUCn_Hg; _dxuserid=G1rAdBWKwYVQRaQIOpZPKmE35zqa5qbbnvcYtGKDWE2qH1m3YMmFo-Xsz8ER0Dt2xp1BUNkvbhctco_AUCn_Hg; logan_session_token=wtds6ycuovegu1clp8ff; _lxsdk_s=17af4f13c26-e8d-fe9-25f%7C%7C216",
	"order_url": 'https://eb.meituan.com/api/v1/ebooking/orders?_token=eJx1k8t2okAQht%252BFrT3aV2g8JwuIGlHxFoyJc7Lwgmi8kAFUTM68%252B1RLYsfFsOGrqq6un7%252BbTyPxFkaVYHgIMo5hYlQNUsZl00BGlkLFpJaJbZPbFubImF9zBAth2io3S55qRvU3EcxEFqWvKjOERJGRJn9FX0gBKUfqZcw8WGKssuw9rVYq4ay8C9fZYbovz%252BMdhJvKPN6nh11YiZNFmJRX2W4Lkv67Po43631UWU730Xn9a5qE08p6vwjzohHm7QI1jxAhEbM5bPWF7IImBiQa8RWlXSDRSG9RarQKZBq5RnGLZoGmRkujvEVRoH1FC2skGqlGppFrFBrNWywssdSIwhKJNRKNagRVhm4uhn4it1d7UfFUG2xz5I6CoNeFFgtLRBhGQQ0Ck0oEGrxufxSokHEkmQ45RyBWVwncnmsowEtCWbGRoBhJvZRQaiKCbT2WUAJzYfY1YxOK4BYjB1iCaQK2V2zZGPLswtBlIY7xD%252FlgpKDkSz4niEKrlqRukF0UuU2hKK9F9eGCi2KeuJwMeuw7alPJVB%252F%252BDi3MQAEv1IBKIQsGt5WaH19lghoq9YzvuOO49c5Fg4koVd1wIJk6EHUwPvzTUEzX0R4obJ3st7Tei96cwbBfagywDJ1G84Q9%252F7met%252FygN2i2t%252Bw%252BTyadLHuqH23xuG72J5noTz7GQbTw5HjSrKcm7i6sUamTe9HO8bMPctrimfTcJP6z9Ffzh85gMhF%252B%252B345cI%252BdmL6tLMeZltzxOX8%252BDF7Gz0zMSj7vpYtk%252FNIYhOz9MG01%252FaF7eMj9SSNdyJyPanb3sZ3jp9Oq17znnWG6Oc8tL1odj39YIuJdkLeW83Mf%252B8fU7VnbdnS6uzP%252B%252FgNHRi5w&endTime={endTime}&filter=ALL&invoiceMark=0&limit=20&memberMark=0&offset={number}&orderId=&orderStatus=&orderType=4,7&partnerId=&phone=&poiId=&roomIds=&searchTimeType=1&sortField=2&sortType=2&startTime={startTime}&zlPois=&_mtsi_eb_u=357110&_mtsi_eb_p=1362216&optimus_uuid=1362216&optimus_risk_level=71&optimus_code=10',
	"comment_url": "https://eb.meituan.com/api/v1/ebooking/comments/commentsInfo?_token=eJyV0ltPwjAUAOD%252F0lebrbf1QuLDxKGgjIgLGowPbExYsICwgcH43z2bWrNH%252B9Kv55xectIPtOvPUYcSGBSjQ75DHUQ94kmEUbmHjGRKUqWoYYphlP3FDBVGBgqjdDe5RJ0nGnCJhWDPdWQMge%252BIluIZ%252F5ABmcD1hNI%252BlKBlWW73Hd%252FPU8%252FmRVnN1l62sbBc%252BS95Pk9n2R%252B8ZWlf4Vn%252F3wPX2aS%252BjhmChTZwSCNDamnjpFuijRSINZIt8UaBk3DiTqwl0Yg6kZaCWso46ZZkI%252BUknQIn4cSdmBNt6ftk0pJw4nXLVnXLYJ651nFoVQhFlDCFqVH4sj%252BBpZYEM6IgBdXl764h%252FCRI7ovFGpQPjvEpim4Wp%252FBuXF2palDQ4v6KFCcbznh1sRkMWTQkR3%252FxYA7zlTkbhXGZH3sqmr6Nprp7vbKJGHfTmE8TEwc9sn27s2d8f987bEUU6yXNFnFmuybJXix9nydpkq9p9ZryDT%252BKm8jXNjKjx2WYFpPB7fAcfX4BpPi96A%253D%253D&limit=100&offset=0&partnerId=1362216&platform=1&poiId=2469484&prefetchIndex=1&replyType=0&reportStatus=&tag=&_mtsi_eb_u=357110&_mtsi_eb_p=1362216&optimus_uuid=1362216&optimus_risk_level=71&optimus_code=10",
	"dianpin_url": "https://eb.meituan.com/api/v1/ebooking/comments/commentsInfo?_token=eJyVklFv2jAQx7%252BLn61g3xk7QeoDG50USDoBgYlOfQCaAqUkjGQtadXv3jPQm%252Fq4SFF%252B%252Fp%252Ft38XymzjE96KjFT1aiuf8IDpCByqwQoq6oooFZ7VzOgIHUiw5Aw3WYmikWBymPdH5rdtopTFw55MRBecktOZOXhAIwUj%252FEYuYpoh1Xe%252BrTquVL4Jdvqn%252FzotgWe5ouG095Pn9Yr78B8G63j1RW%252F%252B%252FhnS7zOvQOIkKaZMzwYlCCRFcsk%252ByTG0mw4RMwKSZ1CdhxMQOZAeyA9mB7EB2IDuQHcgOYAewA9wXOv0vWKY2k2HCL2T8kW1PR%252FYmv%252F3szfx4fjnCUEYguzQXrJNamTPTTfCvZ3S%252BO33OIyUxjE6sFbWjIyd78ZSGoaVpylGJNq%252F95l6S0gWkYrVZFUR5%252F5g1VZG%252BjpvjTTYaNipKBsrUVTYdDtSqGlRPSfLQT6tsom4e0yZ9HGWDcN1ProskCcsf4%252Fy26G5%252BpVn6UmXjY6rj%252Ffg7xn%252BGTZlMyuumPyv29bbsdo%252Bz28nq6kq8fwAT7L%252F8&limit=100&offset=0&partnerId=1362216&platform=0&poiId=2469484&replyType=0&tag=&_mtsi_eb_u=357110&_mtsi_eb_p=1362216&optimus_uuid=1362216&optimus_risk_level=71&optimus_code=10"
	}
}

def mt_scripy(hotel_name, date):
	headers = {
		'cookie': hotels['德清三店']['cookie'],
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
	}
	get_order(date, hotel_name, headers)
	get_comment(date, hotel_name, headers)

def get_order(date, hotel_name, headers):
	start_time, end_time = date_range(date)
	number = 0  # 美团ebook的分页按照 0 10 20 ...
	order_url = hotels[hotel_name]['order_url']
	order_url = order_url.format(startTime=start_time, endTime=end_time, number=number)
	order_list = []
	while True:
		number += 20
		r = requests.get(order_url, headers=headers)
		# print(r.text)
		data = r.json()['data']
		# print(data['total'])
		order_list += data['results']
		if data['total'] < number:
			break

	order_num = 0
	score = 0
	for order in order_list:
		# print(order['checkInDateString'], "入住")
		# print(order['checkOutDateString'], "离店")
		if is_partime(order['checkInDateString'], order['checkOutDateString']):
			order_num += 0.5
			score += 0.5
		else:
			order_num += 1
			score += order['roomCount'] * date_num(order['checkInDateString'], order['checkOutDateString'])
	print("订单数：", order_num, "分数：", score)



# today = datetime.datetime.now()
def get_comment(date, hotel_name, headers):
	# date = datetime.datetime(2021, 7, 25)
	comment_url = hotels[hotel_name]['comment_url']
	dianpin_url =  hotels[hotel_name]['dianpin_url']
	r = requests.get(comment_url, headers=headers)
	# print(len(r.json()['data']['commentList']))
	# print(json.dumps(r.json()['data']['commentList'], indent=4, ensure_ascii=False))
	comment_list = r.json()['data']['commentList']
	r = requests.get(dianpin_url, headers=headers)
	comment_list += r.json()['data']['commentList']
	print(r.text)
	goods_num = 0
	for comment in comment_list:
		if comment['commentTime'] / 1000 < date.timestamp() or \
		   comment['commentTime'] / 1000 > (date + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)).timestamp():
		   continue
		if comment['score'] == 50:
			goods_num += 1
	print("好评数：", goods_num)
	# get_order(date)


mt_scripy('德清三店', datetime.datetime(2021, 7, 25))