import os

import discord
from discord.ext import commands, tasks
import dateparser
import datetime
import psycopg2

class Reminder(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.dburl = os.environ['DATABASE_URL']

	@reminder_check.after_loop
	async def next_item(self):
		self.reminder_check.cancel()
		conn = psycopg2.connect(self.dburl)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM reminder ORDER BY time;")
		thing = cursor.fetchone()
		if thing is not None:
			self.msgid, self.channelid, self.time = thing
			self.reminder_check.start()
		self.closeconn(conn, cursor)

	def delete_item(self, msgid):
		conn = psycopg2.connect(self.dburl)
		cursor = conn.cursor()
		cursor.execute("DELETE FROM reminder WHERE message_id = %s;", (msgid,))
		self.closeconn(conn, cursor)
	
	async def add_n_refresh(self, ctx, time):
		self.reminder_check.cancel()
		msgid = ctx.message.id
		channelid = ctx.channel.id
		time = time.strftime("%Y-%m-%d %H:%M:%S")
		conn = psycopg2.connect(self.dburl)
		cursor = conn.cursor()
		cursor.execute("""INSERT INTO reminder (message_id, channel_id, time)
						VALUES (%s, %s, %s);""", (msgid, channelid, time))
		self.closeconn(conn, cursor)
		await self.next_item()
	
	def closeconn(self, conn, cursor):
		cursor.close()
		conn.commit()
		conn.close()
	
	@commands.command()
	async def initremind(self, ctx):
		if ctx.author.id != 550076298937237544:
			return
		await self.next_item()

	@commands.command()
	async def remind(self, ctx, *, time):
		if ctx.author.id != 550076298937237544:
			return
		date = dateparser.parse(f'{time} UTC+8', languages=['en'])
		if date is None:
			await ctx.send("Can't parse time")
			return
		self.add_n_refresh(ctx, date)
		delta = date - datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
		await ctx.send(f"Reminding you in {str(delta)}")

	@tasks.loop(seconds=30)
	async def reminder_check(self):
		if self.time.astimezone(tz=datetime.timezone(datetime.timedelta(hours=8))) <= datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))):
			channel = self.bot.get_channel(self.channelid)
			message = await channel.fetch_message(self.msgid)
			await channel.send(f"Reminder: {message.jump_url}")
			self.delete_item(self.msgid)
			self.reminder_check.cancel()

def setup(bot):
	bot.add_cog(Reminder(bot))