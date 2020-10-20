import discord
from discord.ext import commands
from random import randint
from helpy import hell

class Chemshit(commands.Cog, name='ChemSpider Database'):
	def __init__(self, bot):
		self.bot = bot
		self.cs = bot.cs

	@commands.command(aliases=['searchcomp','sc'],help=hell['SearchCompound'])
	async def SearchCompound(self,ctx, compound):

		comp = compound
		searchlist = list()
		for result in self.cs.search(comp):
			searchlist.append(result)
		retop = searchlist[0]
		c_id = retop.record_id
		c_name = retop.common_name
		c_image = retop.image_url
		c_formula = retop.molecular_formula
		c_mass = retop.average_mass
		c_link = f"http://www.chemspider.com/Chemical-Structure.{c_id}.html"
		e = discord.Embed(title=c_name, url=c_link,color=0x5ec0d1)
		e.set_image(url=c_image)
		e.add_field(name="ID:", value=c_id)
		e.add_field(name="Molecular Formula:", value=c_formula)
		e.add_field(name="Average Mass:", value=c_mass)
		await ctx.send(embed=e)
		
	@commands.command(aliases=['compid','cid'],help=hell['CompoundId'])
	async def CompoundId(self,ctx, idnumber):
		
		idnum = idnumber
		comp = self.cs.get_compound(idnum)
		c_id = comp.record_id
		c_name = comp.common_name
		c_image = comp.image_url
		c_formula = comp.molecular_formula
		c_mass = comp.average_mass
		c_link = f"http://www.chemspider.com/Chemical-Structure.{c_id}.html"
		e = discord.Embed(title=c_name, url=c_link,color=0x5ec0d1)
		e.set_image(url=c_image)
		e.add_field(name="ID:", value=c_id)
		e.add_field(name="Molecular Formula:", value=c_formula)
		e.add_field(name="Average Mass:", value=c_mass)
		await ctx.send(embed=e)
		
	@commands.command(aliases=['rancomp','rc'],help=hell['RandomCompound'])
	async def RandomCompound(self,ctx):
		
		idnum = randint(0, 1000000)
		await self.CompoundId(ctx, idnum)

def setup(bot):
	bot.add_cog(Chemshit(bot))
