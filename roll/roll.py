from redbot.core import commands
import random
import discord
import json
import os

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "player_stats.json"  # Název souboru, kde budou uložena data

        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.player_stats = json.load(f)
        else:
            self.player_stats = {}

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.player_stats, f, indent=4)

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
        
    @commands.command()
    async def CthulhuChangeStats(self, ctx, stat_name, new_value):
        user_id = str(ctx.author.id)  # Get the user's ID as a string
        stat_name = stat_name.upper()
        if user_id not in self.player_stats:  # Initialize the user's stats if they don't exist
            self.player_stats[user_id] = {}
        if stat_name in self.player_stats[user_id]:
            try:
                new_value = int(new_value)
                self.player_stats[user_id][stat_name] = new_value
                await ctx.send(f"Your {stat_name} has been updated to {new_value}.")
            except ValueError:
                await ctx.send("Invalid new value. Please provide a number.")
        else:
            await ctx.send("Invalid stat name. Use STR, DEX, CON, INT, POW, CHA, EDU, SIZ, HP, MP, LUCK, or SAN.")

            
    @commands.command()
    async def MyCthulhuStats(self, ctx):
        user_id = str(ctx.author.id)  # Get the user's ID as a string
        if user_id not in self.player_stats:  # Initialize the user's stats if they don't exist
            self.player_stats[user_id] = {}
        stats_embed = discord.Embed(
            title="Your Investigator Stats",
            description="Your current investigator statistics:",
            color=discord.Color.gold()
        )
        for stat_name, value in self.player_stats[user_id].items():
            emoji = ":question:"  # Default emoji if no suitable match is found
            if stat_name == "STR":
                emoji = ":muscle:"
            elif stat_name == "DEX":
                emoji = ":runner:"
            elif stat_name == "CON":
                emoji = ":heart:"
            elif stat_name == "INT":
                emoji = ":brain:"
            elif stat_name == "POW":
                emoji = ":zap:"
            elif stat_name == "CHA":
                emoji = ":sparkles:"
            elif stat_name == "EDU":
                emoji = ":mortar_board:"
            elif stat_name == "SIZ":
                emoji = ":bust_in_silhouette:"
            elif stat_name == "HP":
                emoji = ":heartpulse:"
            elif stat_name == "MP":
                emoji = ":sparkles:"
            elif stat_name == "LUCK":
                emoji = ":four_leaf_clover:"
            elif stat_name == "SAN":
                emoji = ":scales:"

            stats_embed.add_field(name=f"{stat_name} {emoji}", value=value, inline=True)

        await ctx.send(embed=stats_embed)
