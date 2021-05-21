import discord
from discord.ext import commands

class Starboard(commands.Cog):
	async def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.cs = bot.cs
		self.bot.loop.create_task(self.starboardinit())

	async def starboardinit(self):
		await self.bot.wait_until_ready()
		self.stardict = dict()
		for guild in self.bot.guilds:
			starchan = discord.utils.get(guild.text_channels, name='kiyo-starboard')
			if starchan is None:
				continue
			self.stardict[str(guild.id)] = starchan
	
	@commands.Cog.listener()
	async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
		guildid = reaction.message.guild.id
		starchan: discord.TextChannel = self.stardict.get(str(guildid))
		if reaction.emoji == '⭐' and reaction.count == 1 and starchan:
			await starchan.send(content=reaction.message.content)

def setup(bot: commands.Bot):
	bot.add_cog(Starboard(bot))
		
