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
                name_value = self.player_stats.get(user_id, {}).get("NAME", ctx.author.display_name)
                
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
                    description=f":game_die: Rolled: {roll}\n{result}\n{formatted_skill}\n{formatted_luck}",
                    color=discord.Color.green()
                )
                
                if roll > skill_value and roll <= skill_value + 10 and luck_value >= roll - skill_value:
                    difference = roll - skill_value
                    prompt_embed = discord.Embed(
                        title="Use LUCK?",
                        description=f":game_die: Rolled: {roll}\n{result}\n{formatted_skill}\n{formatted_luck}\n\nYour roll is close to your skill ({difference}). Do you want to use LUCK to turn it into a Regular Success?\n"
                                    "Reply with 'YES' to use LUCK or 'NO' to skip within 1 minute.",
                        color=discord.Color.orange()
                    )
                    prompt_message = await ctx.send(embed=prompt_embed)
                    
                    def check(message):
                        return message.author == ctx.author and message.content.lower() in ["yes", "no"]
                    
                    try:
                        response = await self.bot.wait_for("message", timeout=60, check=check)
                        await prompt_message.delete()
                        
                        if response.content.lower() == "yes":
                            luck_used = min(luck_value, difference)
                            luck_value -= luck_used
                            self.player_stats[user_id]["LUCK"] = luck_value
                            self.save_data()  # Uložení změn LUCK do dat
                            formatted_luck = f":four_leaf_clover: LUCK: {luck_value}"
                            result = "Regular Success (LUCK Used) :heavy_check_mark:"
                            skill_value += luck_used
                            
                            formatted_skill = f"**{skill_name}**: {skill_value} - {skill_value // 2} - {skill_value // 5}"
                        else:
                            result = "Fail :x:"
                        
                        embed = discord.Embed(
                            title=f"{name_value}'s Skill Check for '{skill_name}'",
                            description=f":game_die: Rolled: {roll}\n{result}\n{formatted_skill}\n{formatted_luck}",
                            color=discord.Color.green()
                        )
                    except asyncio.TimeoutError:
                        await prompt_message.delete()
                
                await ctx.send(embed=embed)
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
        
    @commands.command(aliases=["cstat"])
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
    

            
    @commands.command(aliases=["mychar","mcs"])
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
         
    @commands.command(aliases=["cb"])
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

    @commands.command(aliases=["mb"])
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



    @commands.command(aliases=["rb"])
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

    @commands.command()
    async def db(self, ctx, *, skill_name):
        user_id = str(ctx.author.id)
        
        if skill_name in self.player_stats[user_id]:
            skill_value = self.player_stats[user_id][skill_name]
            luck_value = self.player_stats[user_id]["LUCK"]
            name_value = self.player_stats.get(user_id, {}).get("NAME", ctx.author.display_name)
            
            rolls_1 = [i for i in range(0, 100, 10)]
            roll_1 = random.choice(rolls_1)
            
            rolls_2 = [i for i in range(0, 100, 10)]
            roll_2 = random.choice(rolls_2)
            
            if roll_1 <= roll_2:
                total = roll_1
            else:
                total = roll_2
            
            roll_3 = random.randint(0, 9)
            roll = total + roll_3
            
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
                title=f"{name_value}'s Skill Check for '{skill_name}' with Bonus Die",
                description=f":game_die: Rolled: {roll_1}, {roll_2}, {roll_3} (Total: {total}) + {roll}\n{result}\n{formatted_skill}\n{formatted_luck}",
                color=discord.Color.green()
            )
            
            if roll > skill_value and roll <= skill_value + 10 and luck_value >= roll - skill_value:
                difference = roll - skill_value
                prompt_embed = discord.Embed(
                    title="Use LUCK?",
                    description=f":game_die: Rolled: {roll_1}, {roll_2}, {roll_3} (Total: {total}) + {roll}\n{result}\n{formatted_skill}\n{formatted_luck}\n\nYour roll is close to your skill ({difference}). Do you want to use LUCK to turn it into a Regular Success?\n"
                                "Reply with 'YES' to use LUCK or 'NO' to skip within 1 minute.",
                    color=discord.Color.orange()
                )
                prompt_message = await ctx.send(embed=prompt_embed)
                
                def check(message):
                    return message.author == ctx.author and message.content.lower() in ["yes", "no"]
                
                try:
                    response = await self.bot.wait_for("message", timeout=60, check=check)
                    await prompt_message.delete()
                    
                    if response.content.lower() == "yes":
                        luck_used = min(luck_value, difference)
                        luck_value -= luck_used
                        self.player_stats[user_id]["LUCK"] = luck_value
                        self.save_data()  # Uložení změn LUCK do dat
                        formatted_luck = f":four_leaf_clover: LUCK: {luck_value}"
                        result = "Regular Success (LUCK Used) :heavy_check_mark:"
                        skill_value += luck_used
                        
                        formatted_skill = f"**{skill_name}**: {skill_value} - {skill_value // 2} - {skill_value // 5}"
                    else:
                        result = "Fail :x:"
                    
                    embed = discord.Embed(
                        title=f"{name_value}'s Skill Check for '{skill_name}' with Bonus Die",
                        description=f":game_die: Rolled: {roll_1}, {roll_2}, {roll_3} (Total: {total}) + {roll}\n{result}\n{formatted_skill}\n{formatted_luck}",
                        color=discord.Color.green()
                    )
                except asyncio.TimeoutError:
                    await prompt_message.delete()
            
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Skill Not Found",
                description=f"Skill '{skill_name}' was not found for this user.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    
    @commands.command()
    async def dp(self, ctx, *, skill_name):
        user_id = str(ctx.author.id)
        
        if skill_name in self.player_stats[user_id]:
            skill_value = self.player_stats[user_id][skill_name]
            luck_value = self.player_stats[user_id]["LUCK"]
            name_value = self.player_stats.get(user_id, {}).get("NAME", ctx.author.display_name)
            
            rolls_1 = [i for i in range(0, 100, 10)]
            roll_1 = random.choice(rolls_1)
            
            rolls_2 = [i for i in range(0, 100, 10)]
            roll_2 = random.choice(rolls_2)
            
            if roll_1 >= roll_2:
                total = roll_1
            else:
                total = roll_2
            
            roll_3 = random.randint(0, 9)
            roll = total + roll_3
            
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
                title=f"{name_value}'s Skill Check for '{skill_name}' with Penalty Die",
                description=f":game_die: Rolled: {roll_1}, {roll_2}, {roll_3} (Total: {total}) + {roll}\n{result}\n{formatted_skill}\n{formatted_luck}",
                color=discord.Color.green()
            )
            
            if roll > skill_value and roll <= skill_value + 10 and luck_value >= roll - skill_value:
                difference = roll - skill_value
                prompt_embed = discord.Embed(
                    title="Use LUCK?",
                    description=f":game_die: Rolled: {roll_1}, {roll_2}, {roll_3} (Total: {total}) + {roll}\n{result}\n{formatted_skill}\n{formatted_luck}\n\nYour roll is close to your skill ({difference}). Do you want to use LUCK to turn it into a Regular Success?\n"
                                "Reply with 'YES' to use LUCK or 'NO' to skip within 1 minute.",
                    color=discord.Color.orange()
                )
                prompt_message = await ctx.send(embed=prompt_embed)
                
                def check(message):
                    return message.author == ctx.author and message.content.lower() in ["yes", "no"]
                
                try:
                    response = await self.bot.wait_for("message", timeout=60, check=check)
                    await prompt_message.delete()
                    
                    if response.content.lower() == "yes":
                        luck_used = min(luck_value, difference)
                        luck_value -= luck_used
                        self.player_stats[user_id]["LUCK"] = luck_value
                        self.save_data()  # Uložení změn LUCK do dat
                        formatted_luck = f":four_leaf_clover: LUCK: {luck_value}"
                        result = "Regular Success (LUCK Used) :heavy_check_mark:"
                        skill_value += luck_used
                        
                        formatted_skill = f"**{skill_name}**: {skill_value} - {skill_value // 2} - {skill_value // 5}"
                    else:
                        result = "Fail :x:"
                    
                    embed = discord.Embed(
                        title=f"{name_value}'s Skill Check for '{skill_name}' with Penalty Die",
                        description=f":game_die: Rolled: {roll_1}, {roll_2}, {roll_3} (Total: {total}) + {roll}\n{result}\n{formatted_skill}\n{formatted_luck}",
                        color=discord.Color.green()
                    )
                except asyncio.TimeoutError:
                    await prompt_message.delete()
            
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Skill Not Found",
                description=f"Skill '{skill_name}' was not found for this user.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def cname(self, ctx, gender):
        gender = gender.lower()
        
        if gender == "male":
            name_list = [
                "Aaron", "Abraham", "Addison", "Amos", "Anderson", "Archibald", "August", "Barnabas", "Barney", "Baxter",
                           "Blair", "Caleb", "Cecil", "Chester", "Clifford", "Clinton", "Cornelius", "Curtis", "Dayton", "Delbert",
                           "Douglas", "Dudley", "Ernest", "Eldridge", "Elijah", "Emanuel", "Emmet", "Enoch", "Ephraim", "Everett",
                           "Ezekiel", "Forest", "Gilbert", "Granville", "Gustaf", "Hampton", "Harmon", "Henderson", "Herman",
                           "Hilliard", "Howard", "Hudson", "Irvin", "Issac", "Jackson", "Jacob", "Jeremiah", "Jonah", "Josiah",
                           "Kirk", "Larkin", "Leland", "Leopold", "Lloyd", "Luther", "Manford", "Marcellus", "Martin", "Mason",
                           "Maurice", "Maynard", "Melvin", "Miles", "Milton", "Morgan", "Mortimer", "Moses", "Napoleon", "Nelson",
                           "Newton", "Noble", "Oliver", "Orson", "Oswald", "Pablo", "Percival", "Porter", "Quincy", "Randall",
                           "Reginald", "Richmond", "Rodney", "Roscoe", "Rowland", "Rupert", "Sampson", "Sanford", "Sebastian",
                           "Shelby", "Sidney", "Solomon", "Squire", "Sterling", "Sidney", "Thaddeus", "Walter", "Wilbur", "Wilfred",
                           "Zadok", "Zebedee"
            ]
        elif gender == "female":
            name_list = [
                "Adelaide", "Agatha", "Agnes", "Albertina", "Almeda", "Amelia", "Anastasia", "Annabelle", "Asenath", "Augusta",
                             "Barbara", "Bernadette", "Bernice", "Beryl", "Beulah", "Camilla", "Caroline", "Cecilia", "Carmen",
                             "Charity", "Christina", "Clarissa", "Cordelia", "Cynthia", "Daisy", "Dolores", "Doris", "Edith",
                             "Edna", "Eloise", "Elouise", "Estelle", "Ethel", "Eudora", "Eugenie", "Eunice", "Florence", "Frieda",
                             "Genevieve", "Gertrude", "Gladys", "Gretchen", "Hannah", "Henrietta", "Ingrid", "Irene", "Iris",
                             "Ivy", "Jeanette", "Jezebel", "Josephine", "Joyce", "Juanita", "Keziah", "Laverne", "Leonora", "Loretta",
                             "Lucretia", "Mabel", "Madeleine", "Margery", "Marguerite", "Marjorie", "Matilda", "Melinda", "Mercedes",
                             "Mildred", "Millicent", "Muriel", "Myrtle", "Naomi", "Nora", "Octavia", "Ophelia", "Pansy", "Patience",
                             "Pearle", "Phoebe", "Phyllis", "Rosemary", "Ruby", "Sadie", "Selina", "Selma", "Sibyl", "Sylvia", "Tabitha",
                             "Ursula", "Veronica", "Violet", "Virginia", "Wanda", "Wilhelmina", "Winifred"
            ]
        else:
            await ctx.send("Invalid gender. Use 'male' or 'female'.")
            return
        
        first_name = random.choice(name_list)
        last_name = random.choice([
            "Abraham", "Adler", "Ankins", "Avery", "Barnham", "Bentz", "Bessler", "Blakely", "Bleeker", "Bouche",
                         "Bretz", "Buchman", "Butts", "Caffey", "Click", "Cordova", "Crabtree", "Crankovitch", "Cuthburt",
                         "Cutting", "Dorman", "Eakley", "Eddie", "Fandrick", "Farwell", "Feigel", "Fenske", "Fillman",
                         "Finley", "Firske", "Flanagan", "Franklin", "Freeman", "Frisbe", "Gore", "Greenwald", "Hahn",
                         "Hammermeister", "Heminger", "Hogue", "Hollister", "Kasper", "Kisro", "Kleeman", "Lake", "Levard",
                         "Lockhart", "Luckstrim", "Lynch", "Mantei", "Marsh", "McBurney", "McCarney", "Moses", "Nickels",
                         "O'Neil", "Olson", "Ozanich", "Patterson", "Patzer", "Peppin", "Porter", "Posch", "Raslo", "Razner",
                         "Rifenberg", "Riley", "Ripley", "Rossini", "Schiltgan", "Schmidt", "Schroeder", "Schwartz", "Shane",
                         "Shattuck", "Shea", "Slaughter", "Smith", "Speltzer", "Stimac", "Stimac","Strenburg","Strong","Swanson",
                        "Tillinghast","Traver","Urton","Vallier","Wagner","Walsted","Wang","Warner","Webber","Welch","Winters","Yarbrough","Yeske"
        ])
        
        if random.random() < 0.5:
            second_first_name = random.choice(name_list)
            full_name = f"{first_name} {second_first_name} {last_name}"
        else:
            full_name = f"{first_name} {last_name}"
        
        embed = discord.Embed(
            title="Random name for Call of Cthulhu",
            description=f":game_die: **{full_name}** :game_die:",
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=embed)

    @commands.command()
    async def cNPC(self, ctx, gender):
        gender = gender.lower()
        
        if gender not in ["male", "female"]:
            await ctx.send("Invalid gender. Use 'male' or 'female'.")
            return
        
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
                "LUCK": ":four_leaf_clover:",
            }
            return stat_emojis.get(stat_name, "")
        
        # Generate random names
        if gender == "male":
            first_name_list = [
                "Aaron", "Abraham", "Addison", "Amos", "Anderson", "Archibald", "August", "Barnabas", "Barney", "Baxter",
                           "Blair", "Caleb", "Cecil", "Chester", "Clifford", "Clinton", "Cornelius", "Curtis", "Dayton", "Delbert",
                           "Douglas", "Dudley", "Ernest", "Eldridge", "Elijah", "Emanuel", "Emmet", "Enoch", "Ephraim", "Everett",
                           "Ezekiel", "Forest", "Gilbert", "Granville", "Gustaf", "Hampton", "Harmon", "Henderson", "Herman",
                           "Hilliard", "Howard", "Hudson", "Irvin", "Issac", "Jackson", "Jacob", "Jeremiah", "Jonah", "Josiah",
                           "Kirk", "Larkin", "Leland", "Leopold", "Lloyd", "Luther", "Manford", "Marcellus", "Martin", "Mason",
                           "Maurice", "Maynard", "Melvin", "Miles", "Milton", "Morgan", "Mortimer", "Moses", "Napoleon", "Nelson",
                           "Newton", "Noble", "Oliver", "Orson", "Oswald", "Pablo", "Percival", "Porter", "Quincy", "Randall",
                           "Reginald", "Richmond", "Rodney", "Roscoe", "Rowland", "Rupert", "Sampson", "Sanford", "Sebastian",
                           "Shelby", "Sidney", "Solomon", "Squire", "Sterling", "Sidney", "Thaddeus", "Walter", "Wilbur", "Wilfred",
                           "Zadok", "Zebedee"
            ]
        else:
            first_name_list = [
                "Adelaide", "Agatha", "Agnes", "Albertina", "Almeda", "Amelia", "Anastasia", "Annabelle", "Asenath", "Augusta",
                             "Barbara", "Bernadette", "Bernice", "Beryl", "Beulah", "Camilla", "Caroline", "Cecilia", "Carmen",
                             "Charity", "Christina", "Clarissa", "Cordelia", "Cynthia", "Daisy", "Dolores", "Doris", "Edith",
                             "Edna", "Eloise", "Elouise", "Estelle", "Ethel", "Eudora", "Eugenie", "Eunice", "Florence", "Frieda",
                             "Genevieve", "Gertrude", "Gladys", "Gretchen", "Hannah", "Henrietta", "Ingrid", "Irene", "Iris",
                             "Ivy", "Jeanette", "Jezebel", "Josephine", "Joyce", "Juanita", "Keziah", "Laverne", "Leonora", "Loretta",
                             "Lucretia", "Mabel", "Madeleine", "Margery", "Marguerite", "Marjorie", "Matilda", "Melinda", "Mercedes",
                             "Mildred", "Millicent", "Muriel", "Myrtle", "Naomi", "Nora", "Octavia", "Ophelia", "Pansy", "Patience",
                             "Pearle", "Phoebe", "Phyllis", "Rosemary", "Ruby", "Sadie", "Selina", "Selma", "Sibyl", "Sylvia", "Tabitha",
                             "Ursula", "Veronica", "Violet", "Virginia", "Wanda", "Wilhelmina", "Winifred"
            ]
        
        first_name = random.choice(first_name_list)
        
        last_name = random.choice([
            "Abraham", "Adler", "Ankins", "Avery", "Barnham", "Bentz", "Bessler", "Blakely", "Bleeker", "Bouche",
                         "Bretz", "Buchman", "Butts", "Caffey", "Click", "Cordova", "Crabtree", "Crankovitch", "Cuthburt",
                         "Cutting", "Dorman", "Eakley", "Eddie", "Fandrick", "Farwell", "Feigel", "Fenske", "Fillman",
                         "Finley", "Firske", "Flanagan", "Franklin", "Freeman", "Frisbe", "Gore", "Greenwald", "Hahn",
                         "Hammermeister", "Heminger", "Hogue", "Hollister", "Kasper", "Kisro", "Kleeman", "Lake", "Levard",
                         "Lockhart", "Luckstrim", "Lynch", "Mantei", "Marsh", "McBurney", "McCarney", "Moses", "Nickels",
                         "O'Neil", "Olson", "Ozanich", "Patterson", "Patzer", "Peppin", "Porter", "Posch", "Raslo", "Razner",
                         "Rifenberg", "Riley", "Ripley", "Rossini", "Schiltgan", "Schmidt", "Schroeder", "Schwartz", "Shane",
                         "Shattuck", "Shea", "Slaughter", "Smith", "Speltzer", "Stimac", "Stimac","Strenburg","Strong","Swanson",
                        "Tillinghast","Traver","Urton","Vallier","Wagner","Walsted","Wang","Warner","Webber","Welch","Winters","Yarbrough","Yeske"
        ])  # ... všechna příjmení
        
        full_name = first_name
        
        # 50% chance for a second first name
        if random.random() < 0.5:
            second_first_name = random.choice(first_name_list)
            full_name = f"{first_name} {second_first_name}"
        
        full_name += f" {last_name}"
        
        # Generate stats
        STR = 5 * sum(sorted([random.randint(1, 6) for _ in range(3)])[1:])
        CON = 5 * sum(sorted([random.randint(1, 6) for _ in range(3)])[1:])
        SIZ = 5 * (sum(sorted([random.randint(1, 6) for _ in range(2)])) + 6)
        DEX = 5 * sum(sorted([random.randint(1, 6) for _ in range(3)])[1:])
        APP = 5 * sum(sorted([random.randint(1, 6) for _ in range(3)])[1:])
        INT = 5 * (sum(sorted([random.randint(1, 6) for _ in range(2)])) + 6)
        POW = 5 * sum(sorted([random.randint(1, 6) for _ in range(3)])[1:])
        EDU = 5 * (sum(sorted([random.randint(1, 6) for _ in range(2)])) + 6)
        LUCK = 5 * sum(sorted([random.randint(1, 6) for _ in range(3)])[1:])
        HP = (CON + SIZ) // 10
        
        stats = {
            "STR": STR,
            "DEX": DEX,
            "CON": CON,
            "INT": INT,
            "POW": POW,
            "CHA": APP,
            "EDU": EDU,
            "SIZ": SIZ,
            "HP": HP,
            "LUCK": LUCK,
        }
        
        stats_embed = "\n".join([f"{get_stat_emoji(stat)} {stat}: {value}" for stat, value in stats.items()])
        
        embed = discord.Embed(
            title="NPC Character Sheet",
            description=f":game_die: **Name:** {full_name}\n\n{stats_embed}",
            color=discord.Color.gold()
        )
        
        await ctx.send(embed=embed)

    @commands.command()
    async def autoChar(self, ctx):
        user_id = str(ctx.author.id)
        
        # Check if the player has a character with all stats at 0
        if user_id not in self.player_stats:
            await ctx.send("You don't have a character created.")
            return
        
        existing_stats = self.player_stats[user_id]
        
        if any(existing_stats[stat] != 0 for stat in ["STR", "DEX", "CON", "INT", "POW", "CHA", "EDU", "SIZ"]):
            await ctx.send("Your character's stats are not all at 0.")
            return
        
        # Generate stats
        STR = 5 * sum(sorted([random.randint(1, 6) for _ in range(3)])[1:])
        CON = 5 * sum(sorted([random.randint(1, 6) for _ in range(3)])[1:])
        SIZ = 5 * (sum(sorted([random.randint(1, 6) for _ in range(2)])) + 6)
        DEX = 5 * sum(sorted([random.randint(1, 6) for _ in range(3)])[1:])
        APP = 5 * sum(sorted([random.randint(1, 6) for _ in range(3)])[1:])
        INT = 5 * (sum(sorted([random.randint(1, 6) for _ in range(2)])) + 6)
        POW = 5 * sum(sorted([random.randint(1, 6) for _ in range(3)])[1:])
        EDU = 5 * (sum(sorted([random.randint(1, 6) for _ in range(2)])) + 6)
        LUCK = 5 * sum(sorted([random.randint(1, 6) for _ in range(3)])[1:])
        HP = (CON + SIZ) // 10
        SAN = POW
        MP = POW // 5
        
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
            }
            return stat_emojis.get(stat_name, "")
        
        # Create an embed to display the generated stats and age modifiers
        stats_embed = discord.Embed(
            title="Character Creation Assistant",
            description="You are about to generate new stats for your character. Do you want to proceed?",
            color=discord.Color.blue()
        )
        stats_embed.add_field(name="STR", value=f"{get_stat_emoji('STR')} :game_die: {STR}", inline=True)
        stats_embed.add_field(name="DEX", value=f"{get_stat_emoji('DEX')} :game_die: {DEX}", inline=True)
        stats_embed.add_field(name="CON", value=f"{get_stat_emoji('CON')} :game_die: {CON}", inline=True)
        stats_embed.add_field(name="INT", value=f"{get_stat_emoji('INT')} :game_die: {INT}", inline=True)
        stats_embed.add_field(name="POW", value=f"{get_stat_emoji('POW')} :game_die: {POW}", inline=True)
        stats_embed.add_field(name="CHA", value=f"{get_stat_emoji('CHA')} :game_die: {APP}", inline=True)
        stats_embed.add_field(name="EDU", value=f"{get_stat_emoji('EDU')} :game_die: {EDU}", inline=True)
        stats_embed.add_field(name="SIZ", value=f"{get_stat_emoji('SIZ')} :game_die: {SIZ}", inline=True)
        stats_embed.add_field(name="HP", value=f"{get_stat_emoji('HP')} :game_die: {HP}", inline=True)
        stats_embed.add_field(name="SAN", value=f"{get_stat_emoji('SAN')} :game_die: {SAN}", inline=True)
        stats_embed.add_field(name="MP", value=f"{get_stat_emoji('MP')} :game_die: {MP}", inline=True)
        stats_embed.add_field(name="LUCK", value=f"{get_stat_emoji('LUCK')} :game_die: {LUCK}", inline=True)
        
        age_modifiers = (
            "15 to 19: Deduct 5 points among STR and SIZ. Deduct 5 points from EDU. Roll twice to generate a Luck score and use the higher value.\n"
            "20s or 30s (20-39 years of age): Make an improvement check for EDU.\n"
            "40s: Make 2 improvement checks for EDU and deduct 5 points among STR, CON or DEX, and reduce APP by 5.\n"
            "50s: Make 3 improvement checks for EDU and deduct 10 points among STR, CON or DEX, and reduce APP by 10.\n"
            "60s: Make 4 improvement checks for EDU and deduct 20 points among STR, CON or DEX, and reduce APP by 15.\n"
            "70s: Make 4 improvement checks for EDU and deduct 40 points among STR, CON or DEX, and reduce APP by 20.\n"
            "80s: Make 4 improvement checks for EDU and deduct 80 points among STR, CON or DEX, and reduce APP by 25."
        )
        
        stats_embed.add_field(name="Age Modifiers", value=age_modifiers, inline=False)
        
        confirmation_message = await ctx.send(embed=stats_embed)
        await confirmation_message.add_reaction("✅")
        await confirmation_message.add_reaction("❌")
        
        def check(reaction, user):
            return user == ctx.author and reaction.message.id == confirmation_message.id and str(reaction.emoji) in ["✅", "❌"]
        
        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60, check=check)
            
            if str(reaction.emoji) == "✅":
                self.player_stats[user_id]["STR"] = STR
                self.player_stats[user_id]["DEX"] = DEX
                self.player_stats[user_id]["CON"] = CON
                self.player_stats[user_id]["INT"] = INT
                self.player_stats[user_id]["POW"] = POW
                self.player_stats[user_id]["CHA"] = APP
                self.player_stats[user_id]["EDU"] = EDU
                self.player_stats[user_id]["SIZ"] = SIZ
                self.player_stats[user_id]["HP"] = HP
                self.player_stats[user_id]["SAN"] = SAN
                self.player_stats[user_id]["MP"] = MP
                self.player_stats[user_id]["LUCK"] = LUCK
                self.save_data()  # Save the updated stats
                
                await ctx.send("New stats have been generated and saved for your character.")
            else:
                await ctx.send("Character creation cancelled.")
        except asyncio.TimeoutError:
            await ctx.send("Character creation timed out.")


    @commands.command()
    async def skillinfo(self, ctx, *, skill_name: str = None):
        # Zde můžete definovat informace o dovednostech (malá písmena)
        skills_info = {
            "Accounting": ":chart_with_upwards_trend:  Base stat - 05% \n Accounting skill grants the ability to understand financial operations, detecting discrepancies and fraud in financial records, and evaluating the financial health of businesses or individuals. It involves inspecting account books to uncover misappropriations, bribes, or discrepancies in claimed financial conditions. Difficulty varies based on how well accounts are concealed. Pushing examples involve spending more time reviewing documents or double-checking findings. Failing a Pushed roll could lead to revealing the investigators' intentions or damaging the accounts, with insane investigators possibly eating them.",
            "Animal Handling": ":chart_with_upwards_trend:  Base stat - 05% \n Animal Handling allows one to command and train domesticated animals like dogs to perform tasks. It's also applicable to other animals like birds, cats, and monkeys. This skill isn't used for riding animals (use the Ride skill instead). Difficulty varies based on the animal's training and familiarity. Pushing examples involve greater personal risk while handling animals. Failing a Pushed roll might result in the animal attacking or escaping. Insane investigators might mimic the behavior of the animal they were trying to control.",
            "Anthropology":":chart_with_upwards_trend:  Base stat - 01% \n Anthropology enables understanding of other cultures through observation. Spending time within a culture allows basic predictions about its ways and morals. Extensive study helps comprehend cultural functioning, allowing predictions of actions and beliefs. Difficulty depends on exposure to the subject culture. Pushing examples involve deeper study or immersion. Failing a Pushed roll might lead to attack or imprisonment by the studied culture or side effects from participating in ceremonies.",
            "Appraise":":chart_with_upwards_trend:  Base stat - 01% \n Appraise skill estimates item values, including quality, materials, and historical significance. It helps determine age, relevance, and detect forgeries. Difficulty varies based on the rarity and complexity of the item. Pushing examples involve validation from experts or testing. Failing a Pushed roll could damage the item, draw attention to it, or trigger its function. Insane investigators might destroy the item, believing it's cursed or refuse to give it up.",
            "Archaeology":":chart_with_upwards_trend:  Base stat - 01% \n Archaeology enables dating and identifying artifacts, detecting fakes, and expertise in setting up excavation sites. Users can deduce the purposes and lifestyles of past cultures from remains. It assists in identifying extinct human languages. Difficulty varies based on time and resources. Pushing examples involve further study or research. Failing a Pushed roll could spoil a site, result in seizure of finds, or attract unwanted attention. If an insane investigator fails, they might keep digging deeper.",
            "Art and Craft":":chart_with_upwards_trend:  Base stat - 05% \n Art and Craft skills involve creating or repairing items, possibly with specializations like acting, painting, forgery, and more. Skills can be used to make quality items, duplicate items, or create fakes. Different difficulty levels correspond to crafting different qualities of items. Pushing examples include reworking items or conducting additional research. Failing a Pushed roll might waste time and resources or offend customers. Insane investigators might create unusual works that provoke strong reactions.",
            "Artillery":":chart_with_upwards_trend:  Base stat - 01% \n Artillery is the operation of field weapons in warfare. The user is experienced in operating large weapons requiring crews. Specializations exist based on the period, including cannon and rocket launcher. Difficulty varies with maintenance and conditions. This combat skill cannot be pushed.",
            "Charm":":chart_with_upwards_trend:  Base stat - 15% \n Charm involves physical attraction, seduction, flattery, or a warm personality to influence someone. It can be used for persuasion, bargaining, and haggling. Opposed by Charm or Psychology skills. Difficulty levels depend on the context. Pushing examples involve extravagant flattery, offering gifts, or building trust. Failure might lead to offense, exposure, or interference by third parties. If an insane investigator fails a pushed roll, they might fall in love with the target.",
            "Climb":":chart_with_upwards_trend:  Base stat - 20% \n Climb skill allows a character to ascend vertical surfaces using ropes, climbing gear, or bare hands. Conditions like surface firmness, handholds, weather, and visibility affect the difficulty. Failing on the first roll might indicate the climb's impossibility. A pushed roll failure likely results in a fall with damage. A successful Climb roll usually completes the climb in one attempt. Increased difficulty applies for challenging or longer climbs. Pushing examples include reassessing the climb or finding alternate routes. Consequences of failing a Pushed roll could be falling and suffering damage, losing possessions, or becoming stranded. If an insane investigator fails a pushed roll, they might hold on for dear life and scream.",
            "Computer Use":":chart_with_upwards_trend:  Base stat - 05% \n This skill is for programming in computer languages, analyzing data, breaking into secure systems, exploring networks, and detecting intrusions, back doors, and viruses. The Internet provides vast information, often requiring combined rolls with Library Use. It's not necessary for regular computer use. Difficulty varies for tasks like programming and hacking into networks. Pushing examples include using shortcuts or untested software. Consequences of failing a Pushed roll might include erasing files, leaving evidence, or infecting the system with a virus. If an insane investigator fails a pushed roll, they might become absorbed in the virtual world.",
            "Credit Rating":":chart_with_upwards_trend:  Base stat - 00% \n Credit Rating represents the investigator's financial status and confidence. It's not a skill per se, but a measure of wealth and prosperity. A high Credit Rating can aid in achieving goals using financial status. It can also substitute for APP for first impressions. Credit Rating varies for different occupations and can change over time. A high Credit Rating can open doors and provide resources. It's not meticulously tracked in gameplay but helps gauge the investigator's financial reach. Failing a Pushed roll might lead to negative consequences, such as involvement with loan sharks or loss of possessions. If an insane investigator fails a pushed roll, they might become overly generous with their money.",
            "Cthulhu Mythos":":chart_with_upwards_trend:  Base stat - 00% \n This skill reflects understanding of the Cthulhu Mythos, the Lovecraftian cosmic horrors. Points in this skill are gained through encounters, insanity, insights, and reading forbidden texts. An investigator's Sanity can't exceed 99 minus their Cthulhu Mythos skill. Successful rolls allow identification of Mythos entities, knowledge about them, remembering facts, identifying spells, and manifesting magical effects. The skill starts at zero and is often low. Regular difficulty rolls are common, while hard difficulty might involve identifying entities from rumors or finding vulnerabilities through research. Failing a Pushed roll can lead to dangerous consequences, like exposing oneself to harm or activating spells inadvertently. If an insane investigator fails a pushed roll, they might experience a vision or revelation about the Cthulhu Mythos.",
            "Demolitions":":chart_with_upwards_trend:  Base stat - 01% \n This skill involves safely setting and defusing explosive charges, including mines and military-grade demolitions. Skilled individuals can rig charges for demolition, clearing tunnels, and constructing explosive devices. Regular difficulty might involve defusing explosive devices or knowing where to place charges for maximum effect, while hard difficulty could involve defusing a device under time pressure. Failing a pushed roll when defusing could result in an explosion, while improper detonation might result from placing charges. If an insane investigator fails a pushed roll, they might come up with eccentric ways to deliver explosives.",
            "Disguise":":chart_with_upwards_trend:  Base stat - 05% \n This skill is used when the investigator wants to appear as someone else. It involves changing posture, costume, voice, and possibly makeup or fake ID. Regular difficulty involves convincing strangers of the disguise's authenticity, while hard difficulty requires convincing professionals in face-to-face meetings. Pushing examples could include thorough preparation, stealing personal items, or feigning illness to distract observers. Consequences of failing a pushed roll might involve arrest, offense, or unintended consequences due to the disguise. If an insane investigator fails a pushed roll, they might struggle to recognize their own face even without the disguise.",
            "Diving":":chart_with_upwards_trend:  Base stat - 01% \n This skill covers the use of diving equipment for underwater swimming, including navigation, weighting, and emergency procedures. It includes both historical diving suits and modern scuba diving. Regular difficulty applies to routine dives with proper equipment, while hard difficulty might involve dangerous conditions or poorly maintained gear. Pushing examples could be pushing equipment limits or seeking professional assistance. Consequences of failing a pushed roll might involve becoming trapped underwater or suffering decompression sickness. If an insane investigator fails a pushed roll, they might believe they can understand whale-song.",
            "Dodge":":chart_with_upwards_trend:  Base stat - half DEX% \n Dodge allows an investigator to instinctively evade blows, projectiles, and attacks. It's mostly used in combat as part of opposed rolls. There's no set difficulty level for Dodge, and it cannot be pushed. The skill is related to an investigator's Dexterity stat and can increase through experience.",
            "Drive Auto":":chart_with_upwards_trend:  Base stat - 20% \n This skill allows the investigator to drive a car or light truck, make ordinary maneuvers, and handle common vehicle issues. It's used for driving in various situations, including escaping pursuers or tailing someone. Regular difficulty might involve weaving through light traffic, while hard difficulty could involve weaving through heavy traffic. Pushing examples might involve driving to the vehicle's limit. Consequences of failing a Pushed roll might involve crashing, being pursued by the police, or other complications. If an insane investigator fails a pushed roll, they might act as if they're driving a stationary vehicle and making engine noises.",
            "Electrical Repair":":chart_with_upwards_trend:  Base stat - 10% \n This skill allows the investigator to repair or reconfigure electrical equipment like auto ignitions, electric motors, and burglar alarms. It's separate from Electronics and involves physical repairs rather than dealing with microchips or circuit boards. Regular difficulty tasks include repairing or creating standard electrical devices, while hard difficulty tasks involve more significant repairs or working without proper tools. Pushing examples might involve taking longer to repair or researching new methods. Consequences of failing a Pushed roll could lead to electric shock or damaging the equipment further. If an insane investigator fails a pushed roll, they might attempt to harness the power of living organisms into devices.",
            "Electronics":":chart_with_upwards_trend:  Base stat - 01% \n Electronics skill is for troubleshooting, repairing, and creating electronic devices. It's different from Electrical Repair, as it involves microchips, circuit boards, and modern technology. Regular difficulty tasks might involve minor repairs, while hard difficulty tasks might involve jury-rigging devices with scavenged parts. The availability of correct parts and instructions is essential. Successful skill use can lead to repairs, constructions, or modifications of electronic devices. If an investigator has the right parts and instructions, constructing a standard computer might not require a skill roll. Consequences of failing a Pushed roll might involve damaging circuitry or creating unintended outcomes. If an insane investigator fails a pushed roll, they might become paranoid about electronic surveillance.",
            "Fast Talk":":chart_with_upwards_trend:  Base stat - 05% \n Fast Talk involves verbal trickery, deception, and misdirection to achieve short-term effects. It can be used to deceive, haggle, or manipulate people into temporary actions. The effect is usually temporary, and the target might realize the trick after a while. Regular and hard difficulty levels are similar to other social skills. Pushing examples could involve talking outlandishly or getting close to the target. Fast Talk can't be changed to other skills mid-discussion. Failing a pushed roll might lead to offense or violence. If an insane investigator fails a pushed roll, they might start hurling abusive phrases.",
            "Fighting":":chart_with_upwards_trend:  Base stat - 0X% \n Fighting skills cover melee combat and come in different specializations based on the type of weapon or fighting style. There's no generic Fighting skill; instead, characters choose specialized skills like Axe, Brawl, Chainsaw, Flail, Garrote, Spear, Sword, and Whip. These skills determine proficiency in various weapons and combat styles. They can't be pushed and involve opposed rolls in combat.",
            "Firearms":":chart_with_upwards_trend:  Base stat - 0X% \n Firearms skill covers various types of firearms, bows, and crossbows. Characters choose specialized skills like Bow, Handgun, Heavy Weapons, Flamethrower, Machine Gun, Rifle/Shotgun, and Submachine Gun. These skills determine proficiency in using different firearms and ranged weapons. They can't be pushed and involve opposed rolls in combat.",
            "First Aid":":chart_with_upwards_trend:  Base stat - 30% \n First Aid skill enables an investigator to provide emergency medical care, like splinting broken limbs, stopping bleeding, treating burns, and more. Successful First Aid treatment must be delivered within an hour, granting 1 hit point. Two people can work together for First Aid, with either one rolling successfully for a joint success. Successful use of First Aid can rouse an unconscious person to consciousness. First Aid can stabilize a dying character for an hour, granting 1 temporary hit point, and can be repeated until stabilization or death. Successful First Aid can save the life of a dying character, but further treatment with the Medicine skill or hospitalization is required afterward.",
            "History":":chart_with_upwards_trend:  Base stat - 05% \n History skill allows an investigator to remember the significance of places, people, and events. Regular difficulty tasks involve recalling pertinent information, while hard difficulty tasks involve knowing obscure details. Pushing examples might involve taking more time for research or consulting experts. Consequences of failing a Pushed roll could include wasting time and resources or providing erroneous information. If an insane investigator fails a pushed roll, they might believe they're displaced in time or start acting and speaking in an archaic manner.",
            "Hypnosis":":chart_with_upwards_trend:  Base stat - 01% \n Hypnosis skill allows the user to induce a trancelike state in a target, increasing suggestibility and relaxation. It can be used as hypnotherapy to reduce the effects of phobias or manias, with a series of successful sessions potentially curing the patient. Hypnosis can be opposed by Psychology or POW for unwilling subjects. Pushing examples might involve using lights, props, or drugs to enhance the effect. Consequences of failing a Pushed roll could include triggering forgotten memories or traumas or even leading the target to dangerous situations. If an insane investigator fails a pushed roll, they might regress to a childlike state until treated.",
            "Intimidate":":chart_with_upwards_trend:  Base stat - 05% \n Intimidation involves using physical force, psychological manipulation, or threats to frighten or compel someone. It's opposed by Intimidate or Psychology. Successful intimidation can be used to achieve specific outcomes, like lowering prices or gaining compliance. Backing up threats with weapons or incentives can reduce the difficulty level. Pushing an Intimidation roll might lead to unintended consequences, such as carrying out threats beyond the intended level. Failure consequences could involve accidental harm, a target's unexpected resistance, or backlash from the target.",
            "Jump":":chart_with_upwards_trend:  Base stat - 20% \n Jumping skill allows investigators to perform various types of jumps, both vertically and horizontally. Regular, hard, and extreme difficulties determine the distances and heights that can be successfully jumped. Jump can also be used to mitigate fall damage when falling from heights. Regular success might involve safely jumping down your own height, while extreme success could mean leaping twice your height. Falling damage can be reduced with a successful Jump roll.",
            "Language (Other)":":chart_with_upwards_trend:  Base stat - 01% \n This skill represents a character's ability to understand, speak, read, and write in a language other than their own. The exact language must be specified when choosing this skill. Different levels of skill allow for different degrees of proficiency, from basic communication to fluency and even passing as a native speaker. Success at the skill can encompass understanding an entire book or having a conversation. Different levels of success in Other Languages skill are also described.",
            "Language (Own)":":chart_with_upwards_trend:  Base stat - EUD% \n This skill represents an investigator's proficiency in their own language. The skill percentage starts at the investigator's EDU characteristic, and they understand, speak, read, and write in their own language at that percentage or higher. No skill roll is normally required to use one's own language, even when dealing with technical or uncommon terms. However, if a document is particularly difficult to read or in an archaic dialect, the Keeper may require a roll.",
            "Law":":chart_with_upwards_trend:  Base stat - 05% \n The Law skill represents a character's knowledge of relevant laws, precedents, legal maneuvers, and court procedures. It's used to understand and utilize legal details. This skill is important for legal professions and political office. The difficulty level may increase when using Law in a foreign country. The skill can be used for cross-examining witnesses and understanding legal situations.",
            "Library Use":":chart_with_upwards_trend:  Base stat - 20% \n Library Use allows investigators to locate specific information, such as books, newspapers, or references, in libraries or collections. The skill can be used to find locked cases or rare-book collections, though access might require other skills like Persuade or Credit Rating. Regular difficulty involves locating information, while hard difficulty applies when searching in a disorganized library or under time pressure.",
            "Listen":":chart_with_upwards_trend:  Base stat - 20% \n Listen skill measures an investigator's ability to interpret and understand sounds, including conversations and distant noises. High Listen skill indicates heightened awareness. The skill can be used to detect approaching sounds or eavesdrop on conversations. Listen can be opposed by the Stealth skill when someone is trying to remain hidden.",
            "Locksmith":":chart_with_upwards_trend:  Base stat - 01% \n Locksmith skill allows an investigator to open locks, repair them, create keys, and utilize lock-picking tools. Regular difficulty involves opening or repairing standard locks, while hard difficulty applies to high-security locks. Pushing a roll might involve taking longer, dismantling the lock, or using force to open it.",
            "Lore":":chart_with_upwards_trend:  Base stat - 01% \n The Lore skill represents expert understanding of a specialized subject that falls outside the normal bounds of human knowledge. Specializations can include areas like Dream Lore, Necronomicon Lore, UFO Lore, and more. This skill is used to test an investigator's knowledge of specific topics that are central to the campaign or to convey the knowledge of non-player characters to the Keeper.",
            "Mechanical Repair":":chart_with_upwards_trend:  Base stat - 10% \n This skill allows investigators to repair machines, perform basic carpentry and plumbing, and construct or repair items. It's a companion skill to Electrical Repair and is used for fixing devices and creating new ones. Basic carpentry and plumbing projects are also within the scope of this skill. Mechanical Repair can open basic locks, but for more complex locks, refer to the Locksmith skill.",
            "Medicine":":chart_with_upwards_trend:  Base stat - 01% \n The Medicine skill involves diagnosing and treating accidents, injuries, diseases, poisonings, etc. It allows the user to provide medical care and make public health recommendations. Successful use of the Medicine skill can recover hit points, and the skill is useful for treating major wounds. A successful roll with Medicine provides a bonus die on a weekly recovery roll. The skill takes a minimum of one hour to use for treatment.",
            "Natural World":":chart_with_upwards_trend:  Base stat - 10% \n Natural World represents an investigator's traditional and general knowledge of plants and animals in their environment. It's used to identify species, habits, and habitats in a more folkloric and enthusiastic manner. This skill is not as scientifically accurate as disciplines like Biology or Botany. Natural World can be used to judge the quality of animals, plants, or collections.",
            "Navigate":":chart_with_upwards_trend:  Base stat - 10% \n Navigate skill enables an investigator to find their way in various weather conditions, day or night. The skill involves using landmarks, astronomical tables, charts, instruments, and modern technology for mapping and location. It can be used to measure and map an area. Familiarity with the area grants a bonus die. This skill can also be used as concealed rolls by the Keeper.",
            "Occult":":chart_with_upwards_trend:  Base stat - 05% \n The Occult skill involves recognizing occult paraphernalia, words, concepts, and folk traditions. It's used to identify magical grimoires, occult codes, and general knowledge of secret traditions. The skill doesn't apply to Cthulhu Mythos magic. Successful use of Occult can be used for bargaining and haggling as well.",
            "Operate Heavy Machinery":":chart_with_upwards_trend:  Base stat - 01% \n This skill is required to operate large-scale construction machinery, such as tanks, backhoes, and steam shovels. It's also used for complex machinery, like ship engines. Operating heavy machinery successfully involves making skill rolls, especially in challenging conditions. Failure can result in damage or accidents.",
            "Persuade":":chart_with_upwards_trend:  Base stat - 10% \n Persuade is used to convince others about specific ideas or concepts through reasoned argument and discussion. It's a skill that takes time and can be used for bargaining and haggling. Successful persuasion can have lasting effects on the target's beliefs. This skill can be used to haggle prices down.",
            "Pilot":":chart_with_upwards_trend:  Base stat - 01% \n The Pilot skill is specialized for flying or operating specific types of vehicles, such as aircraft or boats. Each specialization starts at 01%. The success of pilot rolls depends on the situation and conditions, with bad weather or damage raising the difficulty level.",
            "Psychoanalysis":":chart_with_upwards_trend:  Base stat - 01% \n Psychoanalysis involves emotional therapies and can return Sanity points to investigator patients. It can be used to cope with phobias or see through delusions for a brief period. Psychoanalysis cannot increase a character's Sanity points above 99 (Cthulhu Mythos). Successful therapy can help during indefinite insanity.",
            "Psychology":":chart_with_upwards_trend:  Base stat - 10% \n Psychology allows the user to study an individual and form ideas about their motives and character. It can be used to oppose social interaction rolls and see through disguises. The skill roll's difficulty level depends on the target's relevant social interaction skill. It's a skill that can be used to understand and predict behavior.",
            "Read Lips":":chart_with_upwards_trend:  Base stat - 01% \n This skill allows the investigator to understand spoken communication by observing lip movements. It can be used to eavesdrop on conversations or silently communicate with another proficient individual. The skill's effectiveness depends on the situation, visibility, and distance.",
            "Ride":":chart_with_upwards_trend:  Base stat - 05% \n The Ride skill is used to handle and ride animals like saddle horses, donkeys, or mules. It involves knowledge of animal care, riding gear, and riding techniques. Falling from a mount due to an accident or failed skill roll can result in hit point loss. The success of a ride roll depends on the speed and terrain. Riding side-saddle or on unfamiliar mounts increases the difficulty.",
            "Science Specializations":":chart_with_upwards_trend:  Base stat - X% \n Science is a broad skill category that represents knowledge and expertise in various scientific disciplines. Each specialization focuses on a particular field of science and grants the character practical and theoretical abilities within that field. Characters can spend skill points to purchase specialization in a specific field. The generic Science skill cannot be directly purchased and instead, characters must choose from the available specializations. Many specialties overlap, and knowledge in one field may contribute to understanding another related field. \n Astronomy (01%): This specialization involves understanding celestial bodies, their positions, and movements. The character can identify stars, planets, and predict celestial events like eclipses. More advanced knowledge might include concepts of galaxies and extraterrestrial life. \n Biology (01%): The study of life and living organisms. This specialization covers various sub-disciplines such as cytology, genetics, microbiology, and more. Characters with this specialization can analyze organisms, study their functions, and even develop vaccines or treatments for diseases. \n Botany (01%): Botany focuses on plant life. The character can identify plant species, understand their growth patterns, reproductive mechanisms, and chemical properties. This specialization is useful for recognizing plants, their uses, and potential dangers. \n Chemistry (01%): The study of substances, their composition, properties, and interactions. Characters with this specialization can create chemical compounds, analyze unknown substances, and understand chemical reactions. This includes making simple explosives, poisons, and acids. \n Cryptography (01%): This specialization involves the study of secret codes and languages. Characters can create, decipher, and analyze codes used to conceal information. This skill is crucial for cracking complex codes and understanding hidden messages. \n Engineering (01%): While technically not a science, engineering involves practical applications of scientific principles. Characters with this specialization can design and build structures, machines, and materials for various purposes. \n Forensics (01%): Forensics focuses on analyzing evidence, often related to crime scenes. This specialization includes the examination of fingerprints, DNA, hair, and body fluids. Characters can identify and interpret evidence for legal disputes. \n Geology (01%): Geology encompasses the study of Earth's structure, rocks, minerals, and geological processes. Characters with this specialization can evaluate soil, recognize fossils, and anticipate geological events like earthquakes and volcanic eruptions. \n Mathematics (10%): Mathematics involves the study of numbers, logic, and mathematical theories. Characters with this specialization can solve complex mathematical problems, identify patterns, and decrypt intricate codes. \n Meteorology (01%): This specialization covers the scientific study of the atmosphere and weather patterns. Characters can predict weather changes, forecast rain, snow, and fog, and understand atmospheric phenomena. \n Pharmacy (01%): Pharmacy focuses on chemical compounds and their effects on living organisms. Characters with this specialization can formulate medications, identify toxins, and understand pharmaceutical properties and side effects. \n Physics (01%): Physics involves the study of physical phenomena such as motion, magnetism, electricity, and optics. Characters with this specialization have theoretical understanding and can create experimental devices to test ideas. \n Zoology (01%): Zoology centers on the study of animals, their behaviors, structures, and classifications. Characters with this specialization can identify animal species, understand behaviors, and analyze tracks and markings.",
            "Sleight of Hand":":chart_with_upwards_trend:  Base stat - 10% \n This skill enables the user to conceal and manipulate objects using various techniques like palming, pick-pocketing, and creating illusions. It includes hiding items with debris or fabric and performing clandestine actions such as pick-pocketing or hiding objects on a person.",
            "Spot Hidden":":chart_with_upwards_trend:  Base stat - 25% \n Spot Hidden allows the character to notice hidden clues, secret doors, or concealed objects. The skill is essential for detecting subtle details, even in challenging environments. It can also be used to spot hidden intruders or recognize hidden dangers.",
            "Stealth":":chart_with_upwards_trend:  Base stat - 20% \n Stealth involves moving silently and hiding effectively to avoid detection. This skill is crucial for remaining unnoticed by others, whether it's sneaking past guards or hiding from pursuers. Characters can use Stealth to move quietly and maintain a low profile.",
            "Survival":":chart_with_upwards_trend:  Base stat - 10% \n Survival is specialized for different environments such as desert, sea, or arctic conditions. It provides the knowledge needed to survive in extreme situations, including finding shelter, food, and water. Characters can adapt to their chosen environment and overcome challenges specific to it.",
            "Swim":":chart_with_upwards_trend:  Base stat - 20% \n Swim skill represents the ability to navigate through water and other liquids. It's useful in situations where characters need to cross bodies of water, avoid drowning, or swim against currents. Successful Swim rolls can prevent drowning and navigate dangerous waters.",
            "Throw":":chart_with_upwards_trend:  Base stat - 20% \n The Throw skill involves accurately hitting a target with a thrown object. Characters can use this skill to throw weapons like knives or spears and hit specific targets. The distance and accuracy of the throw depend on the skill level and the weight of the object.",
            "Track":":chart_with_upwards_trend:  Base stat - 10% \n Track allows characters to follow trails left by people, animals, or vehicles. This skill is useful for pursuing individuals or uncovering hidden paths. The difficulty of tracking depends on factors such as time passed and the condition of the terrain.",
        }
        if skill_name is None:
            # Pokud není poskytnuto žádné jméno dovednosti, vypíše seznam všech dovedností
            skills_list = ", ".join(skills_info.keys())
            response = f":zap: List of skills: :zap: \n{skills_list}"
        else:
            skill_description = skills_info.get(skill_name, "Skill not found.")
            
            response = f":zap: Skill Info: {skill_name}\n {skill_description}"
        
        embed = discord.Embed(description=response, color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(aliases=["cocc"])
    async def coccupations(self, ctx, *, occupation_name: str = None):
        occupations_info = {
            "accountant": {
                "description": "Either employed within a business or working as a freelance consultant with a portfolio of self-employed clients or businesses...",
                "skill_points": "EDU × 4",
                "credit_rating": "30–70",
                "suggested_contacts": "Business associates, legal professions, financial sector (bankers, other accountants).",
                "skills": "Accounting, Law, Library Use, Listen, Persuade, Spot Hidden, any two other skills as personal or era specialties (e.g. Computer Use)."
            },
            # Přidejte další povolání a jejich informace...
        }
        
        if occupation_name is None:
            occupations_list = ", ".join(occupations_info.keys())
            response = f"List of occupations:\n{occupations_list}"
            embed_title = "Occupations List"
        else:
            lower_occupation_name = occupation_name.lower()
            occupation_info = occupations_info.get(lower_occupation_name)
            if occupation_info is None:
                response = "Occupation not found."
            else:
                embed_title = occupation_name.capitalize()
                description = occupation_info["description"]
                skill_points = occupation_info["skill_points"]
                credit_rating = occupation_info["credit_rating"]
                suggested_contacts = occupation_info.get("suggested_contacts", "None")
                skills = occupation_info["skills"]
                response = (
                    f":clipboard: Description: {description}\n"
                    f":black_joker: Occupation Skill Points: {skill_points}\n"
                    f":moneybag: Credit Rating: {credit_rating}\n"
                    f":telephone: Suggested Contacts: {suggested_contacts}\n"
                    f":zap: Skills: {skills}"
                )
        
        embed = discord.Embed(title=embed_title, description=response, color=discord.Color.green())
        await ctx.send(embed=embed)
            
