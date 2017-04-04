import requests, re, random, string, time, logging

from PIL import Image

from .EmailSender import *
from .config import email_config, douban_config

class Opener(object):
	def __init__(self):		
		self.emailsender = EmailSender(**email_config)
		self.pause = False
		# define user_agents, include useragent_pc, useragent_phone and useragent_all
		self.CONFIG_USERAGENT_PC = [
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0)",

			"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Maxthon 2.0)",
			"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; TencentTraveler 4.0)",
			"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; The World)",
			"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; 360SE)",
			"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Avant Browser)",
			"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",

			"Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; Maxthon 2.0)",
			"Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; TencentTraveler 4.0)",
			"Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; The World)",
			"Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; 360SE)",
			"Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; Avant Browser)",
			"Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/4.0)",

			"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
			"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
			"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
			"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
			"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
			"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0)",

			"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Maxthon 2.0)",
			"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; TencentTraveler 4.0)",
			"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; The World)",
			"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; 360SE)",
			"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Avant Browser)",
			"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",

			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Maxthon 2.0)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; TencentTraveler 4.0)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; The World)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; 360SE)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Avant Browser)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/4.0)",

			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0 Safari/535.11",

			"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
			"Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
			"Mozilla/5.0 (Windows NT 5.1) Gecko/20100101 Firefox/14.0 Opera/12.0",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; de) Opera 11.51",
			"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0 Safari/537.36",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
			"Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko QQBrowser/8.1.3886.400",
			"Mozilla/5.0 (MSIE 9.0; Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko QQBrowser/8.2.3638.400",
			"Mozilla/5.0 (MSIE 9.0; Windows NT 6.0; Trident/7.0; rv:11.0) like Gecko QQBrowser/8.3.4765.400",
			"Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko QQBrowser/9.1.3471.400",
			"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; 2345Explorer 3.4.0.12519)",
			"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; 2345Explorer 3.5.0.12758)",
			"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; 2345Explorer 4.0.0.13120)",
			"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; 2345Explorer 4.2.0.13550)",
			"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; 2345Explorer 5.0.0.14004)",
			"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; 2345Explorer/6.1.0.8158)",
			"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; 2345Explorer/6.2.0.9202)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; UBrowser/5.0.1369.26)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; UBrowser/5.2.2603.1)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; UBrowser/5.4.4237.43)",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:34.0) Gecko/20100101 Firefox/34.0",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:36.0) Gecko/20100101 Firefox/36.0",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:37.0) Gecko/20100101 Firefox/37.0",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:38.0) Gecko/20100101 Firefox/38.0",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:39.0) Gecko/20100101 Firefox/39.0",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:41.0) Gecko/20100101 Firefox/41.0",

			"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/2.1.7.6 Safari/537.36",
			"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
			"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.11 YYE/3.6 Safari/537.36",
			"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
			"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36",
			"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
			"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
			"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36",
			"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36",
			"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36",
			"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.46 Safari/537.36",
			"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2478.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2498.0 Safari/537.36",

			"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
			"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
			"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
			"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
			"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
			"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
			"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",

			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",

			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36",
			"Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",

			"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
			"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
			"Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
			"Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
			"Opera/9.80 (Windows NT 6.1; WOW64; U; pt) Presto/2.10.229 Version/11.62",
			"Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.10.229 Version/11.62",
			"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
			"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52",
			"Opera/9.80 (Windows NT 5.1; U; en) Presto/2.9.168 Version/11.51",
			"Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
			"Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
			"Opera/12.0 (Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00",
			"Opera/12.0 (Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00",
			"Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",

			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
			"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
			"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
		]
		# self.proxies = {'http':'139.196.105.154:9000', 'https':'139.196.105.154:9000'}
		self.proxies = None
		self.visit_count = 0
		self.session = requests.Session()
		self.headers = {
			'Host':'movie.douban.com',
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
			'Connection':'keep-alive',
			'Referer':'https://movie.douban.com',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
		}
		login_headers = {
			'Host':'accounts.douban.com',
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
			'Connection':'keep-alive',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
		}
		login_data = {
			'source':'None',
			'redir':'https://www.douban.com',
			'form_email':'517086085@qq.com',
			'form_password':'3160274z',
			'remember':'on',
			'login':'登录'
		}

		login_url = 'https://accounts.douban.com/login'
		resp = self.session.get(login_url, proxies=self.proxies)
		tempCookies = resp.cookies

		match_obj = re.search(r'https://www.douban.com/misc/captcha\?id=(.*:en)', resp.content.decode())
		if match_obj:
			captcha_url = match_obj.group(0)
			login_data['captcha-id'] = match_obj.group(1)
			with open('./Spider/Log/captcha.jpg', 'wb') as file:
				file.write(requests.get(captcha_url).content)
			if False:
				Image.open('./Spider/Log/captcha.jpg').show()
			else:
				emailsender.makeRoot('2198928117@qq.com', 'DBS验证码')
				with open('./Spider/Log/captcha.jpg', 'rb') as file:
					image = file.read()
				emailsender.addPlainText('DBS的验证码，请查收')
				emailsender.addAttachment((image,))
				emailsender.sendmail()
			login_data['captcha-solution'] = input('请输入验证码：')
		resp = self.session.post(login_url, headers=login_headers, data=login_data, proxies=self.proxies)
		if resp.url != 'https://www.douban.com':
			raise Exception('初始化失败！')

	def update_session(self):
		self.visit_count = 0
		self.headers['User-Agent'] = random.choice(self.CONFIG_USERAGENT_PC)
		self.session.cookies.update({'bid':"".join(random.sample(string.ascii_letters + string.digits, 11))})

	def openPage(self, url, load=False, filename='./Log/index.html'):
		while self.pause:
			time.sleep(5)
		self.visit_count += 1
		if self.visit_count >= 30:
			self.update_session()
		resp = self.session.get(url, headers=self.headers, proxies=self.proxies, allow_redirects=False)
		if resp.status_code in (301, 302, 403):
			print('Error Raise, status_code', resp.status_code)
			self.pause = True			
			print('Opener is pausing, need to restart!')
		if load:
			with open(filename, 'wb') as file:
				file.write(resp.content)
		return resp.content

		

if __name__ == '__main__':
	url = 'http://www.douban.com'