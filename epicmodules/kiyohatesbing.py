import discord
from discord.ext import commands

import requests
import urllib
from bs4 import BeautifulSoup as bs

class Google(commands.Cog):
	'''Main google request'''
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

	def request(self, query: str, extraparam: str = ""):
		self.url = "https://google.com/search?q="+urllib.parse.quote(query)+extraparam
		self.req = requests.get(self.url, headers=self.header)
		self.soup = bs(self.req.text, 'html.parser')

	@commands.group(aliases=['go'], invoke_without_command=True)
	async def google(self, ctx: commands.Context, *, query: str):
		'''google.'''
		if ctx.invoked_subcommand is not None:
			return
		safe = 'strict'
		if ctx.channel.is_nsfw() or isinstance(ctx.channel, discord.DMChannel):
			safe = 'off'
		self.request(query, "&safe="+safe)
		soup = self.soup.find_all("div", class_="kCrYT")
		for i in soup:
			if i.a is not None and i.a['href'].startswith("/url"):
				await ctx.send(urllib.parse.unquote(i.a['href']).split('?q=')[1].split('&sa=')[0])
				return

	@google.command()
	async def answer(self, ctx: commands.Context, *, query: str):
		'''scrapes random answers on google (Not entirely polished)'''
		self.request(query)
		h = self.soup.find('div', class_="BNeawe s3v9rd AP7Wnd")
		self.resp = h.text
		await ctx.send(self.resp)
	
	@google.command()
	async def calculate(self, ctx: commands.Context, *, query: str):
		'''calculates stuff on google'''
		self.request(query)
		question = self.soup.fine('span', class_="BNeawe tAd8D AP7Wnd").text
		ans = self.soup.find('div', class_="BNeawe iBp4i AP7Wnd").text
		e = discord.Embed(description=f"```\n{question}\n{ans}\n```")
		await ctx.send(embed=e)

	@google.command()
	async def weather(self, ctx: commands.Context, *, query: str):
		'''checks weather on google'''
		self.request('weather '+query)
		h = self.soup.find('div', class_="BNeawe tAd8D AP7Wnd").text
		i = self.soup.find('div', class_="BNeawe iBp4i AP7Wnd").text
		self.resp = f'{h} {i}'
		await ctx.send(self.resp)
	
	@google.command()
	async def define(self, ctx: commands.Context, *, query: str):
		'''define stuff on google'''
		self.request('define '+query)
		self.phrase = self.soup.find('div', class_="BNeawe deIvCb AP7Wnd").text
		self.pronounciation = self.soup.find('div', class_="BNeawe tAd8D AP7Wnd").text
		self.type = self.soup.find('span', class_="r0bn4c rQMQod").text.strip()
		self.meaning = self.soup.find('div', class_="v9i61e").text
		e = discord.Embed(title=self.phrase, description=self.meaning)
		e.add_field(name=self.type, value=f'({self.pronounciation})')
		await ctx.send(embed=e)

	@google.command(aliases=['img'])
	async def image(self, ctx: commands.Context, *, query: str):
		'''searches for images on google'''
		self.request(query, "&tbm=isch")
		root = self.soup.find('div', class_="RAyV4b")
		link = root.parent['href']
		imglink = root.img['src']
		e = discord.Embed(title="Jump to result!", color=0x2f3136, url=urllib.parse.unquote(link).split('?q=')[1].split('&sa=')[0])
		e.set_image(url=imglink)
		await ctx.send(embed=e)

def setup(bot: commands.Bot):
	bot.add_cog(Google(bot))
