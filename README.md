# 携程、美团酒店商户后台自动化案例
## 携程、美团酒店商户后台自动化案例
##### 让酒店后台管理员再也不用为多家酒店、多个平台每天的订单和好评统计而烦恼。
##### 统计规则：昨天的入住订单总数和昨天的好评(5星)总数 (也可以自行修改规则)

### 实现的功能
#### 图形化形式呈现
![out](https://user-images.githubusercontent.com/31677476/128104868-ffcdda24-adbe-4f36-b613-d0fad1a06d93.PNG)

#### 携程的Ebook订单以及评论的自动化获取和统计
- 1.用selenium自动化登录携程Ebook后台（需要提供该酒店携程商户的账号密码信息， 需要辅助解决文字的验证码）；
- 2.在订单处理->订单查询界面获取入住的约60条订单的html -> 解析 -> 统计昨日入住的订单数量（Σ间数x天数）；
- 3.在点评问答->订单点评界面获取携程、去哪儿、同城旅行的昨天的评论，统计好评数量(默认5分为好评)；
- 4.支持多酒店自动化处理；
- 5.查询结果输出到result.txt文件；

#### 美团的Ebook订单以及评论的接口自动化获取和统计
- 1.设置酒店的美团Ebook的cookie、订单接口url、 评论和点评接口url
- 2.获取昨日或前日该酒店的订单、评论和点评
- 3.若美团cookie过期需要重新获取cookie信息（一般2星期后会过期， 采集完cookie后用清除浏览器记录的形式登出）

## 运行环境
+ python3
+ selenium
+ webdriver(已提供对应chrome版本为91.0.4472.164也可以自行下载其它版本对应即可)
+ BeautifulSoup

## 使用说明
 + 1.若使用携程，在xc_cookie.json中存储携程Ebook平台中酒店名称和商户的账号密码，详情见xc_cookie-exapmle.json;
 + 2.若使用美团，在mt_cookie.json中存储美团Ebook平台中酒店的名称、cookie值、订单地址、评论和点评地址（仅适合舒适型酒店后台）详情见mt_cookie-example.json;
 + 2.python main.py

## 注意点
- 请勿将该仓库的代码用于违法和商业用途仅用于学习和交流
