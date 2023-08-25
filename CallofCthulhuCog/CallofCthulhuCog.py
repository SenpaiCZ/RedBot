from redbot.core import commands
import random
import discord
import json
import os
import asyncio

class CallofCthulhuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "/home/pi/.local/share/SenpaiBot/cogs/CogManager/cogs/CallofCthulhuCog/player_stats.json" 

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
            await ctx.send("You need to create a new Investigator using !newInv first.")
            return
        
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
                "description": "Either employed within a business or working as a freelance consultant with a portfolio of self-employed clients or businesses. Diligence and an attention to detail means that most accountants can make good researchers, being able to support investigations through the careful analysis of personal and business transactions, financial statements, and other records.",
                "skill_points": "EDU × 4",
                "credit_rating": "30–70",
                "suggested_contacts": "Business associates, legal professions, financial sector (bankers, other accountants).",
                "skills": "Accounting, Law, Library Use, Listen, Persuade, Spot Hidden, any two other skills as personal or era specialties (e.g. Computer Use)."
            },
            "acrobat": {
                "description": "Acrobats may be either amateur athletes competing in staged meets—possibly even the Olympics—or professionals employed within the entertainment sector (e.g. circuses, carnivals, theatrical performances).",
                "skill_points": "EDU × 2 + DEX × 2",
                "credit_rating": "9–20",
                "suggested_contacts": "Amateur athletic circles, sports writers, circuses, carnivals.",
                "skills": "Climb, Dodge, Jump, Throw, Spot Hidden, Swim, any two other skills as personal or era specialties."
            },
            "actor": {
                "description": "Usually a stage or film actor. Many stage actors have a background in the classics and, considering themselves 'legitimate,' have a tendency to look down upon the commercial efforts of the film industry. By the late twentieth century, this is diminished, with film actors able to command greater respect and higher fees. Movie stars and the film industry have long captured the interest of people across the world. Many stars are made overnight and most of them lead flashy, high-profile lives, always in the media spotlight. In the 1920s, the theatrical center of the U.S. is in New York City, although there are major stages in most cities across the country. A similar situation exists in England, with touring repertory companies traveling the counties, and London is the heart of theatrical shows. Touring companies travel by train, presenting new plays, as well as classics by Shakespeare and others. Some companies spend considerable amounts of time touring foreign parts, such as Canada, Hawaii, Australia, and Europe. With the introduction of 'talkies' in the latter part of the 1920s, many stars of the silent film era cannot cope with the transition to sound. The arm-waving histrionics of silent actors give way to more subtle characterizations. John Garfield and Francis Bushman are forgotten for new stars, such as Gary Cooper and Joan Crawford.",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "9–40",
                "suggested_contacts": "Theatre industry, newspaper arts critics, actor’s guild or union.",
                "skills": "Art/Craft (Acting), Disguise, Fighting, History, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any one other skill as a personal or era specialty."
            },
            "film_star": {
                "description": "Film stars are usually actors who have gained fame and recognition in the film industry. Many stars are made overnight and most of them lead flashy, high-profile lives, always in the media spotlight...",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "20–90",
                "suggested_contacts": "Film industry, media critics, writers.",
                "skills": "Art/Craft (Acting), Disguise, Drive Auto, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any two other skills as personal or era specialties (e.g. Ride or Fighting)."
            },
           "agency_detective": {
                "description": "Numerous well-known detective agencies exist around the world, with probably the most famous being the Pinkerton and Burns agencies (merged into one in modern times). Large agencies employ two types of agents: security guards and operatives. Guards are uniformed patrolmen, hired by companies and individuals to protect property and people against burglars, assassins, and kidnappers. Use the Uniformed Police Officer’s (page 87) description for these characters. Company Operatives are plainclothes detectives, sent out on cases requiring them to solve mysteries, prevent murders, locate missing people, and so on.",
                "skill_points": "EDU × 2 + (STR × 2 or DEX × 2)",
                "credit_rating": "20–45",
                "suggested_contacts": "Local law enforcement, clients.",
                "skills": "One interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Fighting (Brawl), Firearms, Law, Library Use, Psychology, Stealth, Track."
            },
            "alienist": {
                "description": "In the 1920s, 'alienist' is the term given for those who treat mental illness (early psychiatrists). Psychoanalysis is barely known in the U.S., and its basis in sexual life and toilet training is felt to be indecent. Psychiatry, a standard medical education augmented by behaviorism, is more common. Intellectual wars rage between alienists, psychiatrists, and neurologists.",
                "skill_points": "EDU × 4",
                "credit_rating": "10–60",
                "suggested_contacts": "Others in the field of mental illness, medical doctors, and occasionally detectives in law enforcement.",
                "skills": "Law, Listen, Medicine, Other Language, Psychoanalysis, Psychology, Science (Biology), (Chemistry)."
            },
            "animal_trainer": {
                "description": "May be employed by film studios, a traveling circus, a horse stable, or possibly working freelance. Whether training guide dogs for the blind or teaching a lion to jump through a flaming hoop, the animal trainer usually works alone, spending long hours in close proximity with the animals in their care.",
                "skill_points": "EDU × 2 + (APP × 2 or POW × 2)",
                "credit_rating": "10–40",
                "suggested_contacts": "Zoos, circus folk, patrons, actors.",
                "skills": "Animal Handling, Jump, Listen, Natural World, Science (Zoology), Stealth, Track, any one other skill as a personal or era specialty."
            },
            "antiquarian": {
                "description": "A person who delights in the timeless excellence of design and execution, and in the power of ancient lore. Probably the most Lovecraft-like occupation available to an investigator. An independent income allows the antiquarian to explore things old and obscure, perhaps sharpening their focus down particular lines of enquiry based on personal preference and interest. Usually a person with an appreciative eye and a swift mind, who frequently finds mordant or contemptuous humor in the foolishness of the ignorant, the pompous, and the greedy.",
                "skill_points": "EDU × 4",
                "credit_rating": "30–70",
                "suggested_contacts": "Booksellers, antique collectors, historical societies.",
                "skills": "Appraise, Art/Craft (any), History, Library Use, Other Language, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Spot Hidden, any one other skill as a personal or era specialty."
            },
            "antique_dealer": {
                "description": "Antique dealers usually own their own shop, retail items out of their homes, or go on extended buying trips, making a profit on reselling to urban stores.",
                "skill_points": "EDU × 4",
                "credit_rating": "30–50",
                "suggested_contacts": "Local historians, other antique dealers, possibly criminal fences.",
                "skills": "Accounting, Appraise, Drive Auto, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), History, Library Use, Navigate."
            },
            "archaeologist": {
                "description": "The study and exploration of the past. Primarily the identification, examination, and analysis of recovered materials relating to human history. The work involves painstaking research and meticulous study, not to mention a willing attitude to getting one’s hands dirty. In the 1920s, successful archaeologists became celebrities, seen as explorers and adventurers. While some used scientific methods, many were happy to apply brute force when unveiling the secrets of the past—a few less reputable types even used dynamite. Such bullish behavior would be frowned upon in modern times.",
                "skill_points": "EDU × 4",
                "credit_rating": "10–40",
                "suggested_contacts": "Patrons, museums, universities.",
                "skills": "Appraise, Archaeology, History, Other Language (any), Library Use, Spot Hidden, Mechanical Repair, Navigate or Science (e.g. chemistry, physics, geology, etc.)"
            },
            "architect": {
                "description": "Architects are trained to design and plan buildings, whether a small conversion to a private house or a multi-million dollar construction project. The architect will work closely with the project manager and oversee the construction. Architects must be aware of local planning laws, health and safety regulation, and general public safety. Some may work for large firms or work freelance. A lot will depend on reputation. In the 1920s, many try and go it alone, working out of their house or a small office. Few manage to sell the grandiose designs they all nurse. Architecture may also encompass specialist areas like naval architecture and landscape architecture.",
                "skill_points": "EDU × 4",
                "credit_rating": "30–70",
                "suggested_contacts": "Local building and city engineering departments, construction firms.",
                "skills": "Accounting, Art/Craft (Technical Drawing), Law, Own Language, Computer Use or Library Use, Persuade, Psychology, Science (Mathematics)."
            },
            "artist": {
                "description": "May be a painter, sculptor, etc. Sometimes self-absorbed and driven with a particular vision, sometimes blessed with a great talent that is able to inspire passion and understanding. Talented or not, the artist’s ego must be hardy and strong to surmount initial obstacles and critical appraisal, and to keep them working if success arrives. Some artists care not for material enrichment, while others have a keen entrepreneurial streak.",
                "skill_points": "EDU × 2 + (DEX × 2 or POW × 2)",
                "credit_rating": "9–50",
                "suggested_contacts": "Art galleries, critics, wealthy patrons, the advertising industry.",
                "skills": "Art/Craft (any), History or Natural World, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Other Language, Psychology, Spot Hidden, any two other skills as personal or era specialties."
            },
            "asylum_attendant": {
                "description": "Although there are private sanitariums for those few who can afford them, the vast bulk of the mentally ill are housed in state and county facilities. Aside from a few doctors and nurses, they employ a large number of attendants, often chosen more for their strength and size rather than medical learning.",
                "skill_points": "EDU × 2 + (STR × 2 or DEX × 2)",
                "credit_rating": "8–20",
                "suggested_contacts": "Medical staff, patients, and relatives of patients. Access to medical records, as well as drugs and other medical supplies.",
                "skills": "Dodge, Fighting (Brawl), First Aid, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Listen, Psychology, Stealth."
            },
           "athlete": {
                "description": "Probably plays in a professional baseball, football, cricket, or basketball team. This may be a major league team with a regular salary and national attention or—particularly in the case of 1920s baseball—one of many minor league teams, some of them owned and operated by major league owners. The latter pay barely enough to keep players fed and on the team. Successful professional athletes will enjoy a certain amount of celebrity within the arena of their expertise—more so in the present day where sporting heroes stand side by side with film stars on red carpets around the world.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–70",
                "suggested_contacts": "Sports personalities, sports writers, other media stars.",
                "skills": "Climb, Jump, Fighting (Brawl), Ride, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Swim, Throw, any one other skill as a personal or era specialty."
            },
            "author": {
                "description": "As distinct from the journalist, the author uses words to define and explore the human condition, especially the range of human emotions. Their labors are solitary and the rewards solipsistic: only a relative handful make much money in the present day, though in previous eras the trade once provided a regular living wage. The work habits of authors vary widely. Typically an author might spend months or years researching in preparation for a book, then withdrawing for periods of intense creation.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–30",
                "suggested_contacts": "Publishers, critics, historians, etc.",
                "skills": "Art (Literature), History, Library Use, Natural World or Occult, Other Language, Own Language, Psychology, any one other skill as a personal or era specialty."
            },
            "bartender": {
                "description": "Normally not the owner of the bar, the bartender is everyone’s friend. For some it’s a career or their business, for many it's a means to an end. In the 1920s the profession is made illegal by the Prohibition Act; however, there’s no shortage of work for a bartender, as someone has to serve the drinks in the speakeasies and secret gin joints.",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "8–25",
                "suggested_contacts": "Regular customers, possibly organized crime.",
                "skills": "Accounting, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Fighting (Brawl), Listen, Psychology, Spot Hidden, any one other skill as a personal or era specialty."
            },
            "big_game_hunter": {
                "description": "Big game hunters are skilled trackers and hunters who usually earn their living leading safaris for wealthy clients. Most are specialized in one part of the world, such as the Canadian woods, African plains, and other locales. Some hunters may work for the black market, capturing live exotic species for private collectors, or trading in illegal or morally objectionable animal products like skins, ivory, and the like—although in the 1920s such activities were more common and were permissible under most countries’ laws. Although the great white hunter is the quintessential type, others may be simply local indigenous people who escort hunters through the backwoods of the Yukon in search of moose or bear.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "20–50",
                "suggested_contacts": "Foreign government officials, game wardens, past (usually wealthy) clients, blackmarket gangs and traders, zoo owners.",
                "skills": "Firearms, Listen or Spot Hidden, Natural World, Navigate, Other Language or Survival (any), Science (Biology, Botany, or Zoology), Stealth, Track."
            },
            "book_dealer": {
                "description": "A book dealer may be the owner of a retail outlet or niche mail order service, or specialize in buying trips across the country and even overseas. Many will have wealthy or regular clients, who provide lists of sought-after and rare works.",
                "skill_points": "EDU × 4",
                "credit_rating": "20–40",
                "suggested_contacts": "Bibliographers, book dealers, libraries and universities, clients.",
                "skills": "Accounting, Appraise, Drive Auto, History, Library Use, Own Language, Other Language, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade)."
            },
           "bounty_hunter": {
                "description": "Bounty hunters track down and return fugitives to justice. Most often, freelancers are employed by Bail Bondsmen to track down bail jumpers. Bounty hunters may freely cross state lines in pursuit of their quarry and may show little regard for civil rights and other technicalities when capturing their prey. Breaking and entering, threats, and physical abuse are all part of the successful bounty hunter’s bag of tricks. In modern times this may stem to illegal phone taps, computer hacking, and other covert surveillance.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Bail bondsmen, local police, criminal informants.",
                "skills": "Drive Auto, Electronic or Electrical Repair, Fighting or Firearms, one interpersonal skill (Fast Talk, Charm, Intimidate, or Persuade), Law, Psychology, Track, Stealth."
            },
            "boxer_wrestler": {
                "description": "Professional boxers and wrestlers are managed by individuals (promoters) possibly backed by outside interests, and usually locked into contracts. Professional boxers and wrestlers work and train full-time. Amateur boxing competitions abound; a training ground for those aspiring to professional status. In addition, amateur and post-professional boxers and wrestlers can sometimes be found making a living from illegal bareknuckle fights, usually arranged by organized crime gangs or entrepreneurial locals.",
                "skill_points": "EDU × 2 + STR × 2",
                "credit_rating": "9–60",
                "suggested_contacts": "Sports promoters, journalists, organized crime, professional trainers.",
                "skills": "Dodge, Fighting (Brawl), Intimidate, Jump, Psychology, Spot Hidden, any two other skills as personal or era specialties."
            },
            "butler_valet_maid": {
                "description": "This occupation covers those who are employed in a servant capacity and includes butler, valet, and lady’s maid. A butler is usually employed as a domestic servant for a large household. Traditionally the butler is in charge of the dining room, wine cellar and pantry, and ranks as the highest male servant. Usually male—a housekeeper would be the female equivalent—the butler is responsible for male servants within the household. The duties of the butler will vary according to the requirements of his employer. A valet or lady’s maid provides personal services, such as maintaining her employer's clothes, running baths, and effectively acting as a personal assistant. The work might include making travel arrangements, managing their employer’s diary, and organizing household finances.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–40 (dependent on their employer’s status and credit rating).",
                "suggested_contacts": "Waiting staff of other households, local businesses and household suppliers.",
                "skills": "Accounting or Appraise, Art/Craft (any, e.g. Cook, Tailor, Barber), First Aid, Listen, Psychology, Spot Hidden, any two other skills as personal or era specialties."
            },
            "clergy": {
                "description": "The hierarchy of the Church usually assigns clergy to their respective parishes or sends them on evangelical missions, most often to a foreign country (see Missionary page 84). Different churches have different priorities and hierarchies: for example, in the Catholic Church a priest may rise through the ranks of bishop, archbishop, and cardinal, while a Methodist pastor may in turn rise to district superintendent and bishop. Many clergy (not just Catholic priests) bear witness to confessions and, though they are not at liberty to divulge such secrets, they are free to act upon them. Some who work in the church are trained in professional skills, acting as doctors, lawyers, and scholars—as appropriate, use the occupation template which best describes the nature of the investigator’s work.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–60",
                "suggested_contacts": "Church hierarchy, local congregations, community leaders.",
                "skills": "Accounting, History, Library Use, Listen, Other Language, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any one other skill."
            },
            "computer_programmer_technician_hacker": {
                "description": "Usually designing, writing, testing, debugging, and/or maintaining the source code of computer programs, the computer programmer is an expert in many different subjects, including formal logic and application platforms. May work freelance or within the confines of a software development house. The computer technician is tasked with the development and maintenance of computer systems and networks, often working alongside other office staff (such as project managers) to ensure systems maintain integrity and provide desired functionality. Similar occupations may include: Database Administrator, IT Systems Manager, Multimedia Developer, Network Administrator, Software Engineer, Webmaster, etc. The computer hacker uses computers and computer networks as a means of protest to promote political ends (sometimes referred to as 'hacktivists') or for criminal gain. Illegally breaking into computers and other user accounts is required, the outcome of which could be anything from defacing web pages, doxing, and swatting, to email bombing designed to enact denials of service.",
                "skill_points": "EDU × 4",
                "credit_rating": "10–70",
                "suggested_contacts": "Other IT workers, corporate workers and managers, specialized Internet web communities.",
                "skills": "Computer Use, Electrical Repair, Electronics, Library Use, Science (Mathematics), Spot Hidden, any two other skills as personal or era specialties."
            },
            "cowboy_girl": {
                "description": "Cowboys work the ranges and ranches of the West. Some own their own ranches, but many are simply hired where and when work is available. Good money can also be made by those willing to risk life and limb on the rodeo circuit, traveling between events for fame and glory. During the 1920s, a few found employment in Hollywood as stuntmen and extras in westerns; for example, Wyatt Earp worked as a technical advisor to the film industry. In modern times some ranches have opened their gates to holidaymakers wishing to experience life as a cowboy.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–20",
                "suggested_contacts": "Local businesspeople, state agricultural departments, rodeo promoters, and entertainers.",
                "skills": "Dodge, Fighting or Firearms, First Aid or Natural World, Jump, Ride, Survival (any), Throw, Track."
            },
            "craftsperson": {
                "description": "May be equally termed an artisan or master craftsperson. The craftsperson is essentially skilled in the manual production of items or materials. Normally quite talented individuals, some gaining a high reputation for works of art, while others provide a needed community service. Possible trades include: furniture, jewelry, watchmaker, potter, blacksmith, textiles, calligraphy, sewing, carpentry, book binding, glassblowing, toy maker, stained glass, and so on.",
                "skill_points": "EDU × 2 + DEX × 2",
                "credit_rating": "10–40",
                "suggested_contacts": "Local businesspeople, other craftspersons and artists.",
                "skills": "Accounting, Art/Craft (any two), Mechanical Repair, Natural World, Spot Hidden, any two other skills as personal specialties."
            },
            "criminal": {
                "description": "Criminals come in all shapes, sizes, and shades of grey. Some are merely opportunistic jacks of all trades, such as pickpockets and thugs...",
                "skill_points": "Varies",
                "credit_rating": "Varies",
                "suggested_contacts": "Depends on the specific criminal activity.",
                "skills": "Depends on the specific criminal activity."
            },
            "assassin": {
                "description": "Assassins are cold-blooded killers of the underworld. They are usually hired for targeted killings, often following strict codes of behavior...",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "30–60",
                "suggested_contacts": "Few, mostly underworld; people prefer not to know them too well. The best will have earned a formidable reputation on the street.",
                "skills": "Disguise, Electrical Repair, Fighting, Firearms, Locksmith, Mechanical Repair, Stealth, Psychology."
            },
            "bank_robber": {
                "description": "Bank robbers are criminals who specialize in robbing banks. They often work in groups and meticulously plan their heists to evade capture...",
                "skill_points": "EDU × 2 + (STR × 2 or DEX × 2)",
                "credit_rating": "5–75",
                "suggested_contacts": "Other gang members (current and retired), criminal freelancers, organized crime.",
                "skills": "Drive Auto, Electrical or Mechanical Repair, Fighting, Firearms, Intimidate, Locksmith, Operate Heavy Machinery, any one other skill as personal or era specialty."
            },
            "bootlegger_thug": {
                "description": "Bootleggers are individuals involved in the illegal production and distribution of alcohol during the Prohibition era. Thugs are enforcers and muscle for criminal organizations...",
                "skill_points": "EDU × 2 + STR × 2",
                "credit_rating": "5–30",
                "suggested_contacts": "Organized crime, street-level law enforcement, local traders.",
                "skills": "Drive Auto, Fighting, Firearms, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Stealth, Spot Hidden."
            },
            "burglar": {
                "description": "Burglars are criminals who specialize in breaking into and entering buildings with the intent to steal valuable items...",
                "skill_points": "EDU × 2 + DEX × 2",
                "credit_rating": "5–40",
                "suggested_contacts": "Fences, other burglars.",
                "skills": "Appraise, Climb, Electrical or Mechanical Repair, Listen, Locksmith, Sleight of Hand, Stealth, Spot Hidden."
            },
            "conman": {
                "description": "Conmen are skilled manipulators who deceive others for financial gain. They use persuasion, charm, and deception to trick their victims...",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "10–65",
                "suggested_contacts": "Other confidence artists, freelance criminals.",
                "skills": "Appraise, Art/Craft (Acting), Law or Other Language, Listen, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Sleight of Hand."
            },
            "freelance_criminal": {
                "description": "Freelance criminals operate on their own terms, pursuing various criminal activities without being tied to organized crime. They are often self-reliant and resourceful...",
                "skill_points": "EDU × 2 + (DEX × 2 or APP × 2)",
                "credit_rating": "5–65",
                "suggested_contacts": "Other petty criminals, street-level law enforcement.",
                "skills": "Art/Craft (Acting) or Disguise, Appraise, one interpersonal skill (Charm, Fast Talk, or Intimidate), Fighting or Firearms, Locksmith or Mechanical Repair, Stealth, Psychology, Spot Hidden."
            },
            "gun_moll": {
                "description": "A gun moll is a female professional criminal associated with gangsters. She may serve as a partner, accomplice, or lover to male criminals...",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "10–80 (income is usually dependent on boyfriend’s income)",
                "suggested_contacts": "Gangsters, law enforcement, local businesses.",
                "skills": "Art/Craft (any), two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Fighting (Brawl) or Firearms (Handgun), Drive Auto, Listen, Stealth, any one other skill as personal or era specialty."
            },
            "fence": {
                "description": "Fences are criminals who deal in buying and selling stolen goods. They provide a market for stolen items, acting as intermediaries between thieves and buyers...",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "20–40",
                "suggested_contacts": "Organized crime, trade contacts, black market and legitimate buyers.",
                "skills": "Accounting, Appraise, Art/Craft (Forgery), History, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Library Use, Spot Hidden, any one other skill."
            },
            "forger_counterfeiter": {
                "description": "Forgers and counterfeits specialize in creating fake documents, art, or currency. They are skilled at replicating genuine items to deceive and profit...",
                "skill_points": "EDU × 4",
                "credit_rating": "20–60",
                "suggested_contacts": "Organized crime, businesspeople.",
                "skills": "Accounting, Appraise, Art/Craft (Forgery), History, Library Use, Spot Hidden, Sleight of Hand, any one other skill as personal or era specialty (e.g. Computer Use)."
            },
            "smuggler": {
                "description": "Smugglers are individuals involved in the illegal transportation and trade of contraband goods across borders or past authorities...",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2)",
                "credit_rating": "20–60",
                "suggested_contacts": "Organized crime, Coast Guard, U.S. Customs officials.",
                "skills": "Firearms, Listen, Navigate, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Drive Auto or Pilot (Aircraft or Boat), Psychology, Sleight of Hand, Spot Hidden."
            },
            "street_punk": {
                "description": "Street punks are individuals known for their involvement in urban subcultures, often engaging in rebellious and anti-authoritarian behavior. They have a reputation for being tough and street-savvy.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "3–10",
                "suggested_contacts": "Petty criminals, other punks, the local fence, maybe the local gangster, certainly the local police.",
                "skills": "Climb, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Fighting, Firearms, Jump, Sleight of Hand, Stealth, Throw. Also, see Gangster."
            },
            "cult_leader": {
                "description": "America has always generated new religions, from the New England Transcendentalists to the Children of God, as well as many others, right up to modern times. The leader is either a firm believer in the dogma they impart to the cult’s members or simply in it for the money and power...",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "30–60",
                "suggested_contacts": "While the majority of followers will be regular people, the more charismatic the leader, the greater the possibility of celebrity followers, such as movie stars and rich widows.",
                "skills": "Accounting, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Occult, Psychology, Spot Hidden, any two other skills as specialties."
            },
            "deprogrammer": {
                "description": "Deprogramming is the act of persuading (or forcing) a person to abandon their belief or allegiance to a religious or social community. Normally, the deprogrammer is hired by relatives of an individual, who has joined some form of cult, in order to break them free (usually by kidnapping) and then subject them to psychological techniques to free them of their association ('conditioning') with the cult. Less extreme deprogrammers exist, who work with those who have voluntarily left a cult. In such cases, the deprogrammer effectively acts as an exit counselor.",
                "skill_points": "EDU × 4",
                "credit_rating": "20–50",
                "suggested_contacts": "Local and federal law enforcement, criminals, religious community.",
                "skills": "Two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Drive Auto, Fighting (Brawl) or Firearms, History, Occult, Psychology, Stealth. Note: With the Keeper’s agreement, the Hypnosis skill may be substituted for one of the listed skills."
            },
            "designer": {
                "description": "Designers work in many fields, from fashion to furniture and most points in-between. The designer may work freelance, for a design house, or for a business designing consumer products, processes, laws, games, graphics, and so on. The investigator’s particular design specialty might influence the choice of skills—adjust the skills as appropriate.",
                "skill_points": "EDU × 4",
                "credit_rating": "20–60",
                "suggested_contacts": "Advertising, media, furnishings, architectural, other.",
                "skills": "Accounting, Art (Photography), Art/Craft (any), Computer Use or Library Use, Mechanical Repair, Psychology, Spot Hidden, any one other skill as personal specialty."
            },
            "dilettante": {
                "description": "Dilettantes are self-supporting, living off an inheritance, trust fund, or some other source of income that does not require them to work. Usually, the dilettante has enough money that specialist financial advisers are needed to take care of it. Probably well-educated, though not necessarily accomplished in anything. Money frees the dilettante to be eccentric and outspoken. In the 1920s, some dilettantes might be flappers or sheiks—as per the parlance of the time—of course, one didn't need to be rich to be a party person. In modern times, 'hipster' might also be an appropriate term. The dilettante has had plenty of time to learn how to be charming and sophisticated; what else has been done with that free time is likely to betray the dilettante’s true character and interests.",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "50–99",
                "suggested_contacts": "Variable, but usually people of a similar background and tastes, fraternal organizations, bohemian circles, high society at large.",
                "skills": "Art/Craft (Any), Firearms, Other Language, Ride, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), any three other skills as personal or era specialties."
            },
            "diver": {
                "description": "Divers could work in various fields such as the military, law enforcement, sponge gathering, salvage, conservation, or treasure hunting. They are skilled in underwater activities and often have contacts in maritime and related industries.",
                "skill_points": "EDU × 2 + DEX × 2",
                "credit_rating": "9–30",
                "suggested_contacts": "Coast guard, ship captains, military, law enforcement, smugglers.",
                "skills": "Diving, First Aid, Mechanical Repair, Pilot (Boat), Science (Biology), Spot Hidden, Swim, any one other skill as personal or era specialty."
            },
            "doctor_of_medicine": {
                "description": "Doctors of Medicine are medical professionals who specialize in various fields such as general practice, surgery, psychiatry, or medical research. They aim to help patients, gain prestige, and contribute to a rational society. They might work in rural practices, urban hospitals, or as medical examiners.",
                "skill_points": "EDU × 4",
                "credit_rating": "30–80",
                "suggested_contacts": "Other physicians, medical workers, patients and ex-patients.",
                "skills": "First Aid, Medicine, Other Language (Latin), Psychology, Science (Biology and Pharmacy), any two other skills as academic or personal specialties."
            },
            "drifter": {
                "description": "Drifters are individuals who choose a wandering and transient lifestyle, often moving from place to place. They may be motivated by a desire for freedom, philosophical reasons, or other factors. Their skills are adapted for mobility and survival on the road.",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2 or STR × 2)",
                "credit_rating": "0–5",
                "suggested_contacts": "Other hobos, friendly railroad guards, contacts in numerous towns.",
                "skills": "Climb, Jump, Listen, Navigate, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Stealth, any two other skills as personal or era specialties."
            },
            "chauffeur": {
                "description": "A chauffeur is either directly employed by an individual or firm, or works for an agency that hires both car and chauffeur out for single engagements or on a retainer basis. Chauffeurs often serve successful business people and may have political connections.",
                "skill_points": "EDU × 2 + DEX × 2",
                "credit_rating": "10–40",
                "suggested_contacts": "Successful business people (criminals included), political representatives.",
                "skills": "Drive Auto, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Listen, Mechanical Repair, Navigate, Spot Hidden, any one other skill as a personal or era specialty."
            },
            "driver": {
                "description": "Professional drivers may work for companies, private individuals, or have their own vehicles. They include taxi drivers and general drivers who navigate various environments. Drivers often have contacts in businesses, law enforcement, and street-level life.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–20",
                "suggested_contacts": "Customers, businesses, law enforcement, general street level life.",
                "skills": "Accounting, Drive Auto, Listen, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Mechanical Repair, Navigate, Psychology, any one other skill as personal or era specialty."
            },
            "taxi_driver": {
                "description": "Taxi drivers provide transportation services for passengers, often working for taxi companies or as independent operators. They navigate the streets and may encounter various customers. Taxi drivers often have knowledge of street scenes and notable customers.",
                "skill_points": "EDU x 2 + DEX x 2",
                "credit_rating": "9–30",
                "suggested_contacts": "Street scene, possibly a notable customer now and then.",
                "skills": "Accounting, Drive Auto, Electrical Repair, Fast Talk, Mechanical Repair, Navigate, Spot Hidden, any one other skill as a personal or era specialty."
            },
            "editor": {
                "description": "Editors work in the news industry, assigning stories, writing editorials, and dealing with deadlines. They play a crucial role in shaping content and meeting journalistic standards. Editors often have contacts in the news industry, local government, and specialized fields.",
                "skill_points": "EDU × 4",
                "credit_rating": "10–30",
                "suggested_contacts": "News industry, local government, specialists (e.g. fashion designers, sports, business), publishers.",
                "skills": "Accounting, History, Own Language, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Spot Hidden, any one other skill as personal or era specialty."
            },
            "elected_official": {
                "description": "Elected officials hold positions of power and influence, ranging from local mayors to federal senators. Their prestige varies based on the level of government and jurisdiction they represent. They often have connections in politics, government, media, business, and sometimes organized crime.",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "50–90",
                "suggested_contacts": "Political operatives, government, news media, business, foreign governments, possibly organized crime.",
                "skills": "Charm, History, Intimidate, Fast Talk, Listen, Own Language, Persuade, Psychology."
            },
            "engineer": {
                "description": "Engineers are specialists in mechanical or electrical devices, often employed in civilian businesses or the military. They use scientific knowledge and creativity to solve technical problems. Engineers have contacts in business, military, and related fields.",
                "skill_points": "EDU × 4",
                "credit_rating": "30–60",
                "suggested_contacts": "Business or military workers, local government, architects.",
                "skills": "Art/Craft (Technical Drawing), Electrical Repair, Library Use, Mechanical Repair, Operate Heavy Machine, Science (Engineering and Physics), any one other skill as personal or era specialty."
            },
            "entertainer": {
                "description": "This occupation includes various roles like clowns, singers, dancers, comedians, musicians, and more, who perform in front of audiences. Entertainers thrive on attention and applause, and their professions gained respect with the rise of Hollywood stars in the 1920s.",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "9–70",
                "suggested_contacts": "Vaudeville, theater, film industry, entertainment critics, organized crime, and television (for modern-day).",
                "skills": "Art/Craft (e.g. Acting, Singer, Comedian, etc.), Disguise, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Listen, Psychology, any two other skills as personal or era specialties."
            },
            "explorer": {
                "description": "Explorers in the early twentieth century embark on careers exploring unknown areas of the world. They often secure funding through grants, donations, and contracts to document their findings through various media. Much of the world remains unexplored, including parts of Africa, South America, Australia, deserts, and Asian interiors.",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2 or STR × 2)",
                "credit_rating": "55–80",
                "suggested_contacts": "Major libraries, universities, museums, wealthy patrons, other explorers, publishers, foreign government officials, local tribespeople.",
                "skills": "Climb or Swim, Firearms, History, Jump, Natural World, Navigate, Other Language, Survival."
            },
            "farmer": {
                "description": "Farmers are agricultural workers who raise crops or livestock, either owning the land or being employed. Farming is physically demanding and suited for those who enjoy outdoor labor. Independent farmers in the 1920s face competition from corporate farms and fluctuating commodity markets.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Local bank, local politicians, state agricultural department.",
                "skills": "Art/Craft (Farming), Drive Auto (or Wagon), one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Mechanical Repair, Natural World, Operate Heavy Machinery, Track, any one other skill as a personal or era specialty."
            },
            "federal_agent": {
                "description": "Federal agents work in various law enforcement agencies, both uniformed and plainclothes. They are responsible for enforcing federal laws and investigating crimes. Federal agents often have contacts within law enforcement, government, and organized crime.",
                "skill_points": "EDU × 4",
                "credit_rating": "20–40",
                "suggested_contacts": "Federal agencies, law enforcement, organized crime.",
                "skills": "Drive Auto, Fighting (Brawl), Firearms, Law, Persuade, Stealth, Spot Hidden, any one other skill as a personal or era specialty."
            },
            "firefighter": {
                "description": "Firefighters are civil servants who work to prevent and combat fires. They often work in shifts and live at fire stations. Firefighting is organized in a hierarchical structure with potential for promotions. Firefighters often have contacts in civic works, medical services, and law enforcement.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Civic workers, medical workers, law enforcement.",
                "skills": "Climb, Dodge, Drive Auto, First Aid, Jump, Mechanical Repair, Operate Heavy Machinery, Throw."
            },
            "foreign_correspondent": {
                "description": "Foreign correspondents are top-tier news reporters who travel the world to cover international events. They work for major news outlets and may focus on various media forms. Foreign correspondents often report on natural disasters, political upheavals, and wars.",
                "skill_points": "EDU × 4",
                "credit_rating": "10–40",
                "suggested_contacts": "National or worldwide news industry, foreign governments, military.",
                "skills": "History, Other Language, Own Language, Listen, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any one other skill as a personal or era specialty."
            },
            "forensic_surgeon": {
                "description": "Forensic surgeons conduct autopsies, determine causes of death, and provide recommendations to prosecutors. They often testify in criminal proceedings and have contacts in laboratories, law enforcement, and the medical profession.",
                "skill_points": "EDU × 4",
                "credit_rating": "40–60",
                "suggested_contacts": "Laboratories, law enforcement, medical profession.",
                "skills": "Other Language (Latin), Library Use, Medicine, Persuade, Science (Biology), (Forensics), (Pharmacy), Spot Hidden."
            },
            "gambler": {
                "description": "Gamblers are stylish individuals who take chances in games of chance. They may frequent racetracks, casinos, or underground gambling establishments. Gamblers often have contacts in bookies, organized crime, and street scenes.",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2)",
                "credit_rating": "8–50",
                "suggested_contacts": "Bookies, organized crime, street scene.",
                "skills": "Accounting, Art/Craft (Acting), two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Listen, Psychology, Sleight of Hand, Spot Hidden."
            },
            "gangster_boss": {
                "description": "Gangster bosses lead criminal organizations, making deals and overseeing illegal activities. They have a network of underlings to carry out their orders. Gangsters rose to prominence in the 1920s, controlling various criminal enterprises.",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "60–95",
                "suggested_contacts": "Organized crime, street-level crime, police, city government, politicians, judges, unions, lawyers, businesses, residents of the same ethnic community.",
                "skills": "Fighting, Firearms, Law, Listen, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Spot Hidden."
            },
            "gangster_underling": {
                "description": "Gangster underlings work for the gangster boss, overseeing specific areas of responsibility. They are involved in illegal activities like protection, gambling, and more. Modern gangster bosses focus on the drug trade and other criminal enterprises.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–20",
                "suggested_contacts": "Street-level crime, police, businesses and residents of the same ethnic community.",
                "skills": "Drive Auto, Fighting, Firearms, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any two other skills as personal or era specialties."
            },
            "gentleman_lady": {
                "description": "A gentleman or lady is a well-mannered and courteous individual, often from the upper class. In the 1920s, they would have had servants and likely owned both city and country residences. Family status is often more important than wealth in this social class.",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "40–90",
                "suggested_contacts": "Upper classes and landed gentry, politics, servants, agricultural workers.",
                "skills": "Art/Craft (any), two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Firearms (Rifle/Shotgun), History, Other Language (any), Navigate, Ride."
            },
            "hobo": {
                "description": "Hobos are wandering workers who travel from town to town, often riding the rails. They are penniless explorers of the road, facing danger from police, communities, and railroad staff. Hobos have contacts among other hobos and some friendly railroad guards.",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2)",
                "credit_rating": "0–5",
                "suggested_contacts": "Other hobos, a few friendly railroad guards, so-called \"touches\" in numerous towns.",
                "skills": "Art/Craft (any), Climb, Jump, Listen, Locksmith or Sleight of Hand, Navigate, Stealth, any one other skill as a personal or era specialty."
            },
            "hospital_orderly": {
                "description": "Hospital orderlies perform various tasks in medical facilities, including cleaning, transporting patients, and other odd jobs. They have contacts among hospital and medical workers as well as access to drugs and medical records.",
                "skill_points": "EDU × 2 + STR × 2",
                "credit_rating": "6–15",
                "suggested_contacts": "Hospital and medical workers, patients. Access to drugs, medical records, etc.",
                "skills": "Electrical Repair, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Fighting (Brawl), First Aid, Listen, Mechanical Repair, Psychology, Stealth."
            },
            "journalist_investigative": {
                "description": "Investigative journalists report on topics and incidents, often working independently to expose corruption and self-serving agendas. They gather information similar to private detectives and may resort to subterfuge.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–30",
                "suggested_contacts": "News industry, politicians, street-level crime or law enforcement.",
                "skills": "Art/Craft (Art or Photography), one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), History, Library Use, Own Language, Psychology, any two other skills as personal or era specialties."
            },
            "reporter": {
                "description": "Reporters use words to report and comment on current events. They work for various media outlets and often gather stories by interviewing witnesses and checking records. Reporters may use subterfuge to gather information.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–30",
                "suggested_contacts": "News and media industries, political organizations and government, business, law enforcement, street criminals, high society.",
                "skills": "Art/Craft (Acting), History, Listen, Own Language, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Stealth, Spot Hidden."
            },
            "judge": {
                "description": "Judges preside over legal proceedings, making decisions and judgments either alone or within a group. They can be appointed or elected and are usually licensed attorneys. Judges have legal connections and possibly contacts with organized crime.",
                "skill_points": "EDU × 4",
                "credit_rating": "50–80",
                "suggested_contacts": "Legal connections, possibly organized crime.",
                "skills": "History, Intimidate, Law, Library Use, Listen, Own Language, Persuade, Psychology"
            },
            "laboratory_assistant": {
                "description": "Laboratory assistants work in scientific environments, performing various tasks under the supervision of lead scientists. Their tasks depend on the discipline and could include testing, recording results, preparing specimens, and more.",
                "skill_points": "EDU × 4",
                "credit_rating": "10–30",
                "suggested_contacts": "Universities, scientists, librarians.",
                "skills": "Computer Use or Library Use, Electrical Repair, Other Language, Science (Chemistry and two others), Spot Hidden, any one other skill as a personal specialty."
            },
            "laborer_unskilled": {
                "description": "Unskilled laborers include factory workers, road crews, and more. Despite being unskilled, they are often experts in using power tools and equipment. They have contacts within their industry.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Other workers and supervisors within their industry.",
                "skills": "Drive Auto, Electrical Repair, Fighting, First Aid, Mechanical Repair, Operate Heavy Machinery, Throw, any one other skill as a personal or era specialty."
            },
            "lumberjack": {
                "description": "Lumberjacks work in forestry, often involved in cutting down trees and handling logs. They have contacts among forestry workers, wilderness guides, and conservationists.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Forestry workers, wilderness guides and conservationists.",
                "skills": "Climb, Dodge, Fighting (Chainsaw), First Aid, Jump, Mechanical Repair, Natural World or Science (Biology or Botany), Throw."
            },
            "miner": {
                "description": "Miners work in various fields such as mining, often dealing with extraction of minerals and ores. They have contacts among union officials and political organizations.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Union officials, political organizations.",
                "skills": "Climb, Geology, Jump, Mechanical Repair, Operate Heavy Machinery, Stealth, Spot Hidden, any one other skill as a personal or era specialty."
            },
            "lawyer": {
                "description": "Lawyers are legal professionals who provide legal counsel, representing clients and presenting legal solutions. They can be hired or appointed and usually have legal connections, including organized crime.",
                "skill_points": "EDU × 4",
                "credit_rating": "30–80",
                "suggested_contacts": "Organized crime, financiers, district attorneys and judges.",
                "skills": "Accounting, Law, Library Use, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any two other skills."
            },
            "librarian": {
                "description": "Librarians manage and maintain libraries, cataloging and overseeing the collection. They have contacts with booksellers, community groups, and specialist researchers.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–35",
                "suggested_contacts": "Booksellers, community groups, specialist researchers.",
                "skills": "Accounting, Library Use, Other Language, Own Language, any four other skills as personal specialties or specialist reading topics."
            },
             "mechanic": {
                "description": "Mechanics and skilled tradespeople include various trades requiring specialized training and experience, such as carpenters, plumbers, electricians, and mechanics. They often have their own unions and contacts within the trade.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–40",
                "suggested_contacts": "Union members, trade-relevant specialists.",
                "skills": "Art/Craft (Carpentry, Welding, Plumbing, etc.), Climb, Drive Auto, Electrical Repair, Mechanical Repair, Operate Heavy Machinery, any two other skills as personal, era or trade specialties."
            },
            "military_officer": {
                "description": "Military officers are command ranks requiring higher education. They undergo training and are often graduates of military academies. They have contacts in the military and federal government.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "20–70",
                "suggested_contacts": "Military, federal government.",
                "skills": "Accounting, Firearms, Navigate, First Aid, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any one other skill as personal or era specialties."
            },
            "missionary": {
                "description": "Missionaries spread religious teachings in remote or urban areas. They can be backed by churches or independent. Missionaries of various faiths exist worldwide.",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "0–30",
                "suggested_contacts": "Church hierarchy, foreign officials.",
                "skills": "Art/Craft (any), First Aid, Mechanical Repair, Medicine, Natural World, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), any two other skills as personal or era specialties."
            },
            "mountain_climber": {
                "description": "Mountain climbers engage in climbing peaks as a sport or profession. They seek challenges in various environments and often have contacts with other climbers, rescue services, and sponsors.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "30–60",
                "suggested_contacts": "Other climbers, environmentalists, patrons, sponsors, local rescue or law enforcement, park rangers, sports clubs.",
                "skills": "Climb, First Aid, Jump, Listen, Navigate, Other Language, Survival (Alpine or as appropriate), Track."
            },
            "museum_curator": {
                "description": "Museum curators manage and oversee exhibits and collections in museums, often specializing in specific topics. They have contacts with local universities, scholars, and patrons.",
                "skill_points": "EDU × 4",
                "credit_rating": "10–30",
                "suggested_contacts": "Local universities and scholars, publishers, museum patrons.",
                "skills": "Accounting, Appraise, Archaeology, History, Library Use, Occult, Other Language, Spot Hidden."
            },
            "musician": {
                "description": "Musicians perform individually or in groups, playing various instruments. While it's difficult to achieve success, some manage to find regular work or become wealthy through their talent.",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Club owners, musicians’ union, organized crime, street-level criminals.",
                "skills": "Art/Craft (Instrument), one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Listen, Psychology, any four other skills."
            },
            "nurse": {
                "description": "Nurses provide healthcare assistance in hospitals, nursing homes, and medical practices. They assist patients with various health-related activities and have contacts with healthcare professionals.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–30",
                "suggested_contacts": "Hospital workers, physicians, community workers.",
                "skills": "First Aid, Listen, Medicine, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Science (Biology) and (Chemistry), Spot Hidden."
            },
            "occultist": {
                "description": "Occultists study esoteric secrets, paranormal phenomena, and arcane magic. They seek to uncover paranormal abilities and often have knowledge of various magical theories.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–65",
                "suggested_contacts": "Libraries, occult societies or fraternities, other occultists.",
                "skills": "Anthropology, History, Library Use, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Occult, Other Language, Science (Astronomy), any one other skill as a personal or era specialty."
            },
            "outdoorsman_woman": {
                "description": "Outdoorsmen/women are skilled in surviving and thriving in the wilderness. They may work as guides, rangers, or simply live a self-sufficient lifestyle in nature.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "5–20",
                "suggested_contacts": "Local people and native folk, traders.",
                "skills": "Firearms, First Aid, Listen, Natural World, Navigate, Spot Hidden, Survival (any), Track."
            },
            "parapsychologist": {
                "description": "Parapsychologists study and investigate paranormal phenomena, often using technology to capture evidence. They specialize in areas like extrasensory perception, telekinesis, and hauntings.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–30",
                "suggested_contacts": "Universities, parapsychological publications.",
                "skills": "Anthropology, Art/Craft (Photography), History, Library Use, Occult, Other Language, Psychology, any one other skill as a personal or era specialty."
            },
            "pharmacist": {
                "description": "Pharmacists are licensed professionals who dispense medications. They may work in hospitals, drug stores, or dispensaries, and have access to a wide range of chemicals and drugs.",
                "skill_points": "EDU × 4",
                "credit_rating": "35–75",
                "suggested_contacts": "Local community, local physicians, hospitals and patients. Access to all manner of chemicals and drugs.",
                "skills": "Accounting, First Aid, Other Language (Latin), Library Use, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Science (Pharmacy), (Chemistry)."
            },
            "photographer": {
                "description": "Photographers capture images using various techniques. They can work in fields like art, journalism, and wildlife conservation, often finding fame and recognition in their specialization.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–30",
                "suggested_contacts": "Advertising industry, local clients (including political organizations and newspapers).",
                "skills": "Art/Craft (Photography), one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Science (Chemistry), Stealth, Spot Hidden, any two other skills as personal or era specialties."
            },
            "photojournalist": {
                "description": "Photojournalists are reporters who use photography to accompany news stories. They work in industries like news and film, often covering events and producing images for publication.",
                "skill_points": "EDU × 4",
                "credit_rating": "10–30",
                "suggested_contacts": "News industry, film industry (1920s), foreign governments and authorities.",
                "skills": "Art/Craft (Photography), Climb, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Other Language, Psychology, Science (Chemistry), any two other skills as personal or era specialties."
            },
            "pilot": {
                "description": "Pilots fly aircraft for various purposes, including commercial airlines and businesses. They may also work as stunt pilots, aviators, or military pilots.",
                "skill_points": "EDU × 2 + DEX × 2",
                "credit_rating": "20–70",
                "suggested_contacts": "Old military contacts, cabin crew, mechanics, airfield staff, carnival entertainers.",
                "skills": "Electrical Repair, Mechanical Repair, Navigate, Operate Heavy Machine, Pilot (Aircraft), Science (Astronomy), any two other skills as personal or era specialties."
            },
            "aviator": {
                "description": "Aviators are stunt pilots who perform at carnivals and air races. They may also work as test pilots or in other aviation-related roles. Some aviators have military backgrounds.",
                "skill_points": "EDU × 4",
                "credit_rating": "30–60",
                "suggested_contacts": "Old military contacts, other pilots, airfield mechanics, businessmen.",
                "skills": "Accounting, Electrical Repair, Listen, Mechanical Repair, Navigate, Pilot (Aircraft), Spot Hidden, any one other skill as a personal or era specialty."
            },
            "police_detective": {
                "description": "Police detectives investigate crimes, gather evidence, and try to solve major felonies. They work closely with uniformed patrol officers and aim to build cases for criminal prosecution.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "20–50",
                "suggested_contacts": "Law enforcement, street level crime, coroner’s office, judiciary, organized crime.",
                "skills": "Art/Craft (Acting) or Disguise, Firearms, Law, Listen, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Spot Hidden, any one other skill."
            },
            "uniformed_police_officer": {
                "description": "Uniformed police officers work in cities, towns, or other law enforcement agencies. They patrol on foot, in vehicles, or at a desk, maintaining public safety and enforcing laws.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Law enforcement, local businesses and residents, street level crime, organized crime.",
                "skills": "Fighting (Brawl), Firearms, First Aid, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Law, Psychology, Spot Hidden, and one of the following as a personal specialty: Drive Automobile or Ride."
            },
            "private_investigator": {
                "description": "Private investigators gather information and evidence for private clients. They may work on civil cases, track down individuals, or assist in criminal defense. Licensing is often required.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Law enforcement, clients.",
                "skills": "Art/Craft (Photography), Disguise, Law, Library Use, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Spot Hidden, and any one other skill as personal or era specialty (e.g. Computer Use, Locksmith, Fighting, Firearms)."
            },
            "professor": {
                "description": "Professors are academics employed by colleges and universities. They may also work for corporations in research and development roles. They often hold a Ph.D. and have expertise in their field.",
                "skill_points": "EDU × 4",
                "credit_rating": "20–70",
                "suggested_contacts": "Scholars, universities, libraries.",
                "skills": "Library Use, Other Language, Own Language, Psychology, any four other skills as academic, era, or personal specialties."
            },
            "prospector": {
                "description": "Prospectors search for valuable resources like gold or oil. While the days of the Gold Rush are gone, independent prospectors still search for valuable finds.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "0–10",
                "suggested_contacts": "Local businesses and residents.",
                "skills": "Climb, First Aid, History, Mechanical Repair, Navigate, Science (Geology), Spot Hidden, any one other skill as a personal or era specialty."
            },
            "prostitute": {
                "description": "Prostitutes engage in various forms of sex work, driven by circumstance or coercion. They may work independently or under the control of pimps.",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "5–50",
                "suggested_contacts": "Street scene, police, possibly organized crime, personal clientele.",
                "skills": "Art/Craft (any), two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Dodge, Psychology, Sleight of Hand, Stealth, any one other skill as a personal or era specialty."
            },
            "psychiatrist": {
                "description": "Psychiatrists are physicians specialized in diagnosing and treating mental disorders. They often use psychopharmacology and other techniques in their practice.",
                "skill_points": "EDU × 4",
                "credit_rating": "30–80",
                "suggested_contacts": "Others in the field of mental illness, physicians and possibly legal professions.",
                "skills": "Other Language, Listen, Medicine, Persuade, Psychoanalysis, Psychology, Science (Biology) and (Chemistry)."
            },
            "psychologist": {
                "description": "Psychologists study human behavior and can specialize in various areas, including psychotherapy, research, and teaching. They may not be medical doctors.",
                "skill_points": "EDU × 4",
                "credit_rating": "10–40",
                "suggested_contacts": "Psychological community, patients.",
                "skills": "Accounting, Library Use, Listen, Persuade, Psychoanalysis, Psychology, any two other skills as academic, era or personal specialties."
            },
            "researcher": {
                "description": "Researchers are involved in academic or private sector research. They can work in various fields, such as astronomy, physics, and chemistry.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–30",
                "suggested_contacts": "Scholars and academics, large businesses and corporations, foreign governments and individuals.",
                "skills": "History, Library Use, one interpersonal skill (Charm, Fast Talk Intimidate, or Persuade), Other Language, Spot Hidden, any three fields of study."
            },
            "sailor_naval": {
                "description": "Naval sailors serve in the military and go through training. They have various roles, including mechanics, radio operators, and more.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Military, veterans’ associations.",
                "skills": "Electrical or Mechanical Repair, Fighting, Firearms, First Aid, Navigate, Pilot (Boat), Survival (Sea), Swim."
            },
            "sailor_commercial": {
                "description": "Commercial sailors work on fishing vessels, charter boats, or haulage tankers. They may be involved in legal or illegal activities, such as smuggling.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "20–40",
                "suggested_contacts": "Coast Guard, smugglers, organized crime.",
                "skills": "First Aid, Mechanical Repair, Natural World, Navigate, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Pilot (Boat), Spot Hidden, Swim."
            },
            "salesperson": {
                "description": "Salespeople promote and sell goods or services for businesses. They may travel to meet clients or work in offices, making calls.",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "9–40",
                "suggested_contacts": "Businesses within the same sector, favored customers.",
                "skills": "Accounting, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Drive Auto, Listen, Psychology, Stealth or Sleight of Hand, any one other skill."
            },
            "scientist": {
                "description": "Scientists are involved in research and expanding the bounds of knowledge in various fields. They work for businesses and universities.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–50",
                "suggested_contacts": "Other scientists and academics, universities, their employers and former employers.",
                "skills": "Any three science specialisms, Computer Use or Library Use, Other Language, Own Language, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Spot Hidden."
            },
            "secretary": {
                "description": "Secretaries provide communication and organizational support to executives and managers. They have insights into the inner workings of the business.",
                "skill_points": "EDU × 2 + (DEX × 2 or APP × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Other office workers, senior executives in client firms.",
                "skills": "Accounting, Art/Craft (Typing or Short Hand), two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Own Language, Library Use or Computer Use, Psychology, any one other skill as a personal or era specialty."
            },
            "shopkeeper": {
                "description": "Shopkeepers own and manage small shops, market stalls, or restaurants. They are usually self-employed and may run family businesses.",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2)",
                "credit_rating": "20–40",
                "suggested_contacts": "Local residents and businesses, local police, local government, customers.",
                "skills": "Accounting, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Electrical Repair, Listen, Mechanical Repair, Psychology, Spot Hidden."
            },
            "soldier_marine": {
                "description": "Soldiers and Marines serve in the enlisted ranks of the Army and Marines. They undergo training and may serve in combat or non-combat roles.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Military, veterans associations.",
                "skills": "Climb or Swim, Dodge, Fighting, Firearms, Stealth, Survival and two of the following: First Aid, Mechanical Repair or Other Language."
            },
            "spy": {
                "description": "Spies work undercover for intelligence agencies to gather information and carry out various tasks. They may have deep cover identities.",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2)",
                "credit_rating": "20–60",
                "suggested_contacts": "Generally only the person the spy reports to, possibly other connections developed while under cover.",
                "skills": "Art/Craft (Acting) or Disguise, Firearms, Listen, Other Language, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Sleight of Hand, Stealth."
            },
            "student_intern": {
                "description": "Students or interns may be enrolled at educational institutions or receive on-the-job training. They may work for minimal compensation.",
                "skill_points": "EDU × 4",
                "credit_rating": "5–10",
                "suggested_contacts": "Academics and other students, while interns may also know business people.",
                "skills": "Language (Own or Other), Library Use, Listen, three fields of study and any two other skills as personal or era specialties."
            },
            "stuntman": {
                "description": "Stuntmen and women work in the film and television industry to perform dangerous stunts. They often simulate falls, crashes, and other catastrophes.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "10–50",
                "suggested_contacts": "The film and television industries, explosive and pyrotechnic firms, actors and directors.",
                "skills": "Climb, Dodge, Electrical Repair or Mechanical Repair, Fighting, First Aid, Jump, Swim, plus one from either Diving, Drive Automobile, Pilot (any), Ride."
            },
            "tribe_member": {
                "description": "Tribe members belong to small groups characterized by kinship and custom. Personal honor, praise, and vengeance play important roles in tribal life.",
                "skill_points": "EDU × 2 + (STR × 2 or DEX × 2)",
                "credit_rating": "0–15",
                "suggested_contacts": "Fellow tribe members.",
                "skills": "Climb, Fighting or Throw, Listen, Natural World, Occult, Spot Hidden, Swim, Survival (any)."
            },
            "undertaker": {
                "description": "Undertakers, also known as morticians or funeral directors, manage funeral rites, including burials or cremations. They are licensed professionals.",
                "skill_points": "EDU × 4",
                "credit_rating": "20–40",
                "suggested_contacts": "Few.",
                "skills": "Accounting, Drive Auto, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), History, Occult, Psychology, Science (Biology) and (Chemistry)."
            },
            "union_activist": {
                "description": "Union activists organize and lead labor unions in various industries. They face challenges from businesses, politicians, and other groups.",
                "skill_points": "EDU × 4",
                "credit_rating": "5–30",
                "suggested_contacts": "Other labor leaders and activists, political friends, possibly organized crime. In the 1920s, also socialists, communists, and subversive anarchists.",
                "skills": "Accounting, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Fighting (Brawl), Law, Listen, Operate Heavy Machinery, Psychology."
            },
            "waitress_waiter": {
                "description": "Waitresses and waiters serve customers in eating or drinking establishments. Tips are earned by providing good service and building rapport.",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2)",
                "credit_rating": "9–20",
                "suggested_contacts": "Customers, organized crime.",
                "skills": "Accounting, Art/Craft (any), Dodge, Listen, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any one skill as a personal or era specialty."
            },
            "clerk_executive": {
                "description": "This could range from the lowest-level white-collar position of a clerk to a middle or senior manager. The employer could be a small to medium-sized locally-owned business, up to a large national or multinational corporation. Clerks are habitually underpaid and the work is drudgery, with those recognized as having talent being earmarked for promotion someday. Middle and senior managers attract higher salaries, with greater responsibilities and say in how the business is managed day-to-day. Although unmarried white-collar workers are not infrequent, most executive types are family-oriented, with a spouse at home and children—it is often expected of them.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–20",
                "suggested_contacts": "Other office workers.",
                "skills": "Accounting, Language (Own or Other), Law, Library Use or Computer Use, Listen, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), any two other skills as personal or era specialties."
            },
             "middle_senior_manager": {
                "description": "This could range from the lowest-level white-collar position of a clerk to a middle or senior manager. The employer could be a small to medium-sized locally-owned business, up to a large national or multinational corporation. Clerks are habitually underpaid and the work is drudgery, with those recognized as having talent being earmarked for promotion someday. Middle and senior managers attract higher salaries, with greater responsibilities and say in how the business is managed day-to-day. Although unmarried white-collar workers are not infrequent, most executive types are family-oriented, with a spouse at home and children—it is often expected of them.",
                "skill_points": "EDU × 4",
                "credit_rating": "20–80",
                "suggested_contacts": "Old college connections, Masons or other fraternal groups, local and federal government, media and marketing.",
                "skills": "Accounting, Other Language, Law, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any two other skills as personal or era specialties."
            },
            "zealot": {
                "description": "Zealots are intense and vision-driven individuals who are passionate about their beliefs. They may agitate for change through various means.",
                "skill_points": "EDU × 2 + (APP × 2 or POW × 2)",
                "credit_rating": "0–30",
                "suggested_contacts": "Religious or fraternal groups, news media.",
                "skills": "History, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Stealth, and any three other skills as personal or era specialties."
            },
            "zookeeper": {
                "description": "Zookeepers care for animals in zoos, ensuring their feeding and well-being. They may specialize in specific animal breeds.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–40",
                "suggested_contacts": "Scientists, environmentalists.",
                "skills": "Animal Handling, Accounting, Dodge, First Aid, Natural World, Medicine, Science (Pharmacy), (Zoology)"
            }
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
            
    @commands.command(aliases=["gbackstory"])
    async def generate_backstory(self, ctx):
        personal_descriptions = [
            "Rugged", "Handsome", "Ungainly",
            "Pretty", "Glamorous", "Baby-faced",
            "Smart", "Untidy", "Dull",
            "Dirty", "Dazzler", "Bookish",
            "Youthful", "Weary", "Plump",
            "Stout", "Hairy", "Slim",
            "Elegant", "Scruffy", "Stocky",
            "Pale", "Sullen", "Ordinary",
            "Rosy", "Tanned", "Wrinkled",
            "Sturdy", "Mousy", "Sharp",
            "Brawny", "Dainty", "Muscular",
            "Strapping", "Gawky", "Frail"
        ]
        
        personal_description_text = ""
        for description in personal_descriptions:
            personal_description_text += f"{description}, "
    
        ideology_beliefs = [
            "There is a higher power that you worship and pray to (e.g. Vishnu, Jesus Christ, Haile Selassie I).",
            "Mankind can do fine without religions (e.g. staunch atheist, humanist, secularist).",
            "Science has all the answers. Pick a particular aspect of interest (e.g. evolution, cryogenics, space exploration).",
            "A belief in fate (e.g. karma, the class system, superstitious).",
            "Member of a society or secret society (e.g. Freemason, Women’s Institute, Anonymous).",
            "There is evil in society that should be rooted out. What is this evil? (e.g. drugs, violence, racism).",
            "The occult (e.g. astrology, spiritualism, tarot).",
            "Politics (e.g. conservative, socialist, liberal).",
            "\"Money is power, and I’m going to get all I can\" (e.g. greedy, enterprising, ruthless).",
            "Campaigner/Activist (e.g. feminism, gay rights, union power)."
        ]
        selected_ideology_beliefs = random.choice(ideology_beliefs)
    
        significant_people_first = [
            "Parent (e.g. mother, father, stepmother).",
            "Grandparent (e.g. maternal grandmother, paternal grandfather).",
            "Sibling (e.g. brother, half-brother, stepsister).",
            "Child (e.g. son or daughter).",
            "Partner (e.g. spouse, fiancé, lover).",
            "Person who taught you your highest occupational skill. Identify the skill and consider who taught you (e.g. a schoolteacher, the person you apprenticed with, your father).",
            "Childhood Friend (e.g. classmate, neighbor, imaginary friend).",
            "A famous person. Your idol or hero. You may never have even met (e.g. film star, politician, musician).",
            "A fellow investigator in your game. Pick one or choose randomly.",
            "A non-player character (NPC) in the game. Ask the Keeper to pick one for you."
        ]
        selected_significant_people_first = random.choice(significant_people_first)
        
        significant_people_why = [
            "You are indebted to them. How did they help you? (e.g. financially, they protected you through hard times, got you your first job).",
            "They taught you something. What? (e.g. a skill, to love, to be a man).",
            "They give your life meaning. How? (e.g. you aspire to be like them, you seek to be with them, you seek to make them happy).",
            "You wronged them and seek reconciliation. What did you do? (e.g. stole money from them, informed the police about them, refused to help when they were desperate).",
            "Shared experience. What? (e.g. you lived through hard times together, you grew up together, you served in the war together).",
            "You seek to prove yourself to them. How? (e.g. by getting a good job, by finding a good spouse, by getting an education).",
            "You idolize them (e.g. for their fame, their beauty, their work).",
            "A feeling of regret (e.g. you should have died in their place, you fell out over something you said, you didn’t step up and help them when you had the chance).",
            "You wish to prove yourself better than them. What was their flaw? (e.g. lazy, drunk, unloving).",
            "They have crossed you and you seek revenge. For what do you blame them? (e.g. death of a loved one, your financial ruin, marital breakup)."
        ]
        selected_significant_people_why = random.choice(significant_people_why)
    
        meaningful_locations = [
            "Your seat of learning (e.g. school, university, apprenticeship).",
            "Your hometown (e.g. rural village, market town, busy city).",
            "The place you met your first love (e.g. a music concert, on holiday, a bomb shelter).",
            "A place for quiet contemplation (e.g. the library, country walks on your estate, fishing).",
            "A place for socializing (e.g. gentlemen’s club, local bar, uncle’s house).",
            "A place connected with your ideology/belief (e.g. parish church, Mecca, Stonehenge).",
            "The grave of a significant person. Who? (e.g. a parent, a child, a lover).",
            "Your family home (e.g. a country estate, a rented flat, the orphanage in which you were raised).",
            "The place you were happiest in your life (e.g. the park bench where you first kissed, your university, your grandmother’s home).",
            "Your workplace (e.g. the office, library, bank)."
        ]
        selected_meaningful_locations = random.choice(meaningful_locations)
    
        treasured_possessions = [
            "An item connected with your highest skill (e.g. expensive suit, false ID, brass knuckles).",
            "An essential item for your occupation (e.g. doctor’s bag, car, lock picks).",
            "A memento from your childhood (e.g. comics, pocketknife, lucky coin).",
            "A memento of a departed person (e.g. jewelry, a photograph in your wallet, a letter).",
            "Something given to you by your Significant Person (e.g. a ring, a diary, a map).",
            "Your collection. What is it? (e.g. bus tickets, stuffed animals, records).",
            "Something you found but you don’t know what it is—you seek answers (e.g. a letter you found in a cupboard written in an unknown language, a curious pipe of unknown origin found among your late father’s effects, a strange silver ball you dug up in your garden).",
            "A sporting item (e.g. cricket bat, a signed baseball, a fishing rod).",
            "A weapon (e.g. service revolver, your old hunting rifle, the hidden knife in your boot).",
            "A pet (e.g. a dog, a cat, a tortoise)."
        ]
        selected_treasured_possessions = random.choice(treasured_possessions)
    
        traits = [
            "Generous (e.g. generous tipper, always helps out a person in need, philanthropist).",
            "Good with Animals (e.g. loves cats, grew up on a farm, good with horses).",
            "Dreamer (e.g. given to flights of fancy, visionary, highly creative).",
            "Hedonist (e.g. life and soul of the party, entertaining drunk, \"live fast and die young\").",
            "Gambler and a risk-taker (e.g. poker-faced, try anything once, lives on the edge).",
            "Good Cook (e.g. bakes wonderful cakes, can make a meal from almost nothing, refined palate).",
            "Ladies’ man/seductress (e.g. suave, charming voice, enchanting eyes).",
            "Loyal (e.g. stands by his or her friends, never breaks a promise, would die for his or her beliefs).",
            "A good reputation (e.g. the best after-dinner speaker in the country, the most pious of men, fearless in the face of danger).",
            "Ambitious (e.g. to achieve a goal, to become the boss, to have it all)."
        ]
        selected_traits = random.choice(traits)
    
        embed = discord.Embed(title="Character Backstory Generator", color=0x00ff00)
        embed.add_field(name=":biting_lip: Personal Description (chose one):", value=personal_description_text, inline=False)
        embed.add_field(name=":church: Ideology/Beliefs:", value=selected_ideology_beliefs, inline=False)
        embed.add_field(name=":bust_in_silhouette: Significant People:", value=f":grey_question: First, who?\n {selected_significant_people_first}\n :grey_question: Why?\n {selected_significant_people_why}", inline=False)
        embed.add_field(name=":map: Meaningful Locations:", value=selected_meaningful_locations, inline=False)
        embed.add_field(name=":gem: Treasured Possessions:", value=selected_treasured_possessions, inline=False)
        embed.add_field(name=":beginner: Traits:", value=selected_traits, inline=False)
    
        await ctx.send(embed=embed)
