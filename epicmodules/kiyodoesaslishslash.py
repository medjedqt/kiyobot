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

def setup(bot: commands.Bot):
	bot.add_cog(Slash(bot))