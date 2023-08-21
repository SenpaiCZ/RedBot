from redbot.core import commands
import random
import discord
import json
import os

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "/home/pi/.local/share/SenpaiBot/cogs/RepoManager/repos/senpaicz/roll/player_stats.json" 

        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.player_stats = json.load(f)
        else:
            self.player_stats = {}

    def save_data(self):
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.player_stats, f, indent=4)
        except Exception as e:
                print(f"Error writing data to file: {e}")

    @commands.command(aliases=["diceroll"])
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
        
    @commands.command(aliases=["ccs"])
    async def CthulhuChangeStats(self, ctx, stat_name, new_value):
        user_id = str(ctx.author.id)  # Get the user's ID as a string
        stat_name = stat_name.upper()
        if user_id not in self.player_stats:  # Initialize the user's stats if they don't exist
            self.player_stats[user_id] = {}
        if stat_name in self.player_stats[user_id]:
            try:
                new_value = int(new_value)
                self.player_stats[user_id][stat_name] = new_value
                self.save_data()
                await ctx.send(f"Your {stat_name} has been updated to {new_value}.")
            except ValueError:
                await ctx.send("Invalid new value. Please provide a number.")
        else:
            await ctx.send("Invalid stat name. Use STR, DEX, CON, INT, POW, CHA, EDU, SIZ, HP, MP, LUCK, or SAN.")

            
    @commands.command(aliases=["mcs"])
    async def MyCthulhuStats(self, ctx):
        user_id = str(ctx.author.id)  # Get the user's ID as a string
        if user_id not in self.player_stats:  # Initialize the user's stats if they don't exist
            self.player_stats[user_id] = {}
        stats_embed = discord.Embed(
            title=name,
            description="Your current investigator statistics:",
            color=discord.Color.gold()
        )
        for stat_name, value in self.player_stats[user_id].items():
            emoji = ":question:"  # Default emoji if no suitable match is found
            if stat_name == "NAME":
                continue  # Skip displaying NAME in the list
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
        
    @commands.command(aliases=["newI"])
    async def newInvestigator(self, ctx, *, investigator_name):
        user_id = str(ctx.author.id)  # Get the user's ID as a string
    
        if user_id in self.player_stats:
            self.player_stats[user_id] = {
            "NAME": investigator_name,
            "STR": 0,
            "DEX": 0,
            "CON": 0,
            "INT": 0,
            "POW": 0,
            "CHA": 0,
            "EDU": 0,
            "SIZ": 0,
            "HP": 0,
            "MP": 0,
            "LUCK": 0,
            "SAN": 0
             }
            self.save_data()  # Uložení změn do souboru
            await ctx.send(f"Investigator '{investigator_name}' has been created with all stats set to 0.")
        else:
            await ctx.send("You already have an investigator. You can't create a new one until you delete the existing one.")

    @commands.command()
    async def deleteInvestigator(self, ctx):
     user_id = str(ctx.author.id)  # Get the user's ID as a string
    
     if user_id in self.player_stats:
        await ctx.send("Are you sure you want to delete your investigator? If you're sure, type 'YES' to confirm.")
        
        def check(message):
            return message.author == ctx.author and message.content.upper() == "YES"
        
        try:
            confirm_message = await self.bot.wait_for("message", check=check, timeout=30)
        except TimeoutError:
            await ctx.send("Confirmation timeout. Investigator deletion canceled.")
            return
        
        del self.player_stats[user_id]
        self.player_stats[user_id] = {}  # Vytvoření prázdného slovníku pro nového investigátora
        self.save_data()  # Uložení změn do souboru
        await ctx.send("Investigator has been deleted.")
     else:
        await ctx.send("You don't have an investigator to delete.")

