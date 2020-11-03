import os

import asyncio
import discord
from discord.ext import commands, tasks
import dateparser
import datetime
import psycopg2

class Reminder(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.dburl = os.environ['DATABASE_URL']

	def delete_item(self, msgid):
		conn = psycopg2.connect(self.dburl)
		cursor = conn.cursor()
		cursor.execute("DELETE FROM reminder WHERE message_id = %s;", (msgid,))
		self.closeconn(conn, cursor)
	
	async def add_n_refresh(self, ctx, time):
		msgid = ctx.message.id
		channelid = ctx.channel.id
		time = time.strftime("%Y-%m-%d %H:%M:%S")
		conn = psycopg2.connect(self.dburl)
		cursor = conn.cursor()
		cursor.execute("""INSERT INTO reminder (message_id, channel_id, time)
						VALUES (%s, %s, %s);""", (msgid, channelid, time))
		self.closeconn(conn, cursor)
		if not self.reminder_check.is_running():
			self.reminder_check.start()
			return
		self.reminder_check.cancel()
	
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
		date = dateparser.parse(f'{time} MYT', languages=['en'])
		if date is None:
			await ctx.send("Can't parse time")
			return
		await self.add_n_refresh(ctx, date)
		then = date.strftime("%H:%M %d-%m")
		await ctx.send(f"Reminding you on {then}")

	@tasks.loop(seconds=30)
	async def reminder_check(self):
		if self.time.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=8))) <= datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))):
			channel = self.bot.get_channel(self.channelid)
			message = await channel.fetch_message(self.msgid)
			await channel.send(f"{message.author.mention} Reminder: {message.jump_url}")
			self.delete_item(self.msgid)
			self.reminder_check.cancel()
	
	@reminder_check.after_loop
	async def next_item(self):
		conn = psycopg2.connect(self.dburl)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM reminder ORDER BY time;")
		thing = cursor.fetchone()
		if thing is not None:
			self.msgid, self.channelid, self.time = thing
			while self.reminder_check.is_running():
				await asyncio.sleep(5)
			self.reminder_check.start()
		self.closeconn(conn, cursor)
	
	@reminder_check.error
	async def error(self, error):
		pass

def setup(bot):
	bot.add_cog(Reminder(bot))
