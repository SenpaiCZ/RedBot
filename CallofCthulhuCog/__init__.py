from .CallofCthulhuCog import CallofCthulhuCog


async def setup(bot):
    await bot.add_cog(CallofCthulhuCog(bot))
