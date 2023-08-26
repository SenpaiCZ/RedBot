from .CthulhuCog import CthulhuCog

async def setup(bot):
    await bot.add_cog(CthulhuCog(bot))
