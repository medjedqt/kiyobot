import os
import psycopg2
import requests
import shutil
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import discord
from discord.ext import commands
import tension

gauth = GoogleAuth()
gauth.LoadCredentialsFile("auth.json")
if gauth.access_token_expired:
	gauth.Refresh()
else:
	gauth.Authorize()
drive = GoogleDrive(gauth)

class Cloudshit(commands.Cog, name='Cloud Transfers'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.command(aliases=['u','up'])
	async def upload(self, ctx: commands.Context, title: str = None):
		'''Uploads file to a cloud server'''
		try:
			attachment =ctx.message.attachments[0]
			fileurl=attachment.url
			exname, ext = 'yes', '.ext'
			if fileurl.find('/'):
				name=fileurl.rsplit('/',1)[1]
				exname, ext = os.path.splitext(name)
			r=requests.get(fileurl,stream=True)
			if title is None:
				newname = exname+ext
			else:
				newname = title+ext
			if r.status_code==200:
				with open(newname,'wb') as f:
					r.raw.decode_content=True
					shutil.copyfileobj(r.raw,f)
		except:
			await ctx.send(content="Attach a file!")
			return
		file1 = drive.CreateFile()
		file1.SetContentFile(newname)
		file1.Upload()
		await ctx.send(content="Uploaded as {0}".format(newname))
		os.remove(newname)

	@commands.command(aliases=['dl','down'])
	async def download(self, ctx: commands.Context, file: str):
		'''Downloads file from cloud server'''
		file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
		file_notthere = True
		for file2 in file_list:
			title = file2['title']
			name, _ = os.path.splitext(title)
			file_notthere = True
			if file in name:
				file1 = drive.CreateFile({'id':file2['id']})
				file1.GetContentFile(title)
				await ctx.send(file=discord.File(title))
				os.remove(title)
				file_notthere = False
				break
		if file_notthere:
			await ctx.send("Can't find file :c")

	@commands.command(aliases=['ls'])
	async def list(self, ctx: commands.Context):
		'''Lists down every file on the cloud'''
		e = discord.Embed(title='Cloud Files',color=0x00ffff)
		file_list = drive.ListFile({'q': "'root' in parents and trashed = false"}).GetList()
		for file1 in file_list:
			_, ext = os.path.splitext(file1['title'])
			nexte = tension.Ext(ext)
			e.add_field(name=file1['title'],value=nexte)
		await ctx.send(embed=e)

	@commands.command()
	async def trash(self, ctx: commands.Context, filename: str):
		'''Dumps a cloud file to trash'''
		file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
		for file in file_list:
			title = file['title']
			name, _ = os.path.splitext(title)
			if filename == name:
				actual_file = drive.CreateFile({'id':file['id']})
				actual_file.Trash()
				await ctx.send(content='Binned {0}'.format(file['title']))

	def closer(self, conn):
		conn.commit()
		conn.close()

	@commands.group(invoke_without_command=True)
	async def tag(self, ctx: commands.Context, *, tagname: str):
		'''Gets tags from a database created with ?tag create'''
		if ctx.invoked_subcommand is not None:
			return
		conn = psycopg2.connect(os.environ['DATABASE_URL'])
		cur = conn.cursor()
		cur.execute("SELECT tag_content FROM tags WHERE tag_name = %s", (tagname,))
		result = cur.fetchone()
		if result is None:
			return await ctx.send(content="No tag found!")
		await ctx.send(content=result[0], allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))
		cur.close()
		self.closer(conn)

	@tag.command()
	async def create(self, ctx: commands.Context, tagname: str = None, *, content: str = None):
		'''Creates tags'''
		conn = psycopg2.connect(os.environ['DATABASE_URL'])
		cur = conn.cursor()
		cur.execute(
"""
INSERT INTO tags(tag_name, tag_author, tag_content)
VALUES(%s, %s, %s)
""", (tagname, ctx.author.id, content)
		)
		cur.close()
		self.closer(conn)
		await ctx.send(content=f"Tag saved as '{tagname}'", allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))

	@tag.command()
	async def delete(self, ctx: commands.Context, tagname):
		'''Deletes tags'''
		conn = psycopg2.connect(os.environ['DATABASE_URL'])
		cur = conn.cursor()
		cur.execute("""SELECT tag_author FROM tags WHERE tag_name = %s""", (tagname,))
		if cur.fetchone()[0] != ctx.author and ctx.author.id != 550076298937237544 and not ctx.author.guild_permissions.manage_messages:
			cur.close()
			self.closer(conn)
			return await ctx.send(content="Not your tag!")
		await ctx.send(content=f"Type the tag name to confirm deletion (`{tagname}`)\n (Send other messages to cancel)")
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
	
	@tag.command(aliases=['find'])
	async def search(self, ctx: commands.Context, *, tagname: str):
		'''Finds tags'''
		conn = psycopg2.connect(os.environ['DATABASE_URL'])
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
				await ctx.send(content=tagn, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))

	@tag.command()
	async def author(self, ctx: commands.Context, *, tagname: str):
		'''fetch the author of a tag'''
		conn = psycopg2.connect(os.environ['DATABASE_URL'])
		cur = conn.cursor()
		cur.execute("SELECT tag_author FROM tags WHERE tag_name = %s", (tagname,))
		res = cur.fetchone()[0]
		cur.close()
		self.closer(conn)
		if res is None:
			await ctx.send(content=f"No tag named {tagname} found")
		else:
			author: discord.User = self.bot.get_user(int(res))
			await ctx.send(content=f"tag was created by {author}")

def setup(bot: commands.Bot):
	bot.add_cog(Cloudshit(bot))