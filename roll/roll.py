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
    async def d(self, ctx, dice_expression):
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
    async def MyCthulhuStats(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        user_id = str(member.id)  # Get the user's ID as a string
        if user_id not in self.player_stats:  # Initialize the user's stats if they don't exist
            await ctx.send(f"{member.display_name} doesn't have an investigator. Use `!newI` for creating a new investigator.")
            return

        name = self.player_stats.get(user_id, {}).get("NAME", f"{member.display_name}'s Investigator Stats")

        stats_embed = discord.Embed(
            title=name,
            description="Investigator statistics - Page 1/3:",
            color=discord.Color.gold()
        )
        
        stats_list = list(self.player_stats[user_id].items())
        stats_page = 1
        max_page = (len(stats_list) - 1) // 12 + 1
        
        def get_emoji(index):
            if index == 0:
                return "⬅️"
            elif index == 1:
                return "➡️"
            else:
                return ""
        
        def get_stat_emoji(stat_name):
            # Your emoji logic here
            return ":question:"
        
        def get_stat_value(stat_name, value):
            # Your value formatting logic here
            return value
        
        def generate_stats_page(page):
            stats_embed.clear_fields()
            stats_embed.description = f"Investigator statistics - Page {page}/{max_page}:"
            
            for i in range((page - 1) * 12, min(page * 12, len(stats_list))):
                stat_name, value = stats_list[i]
                emoji = get_stat_emoji(stat_name)
                value = get_stat_value(stat_name, value)
                stats_embed.add_field(name=f"{stat_name} {emoji}", value=value, inline=True)
            
            return stats_embed
        
        message = await ctx.send(embed=generate_stats_page(stats_page))
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")
        
        def check(reaction, user):
            return user == ctx.author and reaction.message == message and reaction.emoji in ["⬅️", "➡️"]
        
        while True:
            try:
                reaction, _ = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                if reaction.emoji == "⬅️":
                    stats_page = max(stats_page - 1, 1)
                elif reaction.emoji == "➡️":
                    stats_page = min(stats_page + 1, max_page)
                
                await message.edit(embed=generate_stats_page(stats_page))
                await message.remove_reaction(reaction, ctx.author)
            except asyncio.TimeoutError:
                await message.clear_reactions()
                break
        
    @commands.command(aliases=["newInv"])
    async def newInvestigator(self, ctx, *, investigator_name):
        user_id = str(ctx.author.id)  # Get the user's ID as a string
    
        if user_id not in self.player_stats:
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
        self.save_data()  # Uložení změn do souboru
        await ctx.send("Investigator has been deleted.")
     else:
        await ctx.send("You don't have an investigator to delete.")

