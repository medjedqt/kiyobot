import discord
from discord.ext import commands
import os
class InterCom(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		bot.loop.create_task(self.init_comm())

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		if isinstance(message.channel, discord.DMChannel) or message.author.bot or message.channel.name != "kiyo-intercom" or message.content.startswith("?"):
			return
		for hook in self.commhooks:
			files = list()
			if message.attachments == [] and message.stickers == []:
				files = None
			else:
				for atta in message.attachments:
					await atta.save(atta.filename)
					files.append(discord.File(atta.filename))
				for stic in message.stickers:
					if stic.image_url is None:
						continue
					fname = "stic" + os.path.splitext(str(stic.image_url))[1]
					await stic.image_url.save(fname)
					files.append(discord.File(fname))
			hookmsg = await hook.send(content=message.content,
							username=f"{message.author.display_name} #{message.author.id}",
							avatar_url=message.author.avatar_url,
							allowed_mentions=discord.AllowedMentions(everyone=False, roles=False),
							files=files)
		await message.delete()

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
		if str(user.id) == reaction.message.author.display_name.split('#')[-1] and reaction.emoji == "🚮" and isinstance(reaction.message, discord.WebhookMessage):
			await reaction.message.delete()

	async def comm_task(self):
		self.commhooks = list()
		for guild in self.bot.guilds:
			commchannel = discord.utils.get(guild.text_channels, name="kiyo-intercom")
			if commchannel is not None:
				hooks = await commchannel.webhooks()
				if "KiyoCommSdnBhd" not in [_.name for _ in hooks]:
					hook = await commchannel.create_webhook(name="KiyoCommSdnBhd")
					self.commhooks.append(hook)
					continue
				for hook in hooks:
					if hook.name == "KiyoCommSdnBhd":
						self.commhooks.append(hook)
	
	@commands.command(hidden=True)
	async def update_command(self, ctx: commands.Context):
		if ctx.author.id != 550076298937237544:
			return
		await self.comm_task()

	async def init_comm(self):
		await self.bot.wait_until_ready()
		await self.comm_task()

def setup(bot: commands.Bot):
	bot.add_cog(InterCom(bot))