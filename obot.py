import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import CommandNotFound,MissingRequiredArgument
import os



bot = commands.Bot(command_prefix='?',case_insensitive=True)
bot.remove_command('help')
token = os.environ['BOT_TOKEN']

@bot.event
async def on_ready():

	print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_command_error(ctx, error):

	if isinstance(error, CommandNotFound):
		return
	if isinstance(error, MissingRequiredArgument):
		await ctx.send(content="Missing arguments!")
		return
	raise error

@bot.event
async def on_message(message):

	if message.author.bot:
		pass
	await bot.process_commands(message)

@bot.command()
async def ping(ctx):

	await ctx.send(content=":ping_pong: Pong!")
	
bot.run(token)
