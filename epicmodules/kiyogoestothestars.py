import discord
import asyncio
import json

with open(starboardch.json) as st:
	data = json.load(st)
	
class starboardshit(commands.Cog, name='Starboard'):
	def __init__(self, bot: commands.Context):
		self.bot = bot
		self.cs = bot.cs
    
	@commands.command(aliases=['starset'])
	async def starboardset(self, ctx: commands.Context, chid: int):
		data = {}
		serverid = ctx.guild.id
		data.update({serverid : chid})
		with open(starboardch.json, 'w') as json_file:
			json.dump(data, json_file, indent=4)
			
def setup(bot: commands.Bot):
	bot.add_cog(Starboard(bot))
		
