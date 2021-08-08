import asyncio
import discord
from discord.ext import commands

import aiohttp
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
from bs4 import BeautifulSoup as bs

class Google(commands.Cog):
	'''Main google request'''
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	async def request(self, query: str, extraparam: str = ""):
		self.url = "https://google.com/search?q="+urllib.parse.quote(query)+extraparam
		async with aiohttp.ClientSession() as sess:
			async with sess.get(self.url, headers=self.header) as req:
				self.resp = await req.text()
		self.soup = bs(self.resp, 'html.parser')

	@commands.group(aliases=['go'], invoke_without_command=True)
	async def google(self, ctx: commands.Context, *, query: str):
		'''google.'''
		if isinstance(ctx, commands.Context):
			if ctx.invoked_subcommand is not None:
				return
		safe = 'strict'
		if ctx.channel.is_nsfw() or isinstance(ctx.channel, discord.DMChannel):
			safe = 'off'
		await self.request(query, "&safe="+safe)
		soup = self.soup.find_all("div", class_="kCrYT")
		for i in soup:
			if i.a is not None and i.a['href'].startswith("/url") and not 'scholar.google' in i.a['href']:
				return await ctx.send(urllib.parse.unquote(i.a['href']).split('?q=')[1].split('&sa=')[0])
		await ctx.send(content="No results found (or they're nsfw idk)")

	@google.command(aliases=['ans'])
	async def answer(self, ctx: commands.Context, *, query: str):
		'''scrapes random answers on google (Not entirely polished)'''
		await self.request(query)
		h = self.soup.find('div', class_="BNeawe s3v9rd AP7Wnd")
		self.resp = h.text
		await ctx.send(self.resp)
	
	@google.command(aliases=['calc'])
	async def calculate(self, ctx: commands.Context, *, query: str):
		'''calculates stuff on google'''
		await self.request(f'calculate {query}')
		question = self.soup.find('span', class_="BNeawe tAd8D AP7Wnd").text
		ans = self.soup.find('div', class_="BNeawe iBp4i AP7Wnd").text
		e = discord.Embed(description=f"```\n{question}\n{ans}\n```")
		await ctx.send(embed=e)

	@google.command(aliases=['conv'])
	async def convert(self, ctx: commands.Context, *, query: str):
		'''converts measurements and stuff on google'''
		await self.calculate(ctx, query=query)

	@google.command()
	async def weather(self, ctx: commands.Context, *, query: str):
		'''checks weather on google'''
		await self.request('weather '+query)
		h = self.soup.find('div', class_="BNeawe tAd8D AP7Wnd").text
		i = self.soup.find('div', class_="BNeawe iBp4i AP7Wnd").text
		self.resp = f'{h} {i}'
		await ctx.send(self.resp)
	
	@google.command()
	async def define(self, ctx: commands.Context, *, query: str):
		'''define stuff on google'''
		await self.request('define '+query)
		root = self.soup.find_all('div', class_='kCrYT')
		root1 = root[0]
		root2 = root[1].find('div', class_='Ap5OSd').contents
		self.phrase = root1.span.h3.text
		self.pronounciation = root1.contents[1].text
		self.type = root2[0].text.strip()
		self.meaning = root2[1].text
		e = discord.Embed(title=self.phrase, description=self.meaning)
		e.add_field(name=self.type, value=f'({self.pronounciation})')
		await ctx.send(embed=e)

	@google.command(aliases=['img'])
	async def image(self, ctx: commands.Context, *, query: str):
		'''searches for images on google'''
		safe = 'strict'
		if ctx.channel.is_nsfw() or isinstance(ctx.channel, discord.DMChannel):
			safe = 'off'
		await self.request(query, "&tbm=isch&safe="+safe)
		root = self.soup.find('div', class_="NZWO1b")
		link = root.parent['href']
		imglink = root.img['src']
		e = discord.Embed(title="Jump to result!", color=0x2f3136, url=urllib.parse.unquote(link).split('?q=')[1].split('&sa=')[0])
		e.set_image(url=imglink)
		await ctx.send(embed=e)

def setup(bot: commands.Bot):
	bot.add_cog(Google(bot))
