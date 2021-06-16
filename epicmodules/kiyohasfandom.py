import discord
from discord.ext import commands, menus

import fandom as fan
from fandom import FandomPage

class Fandom_Menu(menus.Menu):
	def __init__(self, page: FandomPage):
		self.page = page
		self.summary = page.summary
		if len(self.summary)>200:
			self.summary = self.summary[:150]+"..."
		self.title = page.title
		self.url = page.url
		self.footer = '#'+page.wiki
		self.n = 0
		self.valid_sections = list()
		self.check_if_has_subsections(page.content)
		super().__init__(timeout=600, delete_message_after=True)
	
	def check_if_has_subsections(self, section: dict):
		if section.get('sections'):
			for subsection in section['sections']:
				self.check_if_has_subsections(subsection)
		elif section['title'] != 'Navigation':
			self.valid_sections.append(section['title'])
			return
	
	async def send_initial_message(self, ctx, channel):
		e = discord.Embed(title=self.title, description=self.summary, url=self.url)
		name = self.valid_sections[0]
		value = self.page.section(name)
		if len(value)>3000:
			value = value[:3000]+'...'
		e.add_field(name=name, value=value)
		e.set_footer(text=self.footer+f" (1/{len(self.valid_sections)})")
		return await channel.send(embed=e)

	async def change_page(self):
		name = self.valid_sections[self.n]
		value = self.page.section(name)
		if len(value) > 3000:
			value = value[:3000]+'...'
		e = discord.Embed(title=self.title, description=self.summary, url=self.url)
		e.add_field(name=name, value=value)
		e.set_footer(text=self.footer+f" ({self.n+1}/{len(self.valid_sections)})")
		await self.message.edit(embed=e)

	@menus.button('◀')
	async def left(self, payload):
		self.n -= 1
		if self.n == -1:
			self.n = len(self.valid_sections) - 1
		await self.change_page()

	@menus.button('▶')
	async def right(self, payload):
		self.n += 1
		if self.n >= len(self.valid_sections):
			self.n = 0
		await self.change_page()
	
	@menus.button('🚮')
	async def clear(self, payload):
		self.stop()

class Fandom(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.command()
	async def fandom(self, ctx: commands.Context, fandom_community: str, *, item: str):
		try:
			name = fan.search(query=item, wiki=fandom_community, results=1)[0][0]
		except IndexError:
			await ctx.send(content="Can't find item")
		page = fan.page(title=name, wiki=fandom_community, preload=True)
		m = Fandom_Menu(page)
		await m.start(ctx)
	
	@commands.command()
	async def genshin(self, ctx: commands.Context, *, item: str):
		await self.fandom(ctx, 'genshin-impact', item=item)

def setup(bot: commands.Bot):
	bot.add_cog(Fandom(bot))