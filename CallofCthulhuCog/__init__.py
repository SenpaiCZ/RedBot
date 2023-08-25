from .roll import CallofCthulhuCog


async def setup(bot):
    await bot.add_cog(CallofCthulhuCog(bot))
