from fastapi import FastAPI
import discord
from discord.ext import commands
import uvicorn

app = FastAPI()

@app.get("/")
async def read_root():
	return {"pee": "poo"}

class KiyoCyte(commands.Cog, name="Kiyo Site"):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

def setup(bot: commands.Bot):
	bot.add_cog(KiyoCyte(bot))
	uvicorn.run(app)