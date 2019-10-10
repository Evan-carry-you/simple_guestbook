import os

from tornado import web
from tornado.web import URLSpec
from tornado.options import options, define
import tornado
import aiomysql

define('port', 8888, help="Run in this port", type=int)
options.parse_config_file("conf.cfg")
root = os.path.dirname(os.path.abspath(__file__))

class MainHandler(web.RequestHandler):
	def initialize(self, db):
		self.db = db


	async def get(self):
		id = ""
		name = ""
		email = ""
		address = ""
		message = ""

		pool = await aiomysql.create_pool(host=self.db['host'], port=3306,
																			user=self.db['user'], password=self.db['password'],
																			db=self.db['db_name'], charset="utf8")
		async with pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute("SELECT * from message;")
				try:
					(id, name, email, address, message) = await cur.fetchone()
				except Exception as e:
					pass
		pool.close()
		await pool.wait_closed()
		self.render("message.html", id=id, name=name, email=email, address=address, message=message )

	async def post(self):
		id = self.get_body_argument('id', '')
		name = self.get_body_argument('name', '')
		email = self.get_body_argument('email', '')
		address = self.get_body_argument('address', '')
		message = self.get_body_argument('message', '')
		pool = await aiomysql.create_pool(host=self.db['host'], port=3306,
		                                  user=self.db['user'], password=self.db['password'],
		                                  db=self.db['db_name'], charset="utf8")
		if id is '':
			async with pool.acquire() as conn:
				async with conn.cursor() as cur:
					await cur.execute("INSERT INTO message (name, email, address, message ) VALUES ('{}','{}','{}','{}')".format(name, email, address, message))
				await conn.commit()
			pool.close()
			await pool.wait_closed()
		else:
			async with pool.acquire() as conn:
				async with conn.cursor() as cur:
					await cur.execute("UPDATE message set name = '{}', email = '{}', address = '{}', message = '{}' where id = '{}'".format(name, email, address, message, id))
				await conn.commit()
			pool.close()
			await pool.wait_closed()


guestbook = {
	"db":{
		"db_name":"message",
		"user":"root",
		"host":"127.0.0.1",
		"password":""
	}
}

settings = {
	"debug":True,
	"static_path":os.path.join(root,"static"),
	"template_path":os.path.join(root, "templates"),
}
urls = [
	URLSpec('/', MainHandler,  guestbook, name="index")
]

if __name__ == "__main__":
	app = web.Application(urls, **settings)
	app.listen(options.port)
	tornado.ioloop.IOLoop.current().start()
