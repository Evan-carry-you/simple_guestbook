import asyncio

import aiomysql
import tornado.web
from tornado import ioloop

async def get_message():
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='root', password='',
                                      db='message', charset="utf8", autocommit=True)
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM message")
            result = await cur.fetchone()
            print(result)
    pool.close()
    await pool.wait_closed()

if __name__ == "__main__":
  # 使用 asyncio 的方式
  # loop = asyncio.get_event_loop()
  # loop.run_until_complete(get_message())

  # 使用 tornado 的 loop
  # 注意：这里如果将 current start 了，那么 loop 将开始循环，没有 run_sync 方法
  # 测试 branch 是否创建成功
  loop = tornado.ioloop.IOLoop.current()
  loop.run_sync(get_message)

