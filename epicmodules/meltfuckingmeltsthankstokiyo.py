import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

class MeltIDConverter(commands.Converter):
	async def convert(self, ctx: commands.Context, argument):
		try:
			argument = await commands.MessageConverter().convert(ctx, argument)
		except (commands.MessageNotFound, commands.ChannelNotFound, commands.ChannelNotReadable):
			pass
		if isinstance(argument, discord.Message):
			argument = argument.content
		if len(argument) == 4:
			return argument
		if argument.startswith('MS#'):
			return argument[3:]
		if 'MS#' in argument:
			return argument.split('MS#')[1][:4]
		try:
			intargument = int(argument)
			argument = str(intargument).zfill(4)
			return await self.convert(ctx, argument)
		except ValueError:
			pass
		raise commands.CommandError(message=f'{type(argument).__name__} object is not convertable')

class MeltyScans(commands.Cog, name='Melty Scans'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.queuechan = bot.queuechan

	@commands.is_owner()
	@commands.command()
	async def queue(self, ctx: commands.Context, nhlink: str, raws: str = 'None', doclink: str = 'None', entitle: str = 'None', *en2: str):

		if en2 is None:
			pass
		else:
			en2 = ' '.join(en2)
			entitle = ' '.join((entitle,en2))
		if nhlink.startswith('https://nh'):
			pass
		else:
			try:
				nhcode = int(nhlink)
			except ValueError:
				await ctx.send(content='Error: Check your input')
				return
			nhlink = f'https://nhentai.net/g/{nhcode}'
		queuechannel = self.bot.get_channel(self.queuechan)
		pastqueue = await queuechannel.history(limit=1).flatten()
		prevmessage = pastqueue[0]
		if 'MS#' not in prevmessage.content:
			queuetag = '0001'
		else:
			queuetag = int(prevmessage.content[3:7]) + 1
			queuetag = f'{queuetag:04d}'
		firstpage = requests.get(nhlink)
		soup = BeautifulSoup(firstpage.text, 'html.parser')
		nhimg = requests.get(f'{nhlink}/1')
		imgsoup = BeautifulSoup(nhimg.text, 'html.parser')
		nhimglink = imgsoup.find('section', id='image-container').a.img['src']
		imgresp = requests.get(nhimglink)
		f = open("nhimage.jpg", "wb")
		f.write(imgresp.content)
		f.close()
		orititle = soup.find(id='info').h1.get_text()
		text = f'''MS#{queuetag} **{orititle}** --> {entitle}
NH link: <{nhlink}>
raw source: <{raws}>
TL link: <{doclink}>'''
		await queuechannel.send(content=text, file=discord.File('nhimage.jpg'))
		await ctx.send(f'Queued as MS#{queuetag}')

	@commands.is_owner()
	@commands.command()
	async def raw(self, ctx: commands.Context, id_: MeltIDConverter, url: str):

		messages = await self.bot.get_channel(self.queuechan).history().flatten()
		for message in messages:
			if f'MS#{id_}' in message.content:
				oldcontent = message.content.split('\n')
				for line in oldcontent:
					if 'raw source:' in line:
						newcontent = message.content.replace(line, f'raw source: <{url}>')
						await message.edit(content=newcontent)
				await ctx.message.delete()
				resp = await ctx.send(content=f'Added raw to MS#{id_}')
				await resp.delete(delay=5)

	@commands.is_owner()
	@commands.command()
	async def doc(self, ctx: commands.Context, id_: MeltIDConverter, url: str):

		messages = await self.bot.get_channel(self.queuechan).history().flatten()
		for message in messages:
			if f'MS#{id_}' in message.content:
				oldcontent = message.content.split('\n')
				for line in oldcontent:
					if 'TL link' in line:
						newcontent = message.content.replace(line, f'TL link: <{url}>')
						await message.edit(content=newcontent)
				await ctx.message.delete()
				resp = await ctx.send(content=f'Added doc to MS#{id_}')
				await resp.delete(delay=5)

	@commands.is_owner()
	@commands.command()
	async def title(self, ctx: commands.Context, id_: MeltIDConverter, *, title: str):

		messages = await self.bot.get_channel(self.queuechan).history().flatten()
		for message in messages:
			if f'MS#{id_}' in message.content:
				oldcontent = message.content.split('\n')[0]
				oldline = oldcontent.split(' --> ')
				newline = oldline[0] + ' --> ' + title
				newcontent = message.content.replace(oldcontent, newline)
				await message.edit(content=newcontent)
				await ctx.message.delete()
				resp = await ctx.send(content=f'Added title to MS#{id_}')
				await resp.delete(delay=5)
	
	@commands.is_owner()
	@commands.command()
	async def cancel(self, ctx: commands.Context, id_: MeltIDConverter):

		messages = await self.bot.get_channel(self.queuechan).history().flatten()
		for message in messages:
			if f'MS#{id_}' in message.content:
				if message.content.endswith('~~'):
					resp = await ctx.send(content='Doujin already cancelled')
				elif message.content.endswith('✅'):
					resp = await ctx.send(content='Doujin already finished')
				else:
					await message.edit(content=f'MS#{id_} ~~{message.content[8:]}~~')
					resp = await ctx.send(content=f'Cancelled MS#{id_}')
				await ctx.message.delete()
				await resp.delete(delay=5)
	
	@commands.is_owner()
	@commands.command()
	async def done(self, ctx: commands.Context = None, id_: MeltIDConverter = None):

		messages = await self.bot.get_channel(self.queuechan).history().flatten()
		for message in messages:
			if f'MS#{id_}' in message.content:
				if message.content.endswith('~~') and ctx is not None:
					resp = await ctx.send(content='Doujin already cancelled')
				elif message.content.endswith('✅') and ctx is not None:
					resp = await ctx.send(content='Doujin already finished')
				else:
					await message.edit(content=f'{message.content} ✅')
					if ctx is not None:
						resp = await ctx.send(content=f'Finished MS#{id_}')
					else:
						resp = None
				if ctx is not None:
					await ctx.message.delete()
					await resp.delete(delay=5)

def setup(bot: commands.Bot):
	bot.add_cog(MeltyScans(bot))