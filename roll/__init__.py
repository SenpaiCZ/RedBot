from .roll import Roll


async def setup(bot):
    await bot.add_cog(Roll(bot))
