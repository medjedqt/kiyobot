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
		reactors = await reaction.users().flatten()
		count = 0
		for reactor in reactors:
			if not reactor.bot and reactor != reaction.message.author:
				count += 1
		if reaction.emoji == '⭐' and count == 4 and starchan:
			e = discord.Embed()
			e.color = 0x691337
			e.set_author(name=str(reaction.message.author), icon_url=reaction.message.author.avatar_url)
			if reaction.message.content:
				e.description = reaction.message.content
			if reaction.message.attachments:
				e.set_image(url=reaction.message.attachments[0].url)
			e.add_field(name='Original', value=f'[Jump!]({reaction.message.jump_url})')
			e.timestamp = reaction.message.created_at
			await starchan.send(content=f'ID:{reaction.message.id}, {reaction.message.channel.mention}',embed=e)

	@commands.Cog.listener()
	async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
		guildid = reaction.message.guild.id
		starchan: discord.TextChannel = self.stardict.get(str(guildid))
		reactors = await reaction.users().flatten()
		count = 0
		for reactor in reactors:
			if not reactor.bot and reactor != reaction.message.author:
				count += 1
		if reaction.emoji == '⭐' and count < 4:
			async for message in starchan.history():
				if message.content.split(':')[1].split(',')[0] == str(reaction.message.id) and message.author.id == self.bot.user.id:
					return await message.delete()

def setup(bot: commands.Bot):
	bot.add_cog(Starboard(bot))
		
