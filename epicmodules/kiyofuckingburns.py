import discord
from discord.ext import commands
import asyncio
from random import randint, choice, uniform
from kiyo import burnlist, lines

class Kiyohime(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db
	
	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):

		message_text = message.content.upper()
		luck = uniform(0, 1.0)
		e = discord.Embed(color=0xffff00)
		if message.author.bot or message_text.startswith('?'):
			pass
		elif 'CHEATING' in message_text:
			await message.channel.trigger_typing()
			await asyncio.sleep(3)
			await message.channel.send('Do I smell a liar in here?')
		elif 'CUNNY' in message_text:
			await message.channel.send('Ok pedophile')
		elif message.author.id == 293395455830654977 and luck >= 0.85 and message.guild.id == 569845300244774922:
			await message.add_reaction('❤️')
		elif "587931218146885642>" in message.content:#self.bot.user.mentioned_in(message):
			if message.author.id == 293395455830654977 and luck >= 0.97:
				e.set_image(url="https://cdn.discordapp.com/attachments/569845300244774924/692219666478923776/23a8b2e1-21d4-4dac-84ba-1128207f0e30.png")
				await message.channel.send(embed=e)
			else:
				await message.channel.send(choice(lines))

	@commands.command()
	async def burn(self, ctx: commands.Context):
		'''BURN BURN BURN BURN'''
		e=discord.Embed(color=0xff0000)
		e.set_image(url=choice(burnlist))
		await ctx.send(embed=e)

	@commands.command()
	async def step(self, ctx: commands.Context):
		'''NO STEP ON SNEK'''
		e=discord.Embed(color=0xffff00)
		e.set_image(url="https://cdn.discordapp.com/attachments/611844054669328394/635200592364699649/IMG_20191020_024438.JPG")
		await ctx.send(embed=e)
	
	@commands.is_nsfw()
	@commands.command(aliases=['k','kiyohime'])
	async def kiyo(self, ctx: commands.Context):
		'''poops out kiyo pics'''
		x = []
		page = randint(1,15)
		posts = self.db.post_list(tags='kiyohime_(fate/grand_order)',page=page,limit=100)
		for post in posts:
			try:
				fileurl = post['file_url']
			except:
				fileurl = 'https://danbooru.donmai.us' + post['source']
			x.append(fileurl)
		e = discord.Embed(color=0x00ff00)
		e.set_image(url=choice(x))
		await ctx.send(embed=e)

def setup(bot: commands.Context):
	bot.add_cog(Kiyohime(bot))
