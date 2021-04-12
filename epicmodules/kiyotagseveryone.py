import os
import psycopg2
import discord
from discord.ext import commands
from discord.utils import escape_markdown

class Tagshit(commands.Cog, name='Tag System'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.db_url = os.environ['DATABASE_URL']

	def closer(self, conn):
		conn.commit()
		conn.close()

	@commands.guild_only()
	@commands.group(invoke_without_command=True)
	async def tag(self, ctx: commands.Context, *, tagname: str):
		'''Gets tags from a database created with ?tag create'''
		if ctx.invoked_subcommand is not None:
			return
		conn = psycopg2.connect(self.db_url)
		cur = conn.cursor()
		cur.execute("SELECT tag_content FROM tags WHERE tag_name = %s", (tagname,))
		result = cur.fetchone()
		if result is None:
			return await ctx.send(content="No tag found!")
		await ctx.send(content=result[0])
		cur.close()
		self.closer(conn)

	@commands.guild_only()
	@tag.command()
	async def create(self, ctx: commands.Context, tagname: str = None, *, content: str = None):
		'''Creates tags'''
		conn = psycopg2.connect(self.db_url)
		cur = conn.cursor()
		cur.execute("SELECT tag_name FROM tags WHERE tag_name = %s",
					(tagname,))
		if cur.fetchone() is not None:
			cur.close()
			self.closer(conn)
			return await ctx.send(content=f"tag `{escape_markdown(tagname)}` already exists")
		cur.execute(
"""
INSERT INTO tags(tag_name, tag_author, tag_content)
VALUES(%s, %s, %s)
""", (tagname, ctx.author.id, content)
		)
		cur.close()
		self.closer(conn)
		await ctx.send(content=f"Tag saved as `{escape_markdown(tagname)}`")

	@commands.guild_only()
	@tag.command()
	async def delete(self, ctx: commands.Context, *, tagname: str):
		'''Deletes tags'''
		conn = psycopg2.connect(self.db_url)
		cur = conn.cursor()
		cur.execute("""SELECT tag_author FROM tags WHERE tag_name = %s""", (tagname,))
		if cur.fetchone()[0] != ctx.author and ctx.author.id != 550076298937237544 and not ctx.author.guild_permissions.manage_messages:
			cur.close()
			self.closer(conn)
			return await ctx.send(content="Not your tag!")
		await ctx.send(content=f"Type the tag name to confirm deletion (`{escape_markdown(tagname)}`)\n (Send other messages to cancel)")
		def check(m: discord.Message):
			return m.author == ctx.author and m.channel == ctx.channel
		msg: discord.Message = await self.bot.wait_for('message', check=check)
		if msg.content != tagname:
			cur.close()
			self.closer(conn)
			return await ctx.send(content="Tag deletion cancelled")
		cur.close()
		cur = conn.cursor()
		cur.execute("DELETE FROM tags WHERE tag_name = %s", (tagname,))
		cur.close()
		self.closer(conn)
		await ctx.send(content=f"Tag '{tagname}' deleted")

	@commands.guild_only()
	@tag.command(aliases=['find'])
	async def search(self, ctx: commands.Context, *, tagname: str):
		'''Finds tags'''
		conn = psycopg2.connect(self.db_url)
		cur = conn.cursor()
		cur.execute("SELECT tag_name FROM tags WHERE tag_name LIKE %s", (f'%{tagname}%',))
		res = cur.fetchall()
		res = [_[0] for _ in res]
		cur.close()
		self.closer(conn)
		if res == []:
			await ctx.send(content="No tags found")
		else:
			await ctx.send(content="Tags found:")
			for ind, tagn in enumerate(res):
				if ind == 5:
					return
				await ctx.send(content=tagn)

	@commands.guild_only()
	@tag.command()
	async def author(self, ctx: commands.Context, *, tagname: str):
		'''fetch the author of a tag'''
		conn = psycopg2.connect(self.db_url)
		cur = conn.cursor()
		cur.execute("SELECT tag_author FROM tags WHERE tag_name = %s", (tagname,))
		res = cur.fetchone()[0]
		cur.close()
		self.closer(conn)
		if res is None:
			await ctx.send(content=f"No tag named {tagname} found")
		else:
			author: discord.User = self.bot.get_user(int(res))
			await ctx.send(content=f"tag `{escape_markdown(tagname)}` was created by {author}")
	
	@commands.guild_only()
	@tag.command()
	async def edit(self, ctx: commands.Context, tagname: str, *, tagcontent: str):
		'''edits a tag'''
		conn = psycopg2.connect(self.db_url)
		cur = conn.cursor()
		cur.execute("SELECT tag_content FROM tags WHERE tag_name = %s AND tag_author = %s",
					(tagname, str(ctx.author.id)))
		them = cur.fetchone()
		if them is None:
			cur.close()
			self.closer(conn)
			return await ctx.send(content=f"You have no tag named `{tagname}`")
		cur.execute("UPDATE tags SET tag_content = %s WHERE tag_name = %s",
					(tagcontent, tagname))
		cur.close()
		self.closer(conn)
		await ctx.message.add_reaction('👍')

def setup(bot: commands.Bot):
	bot.add_cog(Tagshit(bot))