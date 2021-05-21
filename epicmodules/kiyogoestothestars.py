import discord
from discord.ext import commands

class Starboard(commands.Cog):
	def __init__(self, bot: commands.Bot):
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
		if reaction.emoji == '⭐' and reaction.count == 5 and starchan and not user.bot and user != reaction.message.author:
			lastmsg: discord.Message = await starchan.history(limit=1).flatten()[0]
			if lastmsg:
				try:
					strid = lastmsg.content.split(':')[1].split(',')[0]
					starid = int(strid)
				except (ValueError, IndexError):
					starid = 1
			else:
				starid = 1
			e = discord.Embed()
			e.color = 0x691337
			e.set_author(name=str(reaction.message.author), icon_url=reaction.message.author.avatar_url)
			e.description = reaction.message.content
			e.add_field(name='Original', value=f'[Jump!]({reaction.message.jump_url})')
			e.timestamp = reaction.message.created_at
			await starchan.send(content=f'StarID:{starid+1},{reaction.message.channel.mention}',embed=e)

def setup(bot: commands.Bot):
	bot.add_cog(Starboard(bot))
		
