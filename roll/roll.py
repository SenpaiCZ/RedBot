from redbot.core import commands
import random
import discord

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dr(self, ctx, dice_expression):
        try:
            num_dice, dice_type = map(int, dice_expression.lower().split('d'))
            if dice_type not in [4, 6, 8, 10, 12, 20, 100]:
                embed = discord.Embed(
                    title="Invalid Dice Type",
                    description="Use :game_die: D4, D6, D8, D10, D12, D20, or D100.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
        except ValueError:
            embed = discord.Embed(
                title="Invalid Dice Expression",
                description="Use format XdY where X is the number of dice and Y is the dice type.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        rolls = [random.randint(1, dice_type) for _ in range(num_dice)]
        total = sum(rolls)
        rolls_str = ", ".join(map(str, rolls))
        
        embed = discord.Embed(
            title=f"Rolled {num_dice} :game_die:d{dice_type}:",
            description=f"Rolls: {rolls_str}\nTotal: {total}",
            color=discord.Color.green()
        )
        
        await ctx.send(embed=embed)

    @commands.command()
    async def investigator(self, ctx):
        embed = discord.Embed(
            title="Call of Cthulhu Stats",
            description="Basic statistics for a Call of Cthulhu character:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Strength (STR) :muscle:", value="70", inline=True)
        embed.add_field(name="Dexterity (DEX) :runner:", value="50", inline=True)
        embed.add_field(name="Constitution (CON) :heart:", value="60", inline=True)
        embed.add_field(name="Intelligence (INT) :brain:", value="80", inline=True)
        embed.add_field(name="Power (POW) :zap:", value="50", inline=True)
        embed.add_field(name="Charisma (CHA) :sparkles:", value="40", inline=True)
        embed.add_field(name="Education (EDU) :mortar_board:", value="70", inline=True)
        embed.add_field(name="Size (SIZ) :bust_in_silhouette:", value="60", inline=True)
        embed.add_field(name="Hit Points :heartpulse:", value="12", inline=True)
        embed.add_field(name="Magic Points :sparkles:", value="10", inline=True)
        embed.add_field(name="Luck :four_leaf_clover:", value="45", inline=True)
        embed.add_field(name="Sanity :scales:", value="70", inline=True)
        
        await ctx.send(embed=embed)
