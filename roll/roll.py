from redbot.core import commands
import random
import discord

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dr(self, ctx, dice_expression):
 if 'd' in dice_expression:
            num_dice, dice_type = map(int, dice_expression.lower().split('d'))
        else:
            num_dice = 1  # Předpokládáme 1 kostku, pokud první číslo není zadáno
            dice_type = int(dice_expression)
            
        if dice_type not in [4, 6, 8, 10, 12, 20, 100]:
            embed = discord.Embed(
                title="Invalid Dice Type",
                description="Use :game_die: D4, D6, D8, D10, D12, D20, or D100.",
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
