import discord
from discord.ext import commands
from random import randint
from helpy import hell

class Chemshit(commands.Cog, name='ChemSpider Database'):
	def __init__(self, bot: commands.Context):
		self.bot = bot
		self.cs = bot.cs

	@commands.command(aliases=['searchcomp','sc'],help=hell['SearchCompound'])
	async def SearchCompound(self, ctx: commands.Context, *, compound: str):

		retop = self.cs.search(compound)[0]
		c_id = retop.record_id
		await self.CompoundId(ctx, c_id)
		
	@commands.command(aliases=['compid','cid'],help=hell['CompoundId'])
	async def CompoundId(self, ctx: commands.Context, idnumber: int):
		
		comp = self.cs.get_compound(idnumber)
		c_id = comp.record_id
		c_name = comp.common_name
		c_image = comp.image_url
		c_formula = discord.utils.escape_markdown(comp.molecular_formula)
		c_mass = comp.average_mass
		c_link = f"http://www.chemspider.com/Chemical-Structure.{c_id}.html"
		e = discord.Embed(title=c_name, url=c_link,color=0x5ec0d1)
		e.set_image(url=c_image)
		e.add_field(name="ID:", value=c_id)
		e.add_field(name="Molecular Formula:", value=c_formula)
		e.add_field(name="Average Mass:", value=c_mass)
		await ctx.send(embed=e)
		
	@commands.command(aliases=['rancomp','rc'],help=hell['RandomCompound'])
	async def RandomCompound(self, ctx: commands.Context):
		
		idnum = randint(0, 1000000)
		await self.CompoundId(ctx, idnum)

def setup(bot: commands.Bot):
	bot.add_cog(Chemshit(bot))
