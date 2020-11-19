import discord
from discord.ext import commands

class InterCom(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		if message.author.bot or message.channel.name != "kiyo-intercom" or message.content.startswith("?"):
			return
		for hook in self.bot.commhooks:
			await hook.send(content=message.content, username=message.author.display_name, avatar_url=message.author.avatar_url, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))

def setup(bot):
	bot.add_cog(InterCom(bot))