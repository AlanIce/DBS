import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header

class EmailSender(object):
	def __init__(self, username=None, password=None):
		if username is None or password is None:
			raise RuntimeError('emailSender 初始化失败')
		self.password = password
		self.username = username

	def makeRoot(self, mailto, subject):
		self.mailto = mailto
		self.msgRoot = MIMEMultipart('related')	
		self.msgRoot['From'] = '<%s>' %self.username
		self.msgRoot['To']   = '<%s>' %mailto
		self.msgRoot['Subject'] = Header(subject, 'utf-8')

	def addPlainText(self, content):
		msgText = MIMEText(content, 'plain', 'utf-8')
		self.msgRoot.attach(msgText)

	def addTextAndImage(self, content, imageList):
		msgAlternative = MIMEMultipart('alternative')
		self.msgRoot.attach(msgAlternative)
		msgBody = MIMEText(content, 'html', 'utf-8')
		msgAlternative.attach(msgBody)
		index = 1
		for image in imageList:
			msgImage = MIMEImage(image)
			msgImage["Content-Type"] = 'image/jpeg'
			msgImage["Content-Disposition"] = 'inline; filename="picture%s.jpg"' %index
			msgImage.add_header('Content-ID', '<image%s>' %index)
			msgAlternative.attach(msgImage)
			index += 1


	def addAttachment(self, fileList):
		for singlefile in fileList:
			att = MIMEText(singlefile, 'base64', 'utf-8')
			att["Content-Type"] = 'application/octet-stream'
			att["Content-Disposition"] = 'attachment; filename="%s"' %singlefile
			self.msgRoot.attach(att)

	def sendmail(self):
		try:
			smtp = smtplib.SMTP('smtp.163.com')
			smtp.login(self.username, self.password)
			smtp.sendmail(self.username, self.mailto, self.msgRoot.as_string())
			smtp.quit()
			print('邮件发送成功！')
		except Exception as e:
			print(e)
			print('邮件发送失败！')

def main():
	emailsender = EmailSender('zwj_ice@163.com', 'mail00')	
	emailsender.makeRoot('2198928117@qq.com', 'DBS验证码')
	content = '''
	<p>DBS启动验证码：</p>
	<p><img src="cid:image1"></p>
	'''
	imageList = []
	with open('3.jpg', 'rb') as file:
		imageList.append(file.read())
	emailsender.addTextAndImage(content, imageList)
	emailsender.sendmail()

if __name__ == '__main__':
	main()

