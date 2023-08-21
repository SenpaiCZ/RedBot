from redbot.core import commands


# Classname should be CamelCase and the same spelling as the folder
class MyFirstCog(commands.Cog):
    @commands.command()
    async def callcthulhu(self, ctx):
        # Your code will go here
        await ctx.send("My first cog!")
