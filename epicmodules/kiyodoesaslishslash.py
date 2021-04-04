import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext

import inspirobot

class Slash(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@cog_ext.cog_slash(description='get inspired, kids')
	async def inspire(self, ctx: SlashContext):
		quote = inspirobot.generate()
		await ctx.send(content=quote.url)

	@cog_ext.cog_subcommand(description='google for stuff here', base='google', base_description='google tools')
	async def search(self, ctx: SlashContext, *, query):
		comm = self.bot.get_cog('Google').google
		await comm(ctx=ctx, query=query)
	
	@cog_ext.cog_subcommand(description="googles some image, i guess", base='google', base_description='google tools')
	async def image(self, ctx: SlashContext, *, query):
		comm = self.bot.get_cog('Google').image
		try:
			await comm(ctx=ctx, query=query)
		except AttributeError:
			await ctx.send(content="Invalid input")

	@cog_ext.cog_slash(description="calculates stuff")
	async def calculate(self, ctx: SlashContext, *, question):
		comm = self.bot.get_cog('Google').calculate
		try:
			await comm(ctx=ctx, query=question)
		except AttributeError:
			await ctx.send(content="Invalid input")
	
	@cog_ext.cog_slash(description="answers your most mundane of questions", base="google")
	async def answer(self, ctx: SlashContext, *, query):
		comm = self.bot.get_cog('Google').answer
		try:
			await comm(ctx=ctx, query=query)
		except AttributeError:
			await ctx.send(content="Invalid input")

	@cog_ext.cog_slash(description="checks the weather")
	async def weather(self, ctx: SlashContext, *, query):
		comm = self.bot.get_cog('Google').weather
		try:
			await comm(ctx=ctx, query=query)
		except AttributeError:
			await ctx.send(content="Invalid input")

def setup(bot: commands.Bot):
	bot.add_cog(Slash(bot))