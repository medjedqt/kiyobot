import discord
from discord.ext import commands
from discord.ext import commands

prefix = '?'
token = ''
bot = commands.Bot(command_prefix=prefix,case_insensitive=True,intents=discord.Intents.all())

@bot.event
async def on_ready():

	print(f'We have logged in as {bot.user}')

@bot.event
async def on_command_error(ctx: commands.Context, error):

	if isinstance(error, commands.CommandNotFound):
		return
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send_help(ctx.command)
		return
	raise error

@bot.event
async def on_message(message):

	if message.author.bot:
		pass
	await bot.process_commands(message)

@bot.command()
async def ping(ctx):
	'''Pings the bot'''
	await ctx.send(content=":ping_pong: Pong!")
	
bot.run(token)
