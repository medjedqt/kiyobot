import aiohttp
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import multidict
import re
import inspirobot
from wordcloud import WordCloud

class MachineLearningShit(commands.Cog, name='Machine Learning Shit'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command()
	async def word(self, ctx: commands.Context):
		'''Generates a word that doesn't exist'''
		async with aiohttp.ClientSession() as sess:
			async with sess.get('https://www.thisworddoesnotexist.com/') as req:
				r = await req.text()
		soup = BeautifulSoup(r, 'html.parser')
		defword = soup.find(id='definition-word').string
		deflink = soup.find(id='link-button-a')['href']
		defgrammar = soup.find(id='definition-pos').string
		defgrammar = defgrammar.replace('"','').strip()
		defex = soup.find(id='definition-example').string
		defdef = soup.find(id='definition-definition').string
		defdesc = defgrammar + ' ' + defdef
		e = discord.Embed(title=defword, url=deflink,color=0x002258)
		e.add_field(name=defdesc, value=defex)
		e.set_footer(text='Powered by This Word Does Not Exist',icon_url='https://www.thisworddoesnotexist.com/favicon-32x32.png')
		await ctx.reply(embed=e)

	@commands.command()
	async def wordcloud(self, ctx: commands.Context, chanlimit: int = 100, maxim: int = 100):
		'''Generates a wordcloud of the server'''
		def getFrequencyDictForText(sentence):
			fullTermsDict = multidict.MultiDict()
			tmpDict = {}

			for text in sentence.split(" "):
				if text.startswith(('.','f.','!','<','-','?','$','_',':')):
					continue
				if re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", text):
					continue
				val = tmpDict.get(text, 0)
				tmpDict[text.lower()] = val + 1
			for key in tmpDict:
				fullTermsDict.add(key, tmpDict[key])
			return fullTermsDict

		async with ctx.channel.typing():
			messages = []
			for channel in ctx.guild.channels:
				if isinstance(channel, discord.TextChannel) and channel.permissions_for(ctx.guild.me).read_messages:
					async for stuff in channel.history(limit=chanlimit):
						messages.append(stuff.content)
			text = ' '.join(messages)
			wordcloud = WordCloud(max_words=maxim,width=1920, height=1080, min_word_length=2).generate_from_frequencies(getFrequencyDictForText(text))
			wordcloud.to_file('wc.png')
			await ctx.reply(file=discord.File('wc.png', filename='wordcloud.png'))

	@commands.command()
	async def inspire(self, ctx: commands.Context):
		'''Generates inspiring (or not) images'''
		quote = inspirobot.generate()
		await ctx.reply(content=quote.url, mention_author=False)

def setup(bot: commands.Bot):
	bot.add_cog(MachineLearningShit(bot))
