import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

import random

class Games(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.comp = DiscordComponents(bot)
	@commands.command()
	async def rater(self, ctx: commands.Context):

		await ctx.send(components=[Button(label="gay", style=ButtonStyle.blue),
									Button(label="cute", style=ButtonStyle.green)])
		resp = await self.comp.wait_for_interact("button_click")
		print(resp)
		if resp.channel == ctx.channel:
			await resp.respond(type=InteractionType.ChannelMessageWithSource, content=f"{resp.user.mention} is {random.randint(0,100)}% {resp.component.label}")

def setup(bot: commands.Bot):
	bot.add_cog(Games(bot))