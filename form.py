from wtforms import form
from wtforms import StringField

class MessageForm(form):
	name = StringField("姓名")
	email = StringField("邮箱")
	address = StringField("地址")
	message = StringField("留言")
