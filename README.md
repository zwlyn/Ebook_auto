# Ebook_auto
## 携程商户后台自动化统计数据的小型自动化解决方案
### 目前具有的功能
- 1.自动化登录Ebook后台（需要提供该酒店ebook的cookie信息）；
- 2.在订单处理->订单查询界面获取入住的约60条订单的html -> 解析 -> 统计昨日入住的订单数量（Σ间数x天数）；
- 3.在点评问答->订单点评界面获取携程、去哪儿、同城旅行的昨天的评论，统计好评数量(默认5分为好评)；
- 4.支持多酒店自动化处理；
- 5.查询结果输出到result.txt文件。

## 运行环境
+ python3
+ selenium
+ webdriver(已提供对应chrome版本为91.0.4472.164也可以自行下载其它版本对应即可)
+ BeautifulSoup

## 使用说明
 + 1.在cookie_storage.json中存储酒店名称和cookie值
 + 2.python scripy_main.py

## 注意点
- 获取Ebook后台的cookie时可在开发者工具中拷贝后使用format_cookie.py这个工具文件来将cookie进行格式化
- 请勿将该仓库的代码用于违法和商业用途仅用于学习和交流
