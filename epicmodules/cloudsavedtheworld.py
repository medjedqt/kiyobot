import os
import requests
import shutil
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import discord
from discord.ext import commands
import tension
from helpy import hell

gauth = GoogleAuth()
gauth.LoadCredentialsFile("auth.json")
if gauth.access_token_expired:
	gauth.Refresh()
else:
	gauth.Authorize()
drive = GoogleDrive(gauth)

class Cloudshit(commands.Cog, name='Cloud Transfers'):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(aliases=['u','up'],help=hell['upload'])
	async def upload(self, ctx,title=None):

		try:
			attachment =ctx.message.attachments[0]
			fileurl=attachment.url
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

	@commands.command(aliases=['dl','down'], help=hell['download'])
	async def download(self, ctx,file):

		file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
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

	@commands.command(aliases=['ls'], help=hell['list'])
	async def list(self, ctx):

		e = discord.Embed(title='Cloud Files',color=0x00ffff)
		file_list = drive.ListFile({'q': "'root' in parents and trashed = false"}).GetList()
		for file1 in file_list:
			_, ext = os.path.splitext(file1['title'])
			next = tension.Ext(ext)
			e.add_field(name=file1['title'],value=next)
		await ctx.send(embed=e)

	@commands.command(help=hell['trash'])
	async def trash(self, ctx, filename):

		file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
		for file in file_list:
			title = file['title']
			name, _ = os.path.splitext(title)
			if filename in name:
				actual_file = drive.CreateFile({'id':file['id']})
				actual_file.Trash()
				await ctx.send(content='Binned {0}'.format(file['title']))