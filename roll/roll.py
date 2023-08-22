from redbot.core import commands
import random
import discord
import json
import os
import asyncio

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
    async def d(self, ctx, *, dice_expression):
        user_id = str(ctx.author.id)
        
        if "Backstory" not in self.player_stats.get(user_id, {}):
            self.player_stats[user_id]["Backstory"] = {}
        
        try:
            if dice_expression in self.player_stats[user_id]:
                skill_name = dice_expression
                
                skill_value = self.player_stats[user_id][skill_name]
                luck_value = self.player_stats[user_id]["LUCK"]
                name_value = self.player_stats[user_id]["name"]
                
                roll = random.randint(1, 100)
                
                if roll == 1:
                    result = "CRITICAL! :star2:"
                elif roll <= skill_value // 5:
                    result = "Extreme Success :star:"
                elif roll <= skill_value // 2:
                    result = "Hard Success :white_check_mark:"
                elif roll <= skill_value:
                    result = "Regular Success :heavy_check_mark:"
                elif roll > 95:
                    result = "Fumble :warning:"
                else:
                    result = "Fail :x:"
                
                formatted_luck = f":four_leaf_clover: LUCK: {luck_value}"
                formatted_skill = f"**{skill_name}**: {skill_value} - {skill_value // 2} - {skill_value // 5}"
                
                embed = discord.Embed(
                    title=f"{name_value}'s Skill Check for '{skill_name}'",
                    description=f":game_die: Rolled: {roll}\n{result}\n\n{formatted_skill}\n\n{formatted_luck}",
                    color=discord.Color.green()
                )
            else:
                num_dice, dice_type = map(int, dice_expression.lower().split('d'))
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
                    description=f":game_die: Rolls: {rolls_str}\nTotal: {total}",
                    color=discord.Color.green()
                )
            
            await ctx.send(embed=embed)
        except ValueError:
            embed = discord.Embed(
                title="Invalid Input",
                description="Use format !d <skill_name> or XdY where X is the number of dice and Y is the dice type.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)



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
            "SAN": 0,
            "Accounting": 5,
            "Anthropology": 1,
            "Appraise": 5,
            "Archaeology": 1,
            "Charm": 15,
            "Climb": 20,
            "Credit Rating": 0,
            "Cthulhu Mythos": 0,
            "Disguise": 5,
            "Dodge": -1,
            "Drive Auto":20,
            "Elec. Repair": 10,
            "Fast Talk": 5,
            "Fighting (Brawl)": 25,
            "Firearms (Handgun)": 20,
            "Firearms (Rifle/Shotgun)":25,
            "First Aid": 30,
            "History": 5,
            "Intimidate": 15,
            "Jump":10,
            "Language (other)": 1,
            "Language (own)": -1,
            "Law":5,
            "Library Use":20,
            "Listen":20,
            "Locksmith":1,
            "Mech. Repair": 10,
            "Medicine": 1,
            "Natural World": 10,
            "Navigate": 10,
            "Ocult": 5,
            "Persuade": 10,
            "Pilot": 1,
            "Psychoanalysis": 1,
            "Psychology": 10,
            "Ride": 5,
            "Science (specific)": 1,
            "Sleight of Hand": 10,
            "Spot Hidden": 25,
            "Stealth": 20,
            "Survival": 10,
            "Swim": 20,
            "Throw": 20,
            "Track": 10,
            "Move": -1,
            "Build": -1,
            "Damage Bonus": -1
            }
            self.save_data()  # Uložení změn do souboru
            await ctx.send(f"Investigator '{investigator_name}' has been created with all stats set to 0.")
        else:
            await ctx.send("You already have an investigator. You can't create a new one until you delete the existing one.")
        
    @commands.command(aliases=["ccs"])
    async def CthulhuChangeStats(self, ctx, stat_name, new_value):
        user_id = str(ctx.author.id)  # Get the user's ID as a string
        stat_name = stat_name.upper()
        if user_id not in self.player_stats:  # Initialize the user's stats if they don't exist
            self.player_stats[user_id] = {}
        
        if stat_name in self.player_stats[user_id]:
            try:
                new_value = int(new_value)
                
                # Handle special cases for DEX and EDU
                if stat_name == "DEX":
                    self.player_stats[user_id][stat_name] = new_value
                    self.player_stats[user_id]["Dodge"] = new_value // 2  # Save half of DEX value as Dodge
                elif stat_name == "EDU":
                    self.player_stats[user_id][stat_name] = new_value
                    self.player_stats[user_id]["Language (own)"] = new_value  # Save EDU value as Language (own)
                else:
                    self.player_stats[user_id][stat_name] = new_value
                    
                self.save_data()
                await ctx.send(f"Your {stat_name} has been updated to {new_value}.")
            except ValueError:
                await ctx.send("Invalid new value. Please provide a number.")
        else:
            await ctx.send("Invalid stat name. Use STR, DEX, CON, INT, POW, CHA, EDU, SIZ, HP, MP, LUCK, or SAN.")
            
    @commands.command(aliases=["cskill"])
    async def CthulhuChangeSkills(self, ctx, *, skill_and_value):
        user_id = str(ctx.author.id)  # Get the user's ID as a string
        skill_and_value = skill_and_value.rsplit(maxsplit=1)
        
        if len(skill_and_value) != 2:
            await ctx.send("Invalid input. Please provide skill name and new value.")
            return
        
        skill_name = skill_and_value[0].title()  # Convert the skill name to title case
        new_value = skill_and_value[1]
        
        # List of skills that can be changed
        changable_skills = [
            "Accounting", "Anthropology", "Appraise", "Archaeology", "Charm", "Climb", "Credit Rating", "Cthulhu Mythos", "Disguise", "Dodge", "Drive Auto", "Elect. Repair", "Fast Talk", "Fighting (Brawl)", "Firearms (Handgun)", "Firearms (Rifle/Shotgun)", "First Aid", "History", "Intimidate", "Jump", "Language (Other)", "Language (Own)", "Law", "Library Use", "Listen", "Locksmith", "Mech. Repair", "Medicine", "Natural World", "Navigate", "Occult", "Persuade", "Pilot", "Psychoanalysis", "Psychology", "Ride", "Science (Specific)", "Sleight of Hand", "Spot Hidden", "Stealth", "Survival", "Swim", "Throw", "Track", "Move", "Build", "Damage Bonus"
        ]
        
        if user_id not in self.player_stats:  # Initialize the user's stats if they don't exist
            self.player_stats[user_id] = {}
        
        if skill_name in changable_skills:
            try:
                new_value = int(new_value)
                self.player_stats[user_id][skill_name] = new_value
                self.save_data()
                await ctx.send(f"Your {skill_name} has been updated to {new_value}.")
            except ValueError:
                await ctx.send("Invalid new value. Please provide a number.")
        else:
            await ctx.send("Invalid skill name. Use one of the following: "
                           "Accounting, Anthropology, Appraise, Archaeology, Charm, Climb, ...")
    

            
    @commands.command(aliases=["mcs"])
    async def MyCthulhuStats(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        user_id = str(member.id)  # Get the user's ID as a string
        if user_id not in self.player_stats:  # Initialize the user's stats if they don't exist
            await ctx.send(f"{member.display_name} doesn't have an investigator. Use `!newInv` for creating a new investigator.")
            return

        name = self.player_stats.get(user_id, {}).get("NAME", f"{member.display_name}'s Investigator Stats")

        stats_embed = discord.Embed(
            title=name,
            description="Investigator statistics:",
            color=discord.Color.green()
        )
        
        stats_list = list(self.player_stats[user_id].items())
        stats_page = 1
        max_page = 3
        
        def get_emoji(index):
            if index == 0:
                return "⬅️"
            elif index == 1:
                return "➡️"
            else:
                return ""
        
        def get_stat_emoji(stat_name):
            stat_emojis = {
                "STR": ":muscle:",
                "DEX": ":runner:",
                "CON": ":heart:",
                "INT": ":brain:",
                "POW": ":zap:",
                "CHA": ":sparkles:",
                "EDU": ":mortar_board:",
                "SIZ": ":bust_in_silhouette:",
                "HP": ":heartpulse:",
                "MP": ":sparkles:",
                "LUCK": ":four_leaf_clover:",
                "SAN": ":scales:",
                "Accounting": ":ledger:",
                "Anthropology": ":earth_americas:",
                "Appraise": ":mag:",
                "Archaeology": ":pick:",
                "Charm": ":heart_decoration:",
                "Climb": ":mountain:",
                "Credit Rating": ":moneybag:",
                "Cthulhu Mythos": ":octopus:",
                "Disguise": ":dress:",
                "Dodge": ":warning:",
                "Drive Auto": ":blue_car:",
                "Elec. Repair": ":wrench:",
                "Fast Talk": ":pinched_fingers:",
                "Fighting (Brawl)": ":boxing_glove:",
                "Firearms (Handgun)": ":gun:",
                "Firearms (Rifle/Shotgun)": ":gun:",
                "First Aid": ":ambulance:",
                "History": ":scroll:",
                "Intimidate": ":fearful:",
                "Jump": ":athletic_shoe:",
                "Language (other)": ":globe_with_meridians:",
                "Language (own)": ":speech_balloon:",
                "Law": ":scales:",
                "Library Use": ":books:",
                "Listen": ":ear:",
                "Locksmith": ":key:",
                "Mech. Repair": ":wrench:",
                "Medicine": ":pill:",
                "Natural World": ":deciduous_tree:",
                "Navigate": ":compass:",
                "Ocult": ":crystal_ball:",
                "Persuade": ":speech_balloon:",
                "Pilot": ":airplane:",
                "Psychoanalysis": ":brain:",
                "Psychology": ":brain:",
                "Ride": ":horse_racing:",
                "Science (specific)": ":microscope:",
                "Sleight of Hand": ":mage:",
                "Spot Hidden": ":eyes:",
                "Stealth": ":footprints:",
                "Survival": ":camping:",
                "Swim": ":swimmer:",
                "Throw": ":dart:",
                "Track": ":mag_right:",
                "Move": ":person_running:",
                "Build": ":restroom: ",
                "Damage Bonus": ":mending_heart:"
            }
            return stat_emojis.get(stat_name, ":question:")
        
        def get_stat_value(stat_name, value):
            if stat_name in ["Move", "Build", "Damage Bonus"]:
                formatted_value = f"{value}"
            else:
                formatted_value = f"{value} - {value // 2} - {value // 5}"
            return formatted_value
        
        def generate_stats_page(page):
            stats_embed.clear_fields()
            stats_embed.description = f"Investigator statistics - Page {page}/{max_page}:"
            
            if page == 1:
                stats_range = range(0, 13)
            elif page == 2:
                stats_range = range(13, 37)
            elif page == 3:
                stats_range = range(37, 60)
            else:
                stats_range = range(61, len(stats_list))
            
            for i in stats_range:
                stat_name, value = stats_list[i]
                if stat_name == "NAME":
                    continue  # Skip displaying NAME in the list
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
         
    @commands.command(aliases=["cbackstory"])
    async def CthulhuBackstory(self, ctx, *, input_text):
        user_id = str(ctx.author.id)
    
        if user_id not in self.player_stats:
            self.player_stats[user_id] = {}
    
        input_text = input_text.strip()
        parts = input_text.split(" - ")
        
        if len(parts) < 2:
            await ctx.send("Invalid input format. Please use 'Category - Entry' format.")
            return
        
        category = parts[0].strip().capitalize()
        entry = " - ".join(parts[1:]).strip()
    
        if "Backstory" not in self.player_stats[user_id]:
            self.player_stats[user_id]["Backstory"] = {}
    
        if category not in self.player_stats[user_id]["Backstory"]:
            self.player_stats[user_id]["Backstory"][category] = []
    
        self.player_stats[user_id]["Backstory"][category].append(entry)
    
        self.save_data()  # Uložení změn do souboru
    
        await ctx.send(f"Entry '{entry}' has been added to the '{category}' category in your Backstory.")

    @commands.command(aliases=["mbackstory"])
    async def MyCthulhuBackstory(self, ctx):
        user_id = str(ctx.author.id)
        
        if user_id not in self.player_stats or "Backstory" not in self.player_stats[user_id]:
            await ctx.send("You don't have any backstory entries.")
            return
        
        name = self.player_stats.get(user_id, {}).get("NAME", "Your")
        backstory_data = self.player_stats[user_id]["Backstory"]
        
        entries_embed = discord.Embed(
            title=f"{name}'s Inventory and Backstory",
            description="Your inventory and backstory entries:",
            color=discord.Color.gold()
        )
        
        for category, entries in backstory_data.items():
            formatted_entries = "\n".join([f"{index + 1}. {entry}" for index, entry in enumerate(entries)])
            entries_embed.add_field(name=category, value=formatted_entries, inline=False)
        
        await ctx.send(embed=entries_embed)



    @commands.command(aliases=["rbackstory"])
    async def RemoveCthulhuBackstory(self, ctx, *, category_and_index: str):
        user_id = str(ctx.author.id)
        
        if user_id not in self.player_stats or "Backstory" not in self.player_stats[user_id]:
            await ctx.send("You don't have any backstory entries.")
            return
        
        backstory_data = self.player_stats[user_id]["Backstory"]
        
        # Rozdělíme vstup na název kategorie a index
        parts = category_and_index.split()
        if len(parts) < 2:
            await ctx.send("Invalid input format. Please provide both the category and the index.")
            return
        
        category = " ".join(parts[:-1])
        index = int(parts[-1])
        
        if category not in backstory_data:
            await ctx.send(f"There is no category named '{category}' in your backstory.")
            return
        
        entries = backstory_data[category]
        
        if not entries or index < 1 or index > len(entries):
            await ctx.send("Invalid index. Please provide a valid index.")
            return
        
        removed_entry = entries.pop(index - 1)
        
        if not entries:
            del backstory_data[category]
        
        self.save_data()
        await ctx.send(f"Removed entry '{removed_entry}' from the '{category}' category.")
