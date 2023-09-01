from redbot.core import Config, commands
import random, discord, json, os, asyncio, re, math

class CthulhuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=4207503951)
        default_guild = {
            "player_stats": {}
        }
        self.config.register_guild(**default_guild)
    
    async def cog_before_invoke(self, ctx):
        self.player_stats = await self.config.guild(ctx.guild).player_stats()
        if not self.player_stats:
            self.player_stats = {}

    async def save_data(self, guild_id, player_stats):
        await self.config.guild_from_id(guild_id).player_stats.set(player_stats)

    def get_stat_description(self, value, descriptions):
        return self.get_nearest_description(value, descriptions)
        
    def get_nearest_description(self, value, descriptions):
        nearest_value = min(descriptions.keys(), key=lambda x: abs(x - value))
        return descriptions[nearest_value]
    
    def get_strength_description(self, value):
        descriptions = {
            0: "Enfeebled: unable to even stand up or lift a cup of tea.",
            15: "Puny, weak.",
            50: "Average human strength.",
            90: "One of the strongest people you’ve ever met.",
            99: "World-class (Olympic weightlifter). Human maximum.",
            140: "Beyond human strength (gorilla or horse).",
        }
        return self.get_nearest_description(value, descriptions)
        
    def get_constitution_description(self, value):
        descriptions = {
            0: "Dead.",
            1: "Sickly, prone to prolonged illness and probably unable to operate without assistance.",
            15: "Weak health, prone to bouts of ill health, great propensity for feeling pain.",
            50: "Average healthy human.",
            90: "Shrugs off colds, hardy and hale.",
            99: "Iron constitution, able to withstand great amounts of pain. Human maximum.",
            140: "Beyond human constitution (e.g. elephant).",
        }
        return self.get_nearest_description(value, descriptions)
        
    def get_dexterity_description(self, value):
        descriptions = {
            0: "Unable to move without assistance.",
            15: "Slow, clumsy with poor motor skills for fine manipulation.",
            50: "Average human dexterity.",
            90: "Fast, nimble and able to perform feats of fine manipulation (e.g. acrobat, great dancer).",
            99: "World-class athlete (e.g. Olympic standard). Human maximum.",
            120: "Beyond human dexterity (e.g. tiger).",
        }
        return self.get_stat_description(value, descriptions)
        
    def get_appearance_description(self, value):
        descriptions = {
            0: "So unsightly that others are affected by fear, revulsion, or pity.",
            15: "Ugly, possibly disfigured due to injury or at birth.",
            50: "Average human appearance.",
            90: "One of the most charming people you could meet, natural magnetism.",
            99: "The height of glamour and cool (supermodel or world-renowned film star). Human maximum.",
        }
        return self.get_stat_description(value, descriptions)
        
    def get_size_description(self, value):
        descriptions = {
            1: "A baby (1 to 12 pounds).",
            15: "Child, very short in stature (dwarf) (33 pounds / 15 kg).",
            65: "Average human size (moderate height and weight) (170 pounds / 75 kg).",
            80: "Very tall, strongly built, or obese. (240 pounds / 110 kg).",
            99: "Oversize in some respect (330 pounds / 150 kg).",
            150: "Horse or cow (960 pounds / 436 kg).",
            180: "Heaviest human ever recorded (1400 pounds / 634 kg).",
        }
        return self.get_stat_description(value, descriptions)

    def get_intelligence_description(self, value):
        descriptions = {
            0: "No intellect, unable to comprehend the world around them.",
            15: "Slow learner, able to undertake only the most basic math, or read beginner-level books.",
            50: "Average human intellect.",
            90: "Quick-witted, probably able to comprehend multiple languages or theorems.",
            99: "Genius (Einstein, Da Vinci, Tesla, etc.). Human maximum.",
        }
        return self.get_stat_description(value, descriptions)

    def get_power_description(self, value):
        descriptions = {
            0: "Enfeebled mind, no willpower or drive, no magical potential.",
            15: "Weak-willed, easily dominated by those with a greater intellect or willpower.",
            50: "Average human.",
            90: "Strong-willed, driven, a high potential to connect with the unseen and magical.",
            100: "Iron will, strong connection to the spiritual 'realm' or unseen world.",
            140: "Beyond human, possibly alien.",
        }
        return self.get_stat_description(value, descriptions)

    def get_education_description(self, value):
        descriptions = {
            0: "A newborn baby.",
            15: "Completely uneducated in every way.",
            60: "High school graduate.",
            70: "College graduate (Bachelor degree).",
            80: "Degree level graduate (Master's degree).",
            90: "Doctorate, professor.",
            96: "World-class authority in their field of study.",
            99: "Human maximum.",
        }
        return self.get_stat_description(value, descriptions)
        
    def get_skill_description(self, value):
        descriptions = {
            0: "Novice",
            6: "Neophyte",
            20: "Amateur",
            50: "Professional",
            75: "Expert",
            90: "Master",
        }
        return self.get_stat_description(value, descriptions)
        
    def get_credit_rating_description(self, value):
        descriptions = {
            0: "Penniles",
            1: "Poor",
            10: "Avarege",
            50: "Wealthy",
            90: "Rich",
            99: "Super Rich",
        }
        return self.get_stat_description(value, descriptions)
        
    def get_charisma_description(self, value):
        descriptions = {
            0: "Extremely off-putting, others are affected by fear, revulsion, or pity.",
            15: "Unpleasant demeanor, likely to repel others.",
            50: "Average human charisma.",
            90: "Charming, magnetic personality, easily wins people over.",
            99: "The pinnacle of charisma and charm (celebrities, leaders). Human maximum.",
        }
        return self.get_stat_description(value, descriptions)
        
    def get_sanity_description(self, value):
        descriptions = {
            0: "Insane, completely detached from reality.",
            15: "Severely disturbed, unable to distinguish between reality and delusion.",
            50: "Average human sanity.",
            80: "Strong mental resilience, able to cope with stress and horrors.",
            99: "Exceptional sanity, unshaken even by the most terrifying experiences. Human maximum.",
        }
        return self.get_stat_description(value, descriptions)
        
    @commands.command(aliases=["coc", "cthulhuhelp", "helpcthulhu"])
    async def cthulhu(self, ctx):
        description = (
            ":exclamation: **Important** :exclamation: \n"
            "To be able to play **Call of Cthulhu** you will need [Call of Cthulhu Keeper Rulebook](https://www.chaosium.com/call-of-cthulhu-keeper-rulebook-hardcover/), [Call of Cthulhu Starter Set](https://www.chaosium.com/call-of-cthulhu-starter-set/) or [Pulp Cthulhu](https://www.chaosium.com/pulp-cthulhu-hardcover/) published by [Chaosium.inc](https://www.chaosium.com/)\n\n"
            "Most of the commands needs you to create Investigator first. \n\n"
            "**Commands Descriptions** \n"
            ":bulb:`!randomname gender` - Generate random name form 1920s era. (e.g. `!randomname female`)\n\n"
            ":bulb:`!newInv Inv-name` - Create a new investigator (e.g. `!newInv Oswald Chester Razner`)\n\n"
            ":bulb:`!autoChar` - Generates random stats for your investigator. You can re-roll, dismiss or save stats.\n\n"
            ":bulb:`!cstat stat-name` - Edit your investigators stats. (e.g. `!cstat STR 50` or `!cstat Listen 50`) This can also calculate \n\n"
            ":bulb:`!sinfo skill-name` - Get information about specific skill (without skill-name you will get list of skills). (e.g. `!sinfo Listen`)\n\n"
            ":bulb:`!oinfo occupation-name` - Get information about occupation (without occupation-name you will get list of occupations). (e.g. `!oinfo bartender`)\n\n"
            ":bulb:`!myChar` - Show your investigators stats and skills. With @ you can show other players stats (e.g. `!myChar @potato`)\n\n"
            ":bulb:`!d YDX` - Roll dice (e.g. `!d 3D6` or `!d 3D6 + 1D10` or `!d 1D6 + 2`)\n\n"
            ":bulb:`!d skill-name` - Roll D100 against a skill. (e.g. `!d Listen`)\n\n"
            ":bulb:`!db skill-name` - Roll D100 with bonus die against a skill. (e.g. `!db Listen`)\n\n"
            ":bulb:`!dp skill-name` - Roll D100 with penality die against a skill. (e.g. `!dp Listen`)\n\n"
            ":bulb:`!mb` - Show your investigators inventory and backstory.\n\n"
            ":bulb:`!cb category - item` - Add a record to your backstory or inventory. (e.g. `!cb Inventory - Colt .45 Automatic M1911` or `!cb Significant People - Mr. Pickles`)\n\n"
            ":bulb:`!rb category itemID` - Remove a record from your backstory or inventory. You can see ID with `!mb` (e.g. `!cb Inventory 1`)\n\n"
            ":bulb:`!gbackstory` - Generate random backstory for your investigator. This will not be saved.\n\n"
            ":bulb:`!deleteInvestigator` - Delete your investigator, all data, backstory and inventory. You will be promptet to write your investigators name to confirm deletion.\n\n"
            ":bulb:`!cyear number` - Get basic information about events in year (1890-2012) (e.g. `!cyear 1920`)\n\n"
            ":bulb:`!firearm name` - Get basic information about firearms. If you use just `!firearm` you will get list of firearms. (e.g. `!firearm m1911`)\n\n"
            ":bulb:`!randomLoot` - Generate random loot from 1920s. 25% chance of finding $0.1-$10. This will not be saved.\n\n"
            ":bulb:`!rskill skill1 skill2` - Rename skill to your liking. (e.g. `!rskill Language (other) German`)\n\n"
            ":bulb:`!cNPC gender` - Generate NPC with random name and stats. (e.g. `!cNPC male`)\n\n"
            ":bulb:`!showUserData` - Debug command showing raw user data (stats, skill, backstory)\n\n"
        )

        embed = discord.Embed(
            title="Call of Cthulhu Help and Commands",
            description=description,
            color=discord.Color.blue()
        )

        await ctx.send(embed=embed)
        
    @commands.command(aliases=["diceroll","D"], guild_only=True)
    async def d(self, ctx, *, dice_expression):
        user_id = str(ctx.author.id)
        if user_id not in self.player_stats:  
            await ctx.send(f"{ctx.author.display_name} doesn't have an investigator. Use `!newInv` for creating a new investigator.")
        else:
            try:
                normalized_dice_expression = dice_expression.lower()  # Převod na malá písmena
                if normalized_dice_expression in map(str.lower, self.player_stats[user_id].keys()):
                    skill_name = next(
                        name for name in self.player_stats[user_id] if name.lower() == normalized_dice_expression
                    )
    
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
                                await self.save_data(ctx.guild.id, self.player_stats)  # Uložení změn LUCK do dat
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
                    components = re.split(r'\s*([+-])\s*', dice_expression)  # Rozdělení výrazu na složky
                    
                    dice_parts = [part for part in components if "d" in part.lower()]  # Pouze části s typem kostky
                    fixed_parts = [part for part in components if part.isdigit()]  # Pouze části s pevnou hodnotou
                    sign_parts = [part for part in components if part == "+" or part == "-"]  # Znaménka
                    
                    total = 0
                    # Inicializace proměnných
                    rolls_str = ""
                    current_operator = "+"  # Předpokládejme začátek sčítání
                    negative_sign = False  # Proměnná pro určení, zda má být před zápornými hodnotami znaménko "-"
                    
                    for i, part in enumerate(components):
                        if part in ["+", "-"]:
                            current_operator = part
                            rolls_str += part
                            negative_sign = False  # Resetujte proměnnou pro znaménko při změně operátoru
                        elif "d" in part.lower():  # Část s typem kostky
                            num_dice, dice_type = map(int, re.split(r'[dD]', part))
                            if dice_type not in [4, 6, 8, 10, 12, 20, 100]:
                                embed = discord.Embed(
                                    title="Invalid Dice Type",
                                    description="Use :game_die: D4, D6, D8, D10, D12, D20, or D100.",
                                    color=discord.Color.red()
                                )
                                await ctx.send(embed=embed)
                                return
                            
                            rolls = [random.randint(1, dice_type) for _ in range(num_dice)]
                            rolls_str += f"{num_dice}d{dice_type}("
                            if negative_sign:  # Přidání znaménka "-" před zápornými hodnotami
                                rolls_str += "-"
                                negative_sign = False
                            rolls_str += ", ".join(map(str, rolls))
                            rolls_str += ")"  # Přidejte uzavírací závorku pro tuto kostku
                            if current_operator == "+":
                                total += sum(rolls)
                            else:
                                total -= sum(rolls)
                            
                            if i < len(components) - 1 and components[i + 1] not in ["+", "-"]:
                                rolls_str += f" {current_operator} "
                        else:  # Část s pevnou hodnotou
                            fixed_value = int(part)
                            if negative_sign:  # Přidání znaménka "-" před zápornými hodnotami
                                rolls_str += "-"
                                negative_sign = False
                            rolls_str += str(abs(fixed_value))  # Použijeme abs() pro zobrazení hodnoty bez znaménka
                            if current_operator == "+":
                                total += fixed_value
                            else:
                                total -= fixed_value
                            
                            if i < len(components) - 1 and components[i + 1] not in ["+", "-"]:
                                rolls_str += f" {current_operator} "
                            if fixed_value < 0:
                                negative_sign = True  # Nastavení proměnné pro znaménko před následujícími hodnotami


                    
                    embed = discord.Embed(
                        title=f"Rolled Dice Expression: {dice_expression}",
                        description=f":game_die: Rolls: {rolls_str}\nTotal: {total}",
                        color=discord.Color.green()
                    )
                
                    await ctx.send(embed=embed)
            except ValueError:
                embed = discord.Embed(
                    title="Invalid Input",
                    description="Use format !d <skill_name>, XdY, XdY+Z, or XdY-Z where X is the number of dice, Y is the dice type, and Z is the modifier.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
    
    @commands.command(aliases=["newInv","newinv"], guild_only=True)
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
            "EDU": 0,
            "SIZ": 0,
            "APP": 0,
            "LUCK": 0,
            "HP": 0,
            "MP": 0,
            "SAN": 0,
            "Move": 0,
            "Build": 0,
            "Damage Bonus": 0,
            "Age": 0,
            "Accounting": 5,
            "Anthropology": 1,
            "Appraise": 5,
            "Archaeology": 1,
            "Charm": 15,
            "Art/Craft": 5,
            "Climb": 20,
            "Credit Rating": 0,
            "Cthulhu Mythos": 0,
            "Disguise": 5,
            "Dodge": 0,
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
            "Language (own)": 0,
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
            "CustomSkill": 0,
            "CustomSkills": 0,
            "CustomSkillss": 0,
            "MAX_HP": 100,
            "MAX_MP": 100,
            "MAX_SAN": 1000,
            "Backstory":{}
            }
            await self.save_data(ctx.author.guild.id, self.player_stats)  # Uložení změn do souboru
            await ctx.send(f"Investigator '{investigator_name}' has been created with all stats set to 0. You can generate random stats by ussing `!autoChar` or you can fill your stats with `!cstat`")
        else:
            await ctx.send("You already have an investigator. You can't create a new one until you delete the existing one with `!deleteInvestigator`.")
            
    @commands.command(aliases=["cstat"], guild_only=True)
    async def CthulhuChangeStats(self, ctx, *args):
        user_id = str(ctx.author.id)  # Get the user's ID as a string

        def get_stat_emoji(stat_name):
            stat_emojis = {
                "STR": ":muscle:",
                "DEX": ":runner:",
                "CON": ":heart:",
                "INT": ":brain:",
                "POW": ":zap:",
                "APP": ":heart_eyes:",
                "EDU": ":mortar_board:",
                "SIZ": ":bust_in_silhouette:",
                "HP": ":heartpulse:",
                "MP": ":sparkles:",
                "LUCK": ":four_leaf_clover:",
                "SAN": ":scales:",
                "Age": ":birthday:",
                "Move": ":person_running:",
                "Build": ":restroom: ",
                "Damage Bonus": ":mending_heart:",
                "Accounting": ":ledger:",
                "Anthropology": ":earth_americas:",
                "Appraise": ":mag:",
                "Archaeology": ":pick:",
                "Charm": ":heart_decoration:",
                "Art/Craft": ":art:",
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
            }
            return stat_emojis.get(stat_name, ":question:")

        if user_id not in self.player_stats:
            await ctx.send(f"{ctx.author.display_name} doesn't have an investigator. Use `!newInv` for creating a new investigator.")
        else:
            stat_name = " ".join(args[:-1])  # Všechny argumenty kromě posledního
            try:
                new_value = int(args[-1])
            except ValueError:
                await ctx.send("Invalid new value. Please provide a number.")
                return

            matching_skills = [stat for stat in self.player_stats[user_id] if re.search(fr'\b{re.escape(stat_name)}\b', stat, re.IGNORECASE)]
            
            if matching_skills:
                if len(matching_skills) > 1:
                    await ctx.send(f"Found multiple matching skills: {', '.join(matching_skills)}. Please specify the skill name more clearly.")
                else:
                    stat_name = matching_skills[0]
                    try:
                        #Surpassing MAX_HP
                        if stat_name == "HP" and new_value > self.player_stats[user_id]["MAX_HP"]:
                            maxhp_message = await ctx.send(f"You're attempting to surpass your **HP**:heartpulse: limit. Would you like me to increase the **maximum HP**:chart_with_upwards_trend::heartpulse:?")
                            await maxhp_message.add_reaction("✅")
                            await maxhp_message.add_reaction("❌")
                            def check(reaction, user):
                                return user == ctx.author and reaction.message.id == maxhp_message.id and str(reaction.emoji) in ["✅", "❌"]
                            try:
                                reaction, _ = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                                if str(reaction.emoji) == "✅":
                                    newMAXHP = new_value
                                    self.player_stats[user_id]["MAX_HP"] = newMAXHP
                                    await self.save_data(ctx.guild.id, self.player_stats)  # Uložení celého slovníku
                                    await ctx.send(f"{ctx.author.display_name}'s **maximum HP**:chart_with_upwards_trend::heartpulse: has been increased to **{newMAXHP}** and successfully saved.")
                                elif str(reaction.emoji) == "❌":
                                    await ctx.send(f"{ctx.author.display_name}'s **maximum HP**:chart_with_upwards_trend::heartpulse: will not been increased.")
                            except asyncio.TimeoutError:
                                await ctx.send(f"{ctx.author.display_name} took too long to react. **Maximum HP**:chart_with_upwards_trend::heartpulse: will not been increased.")                        

                        #Surpassing MAX_MP
                        if stat_name == "MP" and new_value > self.player_stats[user_id]["MAX_MP"]:
                            maxmp_message = await ctx.send(f"You're attempting to surpass your **MP**:sparkles: limit. Would you like me to increase the **maximum MP**:chart_with_upwards_trend::sparkles:?")
                            await maxmp_message.add_reaction("✅")
                            await maxmp_message.add_reaction("❌")
                            def check(reaction, user):
                                return user == ctx.author and reaction.message.id == maxmp_message.id and str(reaction.emoji) in ["✅", "❌"]
                            try:
                                reaction, _ = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                                if str(reaction.emoji) == "✅":
                                    newMAXMP = new_value
                                    self.player_stats[user_id]["MAX_MP"] = newMAXMP
                                    await self.save_data(ctx.guild.id, self.player_stats)  # Uložení celého slovníku
                                    await ctx.send(f"{ctx.author.display_name}'s **maximum MP**:chart_with_upwards_trend::sparkles: has been increased to **{newMAXMP}** and successfully saved.")
                                elif str(reaction.emoji) == "❌":
                                    await ctx.send(f"{ctx.author.display_name}'s **maximum MP**:chart_with_upwards_trend::sparkles: will not been increased.")
                            except asyncio.TimeoutError:
                                await ctx.send(f"{ctx.author.display_name} took too long to react. **Maximum MP**:chart_with_upwards_trend::sparkles: will not been increased.")                        

                        self.player_stats[user_id][stat_name] = new_value
                        await self.save_data(ctx.guild.id, self.player_stats)  # Uložení celého slovníku
                        #Adding emoji to stat update message
                        emoji = get_stat_emoji(stat_name)
                        await ctx.send(f"{ctx.author.display_name}'s **{stat_name}**{emoji} has been updated to **{new_value}**.")

                        #automatic calculation of HP
                        if stat_name == "CON" or stat_name == "SIZ":
                            if self.player_stats[user_id]["CON"] != 0 and self.player_stats[user_id]["SIZ"] != 0 and self.player_stats[user_id]["HP"] == 0:
                                hp_message = await ctx.send(f"{ctx.author.display_name} filled all stats required to calculate **HP**:heartpulse:. Do you want me to calculate HP(MAX_HP):chart_with_upwards_trend::heartpulse:?")
                                await hp_message.add_reaction("✅")
                                await hp_message.add_reaction("❌")
                                def check(reaction, user):
                                    return user == ctx.author and reaction.message.id == hp_message.id and str(reaction.emoji) in ["✅", "❌"]
                                try:
                                    reaction, _ = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                                    if str(reaction.emoji) == "✅":
                                        HP = math.floor((self.player_stats[user_id]["CON"] + self.player_stats[user_id]["SIZ"]) / 10)
                                        self.player_stats[user_id]["HP"] = HP
                                        self.player_stats[user_id]["MAX_HP"] = HP
                                        await self.save_data(ctx.guild.id, self.player_stats)  # Uložení celého slovníku
                                        await ctx.send(f"{ctx.author.display_name}'s **HP**:heartpulse: has been calculated as **{HP}** and successfully saved.")
                                    elif str(reaction.emoji) == "❌":
                                        await ctx.send(f"The calculation of **HP**:heartpulse: will not proceed.")
                                except asyncio.TimeoutError:
                                    await ctx.send(f"{ctx.author.display_name} took too long to react. The calculation of **HP**:heartpulse: will not proceed.")

                        #automatic calculation of MP
                        if stat_name == "POW":
                            if self.player_stats[user_id]["POW"] != 0 and self.player_stats[user_id]["MP"] == 0:
                                mp_message = await ctx.send(f"{ctx.author.display_name} filled all stats required to calculate **MP**:sparkles:. Do you want me to calculate MP(MAX_MP)chart_with_upwards_trend::sparkles:?")
                                await mp_message.add_reaction("✅")
                                await mp_message.add_reaction("❌")
                                def check(reaction, user):
                                    return user == ctx.author and reaction.message.id == mp_message.id and str(reaction.emoji) in ["✅", "❌"]
                                try:
                                    reaction, _ = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                                    if str(reaction.emoji) == "✅":
                                        MP = math.floor(self.player_stats[user_id]["POW"] / 10)
                                        self.player_stats[user_id]["MP"] = MP
                                        self.player_stats[user_id]["MAX_MP"] = MP
                                        await self.save_data(ctx.guild.id, self.player_stats)  # Uložení celého slovníku
                                        await ctx.send(f"{ctx.author.display_name}'s **MP**:sparkles: has been calculated as **{MP}** and successfully saved.")
                                    elif str(reaction.emoji) == "❌":
                                        await ctx.send(f"The calculation of **MP**:sparkles: will not proceed.")
                                except asyncio.TimeoutError:
                                    await ctx.send(f"{ctx.author.display_name} took too long to react. The calculation of **MP**:sparkles: will not proceed.") 

                        #automatic calculation of SAN
                        if stat_name == "POW":
                            if self.player_stats[user_id]["POW"] != 0 and self.player_stats[user_id]["SAN"] == 0:
                                san_message = await ctx.send(f"{ctx.author.display_name} filled all stats required to calculate **SAN**:scales:. Do you want me to calculate SAN:scales:?")
                                await san_message.add_reaction("✅")
                                await san_message.add_reaction("❌")
                                def check(reaction, user):
                                    return user == ctx.author and reaction.message.id == san_message.id and str(reaction.emoji) in ["✅", "❌"]
                                try:
                                    reaction, _ = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                                    if str(reaction.emoji) == "✅":
                                        SAN = self.player_stats[user_id]["POW"]
                                        self.player_stats[user_id]["SAN"] = SAN
                                        await self.save_data(ctx.guild.id, self.player_stats)  # Uložení celého slovníku
                                        await ctx.send(f"{ctx.author.display_name}'s **SAN**:scales: has been calculated as **{SAN}** and successfully saved.")
                                    elif str(reaction.emoji) == "❌":
                                        await ctx.send(f"The calculation of **SAN**:scales: will not proceed.")
                                except asyncio.TimeoutError:
                                    await ctx.send(f"{ctx.author.display_name} took too long to react. The calculation of **SAN**:scales: will not proceed.")

                        #automatic calculation of Dodge
                        if stat_name == "DEX":
                            if self.player_stats[user_id]["DEX"] != 0 and self.player_stats[user_id]["Dodge"] == 0:
                                dod_message = await ctx.send(f"{ctx.author.display_name} filled all stats required to calculate **Dodge**:warning:. Do you want me to calculate Dodge:warning:?")
                                await dod_message.add_reaction("✅")
                                await dod_message.add_reaction("❌")
                                def check(reaction, user):
                                    return user == ctx.author and reaction.message.id == dod_message.id and str(reaction.emoji) in ["✅", "❌"]
                                try:
                                    reaction, _ = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                                    if str(reaction.emoji) == "✅":
                                        DODGE = math.floor(self.player_stats[user_id]["DEX"] / 2)
                                        self.player_stats[user_id]["Dodge"] = DODGE
                                        await self.save_data(ctx.guild.id, self.player_stats)  # Uložení celého slovníku
                                        await ctx.send(f"{ctx.author.display_name}'s **Dodge**:warning: has been calculated as **{DODGE}** and successfully saved.")
                                    elif str(reaction.emoji) == "❌":
                                        await ctx.send(f"The calculation of **Dodge**:warning: will not proceed.")
                                except asyncio.TimeoutError:
                                    await ctx.send(f"{ctx.author.display_name} took too long to react. The calculation of **Dodge**:warning: will not proceed.")   

                        #automatic calculation of Language (own)
                        if stat_name == "EDU":
                            if self.player_stats[user_id]["EDU"] != 0 and self.player_stats[user_id]["Language (own)"] == 0:
                                dod_message = await ctx.send(f"{ctx.author.display_name} filled all stats required to calculate **Language (own)**:speech_balloon:. Do you want me to calculate Language (own):speech_balloon:?")
                                await dod_message.add_reaction("✅")
                                await dod_message.add_reaction("❌")
                                def check(reaction, user):
                                    return user == ctx.author and reaction.message.id == dod_message.id and str(reaction.emoji) in ["✅", "❌"]
                                try:
                                    reaction, _ = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                                    if str(reaction.emoji) == "✅":
                                        LANGUAGEOWN = self.player_stats[user_id]["EDU"]
                                        self.player_stats[user_id]["Language (own)"] = LANGUAGEOWN
                                        await self.save_data(ctx.guild.id, self.player_stats)  # Uložení celého slovníku
                                        await ctx.send(f"{ctx.author.display_name}'s **Language (own)**:speech_balloon: has been calculated as **{LANGUAGEOWN}** and successfully saved.")
                                    elif str(reaction.emoji) == "❌":
                                        await ctx.send(f"The calculation of **Language (own)**:speech_balloon: will not proceed.")
                                except asyncio.TimeoutError:
                                    await ctx.send(f"{ctx.author.display_name} took too long to react. The calculation of **Language (own)**:speech_balloon: will not proceed.")   

                        #Prompt about Age
                        if stat_name == "STR" or stat_name == "DEX" or stat_name == "CON" or stat_name == "EDU" or stat_name == "APP" or stat_name == "SIZ" or stat_name == "LUCK":
                            if self.player_stats[user_id]["STR"] != 0 and self.player_stats[user_id]["DEX"] != 0 and self.player_stats[user_id]["CON"] != 0 and self.player_stats[user_id]["EDU"] != 0 and self.player_stats[user_id]["APP"] != 0 and self.player_stats[user_id]["SIZ"] != 0 and self.player_stats[user_id]["LUCK"] and self.player_stats[user_id]["Age"] == 0:
                                await ctx.send(f"{ctx.author.display_name} filled all stats that are affected by Age. Fill your age with `!cstat Age`")

                        #Age mod help
                        if stat_name == "Age":
                            if self.player_stats[user_id]["Age"] < 15:
                                await ctx.send(f"Age Modifiers: There are no official rules about investigators under 15 years old.")
                            elif self.player_stats[user_id]["Age"] < 20:
                                await ctx.send(f"Age Modifiers: Deduct 5 points among STR:muscle: and SIZ:bust_in_silhouette:. Deduct 5 points from EDU:mortar_board:. Roll twice to generate a Luck score and use the higher value.")
                            elif self.player_stats[user_id]["Age"] < 40:
                                await ctx.send(f"Age Modifiers: Make an improvement check for EDU:mortar_board:.")
                                await ctx.send(f"To make improvement check for EDU:mortar_board: run `!d EDU`. I you FAIL:x: add `!d 1D10` to your EDU:mortar_board:.")
                            elif self.player_stats[user_id]["Age"] < 50:
                                await ctx.send(f"Age Modifiers: Make 2 improvement checks for EDU:mortar_board: and deduct 5 points among STR:muscle:, CON:heart: or DEX:runner:, and reduce APP:heart_eyes: by 5.")
                                await ctx.send(f"To make improvement check for EDU:mortar_board: run `!d EDU`. I you FAIL:x: add `!d 1D10` to your EDU:mortar_board:.")
                            elif self.player_stats[user_id]["Age"] < 60:
                                await ctx.send(f"Age Modifiers: Make 3 improvement checks for EDU:mortar_board: and deduct 10 points among STR:muscle:, CON:heart: or DEX:runner:, and reduce APP:heart_eyes: by 10")
                                await ctx.send(f"To make improvement check for EDU:mortar_board: run `!d EDU`. I you FAIL:x: add `!d 1D10` to your EDU:mortar_board:.")
                            elif self.player_stats[user_id]["Age"] < 70:
                                await ctx.send(f"Age Modifiers: Make 4 improvement checks for EDU:mortar_board: and deduct 20 points among STR:muscle:, CON:heart: or DEX:runner:, and reduce APP:heart_eyes: by 15.")
                                await ctx.send(f"To make improvement check for EDU:mortar_board: run `!d EDU`. I you FAIL:x: add `!d 1D10` to your EDU:mortar_board:.")
                            elif self.player_stats[user_id]["Age"] < 80:
                                await ctx.send(f"Age Modifiers:  Make 4 improvement checks for EDU:mortar_board: and deduct 40 points among STR:muscle:, CON:heart: or DEX:runner:, and reduce APP:heart_eyes: by 20.")
                                await ctx.send(f"To make improvement check for EDU:mortar_board: run `!d EDU`. I you FAIL:x: add `!d 1D10` to your EDU:mortar_board:.")
                            elif self.player_stats[user_id]["Age"] < 90:
                                await ctx.send(f"Age Modifiers: Make 4 improvement checks for EDU:mortar_board: and deduct 80 points among STR:muscle:, CON:heart: or DEX:runner:, and reduce APP:heart_eyes: by 25.")
                                await ctx.send(f"To make improvement check for EDU:mortar_board: run `!d EDU`. I you FAIL:x: add `!d 1D10` to your EDU:mortar_board:.")
                            else:
                                await ctx.send(f"Age Modifiers: There are no official rules about investigators above the age of 90.")
                            

                    except ValueError:
                        await ctx.send("Invalid new value. Please provide a number.")
            else:
                await ctx.send(f"Invalid name {stat_name}. Use STR, DEX, CON, INT, POW, APP, EDU, SIZ, HP, MP, LUCK or SAN. You can also use any name of your skills `!mcs`")


    @commands.command(aliases=["rskill"], guild_only=True)
    async def renameSkill(self, ctx, *, old_and_new_name):
        user_id = str(ctx.author.id)  # Get the user's ID as a string
        old_and_new_name = old_and_new_name.rsplit(maxsplit=1)
        
        if len(old_and_new_name) != 2:
            await ctx.send("Invalid input. Please provide old skill name and new skill name.")
            return
        
        old_skill_name = old_and_new_name[0].title()  # Convert the old skill name to title case
        new_skill_name = old_and_new_name[1].title()  # Convert the new skill name to title case
        
        if user_id in self.player_stats:
            normalized_old_skill_name = old_skill_name.lower()  # Normalize old skill name to lowercase
            matching_skills = [s for s in self.player_stats[user_id] if s.lower().replace(" ", "") == normalized_old_skill_name.replace(" ", "")]
            
            if matching_skills:
                try:
                    self.player_stats[user_id][new_skill_name] = self.player_stats[user_id].pop(matching_skills[0])
                    
                    # Move "Backstory" to the end of the dictionarya
                    if "Backstory" in self.player_stats[user_id]:
                        backstory = self.player_stats[user_id].pop("Backstory")
                        self.player_stats[user_id]["Backstory"] = backstory
                    
                    await self.save_data(ctx.guild.id, self.player_stats)  # Save the entire dictionary
                    await ctx.send(f"Your skill '{matching_skills[0]}' has been updated to '{new_skill_name}'.")
                except KeyError:
                    await ctx.send("An error occurred while updating the skill. Please try again.")
            else:
                await ctx.send("Skill not found in your skills list.")
        else:
            await ctx.send(f"{ctx.author.display_name} doesn't have an investigator. Use `!newInv` for creating a new investigator.")

    #Debugging command to check if your data are corrupted        
    @commands.command(guild_only=True)
    async def showUserData(self, ctx):
        user_id = str(ctx.author.id)  # Get the user's ID as a string
        
        if user_id in self.player_stats:
            user_data = self.player_stats[user_id]
            user_data_formatted = "\n".join([f"{skill}: {value}" for skill, value in user_data.items()])
            await ctx.send(f"Here is your user data:\n```{user_data_formatted}```")
        else:
            await ctx.send(f"{ctx.author.display_name} doesn't have an investigator. Use `!newInv` for creating a new investigator.")


    @commands.command(aliases=["mychar", "mcs","myChar","MyChar"], guild_only=True)
    async def MyCthulhuStats(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author
    
        user_id = str(member.id)  # Get the user's ID as a string
        if user_id not in self.player_stats:  # Initialize the user's stats if they don't exist
            await ctx.send(f"{ctx.author.display_name} doesn't have an investigator. Use `!newInv` for creating a new investigator.")
            return
    
        name = self.player_stats.get(user_id, {}).get("NAME", f"{ctx.author.display_name}'s Investigator Stats")
    
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
                "APP": ":heart_eyes:",
                "EDU": ":mortar_board:",
                "SIZ": ":bust_in_silhouette:",
                "HP": ":heartpulse:",
                "MP": ":sparkles:",
                "LUCK": ":four_leaf_clover:",
                "SAN": ":scales:",
                "Age": ":birthday:",
                "Move": ":person_running:",
                "Build": ":restroom: ",
                "Damage Bonus": ":mending_heart:",
                "Accounting": ":ledger:",
                "Anthropology": ":earth_americas:",
                "Appraise": ":mag:",
                "Archaeology": ":pick:",
                "Charm": ":heart_decoration:",
                "Art/Craft": ":art:",
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
            }
            return stat_emojis.get(stat_name, ":question:")

        def get_stat_value(stat_name, value):
            formatted_value = ""
            if stat_name == "Age":
                formatted_value = f"{value}"
            elif stat_name == "HP":
                formatted_value = f"{value}/" + str(self.player_stats[user_id]["MAX_HP"])
            elif stat_name == "MP":
                formatted_value = f"{value}/" + str(self.player_stats[user_id]["MAX_MP"])
            elif stat_name == "Move":
                if self.player_stats[user_id]["DEX"] != 0 and \
                    self.player_stats[user_id]["SIZ"] != 0 and \
                    self.player_stats[user_id]["STR"] != 0:
                    if  self.player_stats[user_id]["DEX"] < self.player_stats[user_id]["SIZ"] and \
                        self.player_stats[user_id]["STR"] < self.player_stats[user_id]["SIZ"]:
                        MOV = 7                            
                    elif self.player_stats[user_id]["DEX"] < self.player_stats[user_id]["SIZ"] or \
                        self.player_stats[user_id]["STR"] < self.player_stats[user_id]["SIZ"]:
                        MOV = 8
                    elif self.player_stats[user_id]["DEX"] == self.player_stats[user_id]["SIZ"] and \
                        self.player_stats[user_id]["SIZ"] == self.player_stats[user_id]["STR"]:
                        MOV = 8                           
                    elif self.player_stats[user_id]["DEX"] > self.player_stats[user_id]["SIZ"] and \
                        self.player_stats[user_id]["STR"] > self.player_stats[user_id]["SIZ"]:
                        MOV = 9                            
                    else:
                        #This should be impossible. If you see MOV over 9000, i totaly fucked up this code.
                        MOV = 9001
                    formatted_value = f"{MOV}"
                else:
                    formatted_value = f"Fill your DEX, STR and SIZ."

            elif stat_name == "Build":
                if self.player_stats[user_id]["STR"] != 0 and self.player_stats[user_id]["SIZ"] != 0:
                    STRSIZ = self.player_stats[user_id]["STR"] + self.player_stats[user_id]["SIZ"]
                    if 2 <= STRSIZ <= 64:
                        BUILD = -2
                    elif 65 <= STRSIZ <= 84:
                        BUILD = -1
                    elif 85 <= STRSIZ <= 124:
                        BUILD = 0
                    elif 125 <= STRSIZ <= 164:
                        BUILD = 1
                    elif 165 <= STRSIZ <= 204:
                        BUILD = 2
                    elif 205 <= STRSIZ <= 284:
                        BUILD = 3
                    elif 285 <= STRSIZ <= 364:
                        BUILD = 4
                    elif 365 <= STRSIZ <= 444:
                        BUILD = 5
                    elif 445 <= STRSIZ <= 524:
                        BUILD = 6
                    else:
                        #Not posible if used correctly!
                        BUILD = "You are CHONKER! (7+)"
                    formatted_value = f"{BUILD}"
                else:
                    formatted_value = f"Fill your STR and SIZ."

            elif stat_name == "Damage Bonus":
                if self.player_stats[user_id]["STR"] != 0 and self.player_stats[user_id]["SIZ"] != 0:
                    STRSIZ = self.player_stats[user_id]["STR"] + self.player_stats[user_id]["SIZ"]
                    if 2 <= STRSIZ <= 64:
                        BONUSDMG = -2
                    elif 65 <= STRSIZ <= 84:
                        BONUSDMG = -1
                    elif 85 <= STRSIZ <= 124:
                        BONUSDMG = 0
                    elif 125 <= STRSIZ <= 164:
                        BONUSDMG = "1D4"
                    elif 165 <= STRSIZ <= 204:
                        BONUSDMG = "1D6"
                    elif 205 <= STRSIZ <= 284:
                        BONUSDMG = "2D6"
                    elif 285 <= STRSIZ <= 364:
                        BONUSDMG = "3D6"
                    elif 365 <= STRSIZ <= 444:
                        BONUSDMG = "4D6"
                    elif 445 <= STRSIZ <= 524:
                        BONUSDMG = "5D6"
                    else:
                        #Not posible if used correctly!
                        BONUSDMG = "You are too strong! (6D6+)"
                    formatted_value = f"{BONUSDMG}"
                else:
                    formatted_value = f"Fill your STR and SIZ."            
            elif stat_name in ["LUCK"]:
                formatted_value = f"{value} - {value // 2} - {value // 5}"
            else:
                formatted_value = f"{value} - {value // 2} - {value // 5}"
                if stat_name == "STR":
                    formatted_value += f"\n{self.get_strength_description(value)}"
                elif stat_name == "CON":
                    formatted_value += f"\n{self.get_constitution_description(value)}"
                elif stat_name == "SIZ":
                    formatted_value += f"\n{self.get_size_description(value)}"
                elif stat_name == "DEX":
                    formatted_value += f"\n{self.get_dexterity_description(value)}"
                elif stat_name == "APP":
                    formatted_value += f"\n{self.get_appearance_description(value)}"
                elif stat_name == "INT":
                    formatted_value += f"\n{self.get_intelligence_description(value)}"
                elif stat_name == "POW":
                    formatted_value += f"\n{self.get_power_description(value)}"
                elif stat_name == "EDU":
                    formatted_value += f"\n{self.get_education_description(value)}"
                elif stat_name == "Credit Rating":
                    formatted_value += f"\n{self.get_credit_rating_description(value)}"
                elif stat_name == "APP":
                    formatted_value += f"\n{self.get_charisma_description(value)}"
                elif stat_name == "SAN":
                    formatted_value += f"\n{self.get_sanity_description(value)}"
                else:
                    formatted_value += f"\n{self.get_skill_description(value)}"
            return formatted_value
    
        def generate_stats_page(page):
            stats_embed.clear_fields()
            stats_embed.description = f"Investigator statistics - Page {page}/{max_page}:"
    
            if page == 1:
                stats_range = range(0, 17)
            elif page == 2:
                stats_range = range(17, 41)
            elif page == 3:
                stats_range = range(41, 68)
            else:
                stats_range = range(69, len(stats_list))
    
            for i in stats_range:
                stat_name, value = stats_list[i]
                if stat_name == "NAME" or stat_name == "MAX_HP" or stat_name == "MAX_MP" or stat_name == "MAX_SAN" or stat_name == "Backstory":
                    continue
                
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
                
    @commands.command(guild_only=True)
    async def deleteInvestigator(self, ctx):
        user_id = str(ctx.author.id)  # Get the user's ID as a string
    
        if user_id in self.player_stats:
            investigator_name = self.player_stats[user_id]["NAME"]
            await ctx.send(f"Are you sure you want to delete investigator '{investigator_name}'? "
                           f"Type '{investigator_name}' to confirm or anything else to cancel.")
            
            def check(message):
                return message.author == ctx.author and message.content.strip().title() == investigator_name
            
            try:
                confirmation_msg = await self.bot.wait_for("message", timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Confirmation timed out. Investigator was not deleted.")
            else:
                del self.player_stats[user_id]
                await self.save_data(ctx.guild.id, self.player_stats)  # Save the updated dictionary
                await ctx.send(f"Investigator '{investigator_name}' has been deleted.")
        else:
            await ctx.send(f"{ctx.author.display_name} doesn't have an investigator. Use `!newInv` for creating a new investigator.")

         
    @commands.command(aliases=["cb","CB"], guild_only=True)
    async def CthulhuBackstory(self, ctx, *, input_text):
        user_id = str(ctx.author.id)
    
        if user_id not in self.player_stats:
            await ctx.send(f"{ctx.author.display_name} doesn't have an investigator. Use `!newInv` for creating a new investigator.")
            return
    
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
    
        await self.save_data(ctx.guild.id, self.player_stats)  # Save the entire dictionary
    
        await ctx.send(f"Entry '{entry}' has been added to the '{category}' category in your Backstory.")


    @commands.command(aliases=["mb","MB"], guild_only=True)
    async def MyCthulhuBackstory(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in self.player_stats:
            await ctx.send(f"{ctx.author.display_name} doesn't have an investigator. Use `!newInv` for creating a new investigator.")
            return
        
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
        
        await self.save_data(ctx.guild.id, self.player_stats)  # Uložení celého slovníku
        
        for category, entries in backstory_data.items():
            formatted_entries = "\n".join([f"{index + 1}. {entry}" for index, entry in enumerate(entries)])
            entries_embed.add_field(name=category, value=formatted_entries, inline=False)
        
        await ctx.send(embed=entries_embed)



    @commands.command(aliases=["rb","RB"], guild_only=True)
    async def RemoveCthulhuBackstory(self, ctx, *, category_and_index: str):
        user_id = str(ctx.author.id)
        if user_id not in self.player_stats:
            await ctx.send(f"{ctx.author.display_name} doesn't have an investigator. Use `!newInv` for creating a new investigator.")
            return
        
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
        
        await self.save_data(ctx.guild.id, self.player_stats)  # Uložení celého slovníku
        await ctx.send(f"Removed entry '{removed_entry}' from the '{category}' category.")


    @commands.command(aliases=["DB"], guild_only=True)
    async def db(self, ctx, *, skill_name):
        user_id = str(ctx.author.id)
        if user_id not in self.player_stats:
            await ctx.send(f"{ctx.author.display_name} doesn't have an investigator. Use `!newInv` for creating a new investigator.")
            return
        
        normalized_skill_name = skill_name.lower()  # Převod na malá písmena
        
        if normalized_skill_name in map(str.lower, self.player_stats[user_id].keys()):
            skill_name = next(
                name for name in self.player_stats[user_id] if name.lower() == normalized_skill_name
            )
            
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
                description=f":game_die: Rolled: {roll_1}, {roll_2}, {roll_3} (Lower roll: {total}) + {roll}\n{result}\n{formatted_skill}\n{formatted_luck}",
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
                        await self.save_data(ctx.guild.id, self.player_stats)  # Uložení změn LUCK do dat
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

    
    @commands.command(aliases=["DP"], guild_only=True)
    async def dp(self, ctx, *, skill_name):
        user_id = str(ctx.author.id)
        if user_id not in self.player_stats:
            await ctx.send(f"{ctx.author.display_name} doesn't have an investigator. Use `!newInv` for creating a new investigator.")
            return
        
        normalized_skill_name = skill_name.lower()  # Převod na malá písmena
        
        if normalized_skill_name in map(str.lower, self.player_stats[user_id].keys()):
            skill_name = next(
                name for name in self.player_stats[user_id] if name.lower() == normalized_skill_name
            )
            
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
                description=f":game_die: Rolled: {roll_1}, {roll_2}, {roll_3} (Higher roll: {total}) + {roll}\n{result}\n{formatted_skill}\n{formatted_luck}",
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
                        await self.save_data(ctx.guild.id, self.player_stats)  # Uložení změn LUCK do dat
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


    @commands.command(aliases=["randomname"])
    async def cname(self, ctx, gender):
        gender = gender.lower()
        if gender not in ["male", "female"]:
            await ctx.send("Invalid gender. Use 'male' or 'female'.")
            return
        
        if gender == "male":
            name_list = [ "Aaron", "Abraham", "Addison", "Amos", "Anderson", "Archibald", "August", "Barnabas", "Barney", "Baxter","Blair", "Caleb", "Cecil", "Chester", "Clifford", "Clinton", "Cornelius", "Curtis", "Dayton", "Delbert","Douglas", "Dudley", "Ernest", "Eldridge", "Elijah", "Emanuel", "Emmet", "Enoch", "Ephraim", "Everett",
                           "Ezekiel", "Forest", "Gilbert", "Granville", "Gustaf", "Hampton", "Harmon", "Henderson", "Herman","Hilliard", "Howard", "Hudson", "Irvin", "Issac", "Jackson", "Jacob", "Jeremiah", "Jonah", "Josiah","Kirk", "Larkin", "Leland", "Leopold", "Lloyd", "Luther", "Manford", "Marcellus", "Martin", "Mason",
                           "Maurice", "Maynard", "Melvin", "Miles", "Milton", "Morgan", "Mortimer", "Moses", "Napoleon", "Nelson","Newton", "Noble", "Oliver", "Orson", "Oswald", "Pablo", "Percival", "Porter", "Quincy", "Randall",
                           "Reginald", "Richmond", "Rodney", "Roscoe", "Rowland", "Rupert", "Sampson", "Sanford", "Sebastian","Shelby", "Sidney", "Solomon", "Squire", "Sterling", "Sidney", "Thaddeus", "Walter", "Wilbur", "Wilfred",
                           "Zadok", "Zebedee"]
        else:
            name_list = [ "Adelaide", "Agatha", "Agnes", "Albertina", "Almeda", "Amelia", "Anastasia", "Annabelle", "Asenath", "Augusta","Barbara", "Bernadette", "Bernice", "Beryl", "Beulah", "Camilla", "Caroline", "Cecilia", "Carmen","Charity", "Christina", "Clarissa", "Cordelia", "Cynthia", "Daisy", "Dolores", "Doris", "Edith",
                             "Edna", "Eloise", "Elouise", "Estelle", "Ethel", "Eudora", "Eugenie", "Eunice", "Florence", "Frieda","Genevieve", "Gertrude", "Gladys", "Gretchen", "Hannah", "Henrietta", "Ingrid", "Irene", "Iris","Ivy", "Jeanette", "Jezebel", "Josephine", "Joyce", "Juanita", "Keziah", "Laverne", "Leonora", "Loretta",
                             "Lucretia", "Mabel", "Madeleine", "Margery", "Marguerite", "Marjorie", "Matilda", "Melinda", "Mercedes","Mildred", "Millicent", "Muriel", "Myrtle", "Naomi", "Nora", "Octavia", "Ophelia", "Pansy", "Patience","Pearle", "Phoebe", "Phyllis", "Rosemary", "Ruby", "Sadie", "Selina", "Selma", "Sibyl", "Sylvia", "Tabitha",
                             "Ursula", "Veronica", "Violet", "Virginia", "Wanda", "Wilhelmina", "Winifred"]
    
        first_name = random.choice(name_list)
        last_name_list = ["Abraham", "Adler", "Ankins", "Avery", "Barnham", "Bentz", "Bessler", "Blakely", "Bleeker", "Bouche","Bretz", "Buchman", "Butts", "Caffey", "Click", "Cordova", "Crabtree", "Crankovitch", "Cuthburt","Cutting", "Dorman", "Eakley", "Eddie", "Fandrick", "Farwell", "Feigel", "Fenske", "Fillman",
                         "Finley", "Firske", "Flanagan", "Franklin", "Freeman", "Frisbe", "Gore", "Greenwald", "Hahn","Hammermeister", "Heminger", "Hogue", "Hollister", "Kasper", "Kisro", "Kleeman", "Lake", "Levard","Lockhart", "Luckstrim", "Lynch", "Mantei", "Marsh", "McBurney", "McCarney", "Moses", "Nickels",
                         "O'Neil", "Olson", "Ozanich", "Patterson", "Patzer", "Peppin", "Porter", "Posch", "Raslo", "Razner","Rifenberg", "Riley", "Ripley", "Rossini", "Schiltgan", "Schmidt", "Schroeder", "Schwartz", "Shane","Shattuck", "Shea", "Slaughter", "Smith", "Speltzer", "Stimac", "Stimac","Strenburg","Strong","Swanson",
                        "Tillinghast","Traver","Urton","Vallier","Wagner","Walsted","Wang","Warner","Webber","Welch","Winters","Yarbrough","Yeske"
       ] 
    
        last_name = random.choice(last_name_list)
    
        if random.random() < 0.5:
            if random.random() < 0.7:
                second_first_name = random.choice(name_list)
                full_name = f"{first_name} {second_first_name} {last_name}"
            else:
                second_first_name = random.choice(name_list)
                second_last_name = random.choice(last_name_list)
                full_name = f"{first_name} {second_first_name} {last_name}-{second_last_name}"
    
        else:
            if random.random() < 0.7:
                full_name = f"{first_name} {last_name}"
            else:
                second_last_name = random.choice(last_name_list)
                full_name = f"{first_name} {last_name}-{second_last_name}"
        
        embed = discord.Embed(
            title="Random name for Call of Cthulhu",
            description=f":game_die: **{full_name}** :game_die:",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)


    @commands.command(aliases=["createNPC"])
    async def cNPC(self, ctx, gender):
        gender = gender.lower()
        if gender not in ["male", "female"]:
            await ctx.send("Invalid gender. Use 'male' or 'female'.")
            return
        
        if gender == "male":
            name_list = [ "Aaron", "Abraham", "Addison", "Amos", "Anderson", "Archibald", "August", "Barnabas", "Barney", "Baxter","Blair", "Caleb", "Cecil", "Chester", "Clifford", "Clinton", "Cornelius", "Curtis", "Dayton", "Delbert","Douglas", "Dudley", "Ernest", "Eldridge", "Elijah", "Emanuel", "Emmet", "Enoch", "Ephraim", "Everett",
                           "Ezekiel", "Forest", "Gilbert", "Granville", "Gustaf", "Hampton", "Harmon", "Henderson", "Herman","Hilliard", "Howard", "Hudson", "Irvin", "Issac", "Jackson", "Jacob", "Jeremiah", "Jonah", "Josiah","Kirk", "Larkin", "Leland", "Leopold", "Lloyd", "Luther", "Manford", "Marcellus", "Martin", "Mason",
                           "Maurice", "Maynard", "Melvin", "Miles", "Milton", "Morgan", "Mortimer", "Moses", "Napoleon", "Nelson","Newton", "Noble", "Oliver", "Orson", "Oswald", "Pablo", "Percival", "Porter", "Quincy", "Randall",
                           "Reginald", "Richmond", "Rodney", "Roscoe", "Rowland", "Rupert", "Sampson", "Sanford", "Sebastian","Shelby", "Sidney", "Solomon", "Squire", "Sterling", "Sidney", "Thaddeus", "Walter", "Wilbur", "Wilfred",
                           "Zadok", "Zebedee"]
        else:
            name_list = [ "Adelaide", "Agatha", "Agnes", "Albertina", "Almeda", "Amelia", "Anastasia", "Annabelle", "Asenath", "Augusta","Barbara", "Bernadette", "Bernice", "Beryl", "Beulah", "Camilla", "Caroline", "Cecilia", "Carmen","Charity", "Christina", "Clarissa", "Cordelia", "Cynthia", "Daisy", "Dolores", "Doris", "Edith",
                             "Edna", "Eloise", "Elouise", "Estelle", "Ethel", "Eudora", "Eugenie", "Eunice", "Florence", "Frieda","Genevieve", "Gertrude", "Gladys", "Gretchen", "Hannah", "Henrietta", "Ingrid", "Irene", "Iris","Ivy", "Jeanette", "Jezebel", "Josephine", "Joyce", "Juanita", "Keziah", "Laverne", "Leonora", "Loretta",
                             "Lucretia", "Mabel", "Madeleine", "Margery", "Marguerite", "Marjorie", "Matilda", "Melinda", "Mercedes","Mildred", "Millicent", "Muriel", "Myrtle", "Naomi", "Nora", "Octavia", "Ophelia", "Pansy", "Patience","Pearle", "Phoebe", "Phyllis", "Rosemary", "Ruby", "Sadie", "Selina", "Selma", "Sibyl", "Sylvia", "Tabitha",
                             "Ursula", "Veronica", "Violet", "Virginia", "Wanda", "Wilhelmina", "Winifred"]
    
        first_name = random.choice(name_list)
        last_name_list = ["Abraham", "Adler", "Ankins", "Avery", "Barnham", "Bentz", "Bessler", "Blakely", "Bleeker", "Bouche","Bretz", "Buchman", "Butts", "Caffey", "Click", "Cordova", "Crabtree", "Crankovitch", "Cuthburt","Cutting", "Dorman", "Eakley", "Eddie", "Fandrick", "Farwell", "Feigel", "Fenske", "Fillman",
                         "Finley", "Firske", "Flanagan", "Franklin", "Freeman", "Frisbe", "Gore", "Greenwald", "Hahn","Hammermeister", "Heminger", "Hogue", "Hollister", "Kasper", "Kisro", "Kleeman", "Lake", "Levard","Lockhart", "Luckstrim", "Lynch", "Mantei", "Marsh", "McBurney", "McCarney", "Moses", "Nickels",
                         "O'Neil", "Olson", "Ozanich", "Patterson", "Patzer", "Peppin", "Porter", "Posch", "Raslo", "Razner","Rifenberg", "Riley", "Ripley", "Rossini", "Schiltgan", "Schmidt", "Schroeder", "Schwartz", "Shane","Shattuck", "Shea", "Slaughter", "Smith", "Speltzer", "Stimac", "Stimac","Strenburg","Strong","Swanson",
                        "Tillinghast","Traver","Urton","Vallier","Wagner","Walsted","Wang","Warner","Webber","Welch","Winters","Yarbrough","Yeske"
       ] 
    
        last_name = random.choice(last_name_list)
    
        if random.random() < 0.5:
            if random.random() < 0.7:
                second_first_name = random.choice(name_list)
                full_name = f"{first_name} {second_first_name} {last_name}"
            else:
                second_first_name = random.choice(name_list)
                second_last_name = random.choice(last_name_list)
                full_name = f"{first_name} {second_first_name} {last_name}-{second_last_name}"
    
        else:
            if random.random() < 0.7:
                full_name = f"{first_name} {last_name}"
            else:
                second_last_name = random.choice(last_name_list)
                full_name = f"{first_name} {last_name}-{second_last_name}"
        
        def get_stat_emoji(stat_name):
            stat_emojis = {
                "STR": ":muscle:",
                "DEX": ":runner:",
                "CON": ":heart:",
                "INT": ":brain:",
                "POW": ":zap:",
                "APP": ":heart_eyes:",
                "EDU": ":mortar_board:",
                "SIZ": ":bust_in_silhouette:",
                "HP": ":heartpulse:",
                "LUCK": ":four_leaf_clover:",
            }
            return stat_emojis.get(stat_name, "")
        
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
            "APP": APP,
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

    @commands.command(aliases=["autochar","generatestats"], guild_only=True)
    async def autoChar(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in self.player_stats:
            await ctx.send(f"{ctx.author.display_name} doesn't have an investigator. Use `!newInv` for creating a new investigator.")
            return
        
        # Check if the player has a character with all stats at 0
        if user_id in self.player_stats and all(self.player_stats[user_id][stat] == 0 for stat in ["STR", "DEX", "CON", "INT", "POW", "APP", "EDU", "SIZ"]):
            # Generate stats
            BUILD = 0
            BONUSDMG = 0
            MOV = 0
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

            #Bonus DMG and Build
            STRSIZ = STR + SIZ
            if 2 <= STRSIZ <= 64:
                BONUSDMG = -2
                BUILD = -2
            elif 65 <= STRSIZ <= 84:
                BONUSDMG = -1
                BUILD = -1
            elif 85 <= STRSIZ <= 124:
                BONUSDMG = 0
                BUILD = 0
            elif 125 <= STRSIZ <= 164:
                BONUSDMG = "1D4"
                BUILD = 1
            elif 165 <= STRSIZ <= 204:
                BONUSDMG = "1D6"
                BUILD = 2
            elif 205 <= STRSIZ <= 284:
                BONUSDMG = "2D6"
                BUILD = 3
            elif 285 <= STRSIZ <= 364:
                BONUSDMG = "3D6"
                BUILD = 4
            elif 365 <= STRSIZ <= 444:
                BONUSDMG = "4D6"
                BUILD = 5
            elif 445 <= STRSIZ <= 524:
                BONUSDMG = "5D6"
                BUILD = 6
            else:
                # if fuking broken
                BONUSDMG = 0
                BUILD = 0
            #calculatin MOV
            if DEX < SIZ and STR < SIZ:
                MOV = 7
            elif DEX < SIZ or STR < SIZ or (DEX == STR == SIZ):
                MOV = 8
            elif DEX > SIZ and STR > SIZ:
                MOV = 9

            stats_embed = discord.Embed(
                title=":detective: Investigator Creation Assistant",
                description="New stats have been generated for your character.",
                color=discord.Color.green()
            )
            stats_embed.add_field(name="STR", value=f":muscle: 3D6 x 5 :game_die: {STR}", inline=True)
            stats_embed.add_field(name="DEX", value=f":runner: 3D6 x 5 :game_die: {DEX}", inline=True)
            stats_embed.add_field(name="CON", value=f":heart: 3D6 x 5 :game_die: {CON}", inline=True)
            stats_embed.add_field(name="INT", value=f":brain: 3D6 x 5 :game_die: {INT}", inline=True)
            stats_embed.add_field(name="POW", value=f":zap: 3D6 x 5 :game_die: {POW}", inline=True)
            stats_embed.add_field(name="APP", value=f":heart_eyes: 3D6 x 5 :game_die: {APP}", inline=True)
            stats_embed.add_field(name="EDU", value=f":mortar_board: 2D6 x 5 + 5 :game_die: {EDU}", inline=True)
            stats_embed.add_field(name="SIZ", value=f":bust_in_silhouette: 2D6 x 5 + 5 :game_die: {SIZ}", inline=True)
            stats_embed.add_field(name="HP", value=f":heartpulse: (CON + SIZ) / 5 :game_die: {HP}", inline=True)
            stats_embed.add_field(name="SAN", value=f":scales: POW :game_die: {SAN}", inline=True)
            stats_embed.add_field(name="MP", value=f":sparkles: POW / 5 :game_die: {MP}", inline=True)
            stats_embed.add_field(name="LUCK", value=f":four_leaf_clover: 3D6 x 5 :game_die: {LUCK}", inline=True)
            stats_embed.add_field(name="MOV", value=f":person_running: Based of DEX, STR & SIZ :game_die: {MOV}", inline=True)
            stats_embed.add_field(name="Damage Bonus", value=f":boxing_glove: Based of STR & SIZ :game_die: {BONUSDMG}", inline=True)
            stats_embed.add_field(name="Build", value=f":restroom: Based of STR & SIZ :game_die: {BUILD}", inline=True)
            

            message = await ctx.send(embed=stats_embed)
            await message.add_reaction("✅")  # Add checkmark emoji
            await message.add_reaction("❌")  # Add X emoji
            await message.add_reaction("🔁")  # Add loop emoji

            def check(reaction, user):
                return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ["✅", "❌", "🔁"]

            try:
                reaction, _ = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                if str(reaction.emoji) == "✅":
                    self.player_stats[user_id]["STR"] = STR
                    self.player_stats[user_id]["DEX"] = DEX
                    self.player_stats[user_id]["CON"] = CON
                    self.player_stats[user_id]["INT"] = INT
                    self.player_stats[user_id]["POW"] = POW
                    self.player_stats[user_id]["APP"] = APP
                    self.player_stats[user_id]["EDU"] = EDU
                    self.player_stats[user_id]["SIZ"] = SIZ
                    self.player_stats[user_id]["HP"] = HP
                    self.player_stats[user_id]["MAX_HP"] = HP
                    self.player_stats[user_id]["SAN"] = SAN
                    self.player_stats[user_id]["MP"] = MP
                    self.player_stats[user_id]["MAX_MP"] = MP
                    self.player_stats[user_id]["LUCK"] = LUCK
                    self.player_stats[user_id]["Dodge"] = math.floor(DEX/5)
                    self.player_stats[user_id]["Language (own)"] = EDU
                    self.player_stats[user_id]["Build"] = BUILD
                    self.player_stats[user_id]["Damage Bonus"] = BONUSDMG
                    self.player_stats[user_id]["Move"] = MOV

                    await self.save_data(ctx.guild.id, self.player_stats)  # Save the updated stats
                    await ctx.send("Your character's stats have been saved! You should set your Age with `!cstat Age` now.")
                elif str(reaction.emoji) == "❌":
                    await ctx.send("Character creation canceled. Stats have not been saved.")
                elif str(reaction.emoji) == "🔁":
                    await ctx.invoke(self.bot.get_command("autoChar"))  # Reinvoke the command to generate new stats
            except asyncio.TimeoutError:
                await ctx.send("You took too long to react. Automatic character stats creation canceled.")
        else:
            await ctx.send("You already have some stats assigned to your investigator.")



    @commands.command(aliases=["sinfo"])
    async def skillinfo(self, ctx, *, skill_name: str = None):
        # Zde můžete definovat informace o dovednostech (malá písmena)
        skills_info = {
            "Accounting": ":chart_with_upwards_trend:  Base stat - 05% \n :ledger: Accounting skill grants the ability to understand financial operations, detecting discrepancies and fraud in financial records, and evaluating the financial health of businesses or individuals. It involves inspecting account books to uncover misappropriations, bribes, or discrepancies in claimed financial conditions. Difficulty varies based on how well accounts are concealed. Pushing examples involve spending more time reviewing documents or double-checking findings. Failing a Pushed roll could lead to revealing the investigators' intentions or damaging the accounts, with insane investigators possibly eating them.",
            "Animal Handling": ":chart_with_upwards_trend:  Base stat - 05% \n :lion_face: Animal Handling allows one to command and train domesticated animals like dogs to perform tasks. It's also applicable to other animals like birds, cats, and monkeys. This skill isn't used for riding animals (use the Ride skill instead). Difficulty varies based on the animal's training and familiarity. Pushing examples involve greater personal risk while handling animals. Failing a Pushed roll might result in the animal attacking or escaping. Insane investigators might mimic the behavior of the animal they were trying to control.",
            "Anthropology":":chart_with_upwards_trend:  Base stat - 01% \n :earth_americas: Anthropology enables understanding of other cultures through observation. Spending time within a culture allows basic predictions about its ways and morals. Extensive study helps comprehend cultural functioning, allowing predictions of actions and beliefs. Difficulty depends on exposure to the subject culture. Pushing examples involve deeper study or immersion. Failing a Pushed roll might lead to attack or imprisonment by the studied culture or side effects from participating in ceremonies.",
            "Appraise":":chart_with_upwards_trend:  Base stat - 01% \n :mag: Appraise skill estimates item values, including quality, materials, and historical significance. It helps determine age, relevance, and detect forgeries. Difficulty varies based on the rarity and complexity of the item. Pushing examples involve validation from experts or testing. Failing a Pushed roll could damage the item, draw attention to it, or trigger its function. Insane investigators might destroy the item, believing it's cursed or refuse to give it up.",
            "Archaeology":":chart_with_upwards_trend:  Base stat - 01% \n :pick: Archaeology enables dating and identifying artifacts, detecting fakes, and expertise in setting up excavation sites. Users can deduce the purposes and lifestyles of past cultures from remains. It assists in identifying extinct human languages. Difficulty varies based on time and resources. Pushing examples involve further study or research. Failing a Pushed roll could spoil a site, result in seizure of finds, or attract unwanted attention. If an insane investigator fails, they might keep digging deeper.",
            "Art and Craft":":chart_with_upwards_trend:  Base stat - 05% \n :art: Art and Craft skills involve creating or repairing items, possibly with specializations like acting, painting, forgery, and more. Skills can be used to make quality items, duplicate items, or create fakes. Different difficulty levels correspond to crafting different qualities of items. Pushing examples include reworking items or conducting additional research. Failing a Pushed roll might waste time and resources or offend customers. Insane investigators might create unusual works that provoke strong reactions.",
            "Artillery":":chart_with_upwards_trend:  Base stat - 01% \n :crossed_swords: Artillery is the operation of field weapons in warfare. The user is experienced in operating large weapons requiring crews. Specializations exist based on the period, including cannon and rocket launcher. Difficulty varies with maintenance and conditions. This combat skill cannot be pushed.",
            "Charm":":chart_with_upwards_trend:  Base stat - 15% \n :heart_decoration: Charm involves physical attraction, seduction, flattery, or a warm personality to influence someone. It can be used for persuasion, bargaining, and haggling. Opposed by Charm or Psychology skills. Difficulty levels depend on the context. Pushing examples involve extravagant flattery, offering gifts, or building trust. Failure might lead to offense, exposure, or interference by third parties. If an insane investigator fails a pushed roll, they might fall in love with the target.",
            "Climb":":chart_with_upwards_trend:  Base stat - 20% \n :mountain: Climb skill allows a character to ascend vertical surfaces using ropes, climbing gear, or bare hands. Conditions like surface firmness, handholds, weather, and visibility affect the difficulty. Failing on the first roll might indicate the climb's impossibility. A pushed roll failure likely results in a fall with damage. A successful Climb roll usually completes the climb in one attempt. Increased difficulty applies for challenging or longer climbs. Pushing examples include reassessing the climb or finding alternate routes. Consequences of failing a Pushed roll could be falling and suffering damage, losing possessions, or becoming stranded. If an insane investigator fails a pushed roll, they might hold on for dear life and scream.",
            "Computer Use":":chart_with_upwards_trend:  Base stat - 05% \n :computer: This skill is for programming in computer languages, analyzing data, breaking into secure systems, exploring networks, and detecting intrusions, back doors, and viruses. The Internet provides vast information, often requiring combined rolls with Library Use. It's not necessary for regular computer use. Difficulty varies for tasks like programming and hacking into networks. Pushing examples include using shortcuts or untested software. Consequences of failing a Pushed roll might include erasing files, leaving evidence, or infecting the system with a virus. If an insane investigator fails a pushed roll, they might become absorbed in the virtual world.",
            "Credit Rating":":chart_with_upwards_trend:  Base stat - 00% \n :moneybag: Credit Rating represents the investigator's financial status and confidence. It's not a skill per se, but a measure of wealth and prosperity. A high Credit Rating can aid in achieving goals using financial status. It can also substitute for APP for first impressions. Credit Rating varies for different occupations and can change over time. A high Credit Rating can open doors and provide resources. It's not meticulously tracked in gameplay but helps gauge the investigator's financial reach. Failing a Pushed roll might lead to negative consequences, such as involvement with loan sharks or loss of possessions. If an insane investigator fails a pushed roll, they might become overly generous with their money.",
            "Cthulhu Mythos":":chart_with_upwards_trend:  Base stat - 00% \n :octopus: This skill reflects understanding of the Cthulhu Mythos, the Lovecraftian cosmic horrors. Points in this skill are gained through encounters, insanity, insights, and reading forbidden texts. An investigator's Sanity can't exceed 99 minus their Cthulhu Mythos skill. Successful rolls allow identification of Mythos entities, knowledge about them, remembering facts, identifying spells, and manifesting magical effects. The skill starts at zero and is often low. Regular difficulty rolls are common, while hard difficulty might involve identifying entities from rumors or finding vulnerabilities through research. Failing a Pushed roll can lead to dangerous consequences, like exposing oneself to harm or activating spells inadvertently. If an insane investigator fails a pushed roll, they might experience a vision or revelation about the Cthulhu Mythos.",
            "Demolitions":":chart_with_upwards_trend:  Base stat - 01% \n :exploding_head: This skill involves safely setting and defusing explosive charges, including mines and military-grade demolitions. Skilled individuals can rig charges for demolition, clearing tunnels, and constructing explosive devices. Regular difficulty might involve defusing explosive devices or knowing where to place charges for maximum effect, while hard difficulty could involve defusing a device under time pressure. Failing a pushed roll when defusing could result in an explosion, while improper detonation might result from placing charges. If an insane investigator fails a pushed roll, they might come up with eccentric ways to deliver explosives.",
            "Disguise":":chart_with_upwards_trend:  Base stat - 05% \n :dress: This skill is used when the investigator wants to appear as someone else. It involves changing posture, costume, voice, and possibly makeup or fake ID. Regular difficulty involves convincing strangers of the disguise's authenticity, while hard difficulty requires convincing professionals in face-to-face meetings. Pushing examples could include thorough preparation, stealing personal items, or feigning illness to distract observers. Consequences of failing a pushed roll might involve arrest, offense, or unintended consequences due to the disguise. If an insane investigator fails a pushed roll, they might struggle to recognize their own face even without the disguise.",
            "Diving":":chart_with_upwards_trend:  Base stat - 01% \n :diving_mask: This skill covers the use of diving equipment for underwater swimming, including navigation, weighting, and emergency procedures. It includes both historical diving suits and modern scuba diving. Regular difficulty applies to routine dives with proper equipment, while hard difficulty might involve dangerous conditions or poorly maintained gear. Pushing examples could be pushing equipment limits or seeking professional assistance. Consequences of failing a pushed roll might involve becoming trapped underwater or suffering decompression sickness. If an insane investigator fails a pushed roll, they might believe they can understand whale-song.",
            "Dodge":":chart_with_upwards_trend:  Base stat - half DEX% \n :warning: Dodge allows an investigator to instinctively evade blows, projectiles, and attacks. It's mostly used in combat as part of opposed rolls. There's no set difficulty level for Dodge, and it cannot be pushed. The skill is related to an investigator's Dexterity stat and can increase through experience.",
            "Drive Auto":":chart_with_upwards_trend:  Base stat - 20% \n :blue_car: This skill allows the investigator to drive a car or light truck, make ordinary maneuvers, and handle common vehicle issues. It's used for driving in various situations, including escaping pursuers or tailing someone. Regular difficulty might involve weaving through light traffic, while hard difficulty could involve weaving through heavy traffic. Pushing examples might involve driving to the vehicle's limit. Consequences of failing a Pushed roll might involve crashing, being pursued by the police, or other complications. If an insane investigator fails a pushed roll, they might act as if they're driving a stationary vehicle and making engine noises.",
            "Electrical Repair":":chart_with_upwards_trend:  Base stat - 10% \n :wrench: This skill allows the investigator to repair or reconfigure electrical equipment like auto ignitions, electric motors, and burglar alarms. It's separate from Electronics and involves physical repairs rather than dealing with microchips or circuit boards. Regular difficulty tasks include repairing or creating standard electrical devices, while hard difficulty tasks involve more significant repairs or working without proper tools. Pushing examples might involve taking longer to repair or researching new methods. Consequences of failing a Pushed roll could lead to electric shock or damaging the equipment further. If an insane investigator fails a pushed roll, they might attempt to harness the power of living organisms into devices.",
            "Electronics":":chart_with_upwards_trend:  Base stat - 01% \n :electric_plug:  Electronics skill is for troubleshooting, repairing, and creating electronic devices. It's different from Electrical Repair, as it involves microchips, circuit boards, and modern technology. Regular difficulty tasks might involve minor repairs, while hard difficulty tasks might involve jury-rigging devices with scavenged parts. The availability of correct parts and instructions is essential. Successful skill use can lead to repairs, constructions, or modifications of electronic devices. If an investigator has the right parts and instructions, constructing a standard computer might not require a skill roll. Consequences of failing a Pushed roll might involve damaging circuitry or creating unintended outcomes. If an insane investigator fails a pushed roll, they might become paranoid about electronic surveillance.",
            "Fast Talk":":chart_with_upwards_trend:  Base stat - 05% \n :pinched_fingers: Fast Talk involves verbal trickery, deception, and misdirection to achieve short-term effects. It can be used to deceive, haggle, or manipulate people into temporary actions. The effect is usually temporary, and the target might realize the trick after a while. Regular and hard difficulty levels are similar to other social skills. Pushing examples could involve talking outlandishly or getting close to the target. Fast Talk can't be changed to other skills mid-discussion. Failing a pushed roll might lead to offense or violence. If an insane investigator fails a pushed roll, they might start hurling abusive phrases.",
            "Fighting":":chart_with_upwards_trend:  Base stat - 0X% \n :boxing_glove: Fighting skills cover melee combat and come in different specializations based on the type of weapon or fighting style. There's no generic Fighting skill; instead, characters choose specialized skills like Axe, Brawl, Chainsaw, Flail, Garrote, Spear, Sword, and Whip. These skills determine proficiency in various weapons and combat styles. They can't be pushed and involve opposed rolls in combat.",
            "Firearms":":chart_with_upwards_trend:  Base stat - 0X% \n :gun: Firearms skill covers various types of firearms, bows, and crossbows. Characters choose specialized skills like Bow, Handgun, Heavy Weapons, Flamethrower, Machine Gun, Rifle/Shotgun, and Submachine Gun. These skills determine proficiency in using different firearms and ranged weapons. They can't be pushed and involve opposed rolls in combat.",
            "First Aid":":chart_with_upwards_trend:  Base stat - 30% \n :ambulance: First Aid skill enables an investigator to provide emergency medical care, like splinting broken limbs, stopping bleeding, treating burns, and more. Successful First Aid treatment must be delivered within an hour, granting 1 hit point. Two people can work together for First Aid, with either one rolling successfully for a joint success. Successful use of First Aid can rouse an unconscious person to consciousness. First Aid can stabilize a dying character for an hour, granting 1 temporary hit point, and can be repeated until stabilization or death. Successful First Aid can save the life of a dying character, but further treatment with the Medicine skill or hospitalization is required afterward.",
            "History":":chart_with_upwards_trend:  Base stat - 05% \n :scroll: History skill allows an investigator to remember the significance of places, people, and events. Regular difficulty tasks involve recalling pertinent information, while hard difficulty tasks involve knowing obscure details. Pushing examples might involve taking more time for research or consulting experts. Consequences of failing a Pushed roll could include wasting time and resources or providing erroneous information. If an insane investigator fails a pushed roll, they might believe they're displaced in time or start acting and speaking in an archaic manner.",
            "Hypnosis":":chart_with_upwards_trend:  Base stat - 01% \n :face_with_spiral_eyes: Hypnosis skill allows the user to induce a trancelike state in a target, increasing suggestibility and relaxation. It can be used as hypnotherapy to reduce the effects of phobias or manias, with a series of successful sessions potentially curing the patient. Hypnosis can be opposed by Psychology or POW for unwilling subjects. Pushing examples might involve using lights, props, or drugs to enhance the effect. Consequences of failing a Pushed roll could include triggering forgotten memories or traumas or even leading the target to dangerous situations. If an insane investigator fails a pushed roll, they might regress to a childlike state until treated.",
            "Intimidate":":chart_with_upwards_trend:  Base stat - 05% \n :fearful: Intimidation involves using physical force, psychological manipulation, or threats to frighten or compel someone. It's opposed by Intimidate or Psychology. Successful intimidation can be used to achieve specific outcomes, like lowering prices or gaining compliance. Backing up threats with weapons or incentives can reduce the difficulty level. Pushing an Intimidation roll might lead to unintended consequences, such as carrying out threats beyond the intended level. Failure consequences could involve accidental harm, a target's unexpected resistance, or backlash from the target.",
            "Jump":":chart_with_upwards_trend:  Base stat - 20% \n :athletic_shoe: Jumping skill allows investigators to perform various types of jumps, both vertically and horizontally. Regular, hard, and extreme difficulties determine the distances and heights that can be successfully jumped. Jump can also be used to mitigate fall damage when falling from heights. Regular success might involve safely jumping down your own height, while extreme success could mean leaping twice your height. Falling damage can be reduced with a successful Jump roll.",
            "Language (Other)":":chart_with_upwards_trend:  Base stat - 01% \n :globe_with_meridians: This skill represents a character's ability to understand, speak, read, and write in a language other than their own. The exact language must be specified when choosing this skill. Different levels of skill allow for different degrees of proficiency, from basic communication to fluency and even passing as a native speaker. Success at the skill can encompass understanding an entire book or having a conversation. Different levels of success in Other Languages skill are also described.",
            "Language (Own)":":chart_with_upwards_trend:  Base stat - EUD% \n :speech_balloon: This skill represents an investigator's proficiency in their own language. The skill percentage starts at the investigator's EDU characteristic, and they understand, speak, read, and write in their own language at that percentage or higher. No skill roll is normally required to use one's own language, even when dealing with technical or uncommon terms. However, if a document is particularly difficult to read or in an archaic dialect, the Keeper may require a roll.",
            "Law":":chart_with_upwards_trend:  Base stat - 05% \n :scales: The Law skill represents a character's knowledge of relevant laws, precedents, legal maneuvers, and court procedures. It's used to understand and utilize legal details. This skill is important for legal professions and political office. The difficulty level may increase when using Law in a foreign country. The skill can be used for cross-examining witnesses and understanding legal situations.",
            "Library Use":":chart_with_upwards_trend:  Base stat - 20% \n :books: Library Use allows investigators to locate specific information, such as books, newspapers, or references, in libraries or collections. The skill can be used to find locked cases or rare-book collections, though access might require other skills like Persuade or Credit Rating. Regular difficulty involves locating information, while hard difficulty applies when searching in a disorganized library or under time pressure.",
            "Listen":":chart_with_upwards_trend:  Base stat - 20% \n :ear: Listen skill measures an investigator's ability to interpret and understand sounds, including conversations and distant noises. High Listen skill indicates heightened awareness. The skill can be used to detect approaching sounds or eavesdrop on conversations. Listen can be opposed by the Stealth skill when someone is trying to remain hidden.",
            "Locksmith":":chart_with_upwards_trend:  Base stat - 01% \n :key: Locksmith skill allows an investigator to open locks, repair them, create keys, and utilize lock-picking tools. Regular difficulty involves opening or repairing standard locks, while hard difficulty applies to high-security locks. Pushing a roll might involve taking longer, dismantling the lock, or using force to open it.",
            "Lore":":chart_with_upwards_trend:  Base stat - 01% \n :scroll: The Lore skill represents expert understanding of a specialized subject that falls outside the normal bounds of human knowledge. Specializations can include areas like Dream Lore, Necronomicon Lore, UFO Lore, and more. This skill is used to test an investigator's knowledge of specific topics that are central to the campaign or to convey the knowledge of non-player characters to the Keeper.",
            "Mechanical Repair":":chart_with_upwards_trend:  Base stat - 10% \n :wrench: This skill allows investigators to repair machines, perform basic carpentry and plumbing, and construct or repair items. It's a companion skill to Electrical Repair and is used for fixing devices and creating new ones. Basic carpentry and plumbing projects are also within the scope of this skill. Mechanical Repair can open basic locks, but for more complex locks, refer to the Locksmith skill.",
            "Medicine":":chart_with_upwards_trend:  Base stat - 01% \n :pill: The Medicine skill involves diagnosing and treating accidents, injuries, diseases, poisonings, etc. It allows the user to provide medical care and make public health recommendations. Successful use of the Medicine skill can recover hit points, and the skill is useful for treating major wounds. A successful roll with Medicine provides a bonus die on a weekly recovery roll. The skill takes a minimum of one hour to use for treatment.",
            "Natural World":":chart_with_upwards_trend:  Base stat - 10% \n :deciduous_tree: Natural World represents an investigator's traditional and general knowledge of plants and animals in their environment. It's used to identify species, habits, and habitats in a more folkloric and enthusiastic manner. This skill is not as scientifically accurate as disciplines like Biology or Botany. Natural World can be used to judge the quality of animals, plants, or collections.",
            "Navigate":":chart_with_upwards_trend:  Base stat - 10% \n :compass: Navigate skill enables an investigator to find their way in various weather conditions, day or night. The skill involves using landmarks, astronomical tables, charts, instruments, and modern technology for mapping and location. It can be used to measure and map an area. Familiarity with the area grants a bonus die. This skill can also be used as concealed rolls by the Keeper.",
            "Occult":":chart_with_upwards_trend:  Base stat - 05% \n :crystal_ball: The Occult skill involves recognizing occult paraphernalia, words, concepts, and folk traditions. It's used to identify magical grimoires, occult codes, and general knowledge of secret traditions. The skill doesn't apply to Cthulhu Mythos magic. Successful use of Occult can be used for bargaining and haggling as well.",
            "Operate Heavy Machinery":":chart_with_upwards_trend:  Base stat - 01% \n :bullettrain_front: This skill is required to operate large-scale construction machinery, such as tanks, backhoes, and steam shovels. It's also used for complex machinery, like ship engines. Operating heavy machinery successfully involves making skill rolls, especially in challenging conditions. Failure can result in damage or accidents.",
            "Persuade":":chart_with_upwards_trend:  Base stat - 10% \n :speech_balloon: Persuade is used to convince others about specific ideas or concepts through reasoned argument and discussion. It's a skill that takes time and can be used for bargaining and haggling. Successful persuasion can have lasting effects on the target's beliefs. This skill can be used to haggle prices down.",
            "Pilot":":chart_with_upwards_trend:  Base stat - 01% \n :airplane: The Pilot skill is specialized for flying or operating specific types of vehicles, such as aircraft or boats. Each specialization starts at 01%. The success of pilot rolls depends on the situation and conditions, with bad weather or damage raising the difficulty level.",
            "Psychoanalysis":":chart_with_upwards_trend:  Base stat - 01% \n :brain: Psychoanalysis involves emotional therapies and can return Sanity points to investigator patients. It can be used to cope with phobias or see through delusions for a brief period. Psychoanalysis cannot increase a character's Sanity points above 99 (Cthulhu Mythos). Successful therapy can help during indefinite insanity.",
            "Psychology":":chart_with_upwards_trend:  Base stat - 10% \n :brain: Psychology allows the user to study an individual and form ideas about their motives and character. It can be used to oppose social interaction rolls and see through disguises. The skill roll's difficulty level depends on the target's relevant social interaction skill. It's a skill that can be used to understand and predict behavior.",
            "Read Lips":":chart_with_upwards_trend:  Base stat - 01% \n :lips: This skill allows the investigator to understand spoken communication by observing lip movements. It can be used to eavesdrop on conversations or silently communicate with another proficient individual. The skill's effectiveness depends on the situation, visibility, and distance.",
            "Ride":":chart_with_upwards_trend:  Base stat - 05% \n :horse_racing: The Ride skill is used to handle and ride animals like saddle horses, donkeys, or mules. It involves knowledge of animal care, riding gear, and riding techniques. Falling from a mount due to an accident or failed skill roll can result in hit point loss. The success of a ride roll depends on the speed and terrain. Riding side-saddle or on unfamiliar mounts increases the difficulty.",
            "Science Specializations":":chart_with_upwards_trend:  Base stat - X% \n :microscope: Science is a broad skill category that represents knowledge and expertise in various scientific disciplines. Each specialization focuses on a particular field of science and grants the character practical and theoretical abilities within that field. Characters can spend skill points to purchase specialization in a specific field. The generic Science skill cannot be directly purchased and instead, characters must choose from the available specializations. Many specialties overlap, and knowledge in one field may contribute to understanding another related field. \n Astronomy (01%): This specialization involves understanding celestial bodies, their positions, and movements. The character can identify stars, planets, and predict celestial events like eclipses. More advanced knowledge might include concepts of galaxies and extraterrestrial life. \n Biology (01%): The study of life and living organisms. This specialization covers various sub-disciplines such as cytology, genetics, microbiology, and more. Characters with this specialization can analyze organisms, study their functions, and even develop vaccines or treatments for diseases. \n Botany (01%): Botany focuses on plant life. The character can identify plant species, understand their growth patterns, reproductive mechanisms, and chemical properties. This specialization is useful for recognizing plants, their uses, and potential dangers. \n Chemistry (01%): The study of substances, their composition, properties, and interactions. Characters with this specialization can create chemical compounds, analyze unknown substances, and understand chemical reactions. This includes making simple explosives, poisons, and acids. \n Cryptography (01%): This specialization involves the study of secret codes and languages. Characters can create, decipher, and analyze codes used to conceal information. This skill is crucial for cracking complex codes and understanding hidden messages. \n Engineering (01%): While technically not a science, engineering involves practical applications of scientific principles. Characters with this specialization can design and build structures, machines, and materials for various purposes. \n Forensics (01%): Forensics focuses on analyzing evidence, often related to crime scenes. This specialization includes the examination of fingerprints, DNA, hair, and body fluids. Characters can identify and interpret evidence for legal disputes. \n Geology (01%): Geology encompasses the study of Earth's structure, rocks, minerals, and geological processes. Characters with this specialization can evaluate soil, recognize fossils, and anticipate geological events like earthquakes and volcanic eruptions. \n Mathematics (10%): Mathematics involves the study of numbers, logic, and mathematical theories. Characters with this specialization can solve complex mathematical problems, identify patterns, and decrypt intricate codes. \n Meteorology (01%): This specialization covers the scientific study of the atmosphere and weather patterns. Characters can predict weather changes, forecast rain, snow, and fog, and understand atmospheric phenomena. \n Pharmacy (01%): Pharmacy focuses on chemical compounds and their effects on living organisms. Characters with this specialization can formulate medications, identify toxins, and understand pharmaceutical properties and side effects. \n Physics (01%): Physics involves the study of physical phenomena such as motion, magnetism, electricity, and optics. Characters with this specialization have theoretical understanding and can create experimental devices to test ideas. \n Zoology (01%): Zoology centers on the study of animals, their behaviors, structures, and classifications. Characters with this specialization can identify animal species, understand behaviors, and analyze tracks and markings.",
            "Sleight of Hand":":chart_with_upwards_trend:  Base stat - 10% \n :mage: This skill enables the user to conceal and manipulate objects using various techniques like palming, pick-pocketing, and creating illusions. It includes hiding items with debris or fabric and performing clandestine actions such as pick-pocketing or hiding objects on a person.",
            "Spot Hidden":":chart_with_upwards_trend:  Base stat - 25% \n :eyes: Spot Hidden allows the character to notice hidden clues, secret doors, or concealed objects. The skill is essential for detecting subtle details, even in challenging environments. It can also be used to spot hidden intruders or recognize hidden dangers.",
            "Stealth":":chart_with_upwards_trend:  Base stat - 20% \n :footprints: Stealth involves moving silently and hiding effectively to avoid detection. This skill is crucial for remaining unnoticed by others, whether it's sneaking past guards or hiding from pursuers. Characters can use Stealth to move quietly and maintain a low profile.",
            "Survival":":chart_with_upwards_trend:  Base stat - 10% \n :camping: Survival is specialized for different environments such as desert, sea, or arctic conditions. It provides the knowledge needed to survive in extreme situations, including finding shelter, food, and water. Characters can adapt to their chosen environment and overcome challenges specific to it.",
            "Swim":":chart_with_upwards_trend:  Base stat - 20% \n :swimmer: Swim skill represents the ability to navigate through water and other liquids. It's useful in situations where characters need to cross bodies of water, avoid drowning, or swim against currents. Successful Swim rolls can prevent drowning and navigate dangerous waters.",
            "Throw":":chart_with_upwards_trend:  Base stat - 20% \n :dart: The Throw skill involves accurately hitting a target with a thrown object. Characters can use this skill to throw weapons like knives or spears and hit specific targets. The distance and accuracy of the throw depend on the skill level and the weight of the object.",
            "Track":":chart_with_upwards_trend:  Base stat - 10% \n :mag_right: Track allows characters to follow trails left by people, animals, or vehicles. This skill is useful for pursuing individuals or uncovering hidden paths. The difficulty of tracking depends on factors such as time passed and the condition of the terrain.",
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

    @commands.command(aliases=["cocc","oinfo"])
    async def coccupations(self, ctx, *, occupation_name: str = None):
        occupations_info = {
            "Accountant": {
                "description": "Either employed within a business or working as a freelance consultant with a portfolio of self-employed clients or businesses. Diligence and an attention to detail means that most accountants can make good researchers, being able to support investigations through the careful analysis of personal and business transactions, financial statements, and other records.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "30–70",
                "suggested_contacts": "Business associates, legal professions, financial sector (bankers, other accountants).",
                "skills": "Accounting, Law, Library Use, Listen, Persuade, Spot Hidden, any two other skills as personal or era specialties (e.g. Computer Use)."
            },
            "Acrobat": {
                "description": "Acrobats may be either amateur athletes competing in staged meets—possibly even the Olympics—or professionals employed within the entertainment sector (e.g. circuses, carnivals, theatrical performances).",
                "era":"Any",
                "skill_points": "EDU × 2 + DEX × 2",
                "credit_rating": "9–20",
                "suggested_contacts": "Amateur athletic circles, sports writers, circuses, carnivals.",
                "skills": "Climb, Dodge, Jump, Throw, Spot Hidden, Swim, any two other skills as personal or era specialties."
            },
            "Stage Actor": {
                "description": "Usually a stage or film actor. Many stage actors have a background in the classics and, considering themselves 'legitimate,' have a tendency to look down upon the commercial efforts of the film industry. By the late twentieth century, this is diminished, with film actors able to command greater respect and higher fees. Movie stars and the film industry have long captured the interest of people across the world. Many stars are made overnight and most of them lead flashy, high-profile lives, always in the media spotlight. In the 1920s, the theatrical center of the U.S. is in New York City, although there are major stages in most cities across the country. A similar situation exists in England, with touring repertory companies traveling the counties, and London is the heart of theatrical shows. Touring companies travel by train, presenting new plays, as well as classics by Shakespeare and others. Some companies spend considerable amounts of time touring foreign parts, such as Canada, Hawaii, Australia, and Europe. With the introduction of 'talkies' in the latter part of the 1920s, many stars of the silent film era cannot cope with the transition to sound. The arm-waving histrionics of silent actors give way to more subtle characterizations. John Garfield and Francis Bushman are forgotten for new stars, such as Gary Cooper and Joan Crawford.",
                "era":"Any",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "9–40",
                "suggested_contacts": "Theatre industry, newspaper arts critics, actor’s guild or union.",
                "skills": "Art/Craft (Acting), Disguise, Fighting, History, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any one other skill as a personal or era specialty."
            },
            "Film star": {
                "description": "Film stars are usually actors who have gained fame and recognition in the film industry. Many stars are made overnight and most of them lead flashy, high-profile lives, always in the media spotlight...",
                "era":"Any",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "20–90",
                "suggested_contacts": "Film industry, media critics, writers.",
                "skills": "Art/Craft (Acting), Disguise, Drive Auto, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any two other skills as personal or era specialties (e.g. Ride or Fighting)."
            },
           "Agency detective": {
                "description": "Numerous well-known detective agencies exist around the world, with probably the most famous being the Pinkerton and Burns agencies (merged into one in modern times). Large agencies employ two types of agents: security guards and operatives. Guards are uniformed patrolmen, hired by companies and individuals to protect property and people against burglars, assassins, and kidnappers. Use the Uniformed Police Officer’s (page 87) description for these characters. Company Operatives are plainclothes detectives, sent out on cases requiring them to solve mysteries, prevent murders, locate missing people, and so on.",
                "era":"Any",
                "skill_points": "EDU × 2 + (STR × 2 or DEX × 2)",
                "credit_rating": "20–45",
                "suggested_contacts": "Local law enforcement, clients.",
                "skills": "One interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Fighting (Brawl), Firearms, Law, Library Use, Psychology, Stealth, Track."
            },
            "Alienist": {
                "description": "In the 1920s, 'alienist' is the term given for those who treat mental illness (early psychiatrists). Psychoanalysis is barely known in the U.S., and its basis in sexual life and toilet training is felt to be indecent. Psychiatry, a standard medical education augmented by behaviorism, is more common. Intellectual wars rage between alienists, psychiatrists, and neurologists.",
                "era":"Classic - 1920s period",
                "skill_points": "EDU × 4",
                "credit_rating": "10–60",
                "suggested_contacts": "Others in the field of mental illness, medical doctors, and occasionally detectives in law enforcement.",
                "skills": "Law, Listen, Medicine, Other Language, Psychoanalysis, Psychology, Science (Biology), (Chemistry)."
            },
            "Animal trainer": {
                "description": "May be employed by film studios, a traveling circus, a horse stable, or possibly working freelance. Whether training guide dogs for the blind or teaching a lion to jump through a flaming hoop, the animal trainer usually works alone, spending long hours in close proximity with the animals in their care.",
                "era":"Any",
                "skill_points": "EDU × 2 + (APP × 2 or POW × 2)",
                "credit_rating": "10–40",
                "suggested_contacts": "Zoos, circus folk, patrons, actors.",
                "skills": "Animal Handling, Jump, Listen, Natural World, Science (Zoology), Stealth, Track, any one other skill as a personal or era specialty."
            },
            "Antiquarian": {
                "description": "A person who delights in the timeless excellence of design and execution, and in the power of ancient lore. Probably the most Lovecraft-like occupation available to an investigator. An independent income allows the antiquarian to explore things old and obscure, perhaps sharpening their focus down particular lines of enquiry based on personal preference and interest. Usually a person with an appreciative eye and a swift mind, who frequently finds mordant or contemptuous humor in the foolishness of the ignorant, the pompous, and the greedy.",
                "era":"Lovecraftian - Important in Lovecraft’s stories.",
                "skill_points": "EDU × 4",
                "credit_rating": "30–70",
                "suggested_contacts": "Booksellers, antique collectors, historical societies.",
                "skills": "Appraise, Art/Craft (any), History, Library Use, Other Language, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Spot Hidden, any one other skill as a personal or era specialty."
            },
            "Antique dealer": {
                "description": "Antique dealers usually own their own shop, retail items out of their homes, or go on extended buying trips, making a profit on reselling to urban stores.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "30–50",
                "suggested_contacts": "Local historians, other antique dealers, possibly criminal fences.",
                "skills": "Accounting, Appraise, Drive Auto, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), History, Library Use, Navigate."
            },
            "Archaeologist": {
                "description": "The study and exploration of the past. Primarily the identification, examination, and analysis of recovered materials relating to human history. The work involves painstaking research and meticulous study, not to mention a willing attitude to getting one’s hands dirty. In the 1920s, successful archaeologists became celebrities, seen as explorers and adventurers. While some used scientific methods, many were happy to apply brute force when unveiling the secrets of the past—a few less reputable types even used dynamite. Such bullish behavior would be frowned upon in modern times.",
                "era":"Lovecraftian - Important in Lovecraft’s stories.",
                "skill_points": "EDU × 4",
                "credit_rating": "10–40",
                "suggested_contacts": "Patrons, museums, universities.",
                "skills": "Appraise, Archaeology, History, Other Language (any), Library Use, Spot Hidden, Mechanical Repair, Navigate or Science (e.g. chemistry, physics, geology, etc.)"
            },
            "Architect": {
                "description": "Architects are trained to design and plan buildings, whether a small conversion to a private house or a multi-million dollar construction project. The architect will work closely with the project manager and oversee the construction. Architects must be aware of local planning laws, health and safety regulation, and general public safety. Some may work for large firms or work freelance. A lot will depend on reputation. In the 1920s, many try and go it alone, working out of their house or a small office. Few manage to sell the grandiose designs they all nurse. Architecture may also encompass specialist areas like naval architecture and landscape architecture.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "30–70",
                "suggested_contacts": "Local building and city engineering departments, construction firms.",
                "skills": "Accounting, Art/Craft (Technical Drawing), Law, Own Language, Computer Use or Library Use, Persuade, Psychology, Science (Mathematics)."
            },
            "Artist": {
                "description": "May be a painter, sculptor, etc. Sometimes self-absorbed and driven with a particular vision, sometimes blessed with a great talent that is able to inspire passion and understanding. Talented or not, the artist’s ego must be hardy and strong to surmount initial obstacles and critical appraisal, and to keep them working if success arrives. Some artists care not for material enrichment, while others have a keen entrepreneurial streak.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or POW × 2)",
                "credit_rating": "9–50",
                "suggested_contacts": "Art galleries, critics, wealthy patrons, the advertising industry.",
                "skills": "Art/Craft (any), History or Natural World, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Other Language, Psychology, Spot Hidden, any two other skills as personal or era specialties."
            },
            "Asylum Attendant": {
                "description": "Although there are private sanitariums for those few who can afford them, the vast bulk of the mentally ill are housed in state and county facilities. Aside from a few doctors and nurses, they employ a large number of attendants, often chosen more for their strength and size rather than medical learning.",
                "era":"Any",
                "skill_points": "EDU × 2 + (STR × 2 or DEX × 2)",
                "credit_rating": "8–20",
                "suggested_contacts": "Medical staff, patients, and relatives of patients. Access to medical records, as well as drugs and other medical supplies.",
                "skills": "Dodge, Fighting (Brawl), First Aid, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Listen, Psychology, Stealth."
            },
           "Athlete": {
                "description": "Probably plays in a professional baseball, football, cricket, or basketball team. This may be a major league team with a regular salary and national attention or—particularly in the case of 1920s baseball—one of many minor league teams, some of them owned and operated by major league owners. The latter pay barely enough to keep players fed and on the team. Successful professional athletes will enjoy a certain amount of celebrity within the arena of their expertise—more so in the present day where sporting heroes stand side by side with film stars on red carpets around the world.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–70",
                "suggested_contacts": "Sports personalities, sports writers, other media stars.",
                "skills": "Climb, Jump, Fighting (Brawl), Ride, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Swim, Throw, any one other skill as a personal or era specialty."
            },
            "Author": {
                "description": "As distinct from the journalist, the author uses words to define and explore the human condition, especially the range of human emotions. Their labors are solitary and the rewards solipsistic: only a relative handful make much money in the present day, though in previous eras the trade once provided a regular living wage. The work habits of authors vary widely. Typically an author might spend months or years researching in preparation for a book, then withdrawing for periods of intense creation.",
                "era":"Lovecraftian - Important in Lovecraft’s stories.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–30",
                "suggested_contacts": "Publishers, critics, historians, etc.",
                "skills": "Art (Literature), History, Library Use, Natural World or Occult, Other Language, Own Language, Psychology, any one other skill as a personal or era specialty."
            },
            "Bartender": {
                "description": "Normally not the owner of the bar, the bartender is everyone’s friend. For some it’s a career or their business, for many it's a means to an end. In the 1920s the profession is made illegal by the Prohibition Act; however, there’s no shortage of work for a bartender, as someone has to serve the drinks in the speakeasies and secret gin joints.",
                "era":"Any",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "8–25",
                "suggested_contacts": "Regular customers, possibly organized crime.",
                "skills": "Accounting, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Fighting (Brawl), Listen, Psychology, Spot Hidden, any one other skill as a personal or era specialty."
            },
            "Big Game Hunter": {
                "description": "Big game hunters are skilled trackers and hunters who usually earn their living leading safaris for wealthy clients. Most are specialized in one part of the world, such as the Canadian woods, African plains, and other locales. Some hunters may work for the black market, capturing live exotic species for private collectors, or trading in illegal or morally objectionable animal products like skins, ivory, and the like—although in the 1920s such activities were more common and were permissible under most countries’ laws. Although the great white hunter is the quintessential type, others may be simply local indigenous people who escort hunters through the backwoods of the Yukon in search of moose or bear.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "20–50",
                "suggested_contacts": "Foreign government officials, game wardens, past (usually wealthy) clients, blackmarket gangs and traders, zoo owners.",
                "skills": "Firearms, Listen or Spot Hidden, Natural World, Navigate, Other Language or Survival (any), Science (Biology, Botany, or Zoology), Stealth, Track."
            },
            "Book Dealer": {
                "description": "A book dealer may be the owner of a retail outlet or niche mail order service, or specialize in buying trips across the country and even overseas. Many will have wealthy or regular clients, who provide lists of sought-after and rare works.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "20–40",
                "suggested_contacts": "Bibliographers, book dealers, libraries and universities, clients.",
                "skills": "Accounting, Appraise, Drive Auto, History, Library Use, Own Language, Other Language, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade)."
            },
           "Bounty Hunter": {
                "description": "Bounty hunters track down and return fugitives to justice. Most often, freelancers are employed by Bail Bondsmen to track down bail jumpers. Bounty hunters may freely cross state lines in pursuit of their quarry and may show little regard for civil rights and other technicalities when capturing their prey. Breaking and entering, threats, and physical abuse are all part of the successful bounty hunter’s bag of tricks. In modern times this may stem to illegal phone taps, computer hacking, and other covert surveillance.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Bail bondsmen, local police, criminal informants.",
                "skills": "Drive Auto, Electronic or Electrical Repair, Fighting or Firearms, one interpersonal skill (Fast Talk, Charm, Intimidate, or Persuade), Law, Psychology, Track, Stealth."
            },
            "Boxer Wrestler": {
                "description": "Professional boxers and wrestlers are managed by individuals (promoters) possibly backed by outside interests, and usually locked into contracts. Professional boxers and wrestlers work and train full-time. Amateur boxing competitions abound; a training ground for those aspiring to professional status. In addition, amateur and post-professional boxers and wrestlers can sometimes be found making a living from illegal bareknuckle fights, usually arranged by organized crime gangs or entrepreneurial locals.",
                "era":"Any",
                "skill_points": "EDU × 2 + STR × 2",
                "credit_rating": "9–60",
                "suggested_contacts": "Sports promoters, journalists, organized crime, professional trainers.",
                "skills": "Dodge, Fighting (Brawl), Intimidate, Jump, Psychology, Spot Hidden, any two other skills as personal or era specialties."
            },
            "Butler Valet Maid": {
                "description": "This occupation covers those who are employed in a servant capacity and includes butler, valet, and lady’s maid. A butler is usually employed as a domestic servant for a large household. Traditionally the butler is in charge of the dining room, wine cellar and pantry, and ranks as the highest male servant. Usually male—a housekeeper would be the female equivalent—the butler is responsible for male servants within the household. The duties of the butler will vary according to the requirements of his employer. A valet or lady’s maid provides personal services, such as maintaining her employer's clothes, running baths, and effectively acting as a personal assistant. The work might include making travel arrangements, managing their employer’s diary, and organizing household finances.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "9–40 (dependent on their employer’s status and credit rating).",
                "suggested_contacts": "Waiting staff of other households, local businesses and household suppliers.",
                "skills": "Accounting or Appraise, Art/Craft (any, e.g. Cook, Tailor, Barber), First Aid, Listen, Psychology, Spot Hidden, any two other skills as personal or era specialties."
            },
            "Clergy": {
                "description": "The hierarchy of the Church usually assigns clergy to their respective parishes or sends them on evangelical missions, most often to a foreign country (see Missionary page 84). Different churches have different priorities and hierarchies: for example, in the Catholic Church a priest may rise through the ranks of bishop, archbishop, and cardinal, while a Methodist pastor may in turn rise to district superintendent and bishop. Many clergy (not just Catholic priests) bear witness to confessions and, though they are not at liberty to divulge such secrets, they are free to act upon them. Some who work in the church are trained in professional skills, acting as doctors, lawyers, and scholars—as appropriate, use the occupation template which best describes the nature of the investigator’s work.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "9–60",
                "suggested_contacts": "Church hierarchy, local congregations, community leaders.",
                "skills": "Accounting, History, Library Use, Listen, Other Language, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any one other skill."
            },
            "Computer Programmer Technician Hacker": {
                "description": "Usually designing, writing, testing, debugging, and/or maintaining the source code of computer programs, the computer programmer is an expert in many different subjects, including formal logic and application platforms. May work freelance or within the confines of a software development house. The computer technician is tasked with the development and maintenance of computer systems and networks, often working alongside other office staff (such as project managers) to ensure systems maintain integrity and provide desired functionality. Similar occupations may include: Database Administrator, IT Systems Manager, Multimedia Developer, Network Administrator, Software Engineer, Webmaster, etc. The computer hacker uses computers and computer networks as a means of protest to promote political ends (sometimes referred to as 'hacktivists') or for criminal gain. Illegally breaking into computers and other user accounts is required, the outcome of which could be anything from defacing web pages, doxing, and swatting, to email bombing designed to enact denials of service.",
                "era":"Modern - Only available for modern-day game settings.",
                "skill_points": "EDU × 4",
                "credit_rating": "10–70",
                "suggested_contacts": "Other IT workers, corporate workers and managers, specialized Internet web communities.",
                "skills": "Computer Use, Electrical Repair, Electronics, Library Use, Science (Mathematics), Spot Hidden, any two other skills as personal or era specialties."
            },
            "Cowboy Girl": {
                "description": "Cowboys work the ranges and ranches of the West. Some own their own ranches, but many are simply hired where and when work is available. Good money can also be made by those willing to risk life and limb on the rodeo circuit, traveling between events for fame and glory. During the 1920s, a few found employment in Hollywood as stuntmen and extras in westerns; for example, Wyatt Earp worked as a technical advisor to the film industry. In modern times some ranches have opened their gates to holidaymakers wishing to experience life as a cowboy.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–20",
                "suggested_contacts": "Local businesspeople, state agricultural departments, rodeo promoters, and entertainers.",
                "skills": "Dodge, Fighting or Firearms, First Aid or Natural World, Jump, Ride, Survival (any), Throw, Track."
            },
            "Craftsperson": {
                "description": "May be equally termed an artisan or master craftsperson. The craftsperson is essentially skilled in the manual production of items or materials. Normally quite talented individuals, some gaining a high reputation for works of art, while others provide a needed community service. Possible trades include: furniture, jewelry, watchmaker, potter, blacksmith, textiles, calligraphy, sewing, carpentry, book binding, glassblowing, toy maker, stained glass, and so on.",
                "era":"Any",
                "skill_points": "EDU × 2 + DEX × 2",
                "credit_rating": "10–40",
                "suggested_contacts": "Local businesspeople, other craftspersons and artists.",
                "skills": "Accounting, Art/Craft (any two), Mechanical Repair, Natural World, Spot Hidden, any two other skills as personal specialties."
            },
            "Criminal": {
                "description": "Criminals come in all shapes, sizes, and shades of grey. Some are merely opportunistic jacks of all trades, such as pickpockets and thugs. See Assassin, Bank robber, Bootlegger Thug, Burglar, Conman, Freelance Criminal, Gun Moll, Fence, Forger Counterfeiter, Smuggler, Street Punk for detail information.",
                "era":"Any",
                "skill_points": "Varies",
                "credit_rating": "Varies",
                "suggested_contacts": "Depends on the specific criminal activity.",
                "skills": "Depends on the specific criminal activity."
            },
            "Assassin": {
                "description": "Assassins are cold-blooded killers of the underworld. They are usually hired for targeted killings, often following strict codes of behavior.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "30–60",
                "suggested_contacts": "Few, mostly underworld; people prefer not to know them too well. The best will have earned a formidable reputation on the street.",
                "skills": "Disguise, Electrical Repair, Fighting, Firearms, Locksmith, Mechanical Repair, Stealth, Psychology."
            },
            "Bank Robber": {
                "description": "Bank robbers are criminals who specialize in robbing banks. They often work in groups and meticulously plan their heists to evade capture.",
                "era":"Any",
                "skill_points": "EDU × 2 + (STR × 2 or DEX × 2)",
                "credit_rating": "5–75",
                "suggested_contacts": "Other gang members (current and retired), criminal freelancers, organized crime.",
                "skills": "Drive Auto, Electrical or Mechanical Repair, Fighting, Firearms, Intimidate, Locksmith, Operate Heavy Machinery, any one other skill as personal or era specialty."
            },
            "Bootlegger Thug": {
                "description": "Bootleggers are individuals involved in the illegal production and distribution of alcohol during the Prohibition era. Thugs are enforcers and muscle for criminal organizations.",
                "era":"Any",
                "skill_points": "EDU × 2 + STR × 2",
                "credit_rating": "5–30",
                "suggested_contacts": "Organized crime, street-level law enforcement, local traders.",
                "skills": "Drive Auto, Fighting, Firearms, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Stealth, Spot Hidden."
            },
            "Burglar": {
                "description": "Burglars are criminals who specialize in breaking into and entering buildings with the intent to steal valuable items.",
                "era":"Any",
                "skill_points": "EDU × 2 + DEX × 2",
                "credit_rating": "5–40",
                "suggested_contacts": "Fences, other burglars.",
                "skills": "Appraise, Climb, Electrical or Mechanical Repair, Listen, Locksmith, Sleight of Hand, Stealth, Spot Hidden."
            },
            "Conman": {
                "description": "Conmen are skilled manipulators who deceive others for financial gain. They use persuasion, charm, and deception to trick their victims.",
                "era":"Any",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "10–65",
                "suggested_contacts": "Other confidence artists, freelance criminals.",
                "skills": "Appraise, Art/Craft (Acting), Law or Other Language, Listen, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Sleight of Hand."
            },
            "Freelance Criminal": {
                "description": "Freelance criminals operate on their own terms, pursuing various criminal activities without being tied to organized crime. They are often self-reliant and resourceful.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or APP × 2)",
                "credit_rating": "5–65",
                "suggested_contacts": "Other petty criminals, street-level law enforcement.",
                "skills": "Art/Craft (Acting) or Disguise, Appraise, one interpersonal skill (Charm, Fast Talk, or Intimidate), Fighting or Firearms, Locksmith or Mechanical Repair, Stealth, Psychology, Spot Hidden."
            },
            "Gun Moll": {
                "description": "A gun moll is a female professional criminal associated with gangsters. She may serve as a partner, accomplice, or lover to male criminals.",
                "era":"Any",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "10–80 (income is usually dependent on boyfriend’s income)",
                "suggested_contacts": "Gangsters, law enforcement, local businesses.",
                "skills": "Art/Craft (any), two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Fighting (Brawl) or Firearms (Handgun), Drive Auto, Listen, Stealth, any one other skill as personal or era specialty."
            },
            "Fence": {
                "description": "Fences are criminals who deal in buying and selling stolen goods. They provide a market for stolen items, acting as intermediaries between thieves and buyers...",
                "era":"Any",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "20–40",
                "suggested_contacts": "Organized crime, trade contacts, black market and legitimate buyers.",
                "skills": "Accounting, Appraise, Art/Craft (Forgery), History, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Library Use, Spot Hidden, any one other skill."
            },
            "Forger Counterfeiter": {
                "description": "Forgers and counterfeits specialize in creating fake documents, art, or currency. They are skilled at replicating genuine items to deceive and profit.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "20–60",
                "suggested_contacts": "Organized crime, businesspeople.",
                "skills": "Accounting, Appraise, Art/Craft (Forgery), History, Library Use, Spot Hidden, Sleight of Hand, any one other skill as personal or era specialty (e.g. Computer Use)."
            },
            "Smuggler": {
                "description": "Smugglers are individuals involved in the illegal transportation and trade of contraband goods across borders or past authorities.",
                "era":"Any",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2)",
                "credit_rating": "20–60",
                "suggested_contacts": "Organized crime, Coast Guard, U.S. Customs officials.",
                "skills": "Firearms, Listen, Navigate, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Drive Auto or Pilot (Aircraft or Boat), Psychology, Sleight of Hand, Spot Hidden."
            },
            "Street Punk": {
                "description": "Street punks are individuals known for their involvement in urban subcultures, often engaging in rebellious and anti-authoritarian behavior. They have a reputation for being tough and street-savvy.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "3–10",
                "suggested_contacts": "Petty criminals, other punks, the local fence, maybe the local gangster, certainly the local police.",
                "skills": "Climb, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Fighting, Firearms, Jump, Sleight of Hand, Stealth, Throw. Also, see Gangster."
            },
            "Cult Leader": {
                "description": "America has always generated new religions, from the New England Transcendentalists to the Children of God, as well as many others, right up to modern times. The leader is either a firm believer in the dogma they impart to the cult’s members or simply in it for the money and power.",
                "era":"Any",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "30–60",
                "suggested_contacts": "While the majority of followers will be regular people, the more charismatic the leader, the greater the possibility of celebrity followers, such as movie stars and rich widows.",
                "skills": "Accounting, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Occult, Psychology, Spot Hidden, any two other skills as specialties."
            },
            "Deprogrammer": {
                "description": "Deprogramming is the act of persuading (or forcing) a person to abandon their belief or allegiance to a religious or social community. Normally, the deprogrammer is hired by relatives of an individual, who has joined some form of cult, in order to break them free (usually by kidnapping) and then subject them to psychological techniques to free them of their association ('conditioning') with the cult. Less extreme deprogrammers exist, who work with those who have voluntarily left a cult. In such cases, the deprogrammer effectively acts as an exit counselor.",
                "era":"Modern - Only available for modern-day game settings.",
                "skill_points": "EDU × 4",
                "credit_rating": "20–50",
                "suggested_contacts": "Local and federal law enforcement, criminals, religious community.",
                "skills": "Two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Drive Auto, Fighting (Brawl) or Firearms, History, Occult, Psychology, Stealth. Note: With the Keeper’s agreement, the Hypnosis skill may be substituted for one of the listed skills."
            },
            "Designer": {
                "description": "Designers work in many fields, from fashion to furniture and most points in-between. The designer may work freelance, for a design house, or for a business designing consumer products, processes, laws, games, graphics, and so on. The investigator’s particular design specialty might influence the choice of skills—adjust the skills as appropriate.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "20–60",
                "suggested_contacts": "Advertising, media, furnishings, architectural, other.",
                "skills": "Accounting, Art (Photography), Art/Craft (any), Computer Use or Library Use, Mechanical Repair, Psychology, Spot Hidden, any one other skill as personal specialty."
            },
            "Dilettante": {
                "description": "Dilettantes are self-supporting, living off an inheritance, trust fund, or some other source of income that does not require them to work. Usually, the dilettante has enough money that specialist financial advisers are needed to take care of it. Probably well-educated, though not necessarily accomplished in anything. Money frees the dilettante to be eccentric and outspoken. In the 1920s, some dilettantes might be flappers or sheiks—as per the parlance of the time—of course, one didn't need to be rich to be a party person. In modern times, 'hipster' might also be an appropriate term. The dilettante has had plenty of time to learn how to be charming and sophisticated; what else has been done with that free time is likely to betray the dilettante’s true character and interests.",
               "era":"Lovecraftian - Important in Lovecraft’s stories.",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "50–99",
                "suggested_contacts": "Variable, but usually people of a similar background and tastes, fraternal organizations, bohemian circles, high society at large.",
                "skills": "Art/Craft (Any), Firearms, Other Language, Ride, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), any three other skills as personal or era specialties."
            },
            "Diver": {
                "description": "Divers could work in various fields such as the military, law enforcement, sponge gathering, salvage, conservation, or treasure hunting. They are skilled in underwater activities and often have contacts in maritime and related industries.",
                "era":"Any",
                "skill_points": "EDU × 2 + DEX × 2",
                "credit_rating": "9–30",
                "suggested_contacts": "Coast guard, ship captains, military, law enforcement, smugglers.",
                "skills": "Diving, First Aid, Mechanical Repair, Pilot (Boat), Science (Biology), Spot Hidden, Swim, any one other skill as personal or era specialty."
            },
            "Doctor of Medicine": {
                "description": "Doctors of Medicine are medical professionals who specialize in various fields such as general practice, surgery, psychiatry, or medical research. They aim to help patients, gain prestige, and contribute to a rational society. They might work in rural practices, urban hospitals, or as medical examiners.",
                "era":"Lovecraftian - Important in Lovecraft’s stories.",
                "skill_points": "EDU × 4",
                "credit_rating": "30–80",
                "suggested_contacts": "Other physicians, medical workers, patients and ex-patients.",
                "skills": "First Aid, Medicine, Other Language (Latin), Psychology, Science (Biology and Pharmacy), any two other skills as academic or personal specialties."
            },
            "Drifter": {
                "description": "Drifters are individuals who choose a wandering and transient lifestyle, often moving from place to place. They may be motivated by a desire for freedom, philosophical reasons, or other factors. Their skills are adapted for mobility and survival on the road.",
                "era":"Any",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2 or STR × 2)",
                "credit_rating": "0–5",
                "suggested_contacts": "Other hobos, friendly railroad guards, contacts in numerous towns.",
                "skills": "Climb, Jump, Listen, Navigate, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Stealth, any two other skills as personal or era specialties."
            },
            "Chauffeur": {
                "description": "A chauffeur is either directly employed by an individual or firm, or works for an agency that hires both car and chauffeur out for single engagements or on a retainer basis. Chauffeurs often serve successful business people and may have political connections.",
                "era":"Any",
                "skill_points": "EDU × 2 + DEX × 2",
                "credit_rating": "10–40",
                "suggested_contacts": "Successful business people (criminals included), political representatives.",
                "skills": "Drive Auto, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Listen, Mechanical Repair, Navigate, Spot Hidden, any one other skill as a personal or era specialty."
            },
            "Driver": {
                "description": "Professional drivers may work for companies, private individuals, or have their own vehicles. They include taxi drivers and general drivers who navigate various environments. Drivers often have contacts in businesses, law enforcement, and street-level life.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–20",
                "suggested_contacts": "Customers, businesses, law enforcement, general street level life.",
                "skills": "Accounting, Drive Auto, Listen, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Mechanical Repair, Navigate, Psychology, any one other skill as personal or era specialty."
            },
            "Taxi driver": {
                "description": "Taxi drivers provide transportation services for passengers, often working for taxi companies or as independent operators. They navigate the streets and may encounter various customers. Taxi drivers often have knowledge of street scenes and notable customers.",
                "era":"Any",
                "skill_points": "EDU x 2 + DEX x 2",
                "credit_rating": "9–30",
                "suggested_contacts": "Street scene, possibly a notable customer now and then.",
                "skills": "Accounting, Drive Auto, Electrical Repair, Fast Talk, Mechanical Repair, Navigate, Spot Hidden, any one other skill as a personal or era specialty."
            },
            "Editor": {
                "description": "Editors work in the news industry, assigning stories, writing editorials, and dealing with deadlines. They play a crucial role in shaping content and meeting journalistic standards. Editors often have contacts in the news industry, local government, and specialized fields.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "10–30",
                "suggested_contacts": "News industry, local government, specialists (e.g. fashion designers, sports, business), publishers.",
                "skills": "Accounting, History, Own Language, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Spot Hidden, any one other skill as personal or era specialty."
            },
            "Elected Official": {
                "description": "Elected officials hold positions of power and influence, ranging from local mayors to federal senators. Their prestige varies based on the level of government and jurisdiction they represent. They often have connections in politics, government, media, business, and sometimes organized crime.",
                "era":"Any",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "50–90",
                "suggested_contacts": "Political operatives, government, news media, business, foreign governments, possibly organized crime.",
                "skills": "Charm, History, Intimidate, Fast Talk, Listen, Own Language, Persuade, Psychology."
            },
            "Engineer": {
                "description": "Engineers are specialists in mechanical or electrical devices, often employed in civilian businesses or the military. They use scientific knowledge and creativity to solve technical problems. Engineers have contacts in business, military, and related fields.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "30–60",
                "suggested_contacts": "Business or military workers, local government, architects.",
                "skills": "Art/Craft (Technical Drawing), Electrical Repair, Library Use, Mechanical Repair, Operate Heavy Machine, Science (Engineering and Physics), any one other skill as personal or era specialty."
            },
            "Entertainer": {
                "description": "This occupation includes various roles like clowns, singers, dancers, comedians, musicians, and more, who perform in front of audiences. Entertainers thrive on attention and applause, and their professions gained respect with the rise of Hollywood stars in the 1920s.",
                "era":"Any",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "9–70",
                "suggested_contacts": "Vaudeville, theater, film industry, entertainment critics, organized crime, and television (for modern-day).",
                "skills": "Art/Craft (e.g. Acting, Singer, Comedian, etc.), Disguise, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Listen, Psychology, any two other skills as personal or era specialties."
            },
            "Explorer": {
                "description": "Explorers in the early twentieth century embark on careers exploring unknown areas of the world. They often secure funding through grants, donations, and contracts to document their findings through various media. Much of the world remains unexplored, including parts of Africa, South America, Australia, deserts, and Asian interiors.",
                "era":"Classic - 1920s period.",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2 or STR × 2)",
                "credit_rating": "55–80",
                "suggested_contacts": "Major libraries, universities, museums, wealthy patrons, other explorers, publishers, foreign government officials, local tribespeople.",
                "skills": "Climb or Swim, Firearms, History, Jump, Natural World, Navigate, Other Language, Survival."
            },
            "Farmer": {
                "description": "Farmers are agricultural workers who raise crops or livestock, either owning the land or being employed. Farming is physically demanding and suited for those who enjoy outdoor labor. Independent farmers in the 1920s face competition from corporate farms and fluctuating commodity markets.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Local bank, local politicians, state agricultural department.",
                "skills": "Art/Craft (Farming), Drive Auto (or Wagon), one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Mechanical Repair, Natural World, Operate Heavy Machinery, Track, any one other skill as a personal or era specialty."
            },
            "Federal Agent": {
                "description": "Federal agents work in various law enforcement agencies, both uniformed and plainclothes. They are responsible for enforcing federal laws and investigating crimes. Federal agents often have contacts within law enforcement, government, and organized crime.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "20–40",
                "suggested_contacts": "Federal agencies, law enforcement, organized crime.",
                "skills": "Drive Auto, Fighting (Brawl), Firearms, Law, Persuade, Stealth, Spot Hidden, any one other skill as a personal or era specialty."
            },
            "Firefighter": {
                "description": "Firefighters are civil servants who work to prevent and combat fires. They often work in shifts and live at fire stations. Firefighting is organized in a hierarchical structure with potential for promotions. Firefighters often have contacts in civic works, medical services, and law enforcement.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Civic workers, medical workers, law enforcement.",
                "skills": "Climb, Dodge, Drive Auto, First Aid, Jump, Mechanical Repair, Operate Heavy Machinery, Throw."
            },
            "Foreign Correspondent": {
                "description": "Foreign correspondents are top-tier news reporters who travel the world to cover international events. They work for major news outlets and may focus on various media forms. Foreign correspondents often report on natural disasters, political upheavals, and wars.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "10–40",
                "suggested_contacts": "National or worldwide news industry, foreign governments, military.",
                "skills": "History, Other Language, Own Language, Listen, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any one other skill as a personal or era specialty."
            },
            "Forensic Surgeon": {
                "description": "Forensic surgeons conduct autopsies, determine causes of death, and provide recommendations to prosecutors. They often testify in criminal proceedings and have contacts in laboratories, law enforcement, and the medical profession.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "40–60",
                "suggested_contacts": "Laboratories, law enforcement, medical profession.",
                "skills": "Other Language (Latin), Library Use, Medicine, Persuade, Science (Biology), (Forensics), (Pharmacy), Spot Hidden."
            },
            "Gambler": {
                "description": "Gamblers are stylish individuals who take chances in games of chance. They may frequent racetracks, casinos, or underground gambling establishments. Gamblers often have contacts in bookies, organized crime, and street scenes.",
                "era":"Any",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2)",
                "credit_rating": "8–50",
                "suggested_contacts": "Bookies, organized crime, street scene.",
                "skills": "Accounting, Art/Craft (Acting), two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Listen, Psychology, Sleight of Hand, Spot Hidden."
            },
            "Gangster Boss": {
                "description": "Gangster bosses lead criminal organizations, making deals and overseeing illegal activities. They have a network of underlings to carry out their orders. Gangsters rose to prominence in the 1920s, controlling various criminal enterprises.",
                "era":"Any",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "60–95",
                "suggested_contacts": "Organized crime, street-level crime, police, city government, politicians, judges, unions, lawyers, businesses, residents of the same ethnic community.",
                "skills": "Fighting, Firearms, Law, Listen, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Spot Hidden."
            },
            "Gangster Underling": {
                "description": "Gangster underlings work for the gangster boss, overseeing specific areas of responsibility. They are involved in illegal activities like protection, gambling, and more. Modern gangster bosses focus on the drug trade and other criminal enterprises.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–20",
                "suggested_contacts": "Street-level crime, police, businesses and residents of the same ethnic community.",
                "skills": "Drive Auto, Fighting, Firearms, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any two other skills as personal or era specialties."
            },
            "Gentleman Lady": {
                "description": "A gentleman or lady is a well-mannered and courteous individual, often from the upper class. In the 1920s, they would have had servants and likely owned both city and country residences. Family status is often more important than wealth in this social class.",
                "era":"Any",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "40–90",
                "suggested_contacts": "Upper classes and landed gentry, politics, servants, agricultural workers.",
                "skills": "Art/Craft (any), two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Firearms (Rifle/Shotgun), History, Other Language (any), Navigate, Ride."
            },
            "Hobo": {
                "description": "Hobos are wandering workers who travel from town to town, often riding the rails. They are penniless explorers of the road, facing danger from police, communities, and railroad staff. Hobos have contacts among other hobos and some friendly railroad guards.",
                "era":"Any",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2)",
                "credit_rating": "0–5",
                "suggested_contacts": "Other hobos, a few friendly railroad guards, so-called \"touches\" in numerous towns.",
                "skills": "Art/Craft (any), Climb, Jump, Listen, Locksmith or Sleight of Hand, Navigate, Stealth, any one other skill as a personal or era specialty."
            },
            "Hospital Orderly": {
                "description": "Hospital orderlies perform various tasks in medical facilities, including cleaning, transporting patients, and other odd jobs. They have contacts among hospital and medical workers as well as access to drugs and medical records.",
                "era":"Any",
                "skill_points": "EDU × 2 + STR × 2",
                "credit_rating": "6–15",
                "suggested_contacts": "Hospital and medical workers, patients. Access to drugs, medical records, etc.",
                "skills": "Electrical Repair, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Fighting (Brawl), First Aid, Listen, Mechanical Repair, Psychology, Stealth."
            },
            "Investigative Journalist": {
                "description": "Investigative journalists report on topics and incidents, often working independently to expose corruption and self-serving agendas. They gather information similar to private detectives and may resort to subterfuge.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "9–30",
                "suggested_contacts": "News industry, politicians, street-level crime or law enforcement.",
                "skills": "Art/Craft (Art or Photography), one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), History, Library Use, Own Language, Psychology, any two other skills as personal or era specialties."
            },
            "Reporter": {
                "description": "Reporters use words to report and comment on current events. They work for various media outlets and often gather stories by interviewing witnesses and checking records. Reporters may use subterfuge to gather information.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "9–30",
                "suggested_contacts": "News and media industries, political organizations and government, business, law enforcement, street criminals, high society.",
                "skills": "Art/Craft (Acting), History, Listen, Own Language, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Stealth, Spot Hidden."
            },
            "Judge": {
                "description": "Judges preside over legal proceedings, making decisions and judgments either alone or within a group. They can be appointed or elected and are usually licensed attorneys. Judges have legal connections and possibly contacts with organized crime.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "50–80",
                "suggested_contacts": "Legal connections, possibly organized crime.",
                "skills": "History, Intimidate, Law, Library Use, Listen, Own Language, Persuade, Psychology"
            },
            "Laboratory Assistant": {
                "description": "Laboratory assistants work in scientific environments, performing various tasks under the supervision of lead scientists. Their tasks depend on the discipline and could include testing, recording results, preparing specimens, and more.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "10–30",
                "suggested_contacts": "Universities, scientists, librarians.",
                "skills": "Computer Use or Library Use, Electrical Repair, Other Language, Science (Chemistry and two others), Spot Hidden, any one other skill as a personal specialty."
            },
            "Laborer Unskilled": {
                "description": "Unskilled laborers include factory workers, road crews, and more. Despite being unskilled, they are often experts in using power tools and equipment. They have contacts within their industry.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Other workers and supervisors within their industry.",
                "skills": "Drive Auto, Electrical Repair, Fighting, First Aid, Mechanical Repair, Operate Heavy Machinery, Throw, any one other skill as a personal or era specialty."
            },
            "Lumberjack": {
                "description": "Lumberjacks work in forestry, often involved in cutting down trees and handling logs. They have contacts among forestry workers, wilderness guides, and conservationists.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Forestry workers, wilderness guides and conservationists.",
                "skills": "Climb, Dodge, Fighting (Chainsaw), First Aid, Jump, Mechanical Repair, Natural World or Science (Biology or Botany), Throw."
            },
            "Miner": {
                "description": "Miners work in various fields such as mining, often dealing with extraction of minerals and ores. They have contacts among union officials and political organizations.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Union officials, political organizations.",
                "skills": "Climb, Geology, Jump, Mechanical Repair, Operate Heavy Machinery, Stealth, Spot Hidden, any one other skill as a personal or era specialty."
            },
            "Lawyer": {
                "description": "Lawyers are legal professionals who provide legal counsel, representing clients and presenting legal solutions. They can be hired or appointed and usually have legal connections, including organized crime.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "30–80",
                "suggested_contacts": "Organized crime, financiers, district attorneys and judges.",
                "skills": "Accounting, Law, Library Use, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any two other skills."
            },
            "Librarian": {
                "description": "Librarians manage and maintain libraries, cataloging and overseeing the collection. They have contacts with booksellers, community groups, and specialist researchers.",
                "era":"Lovecraftian - Important in Lovecraft’s stories.",
                "skill_points": "EDU × 4",
                "credit_rating": "9–35",
                "suggested_contacts": "Booksellers, community groups, specialist researchers.",
                "skills": "Accounting, Library Use, Other Language, Own Language, any four other skills as personal specialties or specialist reading topics."
            },
             "Mechanic": {
                "description": "Mechanics and skilled tradespeople include various trades requiring specialized training and experience, such as carpenters, plumbers, electricians, and mechanics. They often have their own unions and contacts within the trade.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "9–40",
                "suggested_contacts": "Union members, trade-relevant specialists.",
                "skills": "Art/Craft (Carpentry, Welding, Plumbing, etc.), Climb, Drive Auto, Electrical Repair, Mechanical Repair, Operate Heavy Machinery, any two other skills as personal, era or trade specialties."
            },
            "Military Officer": {
                "description": "Military officers are command ranks requiring higher education. They undergo training and are often graduates of military academies. They have contacts in the military and federal government.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "20–70",
                "suggested_contacts": "Military, federal government.",
                "skills": "Accounting, Firearms, Navigate, First Aid, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any one other skill as personal or era specialties."
            },
            "Missionary": {
                "description": "Missionaries spread religious teachings in remote or urban areas. They can be backed by churches or independent. Missionaries of various faiths exist worldwide.",
                "era":"Any",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "0–30",
                "suggested_contacts": "Church hierarchy, foreign officials.",
                "skills": "Art/Craft (any), First Aid, Mechanical Repair, Medicine, Natural World, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), any two other skills as personal or era specialties."
            },
            "Mountain Climber": {
                "description": "Mountain climbers engage in climbing peaks as a sport or profession. They seek challenges in various environments and often have contacts with other climbers, rescue services, and sponsors.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "30–60",
                "suggested_contacts": "Other climbers, environmentalists, patrons, sponsors, local rescue or law enforcement, park rangers, sports clubs.",
                "skills": "Climb, First Aid, Jump, Listen, Navigate, Other Language, Survival (Alpine or as appropriate), Track."
            },
            "Museum Curator": {
                "description": "Museum curators manage and oversee exhibits and collections in museums, often specializing in specific topics. They have contacts with local universities, scholars, and patrons.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "10–30",
                "suggested_contacts": "Local universities and scholars, publishers, museum patrons.",
                "skills": "Accounting, Appraise, Archaeology, History, Library Use, Occult, Other Language, Spot Hidden."
            },
            "Musician": {
                "description": "Musicians perform individually or in groups, playing various instruments. While it's difficult to achieve success, some manage to find regular work or become wealthy through their talent.",
                "era":"Any",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Club owners, musicians’ union, organized crime, street-level criminals.",
                "skills": "Art/Craft (Instrument), one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Listen, Psychology, any four other skills."
            },
            "Nurse": {
                "description": "Nurses provide healthcare assistance in hospitals, nursing homes, and medical practices. They assist patients with various health-related activities and have contacts with healthcare professionals.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "9–30",
                "suggested_contacts": "Hospital workers, physicians, community workers.",
                "skills": "First Aid, Listen, Medicine, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Science (Biology) and (Chemistry), Spot Hidden."
            },
            "Occultist": {
                "description": "Occultists study esoteric secrets, paranormal phenomena, and arcane magic. They seek to uncover paranormal abilities and often have knowledge of various magical theories.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "9–65",
                "suggested_contacts": "Libraries, occult societies or fraternities, other occultists.",
                "skills": "Anthropology, History, Library Use, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Occult, Other Language, Science (Astronomy), any one other skill as a personal or era specialty."
            },
            "Outdoorsman Woman": {
                "description": "Outdoorsmen/women are skilled in surviving and thriving in the wilderness. They may work as guides, rangers, or simply live a self-sufficient lifestyle in nature.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "5–20",
                "suggested_contacts": "Local people and native folk, traders.",
                "skills": "Firearms, First Aid, Listen, Natural World, Navigate, Spot Hidden, Survival (any), Track."
            },
            "Parapsychologist": {
                "description": "Parapsychologists study and investigate paranormal phenomena, often using technology to capture evidence. They specialize in areas like extrasensory perception, telekinesis, and hauntings.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "9–30",
                "suggested_contacts": "Universities, parapsychological publications.",
                "skills": "Anthropology, Art/Craft (Photography), History, Library Use, Occult, Other Language, Psychology, any one other skill as a personal or era specialty."
            },
            "Pharmacist": {
                "description": "Pharmacists are licensed professionals who dispense medications. They may work in hospitals, drug stores, or dispensaries, and have access to a wide range of chemicals and drugs.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "35–75",
                "suggested_contacts": "Local community, local physicians, hospitals and patients. Access to all manner of chemicals and drugs.",
                "skills": "Accounting, First Aid, Other Language (Latin), Library Use, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Science (Pharmacy), (Chemistry)."
            },
            "Photographer": {
                "description": "Photographers capture images using various techniques. They can work in fields like art, journalism, and wildlife conservation, often finding fame and recognition in their specialization.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "9–30",
                "suggested_contacts": "Advertising industry, local clients (including political organizations and newspapers).",
                "skills": "Art/Craft (Photography), one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Science (Chemistry), Stealth, Spot Hidden, any two other skills as personal or era specialties."
            },
            "Photojournalist": {
                "description": "Photojournalists are reporters who use photography to accompany news stories. They work in industries like news and film, often covering events and producing images for publication.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "10–30",
                "suggested_contacts": "News industry, film industry (1920s), foreign governments and authorities.",
                "skills": "Art/Craft (Photography), Climb, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Other Language, Psychology, Science (Chemistry), any two other skills as personal or era specialties."
            },
            "Pilot": {
                "description": "Pilots fly aircraft for various purposes, including commercial airlines and businesses. They may also work as stunt pilots, aviators, or military pilots.",
                "era":"Any",
                "skill_points": "EDU × 2 + DEX × 2",
                "credit_rating": "20–70",
                "suggested_contacts": "Old military contacts, cabin crew, mechanics, airfield staff, carnival entertainers.",
                "skills": "Electrical Repair, Mechanical Repair, Navigate, Operate Heavy Machine, Pilot (Aircraft), Science (Astronomy), any two other skills as personal or era specialties."
            },
            "Aviator": {
                "description": "Aviators are stunt pilots who perform at carnivals and air races. They may also work as test pilots or in other aviation-related roles. Some aviators have military backgrounds.",
                "era":"Classic - 1920s period.",
                "skill_points": "EDU × 4",
                "credit_rating": "30–60",
                "suggested_contacts": "Old military contacts, other pilots, airfield mechanics, businessmen.",
                "skills": "Accounting, Electrical Repair, Listen, Mechanical Repair, Navigate, Pilot (Aircraft), Spot Hidden, any one other skill as a personal or era specialty."
            },
            "Police Detective": {
                "description": "Police detectives investigate crimes, gather evidence, and try to solve major felonies. They work closely with uniformed patrol officers and aim to build cases for criminal prosecution.",
                "era":"Lovecraftian - Important in Lovecraft’s stories.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "20–50",
                "suggested_contacts": "Law enforcement, street level crime, coroner’s office, judiciary, organized crime.",
                "skills": "Art/Craft (Acting) or Disguise, Firearms, Law, Listen, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Spot Hidden, any one other skill."
            },
            "Uniformed Police Officer": {
                "description": "Uniformed police officers work in cities, towns, or other law enforcement agencies. They patrol on foot, in vehicles, or at a desk, maintaining public safety and enforcing laws.",
                "era":"Lovecraftian - Important in Lovecraft’s stories.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Law enforcement, local businesses and residents, street level crime, organized crime.",
                "skills": "Fighting (Brawl), Firearms, First Aid, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Law, Psychology, Spot Hidden, and one of the following as a personal specialty: Drive Automobile or Ride."
            },
            "Private Investigator": {
                "description": "Private investigators gather information and evidence for private clients. They may work on civil cases, track down individuals, or assist in criminal defense. Licensing is often required.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Law enforcement, clients.",
                "skills": "Art/Craft (Photography), Disguise, Law, Library Use, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Spot Hidden, and any one other skill as personal or era specialty (e.g. Computer Use, Locksmith, Fighting, Firearms)."
            },
            "Professor": {
                "description": "Professors are academics employed by colleges and universities. They may also work for corporations in research and development roles. They often hold a Ph.D. and have expertise in their field.",
                "era":"Lovecraftian - Important in Lovecraft’s stories.",
                "skill_points": "EDU × 4",
                "credit_rating": "20–70",
                "suggested_contacts": "Scholars, universities, libraries.",
                "skills": "Library Use, Other Language, Own Language, Psychology, any four other skills as academic, era, or personal specialties."
            },
            "Prospector": {
                "description": "Prospectors search for valuable resources like gold or oil. While the days of the Gold Rush are gone, independent prospectors still search for valuable finds.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "0–10",
                "suggested_contacts": "Local businesses and residents.",
                "skills": "Climb, First Aid, History, Mechanical Repair, Navigate, Science (Geology), Spot Hidden, any one other skill as a personal or era specialty."
            },
            "Prostitute": {
                "description": "Prostitutes engage in various forms of sex work, driven by circumstance or coercion. They may work independently or under the control of pimps.",
                "era":"Any",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "5–50",
                "suggested_contacts": "Street scene, police, possibly organized crime, personal clientele.",
                "skills": "Art/Craft (any), two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Dodge, Psychology, Sleight of Hand, Stealth, any one other skill as a personal or era specialty."
            },
            "Psychiatrist": {
                "description": "Psychiatrists are physicians specialized in diagnosing and treating mental disorders. They often use psychopharmacology and other techniques in their practice.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "30–80",
                "suggested_contacts": "Others in the field of mental illness, physicians and possibly legal professions.",
                "skills": "Other Language, Listen, Medicine, Persuade, Psychoanalysis, Psychology, Science (Biology) and (Chemistry)."
            },
            "Psychologist": {
                "description": "Psychologists study human behavior and can specialize in various areas, including psychotherapy, research, and teaching. They may not be medical doctors.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "10–40",
                "suggested_contacts": "Psychological community, patients.",
                "skills": "Accounting, Library Use, Listen, Persuade, Psychoanalysis, Psychology, any two other skills as academic, era or personal specialties."
            },
            "Researcher": {
                "description": "Researchers are involved in academic or private sector research. They can work in various fields, such as astronomy, physics, and chemistry.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "9–30",
                "suggested_contacts": "Scholars and academics, large businesses and corporations, foreign governments and individuals.",
                "skills": "History, Library Use, one interpersonal skill (Charm, Fast Talk Intimidate, or Persuade), Other Language, Spot Hidden, any three fields of study."
            },
            "Sailor Naval": {
                "description": "Naval sailors serve in the military and go through training. They have various roles, including mechanics, radio operators, and more.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Military, veterans’ associations.",
                "skills": "Electrical or Mechanical Repair, Fighting, Firearms, First Aid, Navigate, Pilot (Boat), Survival (Sea), Swim."
            },
            "Sailor Commercial": {
                "description": "Commercial sailors work on fishing vessels, charter boats, or haulage tankers. They may be involved in legal or illegal activities, such as smuggling.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "20–40",
                "suggested_contacts": "Coast Guard, smugglers, organized crime.",
                "skills": "First Aid, Mechanical Repair, Natural World, Navigate, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Pilot (Boat), Spot Hidden, Swim."
            },
            "Salesperson": {
                "description": "Salespeople promote and sell goods or services for businesses. They may travel to meet clients or work in offices, making calls.",
                "era":"Any",
                "skill_points": "EDU × 2 + APP × 2",
                "credit_rating": "9–40",
                "suggested_contacts": "Businesses within the same sector, favored customers.",
                "skills": "Accounting, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Drive Auto, Listen, Psychology, Stealth or Sleight of Hand, any one other skill."
            },
            "Scientist": {
                "description": "Scientists are involved in research and expanding the bounds of knowledge in various fields. They work for businesses and universities.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "9–50",
                "suggested_contacts": "Other scientists and academics, universities, their employers and former employers.",
                "skills": "Any three science specialisms, Computer Use or Library Use, Other Language, Own Language, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Spot Hidden."
            },
            "Secretary": {
                "description": "Secretaries provide communication and organizational support to executives and managers. They have insights into the inner workings of the business.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or APP × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Other office workers, senior executives in client firms.",
                "skills": "Accounting, Art/Craft (Typing or Short Hand), two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Own Language, Library Use or Computer Use, Psychology, any one other skill as a personal or era specialty."
            },
            "Shopkeeper": {
                "description": "Shopkeepers own and manage small shops, market stalls, or restaurants. They are usually self-employed and may run family businesses.",
                "era":"Any",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2)",
                "credit_rating": "20–40",
                "suggested_contacts": "Local residents and businesses, local police, local government, customers.",
                "skills": "Accounting, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Electrical Repair, Listen, Mechanical Repair, Psychology, Spot Hidden."
            },
            "Soldier Marine": {
                "description": "Soldiers and Marines serve in the enlisted ranks of the Army and Marines. They undergo training and may serve in combat or non-combat roles.",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "9–30",
                "suggested_contacts": "Military, veterans associations.",
                "skills": "Climb or Swim, Dodge, Fighting, Firearms, Stealth, Survival and two of the following: First Aid, Mechanical Repair or Other Language."
            },
            "Spy": {
                "description": "Spies work undercover for intelligence agencies to gather information and carry out various tasks. They may have deep cover identities.",
                "era":"Any",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2)",
                "credit_rating": "20–60",
                "suggested_contacts": "Generally only the person the spy reports to, possibly other connections developed while under cover.",
                "skills": "Art/Craft (Acting) or Disguise, Firearms, Listen, Other Language, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Sleight of Hand, Stealth."
            },
            "Student Intern": {
                "description": "Students or interns may be enrolled at educational institutions or receive on-the-job training. They may work for minimal compensation.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "5–10",
                "suggested_contacts": "Academics and other students, while interns may also know business people.",
                "skills": "Language (Own or Other), Library Use, Listen, three fields of study and any two other skills as personal or era specialties."
            },
            "Stuntman": {
                "description": "Stuntmen and women work in the film and television industry to perform dangerous stunts. They often simulate falls, crashes, and other catastrophes.",
                "era":"Any",
                "skill_points": "EDU × 2 + (DEX × 2 or STR × 2)",
                "credit_rating": "10–50",
                "suggested_contacts": "The film and television industries, explosive and pyrotechnic firms, actors and directors.",
                "skills": "Climb, Dodge, Electrical Repair or Mechanical Repair, Fighting, First Aid, Jump, Swim, plus one from either Diving, Drive Automobile, Pilot (any), Ride."
            },
            "Tribe Member": {
                "description": "Tribe members belong to small groups characterized by kinship and custom. Personal honor, praise, and vengeance play important roles in tribal life.",
                "era":"Any",
                "skill_points": "EDU × 2 + (STR × 2 or DEX × 2)",
                "credit_rating": "0–15",
                "suggested_contacts": "Fellow tribe members.",
                "skills": "Climb, Fighting or Throw, Listen, Natural World, Occult, Spot Hidden, Swim, Survival (any)."
            },
            "Undertaker": {
                "description": "Undertakers, also known as morticians or funeral directors, manage funeral rites, including burials or cremations. They are licensed professionals.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "20–40",
                "suggested_contacts": "Few.",
                "skills": "Accounting, Drive Auto, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), History, Occult, Psychology, Science (Biology) and (Chemistry)."
            },
            "Union Activist": {
                "description": "Union activists organize and lead labor unions in various industries. They face challenges from businesses, politicians, and other groups.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "5–30",
                "suggested_contacts": "Other labor leaders and activists, political friends, possibly organized crime. In the 1920s, also socialists, communists, and subversive anarchists.",
                "skills": "Accounting, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Fighting (Brawl), Law, Listen, Operate Heavy Machinery, Psychology."
            },
            "Waitress Waiter": {
                "description": "Waitresses and waiters serve customers in eating or drinking establishments. Tips are earned by providing good service and building rapport.",
                "era":"Any",
                "skill_points": "EDU × 2 + (APP × 2 or DEX × 2)",
                "credit_rating": "9–20",
                "suggested_contacts": "Customers, organized crime.",
                "skills": "Accounting, Art/Craft (any), Dodge, Listen, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any one skill as a personal or era specialty."
            },
            "Clerk Executive": {
                "description": "This could range from the lowest-level white-collar position of a clerk to a middle or senior manager. The employer could be a small to medium-sized locally-owned business, up to a large national or multinational corporation. Clerks are habitually underpaid and the work is drudgery, with those recognized as having talent being earmarked for promotion someday. Middle and senior managers attract higher salaries, with greater responsibilities and say in how the business is managed day-to-day. Although unmarried white-collar workers are not infrequent, most executive types are family-oriented, with a spouse at home and children—it is often expected of them.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "9–20",
                "suggested_contacts": "Other office workers.",
                "skills": "Accounting, Language (Own or Other), Law, Library Use or Computer Use, Listen, one interpersonal skill (Charm, Fast Talk, Intimidate, or Persuade), any two other skills as personal or era specialties."
            },
             "Middle Senior Manager": {
                "description": "This could range from the lowest-level white-collar position of a clerk to a middle or senior manager. The employer could be a small to medium-sized locally-owned business, up to a large national or multinational corporation. Clerks are habitually underpaid and the work is drudgery, with those recognized as having talent being earmarked for promotion someday. Middle and senior managers attract higher salaries, with greater responsibilities and say in how the business is managed day-to-day. Although unmarried white-collar workers are not infrequent, most executive types are family-oriented, with a spouse at home and children—it is often expected of them.",
                "era":"Any",
                "skill_points": "EDU × 4",
                "credit_rating": "20–80",
                "suggested_contacts": "Old college connections, Masons or other fraternal groups, local and federal government, media and marketing.",
                "skills": "Accounting, Other Language, Law, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, any two other skills as personal or era specialties."
            },
            "Zealot": {
                "description": "Zealots are intense and vision-driven individuals who are passionate about their beliefs. They may agitate for change through various means.",
                "era":"Any",
                "skill_points": "EDU × 2 + (APP × 2 or POW × 2)",
                "credit_rating": "0–30",
                "suggested_contacts": "Religious or fraternal groups, news media.",
                "skills": "History, two interpersonal skills (Charm, Fast Talk, Intimidate, or Persuade), Psychology, Stealth, and any three other skills as personal or era specialties."
            },
            "Zookeeper": {
                "description": "Zookeepers care for animals in zoos, ensuring their feeding and well-being. They may specialize in specific animal breeds.",
                "era":"Any",
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
            matching_occupations = [
                name for name in occupations_info.keys() if occupation_name.lower() in name.lower()
            ]
            if not matching_occupations:
                response = (
                    f"No matching occupations found for '{occupation_name}'.\n"
                    f"Please choose an occupation from the list or check your spelling."
                )
                embed_title = "No Matching Occupations"
            elif len(matching_occupations) == 1:
                occupation_name = matching_occupations[0]
                occupation_info = occupations_info[occupation_name]
                embed_title = occupation_name.capitalize()
                description = occupation_info["description"]
                era = occupation_info["era"]
                skill_points = occupation_info["skill_points"]
                credit_rating = occupation_info["credit_rating"]
                suggested_contacts = occupation_info.get("suggested_contacts", "None")
                skills = occupation_info["skills"]
                response = (
                    f":clipboard: Description: {description}\n"
                    f":clock: Era: {era}\n"
                    f":black_joker: Occupation Skill Points: {skill_points}\n"
                    f":moneybag: Credit Rating: {credit_rating}\n"
                    f":telephone: Suggested Contacts: {suggested_contacts}\n"
                    f":zap: Skills: {skills}"
                )
            else:
                matching_occupations_list = ", ".join(matching_occupations)
                response = (
                    f"Multiple matching occupations found for '{occupation_name}':\n"
                    f"{matching_occupations_list}"
                )
                embed_title = "Multiple Matching Occupations"

        embed = discord.Embed(title=embed_title, description=response, color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(aliases=["cArchetype"])
    async def pulpofcthulhuarchetype(self, ctx, *, archetype_name: str = None):
        archetypes_info = {
            "Adventurer": {
                "description": "A life without adventure is not worth living. The world is a big place and there is much to be experienced and many chances for glory. Sitting behind the desk, working a job nine to five is a death sentence for such folk. The adventurer yearns for excitement, fun, and challenge.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** Choose either DEX or APP",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Climb, Diving, Drive Auto, First-Aid, Fighting (any), Firearms (any), Jump, Language (other), Mechanical repair, Pilot (any), Ride, Stealth, Survival (any), Swim.",
                    ":construction_worker: **Suggested occupations:** Actor, Archaeologist, Athlete, Aviator, Bank Robber, Big Game Hunter, Cat Burglar, Dilettante, Drifter, Gambler, Gangster, Hobo, Investigative Journalist, Missionary, Nurse, Photographer, Ranger, Sailor, Soldier, Tribe Member",
                    ":man_cartwheeling: **Talents:** any two",
                    ":brain: **Suggested traits:** easily bored, tenacious, glory hunter, egocentric",
                ],
            },
            "Beefcake": {
                "description": "Physical, muscular, and capable of handling themselves when the chips are down. Born that way or has worked hard in the pursuit of physical perfection. You won't find these guys and gals in the library, but you might see their faces on a billboard. Beefcakes come in two varieties: the caring, silent type, or the brazen loud-mouth.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** STR.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Climb, Fighting (Brawl), Intimidate, Listen, Mechanical Repair, Psychology, Swim, Throw.",
                    ":construction_worker: **Suggested occupations:** Athlete, Beat Cop, Bounty Hunter, Boxer, Entertainer, Gangster, Hired Muscle, Hobo, Itinerant Worker, Laborer, Mechanic, Sailor, Soldier, Street Punk, Tribe Member.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** domineering, brash, quiet, soft-centered, slow to anger, quick to anger.",
                ],
            },
            "Bon Vivant": {
                "description": "A bon vivant is 'one who lives well,' but that doesn't necessarily mean they are rich. While many are accustomed to wealth, the bon vivant is someone who could be said to enjoy life to the fullest and damn the consequences! Why wait until tomorrow when you can start living life today? Enjoying food and drink, as well as other pleasurable pursuits, is the key to a lifestyle where excess is the norm. Whether poor or rich, such a person puts little thought to saving for a rainy day, preferring to be the center of attention and a friend to all.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** SIZ.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Appraise, Art/Craft (any), Charm, Fast Talk, Language Other (any), Listen, Spot Hidden, Psychology.",
                    ":construction_worker: **Suggested occupations:** Actor, Artist, Butler, Confidence Trickster, Cult Leader, Dilettante, Elected Official, Entertainer, Gambler, Gun Moll, Gentleman/Lady, Military Officer, Musician, Priest, Professor, Zealot.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** excessive, greedy, hoarder, collector, name-dropper, boastful, attention seeking, kind, generous.",
                ],
            },
            "Cold Blooded": {
                "description": "A rationalist who is capable of just about anything. Cold blooded types may follow some twisted moral code, however, their view of humanity is cold and stark; you're either good or bad. There are no shades of gray to navigate, just the harsh realities of life and death. Such people make effective killers as they have little self-doubt; they are ready to follow orders to the letter, or pursue some personal agenda for revenge. Such people may do anything to get the job done. They are rarely spontaneous people; instead, they embody ruthlessness and premeditation. Sometimes they will try to fool themselves into believing they have a 'line' they will not cross, when in reality they are merciless and will go to any length to fulfill what they see as their goal.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** INT.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Art/Craft (Acting), Disguise, Fighting (any), Firearms (any), First Aid, History, Intimidate, Law, Listen, Mechanical Repair, Psychology, Stealth, Survival (any), Track.",
                    ":construction_worker: **Suggested occupations:** Bank Robber, Beat Cop, Bounty Hunter, Cult Leader, Drifter, Exorcist, Federal Agent, Gangster, Gun Moll, Hired Muscle, Hit Man, Professor, Reporter, Soldier, Street Punk, Tribe Member, Zealot.",
                    ":man_cartwheeling: **Talents:** must take the Hardened talent, plus one other.",
                    ":brain: **Suggested traits:** rationalist, sees everything in black and white, ruthless, callous, brutal, pitiless, hardnosed.",
                ],
            },
            "Dreamer": {
                "description": "Whether an idealist or visionary, the dreamer has a strong and powerful mind. Such types tend to follow their own direction in life. 'The dreamer looks beyond the mundane realities of life, perhaps as a form of escapism or because they yearn for what could be, wishing to right wrongs or improve the world around them.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** POW.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Art/Craft (any), Charm, History, Language Other (any), Library Use, Listen, Natural World, Occult.",
                    ":construction_worker: **Suggested occupations:** Artist, Author, Bartender/Waitress, Priest, Cult Leader, Dilettante, Drifter, Elected Official, Gambler, Gentleman/Lady, Hobo, Hooker, Librarian, Musician, Nurse, Occultist, Professor, Secretary, Student, Tribe Member.",
                    ":man_cartwheeling: **Talents:** any two (Strong Willed talent recommended).",
                    ":brain: **Suggested traits:** idealist, optimist, lazy, generous, quiet, thoughtful, always late.",
                ],
            },
            "Egghead": {
                "description": "Everything can be broken down and analyzed in order to understand how it works. Knowledge is a treasure and a joy - a puzzle to explore. Where the scholar is bookish, the egghead is practical and thoroughly enjoys getting their hands dirty. Whether it's wires and gears, valves and computational engines, or blood and bones, the egghead likes to figure out what makes things tick. Perhaps an absent-minded genius or a razor-sharp virtuoso, the egghead can easily become absorbed in the problem before them, leaving them exposed and unaware of what is actually happening around them. Depending on the pulp level of your game, the egghead may be able to invent all manner of gizmos, useful or otherwise.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** Choose either INT or EDU.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Anthropology, Appraise, Computer Use, Electrical Repair, Language Other (any), Library Use, Mechanical Repair, Operate Heavy Machinery, Science (any).",
                    ":construction_worker: **Suggested occupations:** Butler, Cult Leader, Doctor of Medicine, Engineer, Gentleman/Lady, Investigative Journalist, Mechanic, Priest, Scientist.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** knowledgeable, focused, tunnel vision information seeker, oblivious to surroundings, lack of common sense, tinkerer, irresponsible.",
                ],
            },  
            "Explorer": {
                "description": "\"Don't fence me in,\" is the oft-heard cry of the explorer, who wishes for a more authentic and fulfilling life. Strong-willed and virtually unshakeable, the explorer is ever questing for what lies over the horizon. Possibly at one with nature, such types are content to sleep where they fall, happily disdaining the soft comforts of urban life. Whether hacking through jungles, squeezing through caverns, or simply charting the hidden quarters of the city, the explorer is often a misfit who grows restless and annoyed by those they consider to be weak or cowards.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** Choose either DEX or POW.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Animal Handling, Anthropology, Archaeology, Climb, Fighting (Brawl), First Aid, Jump, Language Other (any), Natural World, Navigate, Pilot (any), Ride, Stealth, Survival (any), Track.",
                    ":construction_worker: **Suggested occupations:** Agency Detective, Archaeologist, Big Game Hunter, Bounty Hunter, Dilettante, Explorer, Get-Away Driver, Gun Moll, Itinerant Worker, Investigative Journalist, Missionary, Photographer, Ranger, Sailor, Soldier, Tribe Member.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** outcast, brave, misfit, loner, bullish, strong-willed, leader, restless.",
                ],
            },  
            "Femme Fatale": {
                "description": "A deadly woman or man whose outward beauty usually masks a self-centered approach to life; one who is ever vigilant. By constructing an alluring and glamorous persona the femme fatale is akin to a spider. She draws others to her web in order to possess what she desires or destroy her target. Brave and cunning, the femme fatale is not shy of getting her hands dirty and is a capable foe. Neither is she foolhardy, and she will wait until her web is constructed before dealing out a sudden and well-timed assault (be it mental or physical). A classic pulp archetype, the femme fatale could as easily be termed homme fatale if so desired.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** Choose either APP or INT.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Art/Craft (Acting), Appraise, Charm, Disguise, Drive Auto, Fast Talk, Fighting (Brawl), Firearms (Handgun), Listen, Psychology, Sleight of Hand, Stealth.",
                    ":construction_worker: **Suggested occupations:** Actor, Agency Detective, Author, Cat Burglar, Confidence Trickster, Dilettante, Elected Official, Entertainer, Federal Agent, Gangster, Gun Moll, Hit Man, Hooker, Investigative Journalist, Musician, Nurse, Private Investigator, Reporter, Spy, Zealot.",
                    ":man_cartwheeling: **Talents:** any two (Smooth Talker talent recommended).",
                    ":brain: **Suggested traits:** alluring, glamorous, wicked, deceitful, cunning, focused, fraudulent.",
                ],
            },            
            "Grease Monkey": {
                "description": "The grease monkey is practically minded, able to make and repair all manner of things, be they useful inventions, machines, engines, or other devices. Grease Monkeys may be found lurking under the hood of a car, or playing with the telephone exchange wires. Such types have a 'can do' attitude, able to make the most of what they have at hand, using their skills and experience to wow those around them. Depending on the pulp level of your game, the grease monkey may be able to 'jury-rig' all manner of gizmos, useful or otherwise (Weird Science).",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** INT.",
                    ":zap: **Add 100 bonus points divided amongst any of the following skills:** Appraise, Art/Craft (any), Fighting (Brawl), Drive Auto, Electrical Repair, Locksmith, Mechanical Repair, Operate Heavy Machinery, Spot Hidden, Throw.",
                    ":construction_worker: **Suggested occupations:** Bartender/Waitress, Butler, Cat Burglar, Chauffeur, Drifter, Engineer, Get-Away Driver, Hobo, Itinerant Worker, Mechanic, Sailor, Soldier, Student, Union Activist.",
                    ":man_cartwheeling: **Talents:** any two (Weird Science talent recommended).",
                    ":brain: **Suggested traits:** practical, hands-on, hard working, oil-stained, capable.",
                ],
            },
            "Hard Boiled": {
                "description": "Tough and streetwise, someone who is hard boiled understands that to catch a thief you have to think like a thief. Usually, such a person isn't above breaking the law in order to get the job done. They'll use whatever tools are at their disposal and may crack a few skulls in the process. Often, at their core, they are honest souls who wish the world wasn't so despicable and downright nasty; however, in order to fight for justice, they can be just as nasty as they need to be.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** CON.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Art/Craft (any), Fighting (Brawl), Firearms (any), Drive Auto, Fast Talk, Intimidate, Law, Listen, Locksmith, Sleight of Hand, Spot Hidden, Stealth, Throw.",
                    ":construction_worker: **Suggested occupations:** Agency Detective, Bank Robber, Beat Cop, Bounty Hunter, Boxer, Gangster, Gun Moll, Laborer, Police Detective, Private Investigator, Ranger, Union Activist.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** cynical, objective, practical, world-weary, corrupt, violent.",
                ],
            },   
            "Harlequin": {
                "description": "While similar to the femme fatale, the harlequin does not like to get their hands dirty (if they can help it). Usually possessing a magnetic personality, although not necessarily classically beautiful, such types find enjoyment in manipulating others to do their bidding, and often hide their own agendas behind outright lies or subtle deceptions. Sometimes they are committed to a cause (personal or otherwise), or act like agents of chaos, delighting in watching how people react to the situations they construe.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** APP.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Art/Craft (Acting), Charm, Climb, Disguise, Fast Talk, Jump, Language Other (any), Listen, Persuade, Psychology, Sleight of Hand, Stealth.",
                    ":construction_worker: **Suggested occupations:** Actor, Agency Detective, Artist, Bartender/Waitress, Confidence Trickster, Cult Leader, Dilettante, Elected Official, Entertainer, Gambler, Gentleman/Lady, Musician, Reporter, Secretary, Union Activist, Zealot.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** calculating, cunning, two-faced, manipulative, chaotic, wild, flamboyant.",
                ],
            },  
            "Hunter": {
                "description": "Maybe it's the thrill of the chase, the prize at the end, or just because they have an innate drive to master their environment, the hunter is relentless in pursuing their prey. Calm and calculated, the hunter is willing to wait for the most opportune moment, despising the reckless behavior of the unwary.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** choose either INT or CON.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Animal Handling, Fighting (any), Firearms (Rifle and/or Handgun), First Aid, Listen, Natural World, Navigate, Spot Hidden, Stealth, Survival (any), Swim, Track.",
                    ":construction_worker: **Suggested occupations:** Agency Detective, Bank Robber, Beat Cop, Bounty Hunter, Boxer, Gangster, Gun Moll, Laborer, Police Detective, Private Investigator, Ranger, Union Activist.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** relentless, cunning, patient, driven, calm, quiet.",
                ],
            },            
            "Mystic": {
                "description": "A seeker of the hidden, explorer of the unseen realm; the mystic quests for secrets and the fundamental truth of existence. They may be book-learned academics, shamanistic healers, circus diviners, or visionaries, but all pursue knowledge and the experience of forces outside of the natural order, be it for personal gain or the betterment of mankind.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** POW.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Art/Craft (any), Science (Astronomy), Disguise, History, Hypnosis, Language Other (any), Natural World, Occult, Psychology, Sleight of Hand, Stealth; if the Psychic talent is taken, allocate skill points to the chosen psychic skill(s).",
                    ":construction_worker: **Suggested occupations:** Artist, Cult Leader, Dilettante, Exorcist, Entertainer, Occultist, Parapsychologist, Tribe Member.",
                    ":man_cartwheeling: **Talents:** any two (Psychic talent recommended).",
                    ":brain: **Suggested traits:** collector, knowledgeable, irresponsible, calculating, opportunist, shrewd, studious, risk taker, wise.",
                ],
            },
            "Outsider": {
                "description": "The outsider stands apart from the rest of society, either figuratively or literally. Such people may be alien to the environment in which they find themselves, perhaps from a different country or culture, or they are part of the society but find themselves at odds with it. The outsider is usually on some form of journey, physically or spiritually, and must complete their objective before they can return to, or at last feel part of, the greater whole. Often the outsider will have distinct skills, different way of approaching things, utilizing forgotten, secret, or alien knowledge.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** choose either INT or CON.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Art/Craft (any), Animal Handling, Fighting (any), First Aid, Intimidate, Language Other (any), Listen, Medicine, Navigation, Stealth, Survival (any), Track.",
                    ":construction_worker: **Suggested occupations:** Artist, Drifter, Explorer, Hired Muscle, Itinerant Worker, Laborer, Nurse, Occultist, Ranger, Tribe Member.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** cold, quiet, detached, indifferent, brutal.",
                ],
            },
            "Rogue": {
                "description": "The rogue disobeys rules of society openly questioning the status quo and mocking those in authority. They delight in being non-conformists, acting on impulse and deriding conventional behavior. Laws are there to be broken or skirted around. Most rogues are not necessarily criminals or anarchists intent on spreading chaos, but rather they find amusement in pulling off stunts that will confound others. They are often sophisticated, governed by their own unique moral codes, lovable, and careless.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** choose either DEX or APP.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Appraise, Art/Craft (any), Charm, Disguise, Fast Talk, Law, Locksmith, Psychology, Read Lips, Spot Hidden, Stealth.",
                    ":construction_worker: **Suggested occupations:** Artist, Bank Robber, Cat Burglar, Confidence Trickster, Dilettante, Entertainer, Gambler, Get-Away Driver, Spy, Student.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** charming, disarming, self-absorbed, crafty, shrewd, scheming.",
                ],
            },
            "Scholar": {
                "description": "Uses intelligence and analysis to understand the world around them. Normally quite happy sitting in the library with a book (rather than actually facing the realities of life). A seeker of knowledge, the scholar is not particularly action-oriented; however, when it comes to the crunch, he or she might be the only person who knows what to do.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** EDU.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Accounting, Anthropology, Cryptography, History, Language Other (any), Library Use, Medicine, Natural World, Occult, Science (any).",
                    ":construction_worker: **Suggested occupations:** Archaeologist, Author, Doctor of Medicine, Librarian, Parapsychologist, Professor, Scientist.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** studious, bookish, superiority complex, condescending, loner, fussy, speaks too quickly, pensive.",
                    ":star2: **Special:** always begins the game as a non-believer of the Mythos.",
                ],
            },
            "Seeker": {
                "description": "Puzzles and riddles enthrall the seeker, who uses intelligence and reasoning to uncover mysteries and solve problems. They look for and enjoy mental challenges, always focused on finding the truth, no matter the consequences or tribulations they must face.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** INT.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Accounting, Appraise, Disguise, History, Law, Library Use, Listen, Occult, Psychology, Science (any), Spot Hidden, Stealth.",
                    ":construction_worker: **Suggested occupations:** Agency Detective, Author, Beat Cop, Federal Agent, Investigative Journalist, Occultist, Parapsychologist, Police Detective, Reporter, Spy, Student.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** risk taker, tunnel vision, deceitful, boastful, driven.",
                ],
            },
            "Sidekick": {
                "description": "The sidekick embodies aspects of the steadfast, rogue, and thrill seeker archetypes. Usually, a younger person who has yet to live up to their full potential, someone who seeks to learn from a mentor type figure, or those content not to be the center of attention. Alternatively, the sidekick wishes to belong, to be the hero but is overshadowed by their peers or mentor. Subordinate sidekicks can at times struggle against their (usually) self-imposed restraints, venturing off on flights of fancy that mostly just get them into trouble. Sidekicks usually possess a strong moral code of duty and responsibility.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** choose either DEX or CON.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Animal Handling, Climb, Electrical Repair, Fast Talk, First Aid, Jump, Library Use, Listen, Navigate, Photography, Science (any), Stealth, Track.",
                    ":construction_worker: **Suggested occupations:** Author, Bartender/Waitress, Beat Cop, Butler, Chauffeur, Doctor of Medicine, Federal Agent, Get-Away Driver, Gun Moll, Hobo, Hooker, Laborer, Librarian, Nurse, Photographer, Scientist, Secretary, Street Punk, Student, Tribe Member.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** helpful, resourceful, loyal, accident-prone, questioning, inquisitive, plucky.",
                ],
            },
            "Steadfast": {
                "description": "Moral righteousness runs thickly in the blood of the steadfast. They protect the weak, put the interests of others before themselves, and would willingly sacrifice their life for another's safety. Whether they follow a clear spiritual or religious path or some internal moral code, they do not stoop to the depths of others, fighting with honor and acting as role models to those around them. Whatever else they fight for, they also fight for justice.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** CON.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Accounting, Drive Auto, Fighting (any), Firearms (Handgun), First Aid, History, Intimidate, Law, Natural World, Navigate, Persuade, Psychology, Ride, Spot Hidden, Survival (any).",
                    ":construction_worker: **Suggested occupations:** Athlete, Beat Cop, Butler, Priest, Chauffeur, Doctor of Medicine, Elected Official, Exorcist, Federal Agent, Gentleman/Lady, Missionary, Nurse, Police Detective, Private Detective, Reporter, Sailor, Soldier, Tribe Member.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** unwavering, loyal, resolute, committed, dedicated, firm but fair, faithful.",
                ],
            },
            "Swashbuckler": {
                "description": "Passionate and idealistic souls who are always looking to rescue damsels in distress. Gallant and heroic, the swashbuckler is action-oriented and fights fairly, disdaining the use of firearms as the tools of cowards. Most likely boastful, noisy, and joyous, even when in the direst of situations. A romantic at heart, a swashbuckler possesses a strong code of honor but is prone to reckless behavior that risks more than just their own life.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** choose either DEX or APP.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Art/Craft (any), Charm, Climb, Fighting (any), Jump, Language Other (any), Mechanical Repair, Navigate, Pilot (any), Stealth, Swim, Throw.",
                    ":construction_worker: **Suggested occupations:** Actor, Artist, Aviator, Big Game Hunter, Bounty Hunter, Dilettante, Entertainer, Gentleman/Lady, Investigative Journalist, Military Officer, Missionary, Private Detective, Ranger, Sailor, Soldier, Spy.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** boastful, gallant, action-oriented, romantic, passionate, highly-strung.",
                ],
            },
            "Thrill Seeker": {
                "description": "Some people are like moths to a flame. For them, the easy life is no life at all, and they must seek out adventure and danger in order to feel alive. The stakes are never high enough for thrill seekers, who are always ready to bet large in order to feel the rush of adrenaline pumping through their veins. Such daredevils are drawn to high-octane sports and activities, and for them, a mountain is a challenge to master. Foolhardy to a fault, they cannot understand why no one else is prepared to take the same risks as they do.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** choose either DEX or POW.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Art/Craft (any), Charm, Climb, Diving, Drive Auto, Fast Talk, Jump, Mechanical Repair, Navigate, Pilot (any), Ride, Stealth, Survival (any), Swim, Throw.",
                    ":construction_worker: **Suggested occupations:** Actor, Athlete, Aviator, Bank Robber, Bounty Hunter, Cat Burglar, Dilettante, Entertainer, Explorer, Gambler, Gangster, Get-Away Driver, Gun Moll, Gentleman/Lady, Hooker, Investigative Journalist, Missionary, Musician, Occultist, Parapsychologist, Ranger, Sailor, Soldier, Spy, Union Activist, Zealot.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** daredevil, risk taker, manic, exhibitionist, braggart, trouble maker.",
                ],
            },
            "Two-Fisted": {
                "description": "\"Live fast, die hard\" is the motto of the two-fisted. Such individuals are storehouses of energy, strong, tough, and very capable. Such types are inclined to resolve disputes with their fists rather than words. Usually hard-drinking and hard-talking, they like getting straight to the point and dislike pomp and ceremony. They do not suffer fools gladly. The two-fisted seem to live life in a hurry, quick to anger, contemptuous of authority, and ready to play as dirty as the next guy.",
                "adjustments": [
                    ":heart_decoration: **Core characteristic:** choose either STR or SIZ.",
                    ":zap: **Add 100 bonus points divided among any of the following skills:** Drive Auto, Fighting (Brawl), Firearms (any), Intimidate, Listen, Mechanical Repair, Spot Hidden, Swim, Throw.",
                    ":construction_worker: **Suggested occupations:** Agency Detective, Bank Robber, Beat Cop, Boxer, Gangster, Gun Moll, Hired Muscle, Hit Man, Hooker, Laborer, Mechanic, Nurse, Police Detective, Ranger, Reporter, Sailor, Soldier, Street Punk, Tribe Member, Union Activist.",
                    ":man_cartwheeling: **Talents:** any two.",
                    ":brain: **Suggested traits:** tough, capable, determined, quick to anger, violent, dirty, corrupt, underhand.",
                ],
            },           
        }
        if archetype_name is None:
            archetypes_list = ", ".join(archetypes_info.keys())
            response = f"Archetypes are used only in Pulp of Cthulhu \n\n List of archetypes:\n{archetypes_list}"
            embed_title = "Archetypes List"
        else:
            matching_archetypes = [archetype for archetype in archetypes_info.keys() if archetype_name.lower() in archetype.lower()]
            if not matching_archetypes:
                response = (
                    f"Archetype '{archetype_name}' not found.\n"
                    f"Please choose an archetype from the list or check your spelling."
                )
                embed_title = "Invalid Archetype"
            elif len(matching_archetypes) > 1:
                response = f"Multiple archetypes found matching '{archetype_name}': {', '.join(matching_archetypes)}"
                embed_title = "Multiple Archetypes Found"
            else:
                matched_archetype = matching_archetypes[0]
                archetype_info = archetypes_info[matched_archetype]
                embed_title = matched_archetype.capitalize()
                description = archetype_info["description"]
                adjustments = "\n".join(archetype_info["adjustments"])
                response = f"Archetypes are used only in Pulp of Cthulhu \n\n :scroll: **Description:** {description}\n\n:gear: **Adjustments:**\n\n{adjustments}"
            
        embed = discord.Embed(title=embed_title, description=response, color=discord.Color.green())
        await ctx.send(embed=embed)
            
    @commands.command(aliases=["gbackstory"])
    async def generatebackstory(self, ctx):
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


    @commands.command(aliases=["firearms","finfo"
                              ])
    async def cfirearms(self, ctx, *, weapon_name=None):
        firearms_data = {
            "Remington Double Derringer M95": {
                "description": "A classic double-barrel derringer design.",
                "year": "1866 onwards",
                "cost": "$60 (1920s price)",
                "range": "3 yards",
                "shots_per_round": "1 (2 max) shots per round",
                "capacity": "2",
                "damage": "1D10",
                "malfunction": "100"
            },
            "Colt Single Action Army Revolver M1873": {
                "description": 'Called "the Peacemaker" or the "Frontier Six-Shooter," the single-action Colt is an Old West classic.',
                "year": "1872 onwards",
                "cost": "$30 (1920s price)",
                "range": "15 yards",
                "shots_per_round": "1 (3 max) shots per round",
                "capacity": "6",
                "damage": "1D10+2 (.45) or 1D6 (.22)",
                "malfunction": "100"
            },
            "Colt .45 Automatic M1911": {
                "description": "First adopted by the military in 1911, this popular handgun saw service in numerous wars, law enforcement, and in civilian sectors. Using the powerful .45 ACP round, this gun has excellent stopping power. It has a seven-round detachable box magazine that loads into the grip. It is extremely reliable even under adverse conditions.",
                "year": "1911 onwards",
                "cost": "$40",
                "range": "15 yards",
                "shots_per_round": "1 (3 max) shots per round",
                "capacity": "7",
                "damage": "1D10+2",
                "malfunction": "100"
            },
            "Mauser 'Broomhandle' Pistol M1912": {
                "description": 'One of the most distinctive handguns ever produced, the semiautomatic "Broomhandle" takes its name from its narrow wooden grip. The Mauser first appeared in 1896 and has been constantly updated since. It is available in a range of calibers, including 9mm parabellum, and a Chinese version that accepts .45 ACP rounds. A Spanish version, the Astra M900, appears in 1928. Most models accept a shoulder stock. The slender grip is too small to house a magazine, which is instead mounted in front of the trigger guard. Clumsy to handle and expensive to manufacture, by the time of the Second World War the Broomhandle was relegated to secondary troops. In the 1920s they are used mostly by law enforcement personnel and security troops.',
                "year": "1896 onwards",
                "cost": "$50 (1920s price)",
                "range": "15 yards",
                "shots_per_round": "1 (3 max) shots per round",
                "capacity": "10",
                "damage": "1D10+2 (.45) or 1D10 (9mm)",
                "malfunction": "100"
            },
            "Webley-Fosbery Automatic Revolver": {
                "description": "A unique weapon, the Webley uses the force of its recoil to rotate the chamber rather than trigger-pull, making it the only semiautomatic revolver on the market. Despite rejection by the British military, it is manufactured until 1939 in both .38 and .455 calibers. The Webley-Fosbery is prone to jams unless kept clean but, unlike most revolvers, it features a safety.",
                "year": "1901 onwards",
                "cost": "$30-40",
                "range": "15 yards",
                "shots_per_round": "1 (3 max) shots per round",
                "capacity": "6 (.455) or 8 (.38)",
                "damage": "1D10 (.38) or 1D10+2 (.455)",
                "malfunction": "97-100"
            },
            "Winchester M1895 Rifle": {
                "description": "This popular model was produced between 1895 and 1931, one of several Winchesters taken by Theodore Roosevelt on his hunting trip to Africa. Of lever-action design, it differs from the usual tubular magazine below the barrel, instead using a non-detachable box forward of the trigger guard. This reduces the rifle's capacity to four rounds, five in the .303 British version. Other calibers manufactured include a 7.62mm Spitzer made for the Russian government during the Great War, the only version incorporating stripper clips. Barrel lengths include the standard 30, 28, and 24-inch rifle lengths, as well as a cumbersome 36-inch long range version, and a 22-inch carbine model. The latter is available only in .30-30, .30-06, and .303 British calibers. Most military versions feature lugs for an 8-inch bayonet.",
                "year": "1895 onwards",
                "cost": "$80 (1920s price)",
                "range": "110 yards",
                "shots_per_round": "1 shot per round",
                "capacity": "4",
                "damage": "2D6+4 (.30-30, 30-06 or 7.62mm)",
                "malfunction": "99-100"
            },
            "Mauser M1898 Rifle": {
                "description": "Available in both rifle and carbine versions, this successor to the M1888 is perhaps the ultimate in bolt-action design. Using the powerful 7.92mm Mauser round, a five-round stripper clip permits quick reloading. The M1898 accommodates any one of several types of bayonets, including the notorious saw-backed 'butcher blade.' This weapon was produced in massive quantities and proved as capable of bringing down big game as well as waging war.",
                "year": "1898 onwards",
                "cost": "$80 (1920s price)",
                "range": "110 yards",
                "shots_per_round": "1 shot per round",
                "capacity": "5",
                "damage": "2D6+4",
                "malfunction": "99-100"
            },
            "Springfield M1903 Rifle": {
                "description": "This rugged, bolt-action rifle, regular issue for U.S. troops during the Great War, was a close copy of the Mauser M1898. Standard caliber after 1906 was the .30-06 cartridge in a five-round clip. Barrel length is a short 24 inches. These models are still prized by serious marksmen.",
                "year": "1903 onwards",
                "cost": "$80 (1920s price)",
                "range": "110 yards",
                "shots_per_round": "1 shot per round",
                "capacity": "5",
                "damage": "2D6+4",
                "malfunction": "99-100"
            },
            "Lee-Enfield Mark III Rifle": {
                "description": "A replacement for the outdated Lee-Metford series, this British rifle uses the .303 British cartridge. Features a smooth bolt-action design, but takes advantage of a ten-round magazine for longer firing. The Mark III was the most common Lee-Enfield of the Great War.",
                "year": "1907 onwards",
                "cost": "$50",
                "range": "110 yards",
                "shots_per_round": "1 shot per round",
                "capacity": "10",
                "damage": "2D6+4",
                "malfunction": "100"
            },
            "Remington M1889": {
                "description": "The last in a series that began with the M1883, this double-barrel shotgun with exposed hammers is available in 10, 12, and 16-gauge, with barrel lengths ranging between 28 and 32 inches. When production ceased in 1909, over 37,500 of these firearms had been produced.",
                "year": "1889 onwards",
                "cost": "$35-40",
                "range": "50 yards",
                "shots_per_round": "1 or 2 shots per round",
                "capacity": "2",
                "damage": "1D10+5 (16-gauge slug) or 1D10+6 (12-gauge slug) or 1D10+7 (10-gauge slug) or 4D6+2/2D6+1/1D6 (10-gauge buckshot at 10/20/50 yards) or 4D6/2D6/1D6 (12-gauge buckshot at 10/20/50 yards) or 2D6+2/1D6+1/1D4 (16-gauge buckshot at 10/20/50 yards)",
                "malfunction": "100"
            },
            "Winchester M1887 Shotgun and M1901 Shotgun": {
                "description": "This distinctive, lever-action, hammer shotgun was popular despite its strange, even ugly appearance. Two models were produced: the M1887 in 10- and 12-gauge black powder, and the M1901 in 10-gauge smokeless powder. Both feature five-round, tubular magazines. In 1898, both versions became available in short-barrel riot versions.",
                "year": "1897 and 1901 onwards",
                "cost": "$50",
                "range": "50 yards",
                "shots_per_round": "1 shot per round",
                "capacity": "5",
                "damage": "1D10+6 (12-gauge slug) or 1D10+7 (10-gauge slug) or 4D6/2D6/1D6 (buckshot at 10/20/50 yards)",
                "malfunction": "100"
            },
            "Winchester M1897 Shotgun": {
                "description": "Intended as a replacement for the trouble-plagued M1893, this shotgun was a tremendous success. Pump-action, with an exposed hammer, over a million were produced between 1897 and 1957. A popular hunting weapon, seeing great use in the civilian sector. Thousands of trench versions served the military, while a riot version was marketed to law enforcement agencies.",
                "year": "1897 onwards",
                "cost": "$45",
                "range": "50 yards",
                "shots_per_round": "1 shot per round",
                "capacity": "5",
                "damage": "1D10+6 (12-gauge slug) or 1D10+7 (10-gauge slug) or 4D6+2/2D6+1/1D6 (10-gauge buckshot at 10/20/50 yards) or 4D6/2D6/1D6 (12-gauge buckshot at 10/20/50 yards)",
                "malfunction": "100"
            },
            "Winchester M1912 Shotgun": {
                "description": "This common firearm, a pump-action hammerless design, is available in 12, 16, and 20-gauge (28-gauge in 1934). Riot and trench versions were first produced in 1918. The riot gun is fairly common but after the end of the Great War the trench model must be special-ordered.",
                "year": "1912 onwards",
                "cost": "$70",
                "range": "50 yards",
                "shots_per_round": "1 shot per round",
                "capacity": "5",
                "damage": "1D10+5 (16-gauge slug) or 1D10+6 (12-gauge slug) or 1D10+7 (10-gauge slug) or 4D6+2/2D6+1/1D6 (10-gauge buckshot at 10/20/50 yards) or 4D6/2D6/1D6 (12-gauge buckshot at 10/20/50 yards) or 2D6+2/1D6+1/1D4 (16-gauge buckshot at 10/20/50 yards)",
                "malfunction": "100"
            },
            "Bergmann MP18I": {
                "description": "This weapon was developed near the end of the Great War. Chambered for 9mm Parabellum, it fired automatic only at a cyclic rate of 350-400 rounds per minute from a 20-round drum magazine. The MP28II is a later version, developed in secret in violation of Germany's surrender conditions. It features minor internal modifications, better sights, and a choice of 20 or 30-round box magazines, or a 32-round snail drum. A selector switch allows a choice of semiautomatic or fully automatic fire.",
                "year": "1918 onwards",
                "cost": "$1000+ (black market)",
                "range": "20 yards",
                "shots_per_round": "1 (2) shots per round or full auto",
                "capacity": "20/30/32",
                "damage": "1D10",
                "malfunction": "96-100"
            },
            "Thompson M1921": {
                "description": "M1921 is a modified version of the original model introduced in 1919. Chambered for the .45 ACP, the 'Tommy gun' uses either 20 or 30-round box magazines, or the more cumbersome 50 or 100-round drums. It has a cyclic firing rate of 800 rounds per minute. The 1928 model features a horizontal forward grip (in place of the original pistol-grip) and a reduced firing rate of 650 rounds per minute.",
                "year": "1921 onwards",
                "cost": "$200+ ($1000+ black market)",
                "range": "20 yards",
                "shots_per_round": "1 shot per round or full auto",
                "capacity": "20/30/50/100",
                "damage": "1D10+2",
                "malfunction": "96-100"
            },
            "Mark I Lewis Gun": {
                "description": "The Lewis gun debuted in Belgium in 1913, soon after making its way into the arsenals of England, the U.S., and Japan. Chambered in either .303 British or .30-06 calibers, the fully automatic Lewis gun is fed by a circular drum holding 97 rounds mounted horizontally atop the gun. Although it has a shoulder stock, the Lewis gun's loaded weight of 47 pounds makes its short bipod and a prone firing position almost essential. Lewis Guns are particularly prone to jams. Lewis Guns were routinely fitted to aircraft, mounted on a swivel, and fired by a passenger. These usually dispense with the shoulder stock and opt for the larger, 97-round drum. They fire at a cyclic rate of 450-500 rounds per minute.",
                "year": "1912 onwards",
                "cost": "$3000+ (black market)",
                "range": "110 yards",
                "shots_per_round": "full auto",
                "capacity": "27 (shoulder) or 97 (drum)",
                "damage": "2D6+4",
                "malfunction": "96-100"
            },
            "Browning M1918 Automatic Rifle": {
                "description": "The famed BAR debuted in 1918. Chambered for the .30-06 round, it weighs an imposing 16 pounds but with the aid of its sling can still be supported and fired from a standing position. A selector switch allows a choice of semiautomatic or full automatic. It carries a 20-round box magazine.",
                "year": "1918 onwards",
                "cost": "$800+ (black market)",
                "range": "90 yards",
                "shots_per_round": "1 (2) or full auto",
                "capacity": "20",
                "damage": "2D6+4",
                "malfunction": "100"
            },
            "Vickers .303 Caliber Machine Gun": {
                "description": "Belt-fed and mounted on a heavy tripod, the British Vickers was first introduced in 1912. Firing a .303 cartridge, it has a cyclic rate of 450-500 rounds per minute. Water-cooled, the early models had a problem with steam rising from the barrel, obscuring the shooter's vision. Later models corrected this. This weapon features dual spade-handle handgrips, the trigger is depressed by the thumbs. A special, air-cooled version is suitable for aircraft only.",
                "year": "1912 onwards",
                "cost": "$5000+ (black market)",
                "range": "110 yards",
                "shots_per_round": "full auto",
                "capacity": "250",
                "damage": "2D6+4",
                "malfunction": "99-100"
            },
            "Heckler & Koch MP5": {
                "description": "A versatile submachine gun used by military and law enforcement around the world. Chambered for 9mm Parabellum, it offers a high rate of fire and accuracy in a compact package. Available in various configurations.",
                "year": "1966 onwards",
                "cost": "$1500+",
                "range": "100 meters",
                "shots_per_round": "full auto or semi-auto",
                "capacity": "15/30/50-round magazines",
                "damage": "2D6",
                "malfunction": "98-100"
            },
            "AK-47": {
                "description": "One of the most iconic assault rifles, the AK-47 is known for its reliability and simplicity. Chambered for 7.62x39mm, it has been widely used in conflicts around the world.",
                "year": "1947 onwards",
                "cost": "$500+",
                "range": "300 meters",
                "shots_per_round": "full auto or semi-auto",
                "capacity": "30-round magazine",
                "damage": "2D6+2",
                "malfunction": "96-100"
            },
            "M16": {
                "description": "The standard U.S. military rifle, the M16 has evolved over the years. Chambered for 5.56x45mm, it offers accuracy and modularity. Variants like the M4 are popular among special forces.",
                "year": "1960 onwards",
                "cost": "$1000+",
                "range": "550 meters",
                "shots_per_round": "semi-auto or burst",
                "capacity": "20/30-round magazine",
                "damage": "2D6",
                "malfunction": "98-100"
            },
            "Glock 17": {
                "description": "A popular and reliable semiautomatic pistol used by law enforcement and civilians. Chambered for 9mm Parabellum, it features a polymer frame for reduced weight.",
                "year": "1982 onwards",
                "cost": "$500+",
                "range": "50 meters",
                "shots_per_round": "semi-auto",
                "capacity": "17-round magazine",
                "damage": "1D10+2",
                "malfunction": "98-100"
            },
            "FN SCAR": {
                "description": "A modular assault rifle available in both 5.56x45mm and 7.62x51mm variants. It offers flexibility and adaptability to different combat scenarios.",
                "year": "2009 onwards",
                "cost": "$2000+",
                "range": "600 meters",
                "shots_per_round": "semi-auto or full auto",
                "capacity": "20/30-round magazine",
                "damage": "2D6",
                "malfunction": "98-100"
            },
            "SIG Sauer P226": {
                "description": "A popular semiautomatic pistol used by military and law enforcement. Chambered for 9mm Parabellum, it offers accuracy and reliability.",
                "year": "1983 onwards",
                "cost": "$800+",
                "range": "50 meters",
                "shots_per_round": "semi-auto",
                "capacity": "15-round magazine",
                "damage": "1D10+2",
                "malfunction": "98-100"
            },
            "Barrett M82": {
                "description": "A powerful anti-materiel rifle chambered for .50 BMG. Known for its long-range precision and stopping power, it's used for long-distance engagements and armor penetration.",
                "year": "1982 onwards",
                "cost": "$8000+",
                "range": "1800 meters",
                "shots_per_round": "bolt-action",
                "capacity": "10-round magazine",
                "damage": "4D6",
                "malfunction": "97-100"
            },
            "MP7": {
                "description": "A compact submachine gun designed for special forces and law enforcement. Chambered for 4.6x30mm, it offers high firepower in a small package.",
                "year": "2001 onwards",
                "cost": "$2000+",
                "range": "200 meters",
                "shots_per_round": "full auto or semi-auto",
                "capacity": "20/40-round magazine",
                "damage": "2D6",
                "malfunction": "98-100"
            },
            "Beretta M9": {
                "description": "The standard U.S. military sidearm, the Beretta M9 is a 9mm semiautomatic pistol. Known for its reliability and accuracy, it's widely used by the armed forces.",
                "year": "1985 onwards",
                "cost": "$600+",
                "range": "50 meters",
                "shots_per_round": "semi-auto",
                "capacity": "15-round magazine",
                "damage": "1D10+2",
                "malfunction": "98-100"
            },
            "HK416": {
                "description": "A modernized variant of the M4, the HK416 offers improved reliability and performance. Chambered for 5.56x45mm, it's used by special forces and law enforcement.",
                "year": "2004 onwards",
                "cost": "$1500+",
                "range": "400 meters",
                "shots_per_round": "semi-auto or burst",
                "capacity": "20/30-round magazine",
                "damage": "2D6",
                "malfunction": "98-100"
            },
            "FN P90": {
                "description": "A compact personal defense weapon (PDW) chambered for 5.7x28mm. It features a high-capacity magazine positioned horizontally on top of the weapon.",
                "year": "1990 onwards",
                "cost": "$1500+",
                "range": "200 meters",
                "shots_per_round": "full auto or semi-auto",
                "capacity": "50-round magazine",
                "damage": "2D6",
                "malfunction": "98-100"
            },
            "Heckler & Koch G36": {
                "description": "A versatile assault rifle chambered for 5.56x45mm, used by various military and law enforcement units. Its modular design allows customization.",
                "year": "1996 onwards",
                "cost": "$2000+",
                "range": "400 meters",
                "shots_per_round": "semi-auto or full auto",
                "capacity": "20/30-round magazine",
                "damage": "2D6",
                "malfunction": "98-100"
            },
            "Steyr AUG": {
                "description": "An Austrian bullpup assault rifle chambered for 5.56x45mm. Known for its distinctive design, it offers good accuracy and is used by various armed forces.",
                "year": "1978 onwards",
                "cost": "$2000+",
                "range": "300 meters",
                "shots_per_round": "semi-auto or full auto",
                "capacity": "30-round magazine",
                "damage": "2D6",
                "malfunction": "98-100"
            },
            "Ruger 10/22": {
                "description": "A popular semiautomatic rimfire rifle chambered for .22 LR. Known for its reliability and affordability, it's often used for sport shooting and small game hunting.",
                "year": "1964 onwards",
                "cost": "$300+",
                "range": "100 meters",
                "shots_per_round": "semi-auto",
                "capacity": "10/25-round magazine",
                "damage": "1D4",
                "malfunction": "99-100"
            },
            "CZ 75": {
                "description": "A widely used semiautomatic pistol designed in Czechoslovakia. Chambered for 9mm Parabellum, it's known for its accuracy and all-steel construction.",
                "year": "1975 onwards",
                "cost": "$600+",
                "range": "50 meters",
                "shots_per_round": "semi-auto",
                "capacity": "15/16-round magazine",
                "damage": "1D10+2",
                "malfunction": "98-100"
            },
            "Remington 870": {
                "description": "A pump-action shotgun available in various configurations and chamberings. Known for its reliability and versatility, it's used for hunting, sport shooting, and law enforcement.",
                "year": "1950 onwards",
                "cost": "$300+",
                "range": "50 meters",
                "shots_per_round": "1 or 2 shots per round",
                "capacity": "4/6/8-round capacity",
                "damage": "1D10+5 (12-gauge slug) or 4D6/2D6/1D6 (buckshot)",
                "malfunction": "99-100"
            },
            "Desert Eagle": {
                "description": "A powerful semiautomatic pistol chambered for various magnum calibers. Known for its large size and distinctive appearance, it's often used for sport shooting.",
                "year": "1983 onwards",
                "cost": "$1500+",
                "range": "50 meters",
                "shots_per_round": "semi-auto",
                "capacity": "7/8/9-round magazine",
                "damage": "2D6+2",
                "malfunction": "98-100"
            },
            "Kel-Tec KSG": {
                "description": "A bullpup pump-action shotgun known for its dual magazine tubes, allowing different types of ammunition to be loaded. Used for home defense and law enforcement.",
                "year": "2011 onwards",
                "cost": "$800+",
                "range": "50 meters",
                "shots_per_round": "1 or 2 shots per round",
                "capacity": "6/7-round capacity",
                "damage": "1D10+5 (12-gauge slug) or 4D6/2D6/1D6 (buckshot)",
                "malfunction": "99-100"
            },
            "Springfield XD": {
                "description": "A semiautomatic pistol chambered for various calibers. Known for its safety features and ergonomic design, it's used for self-defense and sport shooting.",
                "year": "2001 onwards",
                "cost": "$500+",
                "range": "50 meters",
                "shots_per_round": "semi-auto",
                "capacity": "10/13/16-round magazine",
                "damage": "1D10+2",
                "malfunction": "98-100"
            },
            "SIG Sauer P226": {
                "description": "A popular semiautomatic pistol chambered for 9mm Parabellum. Known for its accuracy and reliability, it's used by law enforcement and military units worldwide.",
                "year": "1980 onwards",
                "cost": "$800+",
                "range": "50 meters",
                "shots_per_round": "semi-auto",
                "capacity": "15/17/20-round magazine",
                "damage": "1D10+2",
                "malfunction": "98-100"
            },
            "M1 Garand": {
                "description": "A semiautomatic rifle chambered for .30-06 Springfield. Known for its distinctive 'ping' sound when the clip is ejected. Used by U.S. forces during WWII.",
                "year": "1936-1957",
                "cost": "$85",
                "range": "500 meters",
                "shots_per_round": "semiautomatic",
                "capacity": "8-round en bloc clip",
                "damage": "2D6+4",
                "malfunction": "98-100"
            },
            "Thompson M1928A1": {
                "description": "A submachine gun chambered for .45 ACP. Nicknamed the 'Tommy gun,' it was used by various military and law enforcement units during WWII.",
                "year": "1921-1944",
                "cost": "$225",
                "range": "50 meters",
                "shots_per_round": "semiautomatic or full auto",
                "capacity": "20/30/50/100-round magazine",
                "damage": "1D10+2",
                "malfunction": "96-100"
            },
            "Sten Mk II": {
                "description": "A British submachine gun chambered for 9mm Parabellum. Known for its simple design and mass production, it was used by Commonwealth forces during WWII.",
                "year": "1941-1945",
                "cost": "$10",
                "range": "100 meters",
                "shots_per_round": "full auto",
                "capacity": "32-round magazine",
                "damage": "1D10",
                "malfunction": "96-100"
            },
            "MP40": {
                "description": "A German submachine gun chambered for 9mm Parabellum. Known for its reliability and compact design, it was used by German forces during WWII.",
                "year": "1940-1945",
                "cost": "$30",
                "range": "100 meters",
                "shots_per_round": "full auto",
                "capacity": "32-round magazine",
                "damage": "1D10",
                "malfunction": "98-100"
            },
            "Lee-Enfield No. 4 Mk I": {
                "description": "A bolt-action rifle chambered for .303 British. Used by British and Commonwealth forces during WWII, known for its accuracy and durability.",
                "year": "1941-1955",
                "cost": "$25",
                "range": "500 meters",
                "shots_per_round": "bolt-action",
                "capacity": "10-round magazine",
                "damage": "2D6+4",
                "malfunction": "98-100"
            },
            "Mosin-Nagant M91/30": {
                "description": "A bolt-action rifle chambered for 7.62x54mmR. Used by Soviet forces during WWII, known for its ruggedness and widespread use.",
                "year": "1891-1965",
                "cost": "$15",
                "range": "500 meters",
                "shots_per_round": "bolt-action",
                "capacity": "5-round internal magazine",
                "damage": "2D6+4",
                "malfunction": "98-100"
            },
            "MG42": {
                "description": "A German general-purpose machine gun chambered for 7.92x57mm Mauser. Known for its high rate of fire and reliability, used by German forces during WWII.",
                "year": "1942-1959",
                "cost": "$75",
                "range": "1100 meters",
                "shots_per_round": "full auto",
                "capacity": "50-round belt",
                "damage": "2D6+4",
                "malfunction": "99-100"
            },
            "M1A1 Bazooka": {
                "description": "An American rocket-propelled grenade launcher used during WWII. Effective against tanks and armored vehicles.",
                "year": "1942-1955",
                "cost": "$100",
                "range": "100 meters (antitank rockets)",
                "shots_per_round": "single shot",
                "capacity": "1 rocket",
                "damage": "8D6",
                "malfunction": "100"
            },
            "Karabiner 98k": {
                "description": "A bolt-action rifle chambered for 7.92x57mm Mauser. Standard German infantry rifle during WWII, known for its accuracy and reliability.",
                "year": "1935-1945",
                "cost": "$35",
                "range": "500 meters",
                "shots_per_round": "bolt-action",
                "capacity": "5-round internal magazine",
                "damage": "2D6+4",
                "malfunction": "98-100"
            },
            "PPSh-41": {
                "description": "A Soviet submachine gun chambered for 7.62x25mm Tokarev. Known for its high rate of fire and simplicity, used by Soviet forces during WWII.",
                "year": "1941-1961",
                "cost": "$20",
                "range": "100 meters",
                "shots_per_round": "full auto",
                "capacity": "35-round box or drum magazine",
                "damage": "1D10",
                "malfunction": "97-100"
            },
            # Další zbraně...
        }
        if weapon_name is None:
            weapons_list = "\n".join(f"• {weapon}" for weapon in firearms_data.keys())
            embed = discord.Embed(title="Available Firearms", description=weapons_list, color=discord.Color.blue())
        else:
            matching_weapons = [weapon for weapon in firearms_data.keys() if weapon_name.lower() in weapon.lower()]
    
            if not matching_weapons:
                embed = discord.Embed(description="No matching weapons found.", color=discord.Color.red())
            elif len(matching_weapons) == 1:
                weapon_name = matching_weapons[0]
                weapon_info = firearms_data[weapon_name]
                embed = discord.Embed(title=weapon_name, description=weapon_info["description"], color=discord.Color.green())
                embed.add_field(name="📅 Year", value=weapon_info["year"])
                embed.add_field(name="💰 Cost", value=weapon_info["cost"])
                embed.add_field(name="🎯 Range", value=weapon_info["range"])
                embed.add_field(name="🔫 Shots per Round", value=weapon_info["shots_per_round"])
                embed.add_field(name="📦 Capacity", value=weapon_info["capacity"])
                embed.add_field(name="⚔️ Damage", value=weapon_info["damage"])
                embed.add_field(name="🛠️ Malfunction", value=weapon_info["malfunction"])
            else:
                weapons_list = "\n".join(f"• {weapon}" for weapon in matching_weapons)
                embed = discord.Embed(title="Matching Weapons", description=weapons_list, color=discord.Color.blue())
    
        await ctx.send(embed=embed)
        
    @commands.command(aliases=["yinfo"])
    async def cyear(self, ctx, year: int):
        event_info = self.get_year_events(year)
        
        if not event_info:
            await ctx.send("No historical events found for the specified year.")
            return
        
        year_embed = discord.Embed(
            title=f"Historical Events in {year}",
            description="\n".join(event_info),
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=year_embed)
    
    def get_year_events(self, year):
        events = {
                1760: [
                    "George III becomes King of Great Britain and Ireland.",
                    "The Great Fire of Boston destroys a large part of the city.",
                    "William Blackstone, an English jurist, establishes himself as the first European settler in what is now Boston, Massachusetts.",
                    "The first recorded reference to the game of baseball in North America."
                ],
                1761: [
                    "Mozart's opera 'Apollo et Hyacinthus' premieres when he was just 11 years old.",
                    "The Treaty of Pondicherry ends the Second Carnatic War between France and Britain in India.",
                    "Catherine the Great becomes Empress of Russia following a coup d'état.",
                    "A massive earthquake in Portugal, known as the 1755 Lisbon earthquake, continues to have far-reaching effects on European thought and culture."
                ],
                1762: [
                    "Catherine the Great becomes the ruler of Russia after the death of her husband, Peter III.",
                    "Jean-Jacques Rousseau's book 'Émile, or On Education' is published, emphasizing his ideas on education and child development.",
                    "The Treaty of Fontainebleau is signed, ending the Seven Years' War between France, Spain, and Portugal.",
                    "The first public art gallery, the Dulwich Picture Gallery, opens in London."
                ],
                1763: [
                    "The Treaty of Paris ends the Seven Years' War, with Britain gaining control of Canada, Florida, and various territories in India and the Caribbean.",
                    "John Harrison's marine chronometer, H4, is tested and found to accurately determine longitude at sea.",
                    "Pontiac's War begins as Native American tribes in the Great Lakes region rebel against British rule.",
                    "James Watt, the inventor of the steam engine, is born in Scotland."
                ],
                1764: [
                    "The Sugar Act is passed by the British Parliament, imposing new taxes on sugar and other goods imported to the American colonies.",
                    "The town of St. Louis is founded by Pierre Laclède and Auguste Chouteau in what is now Missouri, USA.",
                    "Eli Whitney, inventor of the cotton gin, is born in Massachusetts.",
                    "The Spanish town of St. Louis, Senegal, is captured by the British during the Seven Years' War."
                ],
                1765: [
                    "The Stamp Act is passed by the British Parliament, leading to widespread protests and resistance in the American colonies.",
                    "The first public museum in the United States, the Charleston Museum in South Carolina, is founded.",
                    "The American colonists convene the Stamp Act Congress to protest against taxation without representation.",
                    "James Watt begins working on improvements to the Newcomen steam engine, laying the foundation for the industrial revolution."
                ],
                1766: [
                    "The British Parliament repeals the Stamp Act but passes the Declaratory Act, asserting its authority over the American colonies.",
                    "Edward Gibbon begins writing 'The History of the Decline and Fall of the Roman Empire,' a monumental work of history.",
                    "The first U.S. patent is issued to John Ruggles for a method of making potash.",
                    "Thomas Robert Malthus, the economist known for his theory on population growth, is born in England."
                ],
                1767: [
                    "The Townshend Acts are passed by the British Parliament, imposing new taxes on a range of goods imported to the American colonies.",
                    "Samuel Wallis becomes the first European to discover Tahiti during his circumnavigation of the globe.",
                    "Thomas Gainsborough, a renowned English portrait and landscape painter, creates his famous painting 'The Blue Boy.'",
                    "Norway's oldest newspaper, 'Adresseavisen,' is founded."
                ],
                1768: [
                    "The first volume of the 'Encyclopædia Britannica' is published in Scotland.",
                    "Captain James Cook sets sail on his first voyage to the Pacific Ocean, during which he explores and maps various regions.",
                    "The Boston Nonimportation Agreement is initiated by American colonists in protest against the Townshend Acts.",
                    "The Treaty of Fort Stanwix is signed between the British Crown and the Iroquois Confederacy, leading to the cession of Native American lands."
                ],
                1769: [
                    "Gaspar de Portolà leads the first Spanish land expedition to California, exploring the future site of San Diego and Monterey.",
                    "The Wedgwood pottery company is founded by Josiah Wedgwood in England.",
                    "Daniel Boone begins exploring the Kentucky region and the Cumberland Gap as part of westward expansion in America.",
                    "Napoleon Bonaparte, the future Emperor of France, is born in Corsica."
                ],
                1770: [
                    "The Boston Massacre occurs when British soldiers open fire on a crowd of American colonists, resulting in several deaths.",
                    "James Cook discovers and names Botany Bay in Australia during his first voyage.",
                    "Ludwig van Beethoven, one of the greatest composers in history, is born in Bonn, Germany.",
                    "The Townshend Acts, a series of British taxes on goods imported to the American colonies, lead to growing tensions."
                ],
                1771: [
                    "William Herschel discovers the planet Uranus, the first new planet to be identified in modern history.",
                    "The first professional ballet company is founded in Paris, France.",
                    "David Hume, the Scottish philosopher, publishes 'Essays and Treatises on Several Subjects.'",
                    "The Regulator Movement, a colonial protest against corrupt officials in North Carolina, gains momentum."
                ],
                1772: [
                    "The Gaspee Affair: American colonists burn the British customs ship HMS Gaspee in protest against British enforcement of trade regulations.",
                    "Daniel Boone and a group of settlers reach the Kentucky region, marking the beginning of westward expansion in the United States.",
                    "Immanuel Kant publishes 'Prolegomena to Any Future Metaphysics,' a major work in the history of philosophy.",
                    "The first Committee of Correspondence is established in Boston, connecting colonial leaders across different colonies."
                ],
                1773: [
                    "The Boston Tea Party takes place, as American colonists, disguised as Native Americans, dump British tea into Boston Harbor in protest of the Tea Act.",
                    "Phillis Wheatley, an enslaved African-American, publishes her book of poetry, 'Poems on Various Subjects, Religious and Moral.'",
                    "The East India Company Act is passed in Britain, granting the company a monopoly on tea sales in America and leading to the Boston Tea Party.",
                    "The first recorded yellow fever epidemic occurs in the United States, affecting Philadelphia."
                ],
                1774: [
                    "The First Continental Congress convenes in Philadelphia, bringing together delegates from twelve of the thirteen American colonies to address grievances against Britain.",
                    "Louis XVI becomes the King of France.",
                    "The Coercive Acts (Intolerable Acts) are passed by the British Parliament in response to the Boston Tea Party, leading to increased tensions.",
                    "Empress Catherine the Great of Russia issues the Charter of the Nobility, granting privileges to the Russian nobility."
                ],
                1775: [
                    "The American Revolutionary War begins with the Battles of Lexington and Concord in Massachusetts.",
                    "George Washington is appointed as the Commander-in-Chief of the Continental Army.",
                    "The Second Continental Congress convenes in Philadelphia, and Thomas Jefferson is chosen to draft the Declaration of Independence.",
                    "The first naval engagement of the American Revolution, the Battle of Machias, takes place in Maine."
                ],
                1776: [
                    "The United States Declaration of Independence is adopted by the Continental Congress on July 4th.",
                    "Adam Smith publishes 'An Inquiry into the Nature and Causes of the Wealth of Nations,' a foundational work in economics.",
                    "Hessian mercenaries, hired by Britain, arrive in America to fight against the Patriots in the American Revolution.",
                    "The first volume of 'The Decline and Fall of the Roman Empire' by Edward Gibbon is published."
                ],
                1777: [
                    "The Battle of Saratoga becomes a turning point in the American Revolutionary War, as American forces win a decisive victory over the British.",
                    "The Articles of Confederation and Perpetual Union are adopted by the Continental Congress, serving as the first constitution of the United States.",
                    "The Marquis de Lafayette, a French military officer, arrives in America to support the American Revolution.",
                    "The Second Battle of Saratoga, also known as the Battle of Bemis Heights, takes place during the American Revolutionary War."
                ],
                1778: [
                    "France formally allies with the American colonies, signing treaties of friendship and trade and entering the American Revolutionary War on the side of the Patriots.",
                    "Captain James Cook explores the Hawaiian Islands and is killed during a dispute with the native Hawaiians.",
                    "The Treaty of Alliance is signed between France and the United States, solidifying their military cooperation against Britain.",
                    "The first recorded ascent of Mont Blanc, the highest mountain in the Alps, is achieved by a French party."
                ],
                1779: [
                    "Spain enters the American Revolutionary War as an ally of France and the United States.",
                    "Poland's Constitution of May 3, one of the earliest modern constitutions, is adopted.",
                    "Captain James Cook's third voyage, during which he explores the Pacific Ocean, including the Hawaiian Islands, ends with his death in Hawaii.",
                    "The British defeat American forces in the Battle of Stono Ferry during the Southern theater of the American Revolutionary War."
                ],
                1780: [
                    "The Gordon Riots, a series of anti-Catholic riots, erupt in London, resulting in widespread destruction and deaths.",
                    "The Great Hurricane of 1780 devastates the Caribbean, killing an estimated 22,000 people, making it one of the deadliest Atlantic hurricanes in recorded history.",
                    "Benedict Arnold, a former American general, defects to the British army during the American Revolutionary War.",
                    "John André, a British officer involved in Benedict Arnold's treason, is captured and later executed by hanging."
                ],
                1781: [
                    "The Articles of Confederation are ratified by all thirteen American states, forming the basis of the United States government until the adoption of the U.S. Constitution.",
                    "The Battle of Yorktown, a decisive American victory, leads to the surrender of British forces under General Cornwallis and effectively ends the American Revolutionary War.",
                    "The Bank of North America, the first chartered bank in the United States, is established in Philadelphia.",
                    "Immanuel Kant publishes 'Critique of Pure Reason,' a foundational work in the history of philosophy."
                ],
                1782: [
                    "The Treaty of Paris is signed, officially ending the American Revolutionary War and recognizing the independence of the United States.",
                    "Wolfgang Amadeus Mozart's opera 'The Abduction from the Seraglio' premieres in Vienna.",
                    "The Bank of North America loses its charter due to controversies and economic difficulties.",
                    "The Spanish capture the British-controlled island of Menorca in the Mediterranean."
                ],
                1783: [
                    "The United States Congress ratifies the Treaty of Paris, officially recognizing the end of the American Revolutionary War.",
                    "The Montgolfier brothers successfully launch the first manned hot air balloon flight in France.",
                    "King George III of Britain formally acknowledges the loss of the American colonies in the Speech from the Throne.",
                    "The Laki volcanic fissure in Iceland erupts, leading to the deaths of tens of thousands of people and a year of severe climate abnormalities worldwide."
                ],
                1784: [
                    "Benjamin Franklin invents bifocal eyeglasses.",
                    "The Treaty of Fort Stanwix is signed, establishing peace between the United States and the Iroquois Confederacy.",
                    "Mozart joins the Freemasons, a fraternal organization.",
                    "The United Empress of China, an American ship, becomes the first American ship to reach China."
                ],
                1785: [
                    "James Madison proposes the idea of the Constitutional Convention in Philadelphia to revise the Articles of Confederation.",
                    "The University of Georgia is founded, becoming the first public university in the United States.",
                    "The dollar sign ($) is first used as a symbol for the United States currency.",
                    "French balloonists Jean-Pierre Blanchard and John Jeffries make the first successful aerial crossing of the English Channel."
                ],
                1786: [
                    "Shays' Rebellion, an armed uprising against the Massachusetts state government, occurs in response to economic hardships and debt.",
                    "The Annapolis Convention is held to discuss issues related to trade and commerce among the states.",
                    "The Virginia Statute for Religious Freedom, written by Thomas Jefferson, is enacted, establishing religious freedom as a fundamental principle.",
                    "The first commercial ice cream is produced in New York City."
                ],
                1787: [
                    "The Constitutional Convention convenes in Philadelphia to draft the United States Constitution.",
                    "The Northwest Ordinance is passed by the U.S. Congress, providing a system for admitting new states to the Union and prohibiting slavery in the Northwest Territory.",
                    "The Society for Effecting the Abolition of the Slave Trade is founded in London, marking a significant step in the abolitionist movement.",
                    "Wolfgang Amadeus Mozart's opera 'Don Giovanni' premieres in Prague."
                ],
                1788: [
                    "The United States Constitution is ratified by the required nine states, officially becoming the supreme law of the land.",
                    "New York becomes the eleventh state to ratify the U.S. Constitution.",
                    "The First Fleet, a convoy of British ships, arrives in Australia, marking the beginning of British colonization.",
                    "The French Revolution begins with the convening of the Estates-General in France."
                ],
                1789: [
                    "George Washington is inaugurated as the first President of the United States in New York City.",
                    "The French Revolution intensifies with the storming of the Bastille prison in Paris.",
                    "James Madison introduces the Bill of Rights, which would become the first ten amendments to the U.S. Constitution.",
                    "The United States Supreme Court holds its first session in New York City."
                ],
                1790: [
                    "The United States Census records a population of nearly 4 million people.",
                    "The Supreme Court of the United States holds its first session in New York City.",
                    "George Washington signs the Residence Act, establishing the location for the permanent U.S. capital, Washington, D.C.",
                    "The first successful U.S. patent is granted to Samuel Hopkins for a process of making potash."
                ],
                1791: [
                    "The Bill of Rights, consisting of the first ten amendments to the U.S. Constitution, is ratified.",
                    "Vermont becomes the 14th state of the United States.",
                    "Eli Whitney invents the cotton gin, revolutionizing cotton production.",
                    "Wolfgang Amadeus Mozart's opera 'The Magic Flute' premieres in Vienna."
                ],
                1792: [
                    "France declares war on Austria, marking the beginning of the French Revolutionary Wars.",
                    "The New York Stock Exchange is founded on Wall Street.",
                    "The Kentucky and Virginia Resolutions are adopted, asserting states' rights and challenging the Alien and Sedition Acts.",
                    "George Washington is reelected as President of the United States."
                ],
                1793: [
                    "King Louis XVI of France is executed during the French Revolution.",
                    "Eli Whitney's cotton gin is patented in the United States.",
                    "Yellow fever epidemic hits Philadelphia, then the U.S. capital, causing thousands of deaths.",
                    "The United States issues the Proclamation of Neutrality, staying out of the conflict between Britain and France."
                ],
                1794: [
                    "The Whiskey Rebellion, a tax protest in western Pennsylvania, is suppressed by the U.S. government.",
                    "The Jay Treaty is signed, resolving disputes between the United States and Great Britain.",
                    "Eli Whitney receives a government contract to produce muskets using interchangeable parts, pioneering mass production.",
                    "Haiti's successful slave revolt against French rule begins."
                ],
                1795: [
                    "Treaty of Greenville is signed, ending the Northwest Indian War and ceding Native American land to the United States.",
                    "John Adams is elected as the second President of the United States.",
                    "James Swan, an American banker, secures a loan from the Dutch Republic to help ease the U.S. financial crisis.",
                    "The Marseillaise, the French national anthem, is composed by Claude Joseph Rouget de Lisle."
                ],
                1796: [
                    "Tennessee becomes the 16th state of the United States.",
                    "John Adams is inaugurated as the second President of the United States.",
                    "Edward Jenner introduces the smallpox vaccine.",
                    "The farewell address of George Washington is published, emphasizing the dangers of political parties and foreign alliances."
                ],
                1797: [
                    "John Adams becomes the first President to occupy the White House in Washington, D.C.",
                    "The XYZ Affair escalates tensions between the United States and France, leading to the Quasi-War.",
                    "Napoleon Bonaparte seizes power in France's Coup of 18 Brumaire, eventually becoming First Consul.",
                    "The first successful parachute jump is made by André-Jacques Garnerin in France."
                ],
                1798: [
                    "The Alien and Sedition Acts are passed by the United States Congress, restricting immigration and freedom of the press.",
                    "The United States Marine Corps is officially re-established.",
                    "The Irish Rebellion of 1798 against British rule begins.",
                    "Thomas Malthus publishes 'An Essay on the Principle of Population,' outlining his theory of population growth."
                ],
                1799: [
                    "George Washington dies at Mount Vernon, Virginia.",
                    "The Rosetta Stone is discovered in Egypt, eventually leading to the decipherment of hieroglyphics.",
                    "Napoleon Bonaparte becomes First Consul of France in a coup d'état.",
                    "The metric system is introduced in France, leading to its eventual global adoption."
                ],
                1800: [
                    "The Library of Congress is established in Washington, D.C., with a collection of 740 books.",
                    "The Act of Union 1800 merges the Kingdom of Great Britain and the Kingdom of Ireland to form the United Kingdom of Great Britain and Ireland.",
                    "Alessandro Volta invents the first true electric battery, known as the Voltaic Pile.",
                    "Napoleon Bonaparte leads a successful military campaign in Italy."
                ],
                1801: [
                    "The United Kingdom officially comes into existence as the result of the Act of Union 1800.",
                    "John Marshall becomes the fourth Chief Justice of the United States Supreme Court.",
                    "The first known asteroid, Ceres, is discovered by Giuseppe Piazzi.",
                    "Thomas Jefferson is inaugurated as the third President of the United States."
                ],
                1802: [
                    "The Treaty of Amiens is signed, temporarily ending hostilities between the United Kingdom and France during the Napoleonic Wars.",
                    "Simon Willard patents the banjo clock, an early American wall clock.",
                    "The first recorded human-powered submarine, the Nautilus, is tested by Robert Fulton.",
                    "The United States Military Academy at West Point is founded."
                ],
                1803: [
                    "The United States completes the Louisiana Purchase from France, doubling its territory.",
                    "The Supreme Court case of Marbury v. Madison establishes the principle of judicial review.",
                    "The British engineer Richard Trevithick builds the first full-scale working railway steam locomotive.",
                    "Haiti gains independence from France after a successful slave revolt."
                ],
                1804: [
                    "Napoleon Bonaparte crowns himself Emperor of the French in Notre-Dame Cathedral in Paris.",
                    "The Lewis and Clark Expedition begins its journey to explore the western United States.",
                    "The first recorded self-propelled vehicle, the Cugnot steam tricycle, is built in France.",
                    "The Serbian revolution against the Ottoman Empire begins."
                ],
                1805: [
                    "The Battle of Trafalgar takes place, resulting in a decisive British victory over the French and Spanish navies.",
                    "Beethoven's Symphony No. 3, also known as the 'Eroica,' premieres in Vienna.",
                    "The Lewis and Clark Expedition reaches the Pacific Ocean, completing its journey.",
                    "The United States Marine Corps Band is established."
                ],
                1806: [
                    "Napoleon establishes the Continental System, an economic blockade against British trade with Europe.",
                    "The double-action revolver is patented by Robert Ball in the United States.",
                    "Meriwether Lewis and William Clark return to St. Louis, completing their expedition.",
                    "The Holy Roman Empire is dissolved."
                ],
                1807: [
                    "The British Parliament passes the Slave Trade Act, prohibiting the slave trade throughout the British Empire.",
                    "Robert Fulton's steamboat, the Clermont, makes its first successful voyage up the Hudson River.",
                    "The United States Congress passes the Embargo Act of 1807, restricting American trade with foreign nations.",
                    "The Royal Navy impresses American sailors, leading to increased tensions between the United States and Britain."
                ],
                1808: [
                    "The Peninsular War begins as part of the Napoleonic Wars, with the French invading Spain and Portugal.",
                    "Beethoven's Symphony No. 5 premieres in Vienna.",
                    "The Atlantic slave trade is officially abolished in the United States, but domestic slavery continues.",
                    "The first practical typewriter, known as the Sholes and Glidden typewriter, is patented."
                ],
                1809: [
                    "James Madison is inaugurated as the fourth President of the United States.",
                    "The War of the Fifth Coalition begins, with Austria and the United Kingdom opposing Napoleon's French Empire.",
                    "Charles Darwin is born in England.",
                    "The first successful steam-driven locomotive railway is built in Wales."
                ],
                1810: [
                    "Mexico begins its war of independence from Spain.",
                    "Friedrich H. C. von Sickingen, a German inventor, builds the first known typewriter.",
                    "Peter Durand patents the tin can, revolutionizing food preservation.",
                    "The first Oktoberfest is held in Munich, Germany."
                ],
                1811: [
                    "The first steam-powered ferryboat, the Juliana, begins operation in the United States.",
                    "Jane Austen's novel 'Sense and Sensibility' is published anonymously.",
                    "The Peruvian War of Independence against Spanish rule intensifies.",
                    "The first recorded women's golf tournament is held in Musselburgh, Scotland."
                ],
                1812: [
                    "War of 1812 between the United States and the United Kingdom begins.",
                    "Charles Dickens, a famous English writer, is born.",
                    "The world's first known gas street lamp is installed in London.",
                    "Napoleon Bonaparte's invasion of Russia ends in disaster."
                ],
                1813: [
                    "The United States wins the Battle of Lake Erie during the War of 1812.",
                    "Beethoven premieres his Symphony No. 7 in A Major.",
                    "The world's first suspension bridge, the Colossus Bridge, is built in Scotland.",
                    "The United States experiences the largest earthquake in its history in the Missouri Territory."
                ],
                1814: [
                    "The United States and the United Kingdom sign the Treaty of Ghent, ending the War of 1812.",
                    "The Star-Spangled Banner, the U.S. national anthem, is written by Francis Scott Key.",
                    "The world's first plastic, Parkesine, is invented by Alexander Parkes.",
                    "The eruption of Mount Tambora in Indonesia causes the 'Year Without a Summer' in 1816."
                ],
                1815: [
                    "The Battle of Waterloo marks the end of the Napoleonic Wars in Europe.",
                    "The eruption of Mount Tambora in Indonesia causes the most powerful volcanic eruption in recorded history.",
                    "The Congress of Vienna is held to redraw the map of Europe after the Napoleonic Wars.",
                    "The first modern gold coin, the Sovereign, is minted in the United Kingdom."
                ],
                1816: [
                    "The Year Without a Summer causes widespread crop failures and food shortages.",
                    "The American Colonization Society is founded to promote the colonization of Africa by freed African Americans.",
                    "The first successful human blood transfusion is performed by Dr. James Blundell.",
                    "Argentina declares its independence from Spain."
                ],
                1817: [
                    "The first public gas street lighting in the United States is installed in Baltimore, Maryland.",
                    "Mississippi becomes the 20th U.S. state.",
                    "Simón Bolívar writes his famous 'Letter from Jamaica,' outlining his vision for Latin American independence.",
                    "The New York Stock Exchange (NYSE) is formally organized under the Buttonwood Agreement."
                ],
                1818: [
                    "Mary Shelley's novel 'Frankenstein; or, The Modern Prometheus' is published.",
                    "Illinois becomes the 21st U.S. state.",
                    "The Maronite Christian peasants of Mount Lebanon revolt against Ottoman rule.",
                    "The first successful human blood transfusion using a syringe is performed by Dr. James Blundell."
                ],
                1819: [
                    "The Adams-Onís Treaty is signed, ceding Florida from Spain to the United States.",
                    "Queen Victoria is born in the United Kingdom.",
                    "The bicycle, called the draisine, is invented by Karl Drais.",
                    "The Panic of 1819 becomes the first major financial crisis in the United States."
                ],
                1820: [
                    "The Missouri Compromise is passed in the United States, admitting Missouri as a slave state and Maine as a free state.",
                    "Astronomer Mary Anning discovers the first complete Ichthyosaurus skeleton in England.",
                    "The Venus de Milo, a famous ancient Greek statue, is discovered on the island of Milos.",
                    "The world's first known comic book, 'The Glasgow Looking Glass,' is published."
                ],
                1821: [
                    "The Greek War of Independence against the Ottoman Empire begins.",
                    "Mexico gains independence from Spain.",
                    "Faraday's law of electromagnetic induction is discovered by Michael Faraday.",
                    "The first edition of 'The Guardian' newspaper is published in London."
                ],
                1822: [
                    "Brazil declares its independence from Portugal.",
                    "The world's first mechanical computer, the 'Difference Engine,' is designed by Charles Babbage.",
                    "Gregor Mendel, the father of modern genetics, is born.",
                    "The first patent for a self-propelled railway locomotive is granted to George Stephenson."
                ],
                1823: [
                    "The Monroe Doctrine is declared by U.S. President James Monroe, warning against European interference in the Americas.",
                    "The first practical photography technique, called Niepce's 'heliography,' is created by Joseph Nicéphore Niépce.",
                    "Beethoven's Ninth Symphony, including the 'Ode to Joy,' premieres in Vienna.",
                    "The first U.S. patent for a horseshoe manufacturing machine is granted."
                ],
                1824: [
                    "The United Kingdom formally recognizes the independence of Latin American countries.",
                    "Lafcadio Hearn, a famous writer known for his works on Japan, is born.",
                    "The first photograph ever taken of a person is captured by Louis Daguerre.",
                    "The Rensselaer School, which later becomes Rensselaer Polytechnic Institute (RPI), is founded in the United States."
                ],
                1825: [
                    "The Erie Canal opens in the United States, connecting the Great Lakes to the Hudson River.",
                    "John Quincy Adams becomes the sixth President of the United States.",
                    "The first public railway to use steam locomotives opens in England.",
                    "The world's first public passenger railway, the Stockton and Darlington Railway, begins operations in England."
                ],
                1826: [
                    "The University of London is founded, becoming the first university in England to admit students regardless of religious affiliation.",
                    "John Walker invents the friction match, revolutionizing fire-starting methods.",
                    "The first photograph of a human being is taken by Louis Daguerre.",
                    "Joseph Nicéphore Niépce creates the first successful permanent photograph, 'View from the Window at Le Gras.'"
                ],
                1827: [
                    "Freedom's Journal, the first African American newspaper, is published in the United States.",
                    "The Baltimore and Ohio Railroad becomes the first commercial railroad in the United States.",
                    "Composer Ludwig van Beethoven dies in Vienna.",
                    "Sir George Stokes, a renowned physicist, is born."
                ],
                1828: [
                    "Andrew Jackson is elected as the seventh President of the United States.",
                    "Noah Webster publishes his first dictionary, 'An American Dictionary of the English Language.'",
                    "The first patent for a modern fire extinguisher is granted to George William Manby.",
                    "The Tariff of 1828, also known as the 'Tariff of Abominations,' causes controversy in the United States."
                ],
                1829: [
                    "The Metropolitan Police Service, known as the Met, is founded in London, becoming the world's first modern and professional police force.",
                    "King's College London is established as a university.",
                    "Photography pioneer Louis Daguerre creates the first photograph of the Moon.",
                    "The Indian Removal Act is signed into law by U.S. President Andrew Jackson, leading to the forced removal of Native American tribes."
                ],
                1830: [
                    "The Indian Removal Act is signed into law by U.S. President Andrew Jackson.",
                    "The Book of Mormon is published by Joseph Smith.",
                    "The Liverpool and Manchester Railway, the world's first passenger railway, opens in England.",
                    "First known photograph, 'View from the Window at Le Gras,' is taken by Joseph Nicéphore Niépce."
                ],
                1831: [
                    "Nat Turner's slave rebellion takes place in Virginia, leading to a crackdown on enslaved people.",
                    "Charles Darwin embarks on his voyage aboard HMS Beagle, eventually leading to his theory of evolution.",
                    "The Belgian Revolution results in Belgium gaining independence from the Netherlands.",
                    "The first issue of The Liberator, an abolitionist newspaper, is published by William Lloyd Garrison."
                ],
                1832: [
                    "The Reform Act 1832 is passed in the United Kingdom, expanding voting rights.",
                    "The Black Hawk War takes place in the United States, involving conflicts with Native American tribes.",
                    "The cholera pandemic reaches Europe, causing widespread deaths.",
                    "The world's first roller coaster opens at Russia Mountain in St. Petersburg."
                ],
                1833: [
                    "The Slavery Abolition Act 1833 is passed in the United Kingdom, ending slavery in most British colonies.",
                    "The Factory Act 1833 is passed in the UK, setting limits on child labor in factories.",
                    "Oberlin College becomes the first coeducational college in the United States.",
                    "Felix Mendelssohn's \"Italian Symphony\" premieres in London."
                ],
                1834: [
                    "The Poor Law Amendment Act 1834 is passed in the UK, reforming the welfare system.",
                    "The Spanish Inquisition is officially disbanded.",
                    "The Zollverein, a customs union, is established in Germany, promoting economic unity.",
                    "The United States establishes diplomatic relations with the Empire of Japan."
                ],
                1835: [
                    "The Texas Revolution begins, leading to the independence of the Republic of Texas.",
                    "Mark Twain (Samuel Clemens), American author, is born.",
                    "The Great Moon Hoax is published in The New York Sun, falsely claiming the discovery of life on the moon.",
                    "The first assassination attempt on a sitting U.S. President occurs when Richard Lawrence attempts to kill Andrew Jackson."
                ],
                1836: [
                    "The Battle of the Alamo takes place during the Texas Revolution.",
                    "Arkansas becomes the 25th state of the United States.",
                    "Charles Darwin returns from his voyage on HMS Beagle, laying the groundwork for his theory of evolution.",
                    "The Treaty of Velasco ends the Texas Revolution, recognizing Texan independence from Mexico."
                ],
                1837: [
                    "Queen Victoria ascends to the British throne.",
                    "The Panic of 1837 causes a severe economic depression in the United States.",
                    "Hans Christian Andersen's first book of fairy tales is published.",
                    "Samuel Morse demonstrates the electric telegraph for the first time."
                ],
                1838: [
                    "The Trail of Tears forcibly relocates thousands of Cherokee Nation members from the southeastern United States to Indian Territory.",
                    "Anti-abolitionist riots occur in Philadelphia.",
                    "The first photograph of the Moon is taken by François Arago.",
                    "The first known use of the term 'OK' is published in The Boston Morning Post."
                ],
                1839: [
                    "The Opium War between China and the United Kingdom begins.",
                    "Louis Daguerre announces the daguerreotype photographic process.",
                    "The first recorded baseball game is played in Hoboken, New Jersey.",
                    "Edgar Allan Poe's short story 'The Fall of the House of Usher' is published."
                ],
                1840: [
                    "Queen Victoria marries Prince Albert of Saxe-Coburg and Gotha.",
                    "The Penny Black, the world's first adhesive postage stamp, is issued in the United Kingdom.",
                    "The Treaty of Waitangi is signed in New Zealand, establishing British sovereignty.",
                    "Samuel Morse receives a patent for the telegraph."
                ],
                1841: [
                    "Hong Kong is ceded to the United Kingdom by China after the First Opium War.",
                    "Edgar Allan Poe publishes 'The Murders in the Rue Morgue,' considered the first detective story.",
                    "Thomas Cook organizes the first organized travel excursion by train in England.",
                    "William Henry Harrison becomes the 9th President of the United States but dies after just 31 days in office."
                ],
                1842: [
                    "The United States and the United Kingdom sign the Webster-Ashburton Treaty, resolving border disputes.",
                    "Charles Dickens publishes 'The Old Curiosity Shop,' a novel about a young girl named Nell Trent.",
                    "First ether anesthetic is administered to a patient in the United States.",
                    "The Mines Act of 1842 is passed in the UK, prohibiting women and boys under 10 from working in mines."
                ],
                1843: [
                    "The Great Migration of the Mormon pioneers to Utah begins.",
                    "Charles Dickens publishes 'A Christmas Carol,' a novella emphasizing the spirit of giving.",
                    "The first minstrel show in the United States takes place in New York City.",
                    "The disputed border between the United States and Canada is established by the Treaty of Washington."
                ],
                1844: [
                    "The first telegraph message, 'What hath God wrought?' is sent by Samuel Morse.",
                    "Karl Marx and Friedrich Engels publish 'The Communist Manifesto.'",
                    "The Dominican Republic gains independence from Haiti.",
                    "The Young Men's Christian Association (YMCA) is founded in London."
                ],
                1845: [
                    "Texas is admitted as the 28th state of the United States.",
                    "Edgar Allan Poe publishes 'The Raven,' one of his most famous poems.",
                    "The Irish Potato Famine begins, leading to mass emigration and suffering.",
                    "U.S. President James K. Polk initiates the annexation of Oregon Territory."
                ],
                1846: [
                    "The United States declares war on Mexico, leading to the Mexican-American War.",
                    "Iowa becomes the 29th state of the United States.",
                    "The Smithsonian Institution is established in Washington, D.C.",
                    "The sewing machine is patented by Elias Howe, revolutionizing textile production."
                ],
                1847: [
                    "The Treaty of Cahuenga ends the Mexican-American War in California.",
                    "Charlotte Brontë's novel 'Jane Eyre' is published.",
                    "Phineas Gage survives a severe brain injury, contributing to neuroscience research.",
                    "American inventor Samuel Colt receives a U.S. patent for his revolver design."
                ],
                1848: [
                    "The Treaty of Guadalupe Hidalgo ends the Mexican-American War, ceding vast territories to the United States.",
                    "Gold is discovered at Sutter's Mill in California, sparking the California Gold Rush.",
                    "Karl Marx and Friedrich Engels publish 'The Communist Manifesto' in book form.",
                    "The first women's rights convention is held in Seneca Falls, New York."
                ],
                1849: [
                    "The California Gold Rush draws hundreds of thousands of prospectors to the western United States.",
                    "Harriet Tubman escapes from slavery and begins her work as a conductor on the Underground Railroad.",
                    "Robert Browning's poem 'The Pied Piper of Hamelin' is published.",
                    "The U.S. Congress passes the Oregon Trail Act, encouraging westward migration."
                ],
                1850: [
                    "California becomes the 31st state of the United States during the Gold Rush era.",
                    "The novel 'The Scarlet Letter' by Nathaniel Hawthorne is published.",
                    "The U.S. Congress passes the Fugitive Slave Act, intensifying tensions over slavery.",
                    "China's Taiping Rebellion begins, leading to one of the deadliest conflicts in history."
                ],
                1851: [
                    "The Great Exhibition, the first World's Fair, is held in London's Crystal Palace.",
                    "Isaac Singer patents the sewing machine, revolutionizing textile and clothing production.",
                    "Herman Melville publishes 'Moby-Dick,' a classic American novel.",
                    "The first America's Cup yacht race takes place in New York Harbor."
                ],
                1852: [
                    "Harriet Beecher Stowe publishes 'Uncle Tom's Cabin,' a novel highlighting the horrors of slavery.",
                    "Louis Braille, inventor of the Braille system, dies in France.",
                    "Leo Tolstoy enters the University of Kazan, beginning his literary career.",
                    "The Second Anglo-Burmese War ends with the British annexation of Lower Burma."
                ],
                1853: [
                    "Commodore Matthew Perry of the United States arrives in Japan, opening diplomatic relations.",
                    "The Crimean War begins, involving Russia, the Ottoman Empire, France, and Britain.",
                    "The Taiping Heavenly Kingdom captures Nanjing, making it their capital.",
                    "The first edition of 'Crimean War Notes' by Florence Nightingale is published."
                ],
                1854: [
                    "The United States acquires the Gadsden Purchase, establishing the current U.S.-Mexico border.",
                    "The Republican Party is founded in the United States as an anti-slavery political party.",
                    "Henry David Thoreau's essay 'Walden' is published.",
                    "Alfred Lord Tennyson's poem 'The Charge of the Light Brigade' is published."
                ],
                1855: [
                    "The Great Barrier Reef in Australia is discovered by Europeans.",
                    "Leo Tolstoy begins writing 'War and Peace,' his epic novel of Russian society during the Napoleonic era.",
                    "Charlotte Brontë's novel 'The Professor' is published.",
                    "Nebraska Territory is established in the United States, intensifying the slavery debate."
                ],
                1856: [
                    "Violent conflicts between pro-slavery and anti-slavery forces in Kansas become known as 'Bleeding Kansas.'",
                    "The Second Opium War begins as British and French forces attack China.",
                    "Nikola Tesla, inventor and engineer, is born in Croatia (then part of the Austrian Empire).",
                    "The Battle of Osawatomie in Kansas is a significant clash during Bleeding Kansas."
                ],
                1857: [
                    "The Indian Rebellion of 1857, also known as the Sepoy Mutiny, begins against British rule.",
                    "Gustave Flaubert's novel 'Madame Bovary' is published.",
                    "The Dred Scott v. Sandford Supreme Court decision in the United States upholds slavery.",
                    "The Panic of 1857 triggers a financial crisis in the United States."
                ],
                1858: [
                    "Charles Darwin publishes 'On the Origin of Species,' introducing the theory of evolution.",
                    "The first transatlantic telegraph cable is successfully laid, connecting Europe and North America.",
                    "Minnesota becomes the 32nd state of the United States.",
                    "The Fraser Canyon Gold Rush begins in British Columbia, Canada."
                ],
                1859: [
                    "John Brown's raid on Harpers Ferry, an attempt to start a slave rebellion, takes place in Virginia.",
                    "Charles Dickens' novel 'A Tale of Two Cities' is published.",
                    "The Suez Canal Company is formed to oversee the construction of the Suez Canal.",
                    "The publication of 'Origin of Species' by Charles Darwin leads to debates over evolution."
                ],
                1860: [
                    "Abraham Lincoln is elected as the 16th President of the United States, leading to tensions over slavery.",
                    "The Pony Express, a fast mail delivery service, begins operations between Missouri and California.",
                    "The First Italian War of Independence begins as Italian states seek unification.",
                    "The construction of the Brooklyn Bridge begins, eventually becoming an iconic New York City landmark."
                ],
                1861: [
                    "The American Civil War officially begins with the Confederate attack on Fort Sumter in South Carolina.",
                    "Queen Victoria issues the proclamation recognizing Canada as a self-governing dominion within the British Empire.",
                    "Leo Tolstoy publishes 'War and Peace,' a classic of Russian literature.",
                    "The first successful use of a machine gun in battle takes place during the American Civil War."
                ],
                1862: [
                    "The Emancipation Proclamation is issued by President Abraham Lincoln, declaring the freedom of enslaved people in Confederate-held territories.",
                    "The First Battle of Bull Run (First Manassas) becomes the first major battle of the American Civil War.",
                    "Victor Hugo publishes 'Les Misérables,' a widely acclaimed French novel.",
                    "The Central Pacific Railroad Company is chartered, eventually playing a key role in the First Transcontinental Railroad."
                ],
                1863: [
                    "The Battle of Gettysburg, a pivotal engagement of the American Civil War, takes place.",
                    "The U.S. Congress enacts the draft, leading to the New York City draft riots.",
                    "The International Committee of the Red Cross is founded, setting the stage for humanitarian aid worldwide.",
                    "Abraham Lincoln delivers the Gettysburg Address, emphasizing the principles of liberty and equality."
                ],
                1864: [
                    "The First Geneva Convention is adopted, establishing rules for the treatment of wounded soldiers in armed conflicts.",
                    "The U.S. Congress passes the National Banking Act, creating a system of national banks.",
                    "The novel 'Crime and Punishment' by Fyodor Dostoevsky is published in Russia.",
                    "The Red Cross is established to provide humanitarian aid during the American Civil War."
                ],
                1865: [
                    "The American Civil War ends with the surrender of General Robert E. Lee to General Ulysses S. Grant at Appomattox Court House.",
                    "Abraham Lincoln is assassinated by John Wilkes Booth, leading to Andrew Johnson becoming President of the United States.",
                    "The Thirteenth Amendment to the U.S. Constitution is ratified, abolishing slavery.",
                    "The International Telegraph Union is founded, promoting global communication networks."
                ],
                1866: [
                    "The Atlantic Cable is successfully laid, enabling telegraphic communication between North America and Europe.",
                    "The Red Stockings, a Cincinnati baseball team, become the first professional baseball team.",
                    "The Austrian Empire faces political unrest, leading to the Austro-Hungarian Compromise of 1867.",
                    "The first recorded automobile accident occurs in New York City."
                ],
                1867: [
                    "Canada becomes a self-governing dominion within the British Empire through the British North America Act.",
                    "Alfred Nobel patents dynamite, revolutionizing explosives and construction.",
                    "The Meiji Restoration in Japan leads to significant political and social reforms.",
                    "The United States purchases Alaska from Russia in the Alaska Purchase."
                ],
                1868: [
                    "The Meiji Restoration in Japan officially marks the end of the Tokugawa shogunate and the return of imperial rule.",
                    "The Fourteenth Amendment to the U.S. Constitution is ratified, granting equal protection under the law to all citizens.",
                    "The Great Train Robbery, one of the earliest silent films, is released.",
                    "Louisa May Alcott publishes 'Little Women,' a beloved American novel."
                ],
                1869: [
                    "The First Transcontinental Railroad in the United States is completed, connecting the east and west coasts.",
                    "The Suez Canal, a major engineering feat, is opened in Egypt, providing a shortcut for maritime trade.",
                    "The Periodic Table of Elements, developed by Dmitri Mendeleev, is published, revolutionizing chemistry.",
                    "John Wesley Powell leads the first successful expedition through the Grand Canyon."
                ],
                1870: [
                    "The Franco-Prussian War begins, leading to significant political and territorial changes in Europe.",
                    "John D. Rockefeller founds Standard Oil Company, becoming a major player in the American oil industry.",
                    "The first use of a weather map in a newspaper occurs in 'The Times' of London, marking a milestone in meteorology.",
                    "The population of the United States surpasses 38 million as the nation continues to grow.",
                    "Charles Dickens, the famous English novelist, passes away, leaving a lasting literary legacy.",
                    "The construction of the Brooklyn Bridge begins, eventually becoming an iconic New York City landmark."
                ],
                1871: [
                    "The Great Chicago Fire devastates the city, leading to widespread destruction and rebuilding efforts.",
                    "The German Empire is officially proclaimed, with Otto von Bismarck as its first chancellor.",
                    "Amadeo I becomes the king of Spain, marking a period of political transition in the country.",
                    "The National Rifle Association (NRA) is founded in the United States, promoting firearm safety and marksmanship.",
                    "Henry Stanley sets out to find missing explorer David Livingstone, resulting in their famous meeting in Africa.",
                    "The first performance of Gilbert and Sullivan's comic opera 'Thespis' takes place in London."
                ],
                1872: [
                    "The first national park in the world, Yellowstone National Park, is established in the United States.",
                    "The world's first international soccer match takes place between England and Scotland.",
                    "Susan B. Anthony is arrested for voting in a U.S. election, becoming a prominent figure in the suffrage movement.",
                    "The first U.S. national labor union, the National Labor Union, holds its last convention.",
                    "Ilya Mechnikov, a pioneer in immunology, discovers phagocytes, advancing our understanding of the immune system.",
                    "The first official football (soccer) match in Argentina is played, marking the beginning of football in the country."
                ],
                1873: [
                    "The Panic of 1873, a global financial crisis, begins in the United States and leads to economic hardships.",
                    "The Comstock Lode, one of the richest silver mines in the United States, is discovered in Nevada.",
                    "Levi Strauss and Jacob Davis receive a patent for blue jeans with copper rivets, laying the foundation for denim fashion.",
                    "The Women's Christian Temperance Union (WCTU) is founded, advocating for temperance and women's suffrage.",
                    "P. T. Barnum's 'Greatest Show on Earth' circus debuts, becoming a popular form of entertainment.",
                    "The world's first cable car begins operating in San Francisco, revolutionizing urban transportation."
                ],
                1874: [
                    "The Remington No. 1, the first commercially successful typewriter, is introduced by E. Remington and Sons.",
                    "Winston Churchill is born, eventually becoming a prominent British statesman and leader during World War II.",
                    "The first recorded ascent of Mount St. Helens in the United States takes place.",
                    "The Impressionist Exhibition in Paris showcases the works of emerging artists like Monet, Renoir, and Degas.",
                    "The first officially recognized women's tennis tournament is held at the All England Croquet Club.",
                    "The U.S. Weather Bureau is established, providing improved weather forecasting and data collection."
                ],
                1875: [
                    "The Civil Rights Act of 1875 is enacted in the United States, prohibiting racial discrimination in public accommodations.",
                    "The Cape Town-Port Elizabeth railway, the first railway line in South Africa, is opened.",
                    "Composer Richard Wagner's 'Parsifal' premieres in Bayreuth, Germany.",
                    "The first Kentucky Derby horse race is held in Louisville, Kentucky.",
                    "The invention of the electric dental drill by George Green revolutionizes dentistry.",
                    "Mathematician and logician Georg Cantor introduces set theory, impacting the foundations of mathematics."
                ],
                1876: [
                    "The Battle of Little Bighorn, also known as Custer's Last Stand, occurs between Native American forces and the U.S. Army.",
                    "The United States celebrates its centennial with the Philadelphia Centennial Exposition, showcasing innovations and inventions.",
                    "Alexander Graham Bell patents the telephone, transforming communication worldwide.",
                    "Colorado becomes the 38th state of the United States.",
                    "Mark Twain publishes 'The Adventures of Tom Sawyer,' a classic of American literature.",
                    "The National League of Professional Baseball Clubs (MLB) is founded, becoming a major baseball organization."
                ],
                1877: [
                    "The Great Railroad Strike of 1877 takes place in the United States, leading to labor unrest and strikes.",
                    "Thomas Edison invents the phonograph, allowing sound to be recorded and reproduced.",
                    "Rutherford B. Hayes is inaugurated as the 19th President of the United States, ending the disputed 1876 election.",
                    "The Wimbledon Championships, one of the world's oldest tennis tournaments, is first held in London.",
                    "Giovanni Schiaparelli observes and maps Mars, introducing the term 'canali' (channels) on the planet.",
                    "The first Wimbledon tennis tournament is held in London, becoming a prestigious event in the sport."
                ],
                1878: [
                    "The Treaty of Berlin is signed, reshaping the political landscape of Eastern Europe after the Russo-Turkish War.",
                    "The first commercial telephone exchange opens in New Haven, Connecticut, enabling long-distance communication.",
                    "The Yellow Fever Epidemic strikes the southern United States, causing widespread illness and fatalities.",
                    "Thomas Edison patents the electric light bulb, revolutionizing indoor lighting.",
                    "The Russo-Turkish War of 1877-1878 ends with the signing of the Treaty of San Stefano.",
                    "Gilbert and Sullivan's comic opera 'H.M.S. Pinafore' premieres in London, becoming a musical sensation."
                ],
                1879: [
                    "Albert Einstein is born in Ulm, Germany, laying the foundation for future breakthroughs in theoretical physics.",
                    "The Anglo-Zulu War begins in Southern Africa, leading to conflicts between British forces and the Zulu Kingdom.",
                    "Frank Woolworth opens the first 'five-and-dime' store in Utica, New York, introducing the concept of fixed-price retailing.",
                    "The Tay Bridge Disaster in Scotland results in a railway bridge collapse, causing a tragic train accident.",
                    "Gottlieb Daimler and Wilhelm Maybach develop the first successful high-speed internal combustion engine.",
                    "Thomas Edison conducts his first successful test of an electric light bulb, paving the way for widespread use."
                ],
                1880: [
                    "The first electric streetlight is installed in Wabash, Indiana, marking an advancement in urban lighting technology.",
                    "Thomas Edison patents the incandescent light bulb, revolutionizing the way people illuminate their homes and workplaces.",
                    "The American Federation of Labor (AFL) is founded, becoming a prominent labor union in the United States.",
                    "The population of the United States surpasses 50 million, reflecting the nation's continued growth.",
                    "The first electric tramway system begins operation in Blackpool, England, ushering in a new era of public transportation.",
                    "Construction of the Eiffel Tower begins in Paris, France, eventually becoming an iconic symbol of the city and engineering achievement."
                ],
                1881: [
                    "The American Red Cross is established by Clara Barton, providing humanitarian aid during disasters and conflicts.",
                    "Gunfight at the O.K. Corral takes place in Tombstone, Arizona, involving legendary figures like Wyatt Earp and Doc Holliday.",
                    "Booker T. Washington founds the Tuskegee Institute, a historically black college, to provide education and vocational training.",
                    "The Federation of Australia is formed, leading to the eventual creation of the Commonwealth of Australia.",
                    "Thomas Edison invents the electric voting machine, aiming to improve the accuracy and efficiency of elections.",
                    "The Natural History Museum opens in London, UK, becoming a hub for scientific research and public education."
                ],
                1882: [
                    "The Chinese Exclusion Act is signed into law in the United States, restricting immigration of Chinese laborers.",
                    "Robert Koch discovers the bacterium responsible for tuberculosis, advancing the field of microbiology.",
                    "The Triple Alliance is formed between Germany, Austria-Hungary, and Italy, shaping European alliances.",
                    "The first electric fan is patented by Schuyler Skaats Wheeler, providing relief in hot climates.",
                    "The world's first electric iron is patented, simplifying household chores and clothing care.",
                    "The Knights of Columbus, a Catholic fraternal organization, is founded in New Haven, Connecticut."
                ],
                1883: [
                    "The eruption of Krakatoa in Indonesia results in one of the most powerful volcanic eruptions in recorded history.",
                    "The Brooklyn Bridge in New York City opens to the public, becoming an iconic landmark and engineering marvel.",
                    "Time zones are introduced by Sir Sandford Fleming at the International Meridian Conference, leading to standardized timekeeping.",
                    "The Orient Express, a famous luxury train service, begins operations, connecting Paris to Istanbul.",
                    "The first vaudeville theater opens in Boston, Massachusetts, paving the way for popular entertainment.",
                    "The Metropolitan Opera House opens in New York City, becoming a renowned venue for opera performances."
                ],
                1884: [
                    "The International Meridian Conference establishes the Greenwich Meridian as the prime meridian, standardizing global timekeeping.",
                    "The cornerstone of the Statue of Liberty is laid on Bedloe's Island in New York Harbor, a gift from France to the United States.",
                    "The Fabian Society is founded in London, advocating for socialism and social reform.",
                    "Dow Jones & Company publishes its first stock average, leading to the creation of the Dow Jones Industrial Average.",
                    "The Oxford English Dictionary project begins, aiming to comprehensively document the English language's vocabulary and usage.",
                    "The first known photograph of a tornado is taken in South Dakota, contributing to meteorological research."
                ],
                1885: [
                    "The Indian National Congress is founded, playing a pivotal role in the struggle for Indian independence.",
                    "The Statue of Liberty arrives in New York City from France, awaiting assembly on Liberty Island.",
                    "The first successful appendectomy is performed by Dr. William W. Grant, advancing surgical practices.",
                    "The Congo Free State is established under the personal rule of King Leopold II of Belgium, leading to colonial exploitation.",
                    "The first motorcycle is patented by Gottlieb Daimler, paving the way for motorized transportation.",
                    "The Indian National Congress holds its first session in Bombay, marking a significant moment in the Indian independence movement."
                ],
                1886: [
                    "The Haymarket affair in Chicago leads to labor protests and violence, highlighting workers' demands for better conditions.",
                    "The Statue of Liberty is dedicated on Liberty Island, symbolizing freedom and democracy.",
                    "The Coca-Cola Company is founded in Atlanta, Georgia, introducing the iconic soft drink to the world.",
                    "The Apache warrior Geronimo surrenders to U.S. authorities, marking a significant event in Native American history.",
                    "Karl Benz patents the first successful gasoline-powered car, revolutionizing personal transportation.",
                    "The Folies Bergère music hall opens in Paris, becoming famous for its entertainment shows and cabaret performances."
                ],
                1887: [
                    "The Dawes Act is passed in the United States, aiming to assimilate Native American tribes and distribute reservation lands to individuals.",
                    "Construction of the Eiffel Tower is completed in Paris, becoming the tallest man-made structure in the world at the time.",
                    "The publication of Arthur Conan Doyle's novel 'A Study in Scarlet' introduces the character Sherlock Holmes to the literary world.",
                    "Helen Keller meets her teacher, Anne Sullivan, marking the beginning of her education and remarkable life story.",
                    "The American Protective Association, a nativist organization, is founded in the United States.",
                    "The University of London grants degrees to women for the first time, contributing to the advancement of women's education."
                ],
                1888: [
                    "The National Geographic Society is founded in Washington, D.C., promoting geography, exploration, and education.",
                    "Jack the Ripper's infamous series of murders occurs in London's Whitechapel district, creating a lasting mystery.",
                    "The Great Blizzard of 1888 strikes the northeastern United States, causing widespread disruption and snow accumulation.",
                    "The invention of the drinking straw by Marvin C. Stone revolutionizes beverage consumption.",
                    "Bertha Benz embarks on the first long-distance automobile journey, demonstrating the feasibility of automobiles for travel.",
                    "The Rio de Janeiro Botanical Garden in Brazil is established, showcasing diverse plant species and research."
                ],
                1889: [
                    "The Eiffel Tower officially opens to the public during the Exposition Universelle (World's Fair) in Paris, becoming a global symbol of engineering and design.",
                    "North Dakota and South Dakota become the 39th and 40th states of the United States, respectively.",
                    "The first successful commercial automobile, the Flocken Elektrowagen, is built in Germany.",
                    "Jane Addams and Ellen Gates Starr co-found Hull House in Chicago, one of the first settlement houses in the United States.",
                    "The Oklahoma Land Run opens up unassigned lands for settlement, leading to the founding of Oklahoma City.",
                    "Vincent van Gogh paints 'Starry Night,' a masterpiece of post-impressionist art."
                ],
            1890: [
                "The first entirely steel-framed building is erected in Chicago, a pivotal moment in architecture.",
                "London introduces the world's first electric tube railway, transforming urban transportation.",
                "Tragedy strikes as the British cruiser Serpent is wrecked off the Spanish coast during a fierce storm, resulting in the loss of 167 lives.",
                "Sitting Bull, a prominent figure in the Sioux uprising, meets his demise.",
                "The delightful ice-cream sundae makes its debut as a sweet treat.",
                "The United States boasts a resident population of 62.9 million, reflecting its continued growth.",
                "Thomas Edison patents the motion picture camera, laying the foundation for the film industry."
            ],
            1891: [
                "Japan endures a catastrophic earthquake that levels 20,000 structures and claims the lives of 25,000 people.",
                "A groundbreaking moment arrives with the creation of the first practical hydroelectric station, ushering in a new era of energy production.",
                "England embraces the electric torch, a technological advancement with far-reaching implications.",
                "Whitcomb Judson invents the zipper, a convenient fastening device with various applications."
            ],
            1892: [
                "Oil City, Pennsylvania, descends into chaos as fires and floods lead to a harrowing ordeal, resulting in 130 casualties.",
                "A crucial breakthrough occurs with the development of a cholera vaccine, a significant stride in public health.",
                "The completion of the Cape-Johannesburg railroad connects distant regions, facilitating transportation and trade.",
                "Innovation takes the form of the crown top for bottles and the patenting of the Diesel engine.",
                "The first automatic escalator is patented by Jesse W. Reno, revolutionizing vertical transportation."
            ],
            1893: [
                "Hurricane-driven floods wreak havoc along the U.S. South Atlantic coast, causing a staggering loss of 2000 lives.",
                "Chicago hosts the World Exposition, showcasing human achievement and innovation on a global scale.",
                "A major leap in photography occurs with the invention of practical roll film.",
                "Breakfast tables are forever changed with the creation of shredded wheat cereal.",
                "Rudolf Diesel develops the concept of the diesel engine, paving the way for efficient and powerful engines."
            ],
            1894: [
                "Tensions escalate into war between China and Japan, marking a turning point in East Asian history.",
                "A devastating forest fire in Minnesota claims the lives of 480 people, leaving a lasting impact on the region.",
                "Captain Dreyfus is exiled to Devil’s Island amid a controversial and politically charged case.",
                "The world witnesses the birth of wireless communication, a technology that would shape the future.",
                "The first kinetoscope parlor opens in New York City, offering a glimpse into the world of moving pictures."
            ],
            1895: [
                "Wilhelm Conrad Roentgen makes a groundbreaking discovery with the identification of X-rays, revolutionizing medicine and imaging.",
                "The cigarette-making machine is invented, streamlining the production of a popular consumer product.",
                "The Lumieres introduce their Cinematographie, a precursor to modern cinema, setting the stage for a new era of entertainment.",
                "Alfred Nobel establishes the Nobel Prize, recognizing outstanding contributions to humanity in various fields."
            ],
            1896: [
                "The Klondike gold rush commences, sparking a frenzied search for precious metals in the icy wilderness of Canada.",
                "Addressograph patents are officially granted, revolutionizing the field of data processing and record-keeping.",
                "Henry Ford unveils his first motorcar, laying the foundation for the modern automobile industry.",
                "Innovative periscopes for submarines are invented, enhancing the stealth and capabilities of underwater vessels.",
                "The inaugural modern Olympic Games are hosted in Athens, Greece, celebrating athleticism and international unity.",
                "Wilhelm Röntgen discovers the X-ray, revolutionizing medical diagnostics and imaging technology.",
                "Marconi sends the first wireless telegraph transmission across the English Channel, marking a major advancement in wireless communication."
            ],
            1897: [
                "The invention of mimeo stencils revolutionizes duplicating documents and publications.",
                "Scientist Karl Ferdinand Braun introduces the world's first cathode ray tube (CRT), a milestone in the development of electronic displays.",
                "Aspirin is synthesized for the first time, leading to the widespread use of this pain-relief medication."
            ],
            1898: [
                "A devastating tropical cyclone strikes the southern United States, causing widespread destruction and claiming hundreds of lives.",
                "The Spanish-American War unfolds, resulting in the loss of 2446 U.S. soldiers and marking a turning point in American foreign policy.",
                "The practicality of disc recordings is realized, revolutionizing the music industry and audio technology.",
                "Commercial aspirin makes its debut, providing a widely accessible remedy for pain and fever.",
                "Kellogg’s Corn Flakes are introduced as a wholesome breakfast option, becoming a household staple.",
                "The tubular flashlight is invented, illuminating the way for portable and reliable light sources.",
                "Emile Zola publishes his famous open letter \"J'Accuse!\" in defense of Captain Alfred Dreyfus, igniting a national debate in France."
            ],
            1899: [
                "The Windsor Hotel in New York City is engulfed in flames, causing millions in damages and tragically claiming 14 lives.",
                "Ernest Rutherford makes groundbreaking discoveries about alpha and beta particles, advancing our understanding of atomic structure.",
                "The general adoption of typewriters accelerates, transforming written communication and office work.",
                "The Wright brothers, Orville and Wilbur, start experimenting with their first powered aircraft, paving the way for the age of aviation."
            ],
            1900: [
                "The tragic wreck of the steamship Rio de Janeiro pierces the heart of San Francisco harbor, resulting in the loss of 128 lives.",
                "The devastating Galveston hurricane strikes, leaving a trail of destruction and claiming the lives of 6,000 people.",
                "A mine explosion in Utah leads to the tragic loss of 200 lives, highlighting the dangers faced by miners.",
                "The Boxer Rebellion erupts in China, marking a violent struggle against foreign influence and imperialism.",
                "Eastman Kodak introduces the revolutionary “Brownie” camera, making photography accessible to the masses.",
                "Count Ferdinand von Zeppelin launches his 420-foot airship, pioneering the era of modern air travel.",
                "The U.S. public debt stands at $1.263 billion, reflecting economic and financial trends of the time.",
                "Sigmund Freud publishes \"The Interpretation of Dreams,\" laying the foundation for modern psychoanalysis."
            ],
            1901: [
                "The assassination of President William McKinley sends shockwaves through the nation.",
                "Two significant typhoid outbreaks strike the United States, raising concerns about public health.",
                "The passing of Queen Victoria marks the end of an era in British history.",
                "Advancements in medicine occur with the classification of human blood groups.",
                "Guglielmo Marconi achieves a groundbreaking milestone by successfully establishing the first transatlantic wireless communication link.",
                "The inaugural Nobel Prizes are awarded, recognizing outstanding contributions to humanity in various fields."
            ],
            1902: [
                "The Boer War continues to shape the geopolitical landscape in South Africa.",
                "The catastrophic eruption of Mt. Pelée on Martinique claims the lives of 40,000 people in a devastating natural disaster.",
                "The launch of the first steam-turbine-driven passenger ship revolutionizes maritime transportation.",
                "The development of modern macadam improves road construction techniques, benefiting infrastructure worldwide.",
                "Alum-dried powdered milk is introduced, revolutionizing food preservation and accessibility.",
                "Puffed cereals make their debut in the breakfast market, offering a novel and convenient choice for consumers.",
                "The iconic Teddy bear is born, becoming a beloved childhood toy.",
                "Enrico Caruso, the legendary tenor, makes his historic debut in gramophone recordings, sharing his vocal prowess with the world.",
                "The development of economical hydrogenated fats makes fats readily available for soap and cooking, impacting daily life."
            ],
            1903: [
                "A devastating fire at the Iroquois Theatre in Chicago claims the lives of 602 people, marking one of the deadliest theater fires in U.S. history.",
                "The Wright Brothers successfully achieve powered flight with their heavier-than-air aircraft, marking a historic milestone in aviation.",
                "The first fluorescent light is developed, revolutionizing interior lighting and energy efficiency.",
                "The invention of the postal meter streamlines mail processing and postage payment.",
                "The introduction of the center-frame motorcycle engine improves motorcycle design and performance.",
                "Marie Curie becomes the first woman to win a Nobel Prize, receiving the Nobel Prize in Physics for her groundbreaking research on radioactivity."
            ],
            1904: [
                "A tragic train derailment into a flood in Eden, Colorado, results in the loss of 96 lives, highlighting the risks of rail travel.",
                "The Broadway subway opens in New York City, expanding the city's transportation network and facilitating urban growth.",
                "The patenting of the thermos flask revolutionizes the way people keep liquids hot or cold for extended periods.",
                "Farm machinery sees a significant advancement as tracks (as opposed to wheels) are introduced, enhancing agricultural efficiency.",
                "Kapok life belts are introduced, improving water safety for sailors and passengers on ships.",
                "The Russo-Japanese War begins, reshaping the political and territorial landscape in East Asia."
            ],
            1905: [
                "The discovery of the Cullinan diamond, weighing a staggering 3,000 carats, captures the world's attention as the largest diamond find to date.",
                "Steam turbines become the standard propulsion system for the British navy, enhancing the capabilities of naval vessels.",
                "An abortive revolution in Russia hints at the impending political changes that will transform the country.",
                "The invention of the electric motor horn enhances automotive safety and communication on the road.",
                "The creation of the chemical foam fire extinguisher marks a significant advancement in fire suppression technology.",
                "Albert Einstein proposes his Special Theory of Relativity, revolutionizing our fundamental understanding of the universe."
            ],
            1906: [
                "A devastating earthquake and fire strike San Francisco, resulting in the destruction of 28,818 houses and an announced death toll of 700.",
                "U.S. troops occupy Cuba until 1909, shaping the nation's foreign policy and influence in the Caribbean.",
                "The grand ocean liners Lusitania and Mauretania are launched, setting new standards in transatlantic travel.",
                "The jukebox makes its debut, revolutionizing music entertainment in public spaces.",
                "Mass-production of marine outboard motors begins, transforming boating and water transportation.",
                "Albert Einstein introduces his theory of Special Relativity, reshaping our understanding of the universe."
            ],
            1907: [
                "A tragic West Virginian coal mine explosion claims the lives of 361 miners, highlighting the dangers of coal mining.",
                "Rasputin gains significant influence in Czarist Russia, becoming a mysterious and controversial figure in the Russian court.",
                "The world is introduced to animated cartoons, a form of entertainment that will captivate audiences for generations.",
                "The electric washing machine is invented, revolutionizing household chores and laundry practices.",
                "Household detergent is introduced, providing a more effective means of cleaning and laundry care.",
                "The upright vacuum cleaner is created, simplifying home cleaning and maintenance.",
                "The first electric iron is patented, revolutionizing garment care."
            ],
            1908: [
                "Hermann Minkowski formulates his groundbreaking 4-dimensional geometry, advancing the understanding of space and time.",
                "Paper cups for drinking are introduced, offering a convenient and hygienic way to consume beverages.",
                "The Ford Model T, the first mass-produced automobile, hits the market, revolutionizing transportation.",
                "The concept of the \"Boy Scouts\" is introduced, paving the way for the establishment of the Boy Scouts of America."
            ],
            1909: [
                "Explorer Robert E. Peary reaches the North Pole, achieving a historic milestone in polar exploration.",
                "A devastating hurricane strikes Louisiana and Mississippi, claiming the lives of 350 people and causing widespread destruction.",
                "The first powered flight across the English Channel takes place, showcasing the possibilities of aviation.",
                "Double-decker buses are introduced in the United Kingdom, becoming an iconic sight on British streets.",
                "The first neon lights are demonstrated, opening new possibilities in signage and advertising.",
                "The invention of instant coffee revolutionizes coffee consumption, offering a quick and convenient way to enjoy the beverage."
            ],
            1911: [
                "A massive explosion of forty tons of dynamite occurs at the Communipaw terminal in New Jersey, resulting in the tragic loss of 30 lives.",
                "The Triangle Shirtwaist Factory fire in New York City becomes a tragic landmark, leaving 145 people dead and prompting labor reform efforts.",
                "Emiliano Zapata arrives in Mexico City, marking a significant moment in the Mexican Revolution, but the battles continue.",
                "A revolution in China leads to the establishment of a republic under the leadership of Sun Yat-sen.",
                "The electric frying pan is introduced, simplifying and modernizing cooking techniques.",
                "Norwegian explorer Roald Amundsen achieves a historic milestone by reaching the South Pole.",
                "The development of stainless steel revolutionizes industry and manufacturing."
            ],
            1912: [
                "The RMS Titanic collides with an iceberg, resulting in the tragic loss of 1,517 passengers and crew, one of the most infamous maritime disasters in history.",
                "Woodrow Wilson's cloud chamber leads to the detection of protons and electrons, advancing the field of particle physics.",
                "Cellophane, a transparent packaging material, is patented, offering new possibilities for food preservation and presentation.",
                "Savile Row tailors create what will be named the “trench coat,” which becomes an iconic garment during World War I.",
                "Cadillac introduces the first electric self-starter for automobiles, making cars more accessible and user-friendly.",
                "The first self-service grocery stores open in California, revolutionizing the retail industry.",
                "The crossword puzzle is invented, becoming a popular pastime and form of entertainment."
            ],
            1913: [
                "The Balkan War begins, reshaping the geopolitical landscape in Southeastern Europe.",
                "The British steamer Calvados is lost in a blizzard in the Sea of Marmara, resulting in the tragic loss of 200 lives.",
                "Woodrow Wilson is inaugurated as President of the United States, ushering in a new era of American leadership.",
                "Electric starters for motorcycles are introduced, improving motorcycle usability and safety.",
                "Vitamin A is discovered, leading to advancements in nutrition and health.",
                "The U.S. Constitution is amended to include income tax and the popular election of senators, shaping American governance.",
                "Stainless steel cutlery is introduced, offering a durable and rust-resistant alternative to traditional materials."
            ],
            1914: [
                "The Great War (World War I) begins, launching a devastating conflict that reshapes the course of history.",
                "The first air raids occur, marking the beginning of aerial warfare in the Great War.",
                "The Panama Canal is used for the first time, revolutionizing global trade and transportation.",
                "The Canadian Pacific steamship Empress of India is sunk in a collision with the Storstad in the St. Lawrence River, resulting in the tragic loss of 1,024 lives.",
                "The first successful blood transfusion is performed, advancing the field of medicine.",
                "The invention of the traffic signal improves road safety and traffic management in cities.",
                "The brassiere (bra) is patented, revolutionizing women's undergarments and fashion."
            ],
            1915: [
                "The sinking of the Lusitania by a German submarine results in the tragic loss of 1,199 lives and sparks consternation and anger in the United States.",
                "The Great War witnesses enormous and unprecedented casualties, reshaping the global political landscape.",
                "Cereal flakes are marketed as a convenient and nutritious breakfast option, changing morning routines.",
                "Chlorine gas is used as a weapon in the Great War, introducing a new and deadly form of warfare.",
                "The gas mask is invented, providing protection for soldiers against chemical weapons.",
                "The zipper is patented, revolutionizing clothing fasteners and becoming a staple in fashion and industry.",
                "Einstein's theory of General Relativity is published, furthering our understanding of gravity and the universe."
            ],
            1916: [
                "The Battle of Verdun claims the lives of some 700,000 soldiers, becoming one of the deadliest battles of World War I.",
                "One million lives are lost in the Battle of the Somme, marking a harrowing chapter in the Great War.",
                "A polio epidemic in the United States results in 7,000 deaths and leaves 27,000 youngsters paralyzed, highlighting the need for medical advances.",
                "The Gallipoli Campaign is waged, leading to significant casualties and reshaping the course of World War I.",
                "The Easter Uprising takes place in Ireland, marking a pivotal moment in the struggle for Irish independence.",
                "The Battle of Jutland in the North Sea becomes the largest naval battle of World War I.",
                "Mechanical windshield wipers are invented, improving visibility and safety in automobiles.",
                "Albert Einstein proposes his General Theory of Relativity, revolutionizing our understanding of the laws governing the universe.",
                "General John J. Pershing leads a raid into Mexico in pursuit of Pancho Villa, escalating tensions between the U.S. and Mexico."
            ],
            1917: [
                "The United States enters World War I, changing the course of the conflict and becoming a major player in the Allied forces.",
                "The Russian Revolution unfolds, leading to the Bolsheviks seizing power and transforming Russia into a communist state.",
                "Mustard gas is used in warfare for the first time, introducing a new and devastating form of chemical warfare.",
                "Ford begins mass-producing tractors, revolutionizing agriculture and farming practices.",
                "The steamer Castalia is wrecked on Lake Superior, resulting in the loss of 22 lives.",
                "A munitions plant explosion in Pennsylvania kills 133 workers and underscores the dangers of wartime production.",
                "A ship collision and explosion in Halifax, Nova Scotia, result in the tragic loss of 1,600 lives.",
                "The United States establishes its first regular airmail service, advancing aviation and communication.",
                "The development of the first tank prototype in World War I leads to advancements in armored warfare."
            ],
            1918: [
                "World War I comes to an end, bringing an end to one of the most devastating conflicts in history.",
                "The Russian Civil War erupts, leading to a protracted struggle for power and control in post-revolutionary Russia.",
                "Regular U.S. airmail service is established, connecting the nation through air travel.",
                "A world influenza epidemic, known as the Spanish flu, sweeps the globe and claims the lives of 21.6 million people.",
                "The USS Cyclops disappears without a trace after leaving Barbados, becoming one of the greatest mysteries of maritime history.",
                "Powered flight reaches speeds exceeding 150 mph and altitudes exceeding 30,000 feet, pushing the boundaries of aviation.",
                "Electric clocks are introduced, becoming a common household timekeeping device."
            ],
            1919: [
                "Prohibition is enacted in the United States, ushering in an era of alcohol prohibition and the rise of bootlegging.",
                "The first transatlantic flight covers 1,880 miles in 16 hours and 12 minutes, marking a historic achievement in aviation.",
                "Grease guns are invented, becoming essential tools in various industries and maintenance work.",
                "Parachutes are introduced, revolutionizing safety measures for aviation and parachuting sports."
            ],
            1920: [
                "Prohibition is in effect in the United States, leading to a significant impact on the alcohol industry and culture.",
                "The Bolsheviks consolidate power in Russia, establishing the Soviet Union and reshaping global politics.",
                "An earthquake in Gansu province, China, claims the lives of 200,000 people, highlighting the vulnerability of populated regions to natural disasters.",
                "The first radio broadcasting station goes on the air, revolutionizing mass communication and entertainment.",
                "Teabags are introduced as a convenient and mess-free way to prepare tea, changing tea consumption habits.",
                "The U.S. public debt stands at $24.3 billion, reflecting the economic and financial challenges of the era.",
                "Women's suffrage is ratified in the United States, granting women the right to vote and marking a milestone in the fight for gender equality.",
                "The United States boasts a resident population of 105.7 million, reflecting the nation's continued growth and development."
            ],
            1921: [
                "Hermann Rorschach devises his inkblot tests, pioneering a psychological assessment method.",
                "Inflation of the German Mark begins, leading to economic turmoil and hyperinflation in Germany.",
                "KDKA in Pittsburgh broadcasts sports events, marking a significant milestone in radio broadcasting.",
                "Karel Čapek coins the word “robot” in his play \"R.U.R.\", introducing the concept of artificial beings."
            ],
            1922: [
                "The Ku Klux Klan experiences a revival and growth in the United States, sparking concerns about racial violence and discrimination.",
                "The British dirigible AR-2 breaks in two, resulting in the tragic loss of 62 lives and raising safety concerns in air travel.",
                "Insulin is isolated, revolutionizing the treatment of diabetes and saving countless lives.",
                "The first practical postal franking machine is introduced, streamlining mail processing and postage payment.",
                "Soviet May Day slogans omit “world revolution,” reflecting shifts in Soviet foreign policy.",
                "Water-skiing is invented, creating a popular water sport and recreational activity.",
                "Benito Mussolini and his supporters march on Rome, leading to his appointment as Prime Minister of Italy."
            ],
            1923: [
                "The Teapot Dome scandal rocks the administration of President Warren G. Harding, revealing corruption in government oil leases.",
                "A big fire in Berkeley, California, destroys 600 buildings, causes $10 million in damage, and results in 60 deaths.",
                "The German Mark is stabilized, bringing economic relief to Germany after a period of hyperinflation.",
                "Continuing Ku Klux Klan violence is reported in Georgia, prompting concerns about civil rights and racial tensions.",
                "The Nazi putsch in Munich fails, marking an early attempt by Adolf Hitler to seize power.",
                "The tomb of King Tutankhamun (King Tut) is opened, unveiling treasures and insights into ancient Egypt.",
                "A vaccine for whooping cough is developed, improving child health and reducing mortality rates."
            ],
            1924: [
                "Leopold and Loeb are convicted of the kidnap and slaying of Bobby Franks in a sensational trial.",
                "Paper egg cartons are developed, providing a more convenient and sanitary way to package eggs.",
                "Kleenex facial tissues are introduced, becoming a household staple for personal hygiene."
            ],
            1925: [
                "Wolfgang Pauli formulates the Exclusion Principle, a fundamental concept in quantum mechanics.",
                "I.G. Farben, a major chemical conglomerate, is formed, playing a significant role in the chemical industry.",
                "Sun Yat-sen, a key figure in Chinese history, dies, leading to political changes in China.",
                "In the Midwest, 792 people die in a single day from tornadoes, highlighting the destructive power of natural disasters.",
                "The U.S. dirigible Shenandoah breaks apart in mid-air, resulting in the tragic loss of 14 lives and raising safety concerns in airship travel.",
                "The German SS (Schutzstaffel) is formed, becoming a key organization in Nazi Germany.",
                "The Scopes “Monkey Trial” takes place, testing the teaching of evolution in American schools and sparking a national debate.",
                "Aerial commercial crop-dusting is introduced, improving agricultural efficiency."
            ],
            1926: [
                "Dr. Robert H. Goddard fires his first liquid-fuel rocket, laying the foundation for modern rocketry and space exploration.",
                "Lightning starts a massive explosion at the U.S. Naval ammunition dump in Lake Denmark, New Jersey, causing $85 million in damages and resulting in 30 deaths.",
                "A hurricane sweeps through Florida and Alabama, leaving 243 people dead and causing extensive destruction.",
                "Chiang Kai-Shek stages a coup in Canton, marking a significant development in Chinese politics.",
                "Leon Trotsky is expelled from the Politburo, leading to political shifts within the Soviet Union.",
                "Rolex introduces a waterproof watch, setting a new standard for timepieces."
            ],
            1927: [
                "Charles A. Lindbergh achieves fame by flying solo and non-stop between New York City and Paris, becoming a pioneering aviator.",
                "The Jazz Singer becomes the first feature-length sound film, ushering in the era of \"talkies\" in the motion picture industry.",
                "The first remote jukebox is introduced, transforming the way people enjoy music in public spaces.",
                "The pop-up toaster is introduced, simplifying and modernizing breakfast preparation.",
                "Nicola Sacco and Bartolomeo Vanzetti are executed, later cleared of charges by proclamation in 1977, sparking debate and protests."
            ],
            1928: [
                "Television experiments pave the way for the development of television as a medium for entertainment and communication.",
                "A devastating hurricane strikes southern Florida, resulting in the tragic loss of 1,836 lives and significant damage.",
                "Admiral Richard E. Byrd leads an expedition to Antarctica, advancing exploration of the continent.",
                "Teletypes come into use, improving telecommunication and printing technology.",
                "Waterproof cellophane is developed, offering new possibilities for packaging and preserving products.",
                "The Geiger counter is introduced, revolutionizing the detection of ionizing radiation.",
                "Vitamin C is discovered, leading to insights into nutrition and health."
            ],
            1929: [
                "The Great Stock Market Crash occurs on October 24, leading to the Wall Street Crash of 1929 and the onset of the Great Depression.",
                "The Graf Zeppelin completes a historic circumnavigation of the world, demonstrating the potential of airship travel.",
                "The Russian passenger steamer Volga is struck by a remnant World War I mine in the Black Sea, resulting in the loss of 31 lives.",
                "16mm color film is developed, enhancing the visual quality of motion pictures.",
                "Scotch tape is introduced, becoming a versatile adhesive tape for various applications.",
                "The tune-playing automobile horn is invented, adding musicality to car horns."
            ],
            1930: [
                "The Technocracy movement reaches its peak, advocating for the application of scientific principles to social and economic governance.",
                "The flash bulb ends flash powder explosions at press conferences and photography, improving safety and convenience.",
                "The first frozen foods are marketed, transforming food preservation and convenience for consumers.",
                "The bathysphere is invented, enabling deep-sea exploration and research.",
                "The cyclotron, a particle accelerator, is invented, advancing the field of nuclear physics.",
                "Pluto is discovered, expanding our understanding of the solar system.",
                "The telescopic umbrella is introduced, offering enhanced protection from rain and sun.",
                "The U.S. public debt reaches $16.18 billion, reflecting the economic challenges of the era.",
                "The U.S. resident population grows to 122.8 million, indicating continued demographic growth."
            ],
            1931: [
                "German millionaire support builds for the Nazi Party, contributing to the rise of Adolf Hitler.",
                "A mutiny occurs in the British Navy at Invergordon, highlighting labor disputes and unrest within the military.",
                "The Empire State Building formally opens, becoming an iconic symbol of New York City.",
                "Al Capone is imprisoned, marking a significant moment in the prosecution of organized crime figures.",
                "Alka-Seltzer is introduced as an antacid and pain reliever.",
                "The electric razor is introduced, offering a more convenient and efficient shaving experience.",
                "The George Washington Bridge, spanning 3,500 feet, is completed, becoming a vital transportation link."
            ],
            1932: [
                "Mahatma Gandhi is arrested in India as part of his civil disobedience campaign for independence.",
                "A British submarine sinks in the English Channel, raising questions about naval safety.",
                "Franklin D. Roosevelt is elected President of the United States in a landslide victory, bringing hope during the Great Depression.",
                "Benito Mussolini initiates the draining of the Pontine Marshes in Italy, addressing a long-standing environmental issue.",
                "The Lindbergh baby is kidnapped, leading to a high-profile investigation and public fascination.",
                "The first car radios are introduced, changing the way people enjoy music and news while driving.",
                "The first Gallup Poll is conducted, revolutionizing public opinion research and polling.",
                "Mars Bars are introduced as a popular candy bar.",
                "The invention of the zoom lens enhances photography and filmmaking.",
                "The Zippo lighter is introduced, becoming a classic and iconic product."
            ],
            1933: [
                "Adolf Hitler is named Chancellor of Germany, marking a turning point in German politics and history.",
                "Japan withdraws from the League of Nations, signaling increasing militarism and expansionist ambitions.",
                "The United States abandons the gold standard, a major economic policy shift during the Great Depression.",
                "The Long Beach earthquake kills 123 people and causes significant damage in California.",
                "Hundreds of lives are lost in a Cuban rebellion against the government of Gerardo Machado.",
                "Freed from imprisonment, Mahatma Gandhi weighs 90 pounds due to his hunger strikes and dedication to nonviolent resistance.",
                "The first German concentration camp, Dachau, is established, marking a grim chapter in history.",
                "Day-Glo pigments are introduced, leading to the creation of vibrant and fluorescent colors.",
                "The game Monopoly is published, becoming one of the most popular board games worldwide.",
                "Fluorescent lights are introduced commercially, offering energy-efficient lighting options."
            ],
            1934: [
                "The economic depression deepens as starvation and unrest spread in the United States, reflecting the challenges of the Great Depression.",
                "Drought extends from New York State to California, leading to the Dust Bowl and agricultural hardships.",
                "Augusto César Sandino is assassinated by supporters of Anastasio Somoza García, shaping the political landscape in Nicaragua.",
                "A general strike in San Francisco ends, concluding a period of labor unrest and strikes in the city.",
                "Huey Long assumes a dictatorship of Louisiana, implementing populist policies and consolidating power.",
                "The first commercial launderette is established, providing a new approach to laundry services."
            ],
            1935: [
                "Increasingly severe dust storms batter the High Plains and Midwest of the United States, leading to the Dust Bowl era.",
                "The first Pan-Am Clipper departs from San Francisco for China, marking the dawn of transpacific flight.",
                "The Social Security system is enacted in the United States, providing a safety net for retirees and disabled individuals.",
                "Huey Long, the charismatic Louisiana politician, is assassinated, altering the political landscape in the state.",
                "Mao Zedong's Long March concludes in Yenan, a pivotal moment in the Chinese Communist Party's history.",
                "The first passenger flight for the Douglas DC-3 aircraft takes place, revolutionizing air travel.",
                "Mass-market paperback books are introduced, making literature more accessible to the general public.",
                "The Richter earthquake scale is developed, allowing for more accurate measurement of earthquake magnitudes.",
                "The tape recorder is retailed, enabling the recording and playback of audio recordings."
            ],
            1936: [
                "The Nazis enter the Rhineland, a significant violation of the Treaty of Versailles and a precursor to further aggression.",
                "Italy conquers Ethiopia, marking a brutal episode of colonialism in East Africa.",
                "The Spanish Civil War begins, leading to years of conflict and ideological battles in Spain.",
                "A severe U.S. heat wave kills 3,000 people, underscoring the impact of extreme weather events.",
                "Dust-bowl conditions continue to plague the Great Plains, causing ecological and agricultural challenges.",
                "Jesse Owens wins four gold medals at the Berlin Olympics, challenging racial stereotypes and Nazi ideology.",
                "Axis powers, including Germany, Italy, and Japan, sign the Anti-Comintern Pact, signaling closer collaboration.",
                "The Boulder Dam (later known as the Hoover Dam) becomes operational, providing hydroelectric power and water storage.",
                "The first Volkswagen (VW) car is introduced, laying the foundation for a globally recognized automobile brand."
            ],
            1937: [
                "A devastating gas explosion kills 294 people in a Texas school, highlighting the need for safety measures in schools.",
                "The Hindenburg dirigible explodes while attempting to dock in Lakehurst, New Jersey, resulting in the loss of 36 lives.",
                "Eight Soviet generals die in Stalinist purges, reflecting the brutal political climate in the Soviet Union.",
                "DuPont patents nylon, a synthetic material that revolutionizes various industries, including fashion and manufacturing.",
                "Japanese forces sink the U.S. gunboat Panay in the Yangtze River, leading to diplomatic tensions.",
                "The Golden Gate Bridge, spanning 4,200 feet, is completed, becoming an iconic landmark in San Francisco.",
                "The first supermarket shopping carts are introduced, simplifying the grocery shopping experience.",
                "Buchenwald concentration camp opens in Germany, foreshadowing the horrors of the Holocaust."
            ],
            1938: [
                "Mexico expropriates all foreign oil holdings, asserting national control over the country's oil resources.",
                "German forces, unopposed, enter Austria, leading to the Anschluss and the annexation of Austria by Nazi Germany.",
                "Kristallnacht, or the Night of Broken Glass, marks a violent pogrom against Jews and Jewish-owned businesses in Nazi Germany.",
                "An electric steam iron with a thermostat is invented, improving the efficiency and safety of ironing.",
                "Instant coffee is introduced, offering a convenient and quick way to prepare coffee.",
                "Nylon, the synthetic fabric, is introduced to the market, influencing fashion and industry.",
                "The ball-point pen is patented, replacing fountain pens and revolutionizing writing instruments.",
                "A prototype of the photocopy machine is developed, paving the way for modern document reproduction technology.",
                "A major German-American Bund rally takes place at Madison Square Garden, showcasing Nazi sympathizers in the United States.",
                "Arrests of Jews throughout Germany and Austria foreshadow the escalating persecution of Jewish communities."
            ],
            1939: [
                "Germany annexes Czechoslovakia, signaling further aggression and territorial expansion.",
                "Madrid falls to General Francisco Franco's forces, marking a turning point in the Spanish Civil War.",
                "The U.S. submarine Squalus sinks with the loss of 26 crew members, highlighting submarine safety concerns.",
                "The French submarine Phoenix sinks with the loss of 63 lives, raising questions about naval operations.",
                "Two IRA bombs explode in London, reflecting political tensions and violence in Northern Ireland.",
                "Cellophane wrappers for products first appear in stores, offering transparent and protective packaging.",
                "Annexation of the Baltic states by the Soviet Union occurs, reshaping the geopolitical landscape.",
                "Germany invades Poland, leading to the outbreak of World War II, with France and Britain declaring war.",
                "Rockefeller Center opens in New York City, becoming an iconic entertainment and commercial complex.",
                "DDT, an insecticide, is introduced, influencing pest control practices.",
                "A yellow-fever vaccine is developed, advancing public health measures against tropical diseases.",
                "Radar technology is developed and deployed, playing a crucial role in military and aviation applications."
            ],
            1940: [
                "Finland surrenders to Soviet forces, ending the Russo-Finnish War.",
                "Nazi Germany strikes at Denmark and Norway, expanding its territorial control in Europe.",
                "Winston Churchill becomes Prime Minister of the United Kingdom, leading during a critical period of World War II.",
                "Holland and Belgium fall to German forces, marking further Nazi advances in Western Europe.",
                "The Dunkirk evacuation, also known as Operation Dynamo, rescues British and Allied troops from the beaches of Dunkirk, France.",
                "Thousands of lives are lost in the Russo-Finnish War, a conflict between Finland and the Soviet Union.",
                "German blitzkrieg tactics bring Nazi forces to the English Channel, threatening an invasion of Britain.",
                "Bombings in Germany and England result in tens of thousands of casualties and extensive damage.",
                "Franklin D. Roosevelt is elected for a third term as President of the United States, a historic and unprecedented move.",
                "The automatic gearbox for automobiles is introduced, simplifying driving and improving comfort.",
                "Inflatable life vests are introduced, enhancing safety for individuals involved in water activities.",
                "Radar becomes operational and is deployed in Britain, playing a critical role in defense and aviation.",
                "Artificial insemination is developed, contributing to advances in reproductive medicine.",
                "Penicillin is produced in quantity, revolutionizing medicine and antibiotics.",
                "The U.S. public debt reaches $42.97 billion, reflecting the economic challenges of World War II.",
                "The U.S. resident population grows to 131.7 million, indicating continued demographic growth."
            ],
            1941: [
                "The aerial Battle of Britain is joined, as the Royal Air Force defends against German bombing raids.",
                "The Lend-Lease policy is enacted in the United States, providing military aid to Allied nations during World War II.",
                "The U.S. institutes a military draft as it prepares for its involvement in World War II.",
                "Approximately 2,500 people die in the Japanese raid on Pearl Harbor, a major event that leads to U.S. entry into World War II.",
                "The Coconut Grove nightclub fire in Boston kills 491 people, leading to improved safety regulations for public venues.",
                "The Jeep is adopted as a general-purpose military vehicle, becoming an iconic part of military history.",
                "German forces invade the Soviet Union, initiating the Eastern Front of World War II."
            ],
            1942: [
                "Singapore and the Philippines fall to Japanese forces, marking significant losses for the Allies in the Pacific theater of World War II.",
                "A major carrier battle occurs off Midway Island, a pivotal engagement that shifts the balance in the Pacific War.",
                "The German siege of Leningrad continues, leading to a long and brutal siege during World War II.",
                "The Crimea falls to German forces, impacting the Eastern Front of World War II.",
                "The Doolittle raid on Tokyo is carried out by U.S. Army Air Forces, delivering a morale boost to the United States.",
                "The Battle of Stalingrad is joined, becoming one of the deadliest battles in history.",
                "U.S. forces land on Guadalcanal, marking the beginning of the Guadalcanal Campaign in the Pacific War.",
                "Allied forces land in North Africa, initiating the North African Campaign in World War II.",
                "Atomic fission is achieved, a significant step towards the development of atomic weapons.",
                "The Bazooka is introduced, providing anti-tank firepower to infantry units.",
                "Napalm, a highly flammable weapon, is introduced, influencing warfare tactics."
            ],
            1943: [
                "Approximately 190,000 Germans, along with greater numbers of Soviet soldiers and civilians, lose their lives in the Battle of Stalingrad, one of the deadliest battles in history.",
                "German forces surrender at Stalingrad, marking a turning point in World War II's Eastern Front.",
                "The Warsaw Ghetto uprising demonstrates the resistance of Jewish inhabitants against Nazi oppression.",
                "Germany faces defeat in the Battle of Kursk, the largest tank battle in history.",
                "Allied forces land in Sicily, advancing the liberation of Italy from Axis control.",
                "Benito Mussolini is deposed and later reseated by German forces, reflecting the fluid political situation in Italy.",
                "Allied forces invade Italy, contributing to the weakening of Axis control in Southern Europe.",
                "Soviet forces crack the Dnieper River line, pushing back German defenses in Eastern Europe.",
                "The Marshall Islands fall to U.S. forces in the Pacific theater of World War II.",
                "29 individuals lose their lives in Detroit race riots, highlighting racial tensions and social issues.",
                "Ball-point pens gain acceptance as a practical writing instrument, replacing fountain pens for many.",
                "Jacques-Yves Cousteau and Emile Gagnan invent the Aqualung, revolutionizing underwater exploration.",
                "Lysergic acid diethylamide (LSD) is synthesized, leading to its use in psychological research."
            ],
            1944: [
                "Charles de Gaulle becomes the Free-French commander-in-chief, leading the French resistance during World War II.",
                "Massive air raids on Germany continue as Allied forces intensify their strategic bombing campaign.",
                "The Crimea is liberated from German forces, relieving Soviet control of the region.",
                "Allied forces take control of Rome, marking a significant victory in the Italian Campaign.",
                "D-Day landings in Normandy (Operation Overlord) initiate the liberation of Western Europe from Nazi occupation.",
                "The Marianas Islands come under attack as Allied forces continue to advance in the Pacific theater.",
                "Paris falls to Allied forces, marking the liberation of the French capital from Nazi control.",
                "Franklin D. Roosevelt is re-elected for a fourth term as President of the United States, a record-setting achievement.",
                "The mass killings in Nazi concentration camps are revealed to the world, exposing the horrors of the Holocaust.",
                "V-1 and V-2 missiles launched by Germany target London and other Allied cities.",
                "General Douglas MacArthur returns to the Philippines, fulfilling his promise to return after its capture by Japanese forces.",
                "The Battle of the Bulge is fought as German forces launch a surprise offensive in the Ardennes region.",
                "A hurricane kills 46 people along the U.S. East Coast and claims the lives of 344 individuals at sea.",
                "A fire at a Ringling Bros. circus tent in Hartford, Connecticut, kills 168 people and injures many more.",
                "An ammunition explosion at Port Chicago, California, results in the deaths of 322 people and raises safety concerns.",
                "Nerve gas is developed as a chemical weapon, adding to the arsenal of deadly substances in warfare."
            ],
            1945: [
                "Approximately 130,000 people die in the firebombing of Dresden, a devastating aerial attack during World War II.",
                "The nuclear blast at Nagasaki kills approximately 60,000 people, and mass bombings in Japan claim hundreds of thousands more lives.",
                "The total casualties of World War II are estimated at 50 million people, reflecting the staggering human cost of the war.",
                "Europe and Japan require 15 years to achieve significant recovery in the aftermath of World War II.",
                "The U.S. war-related deaths reach a total of 405,399, underscoring the sacrifices made during the conflict.",
                "Auschwitz concentration camp is liberated by Allied forces, exposing the extent of Nazi atrocities.",
                "The Yalta Conference brings together Allied leaders to discuss post-war Europe and the division of Germany.",
                "Iwo Jima falls to U.S. Marines after intense fighting on the island.",
                "The Remagen Bridge is captured by U.S. forces, providing a key crossing of the Rhine River.",
                "President Franklin D. Roosevelt passes away, leading to the succession of Harry S. Truman.",
                "Benito Mussolini is executed by Italian partisans, marking the end of his fascist regime.",
                "Adolf Hitler commits suicide in his bunker in Berlin as Allied forces close in on the German capital.",
                "The full extent of Nazi death camps is revealed to the world, prompting outrage and condemnation.",
                "Berlin falls to Allied forces, effectively ending World War II in Europe.",
                "Winston Churchill resigns as Prime Minister of the United Kingdom, a role he held during much of the war.",
                "The Battle of Okinawa is fought in the Pacific theater, resulting in significant casualties on both sides.",
                "The United Nations is officially formed, providing a platform for international cooperation and diplomacy.",
                "The Potsdam Conference convenes to address post-war issues and the occupation of Germany.",
                "Japan surrenders, officially ending World War II and leading to the occupation of Japan by Allied forces.",
                "Korea is partitioned along the 38th parallel, setting the stage for future conflicts on the Korean Peninsula.",
                "Jackie Robinson breaks the color barrier in Major League Baseball, becoming the first modern African-American player.",
                "The Nuremberg war-crime trials begin, prosecuting Nazi officials for their roles in war crimes and atrocities.",
                "Tupperware, a popular food storage product, is introduced to consumers."
            ],
            1946: [
                "A fire at a Chicago hotel claims the lives of 58 people, highlighting the importance of fire safety measures.",
                "The Electronic Numerical Integrator and Computer (ENIAC), an early computer, is unveiled by the U.S. War Department.",
                "Winston Churchill delivers his Iron Curtain speech, foreshadowing the Cold War division of Europe.",
                "Violence continues in Palestine as tensions persist between Jewish and Arab communities.",
                "Labor strikes occur across the United States, reflecting post-war labor disputes and demands.",
                "The Chinese Civil War is renewed as Nationalist and Communist forces clash in a struggle for control.",
                "Scientific research suggests a link between smoking and lung cancer, leading to increased awareness of health risks.",
                "An uprising occurs in Vietnam as resistance against colonial rule intensifies.",
                "Chester F. Carlson unveils 'xerography,' a pioneering technology that will later become known as photocopying.",
                "Bikini swimsuits are introduced, making a splash in swimwear fashion.",
                "Espresso coffee machines are invented, contributing to the popularity of espresso-based beverages."
            ],
            1947: [
                "The United States abandons attempts to broker a peace in China's ongoing civil war.",
                "Religious strife and communal violence escalate in India following its independence from British colonial rule.",
                "The Marshall Plan, officially known as the European Recovery Program, is advanced to aid European post-war reconstruction.",
                "The last New York streetcar is retired as cities transition to other forms of public transportation.",
                "India and Pakistan gain independence from British rule, marking the end of the British Raj and the beginning of new nations.",
                "The Polaroid Land Camera is introduced, revolutionizing instant photography.",
                "The House Un-American Activities Committee (HUAC) investigates alleged subversive activities in the film industry.",
                "The Cold War climate prompts concerns about communist influence and loyalty in the United States."
            ],
            1948: [
                "Mahatma Gandhi is assassinated by a Hindu nationalist, leading to mourning in India and beyond.",
                "A communist coup takes place in Czechoslovakia, consolidating communist control over the country.",
                "Civil war continues in the Palestine Mandate as tensions between Jewish and Arab populations persist.",
                "The Berlin Airlift begins as Allied forces provide essential supplies to West Berlin during the Soviet blockade.",
                "The State of Israel is officially recognized, but conflict with neighboring states continues.",
                "The 200-inch Hale Telescope at Mount Palomar is completed, becoming a landmark in astronomical observation.",
                "The New York City subway fare doubles to ten cents, affecting daily commuters.",
                "The Kinsey Report on human sexuality is published, shedding light on previously taboo subjects.",
                "Scrabble, the popular word game, is introduced, challenging players' vocabulary and strategy.",
                "The solid-body electric guitar is developed, revolutionizing music and instrument design.",
                "Velcro, a versatile fastening system, is invented, finding numerous practical applications.",
                "The first 33 1/3 long-playing (LP) records are introduced, changing the music industry."
            ],
            1949: [
                "Chinese Communists, led by Mao Zedong, take control of Beijing (Peking), leading to the establishment of the People's Republic of China.",
                "The North Atlantic Treaty Organization (NATO) is organized, forming a military alliance among Western nations during the Cold War.",
                "The Berlin Blockade, a Soviet attempt to isolate West Berlin, concludes without achieving its objectives.",
                "The Federal Republic of Germany (West Germany) is officially established as a separate entity from East Germany.",
                "The Red Scare and anti-communist sentiments continue in the United States during the early years of the Cold War.",
                "The Soviet Union successfully detonates its first nuclear device, entering the nuclear arms race.",
                "Nationalist Chinese forces, led by Chiang Kai-shek, retreat to Taiwan, where they establish a separate government.",
                "Cable television is introduced as a means of delivering television broadcasts to a wider audience.",
                "The development of color television tubes contributes to the eventual introduction of color television.",
                "Key-starting automobile ignitions are introduced, simplifying the process of starting vehicles."
            ],
            1950: [
                "One-piece windshields become a feature of Cadillacs, improving automotive design.",
                "RCA announces the development of color television technology, signaling advancements in television broadcasting.",
                "France appeals for international aid in its struggle against the Viet Minh in Indochina (Vietnam).",
                "Blizzards in the United States result in hundreds of deaths and significant challenges to transportation and infrastructure.",
                "The Korean War begins, leading to the loss of thousands of lives and international conflict.",
                "U.S. forces conduct successful landings at Inchon, Korea, altering the course of the Korean War.",
                "China enters the Korean War on the side of North Korea, escalating the conflict and international tensions.",
                "Tennis player Gussie Moran gains attention by sporting lace underwear at Wimbledon, sparking controversy.",
                "The Diners' Club card is introduced, pioneering the concept of a credit card for dining and entertainment expenses.",
                "The Xerox 914, a commercial photocopier, is introduced, revolutionizing document reproduction.",
                "The U.S. public debt reaches $256 billion, reflecting post-war economic challenges and government spending.",
                "The U.S. resident population grows to 150.7 million, indicating demographic growth in the post-war era."
            ],
            1951: [
                "General Douglas MacArthur is stripped of all commands, marking a significant development in the Korean War and U.S. military leadership.",
                "A U.S. plane crash claims the lives of 50 individuals, highlighting the importance of aviation safety measures.",
                "Color television transmission from the Empire State Building represents a milestone in the evolution of television technology.",
                "Hydrogen bomb tests take place at Eniwetok, showcasing the growing capabilities of nuclear weaponry.",
                "Truce talks in Korea aim to bring an end to the Korean War, a conflict that has endured for several years.",
                "Cinerama, a widescreen film format, is introduced, enhancing the cinematic experience.",
                "Chrysler introduces power steering, a feature that improves vehicle handling and maneuverability.",
                "Three-color stoplights for automobiles are introduced, enhancing traffic control and safety."
            ],
            1952: [
                "Queen Elizabeth II accedes to the British throne, marking a significant moment in British monarchy.",
                "The worst U.S. bus crash to date kills 28 individuals, prompting increased attention to road safety.",
                "The French submarine La Sybille disappears in the Mediterranean with 49 individuals aboard, leading to maritime safety concerns.",
                "A U.S. polio epidemic claims the lives of 3,300 people and affects 57,000 children, emphasizing the importance of polio vaccination.",
                "Walk/Don't Walk lighted pedestrian signs are introduced in New York City, enhancing pedestrian safety.",
                "General Motors (GM) offers built-in air conditioning in some 1953 cars, improving passenger comfort.",
                "Eva Peron, a prominent political figure in Argentina, passes away.",
                "The first transistorized hearing aid is introduced, offering improved hearing assistance technology.",
                "The announcement of the hydrogen bomb underscores the ongoing development of nuclear weaponry.",
                "Videotape technology is introduced, revolutionizing recording and playback of video content."
            ],
            1953: [
                "Joseph Stalin, the leader of the Soviet Union, passes away, leading to a period of transition and uncertainty in the USSR.",
                "Storms off the North Sea result in the loss of 200 lives in Britain, highlighting the impact of severe weather events.",
                "The structure of DNA is described as a double helix, a groundbreaking discovery in genetics.",
                "Pope Pius XII approves of psychoanalysis in therapy, marking a shift in the Catholic Church's stance on psychology.",
                "Julius and Ethel Rosenberg are executed in the United States following their espionage conviction during the Cold War.",
                "An uprising in East Berlin is quashed by Soviet forces, reflecting political tensions in post-war Germany.",
                "The Korean Armistice is signed, bringing an end to the active combat phase of the Korean War.",
                "A trend of suburbanization is noted in the United States as more people move away from urban centers.",
                "John F. Kennedy and Jacqueline Bouvier are married, marking the beginning of a prominent political family.",
                "An expedition searches for the elusive yeti, a mythical creature in Himalayan folklore.",
                "The measles vaccine is introduced, contributing to the prevention of this infectious disease."
            ],
            1954: [
                "The USS Nautilus becomes the first atomic-powered submarine, showcasing advancements in naval technology.",
                "The Army-McCarthy hearings take place, scrutinizing Senator Joseph McCarthy's allegations of communist influence in the U.S. Army.",
                "Edward R. Murrow challenges McCarthy's tactics and investigates allegations in a series of televised reports.",
                "The French garrison at Dien Bien Phu falls to Vietnamese forces, leading to increased involvement of the United States in Vietnam.",
                "The first hydrogen bomb is successfully detonated, signifying a major milestone in nuclear weapons development.",
                "The U.S. Supreme Court orders the integration of public schools, a pivotal moment in the civil rights movement.",
                "North and South Vietnam are formally established as separate entities, setting the stage for future conflicts.",
                "The retractable ball-point pen is introduced, providing a convenient writing instrument.",
                "The silicon transistor is developed, contributing to the miniaturization of electronic devices."
            ],
            1955: [
                "A missile with an atomic warhead is exploded in a Nevada test, showcasing advances in military technology.",
                "Hurricane Diane strikes, resulting in the deaths of 184 individuals and highlighting the destructive power of natural disasters.",
                "Albert Einstein, the renowned physicist, passes away, leaving a lasting legacy in the field of science.",
                "The Warsaw Pact treaty is signed, solidifying the Soviet Union's influence over Eastern European nations.",
                "Rebellion erupts in Algeria as resistance against French colonial rule intensifies.",
                "The Mickey Mouse Club debuts on television, becoming a popular children's program.",
                "Air-to-air guided missiles are introduced, enhancing military aviation capabilities.",
                "Disneyland, a famous theme park, opens its doors to the public, becoming a major entertainment attraction."
            ],
            1956: [
                "Over 10,000 Mau-Mau rebels are killed in a four-year conflict in Kenya, marking a significant chapter in the Mau-Mau Uprising.",
                "A bus boycott takes place in Montgomery, Alabama, as part of the civil rights movement against racial segregation.",
                "Suburbs experience significant growth in the United States as more people move away from urban centers.",
                "Soviet Premier Nikita Khrushchev denounces the actions and policies of his predecessor, Joseph Stalin.",
                "Gamal Abdel Nasser seizes control of the Suez Canal, leading to the Suez Crisis and international tensions.",
                "The Hungarian Revolution unfolds as Hungarians rebel against Soviet domination but are ultimately suppressed by Soviet forces.",
                "The Teon Company is formed, contributing to advancements in technology and industry.",
                "Go-karts are introduced as a recreational and competitive activity, popularizing kart racing."
            ],
            1957: [
                "Scientific research demonstrates that smoking is linked to the promotion of cancer, leading to increased awareness of smoking-related health risks.",
                "Nike Hercules missiles with atomic warheads are deployed to defend U.S. cities from potential enemy aircraft attacks.",
                "The launch of Sputnik, the world's first artificial satellite, shocks the United States and initiates the space race.",
                "The Mackinac Straits Bridge, spanning 3,800 feet, is completed, connecting Michigan's Upper and Lower Peninsulas."
            ],
            1958: [
                "Elvis Presley is drafted into the U.S. Army, temporarily leaving his music career.",
                "A tragic fire in a Chicago school claims the lives of 90 people, highlighting the importance of fire safety measures.",
                "The U.S. Navy submarine Nautilus successfully sails across the North Pole under the ice, achieving a historic feat.",
                "Governor Orval Faubus of Arkansas closes Little Rock's high schools to resist desegregation efforts.",
                "Pan American World Airways (Pan Am) inaugurates the first commercial flight of the Boeing 707 jet service to Paris, marking a milestone in air travel.",
                "Dr. Albert Sabin introduces the oral polio vaccine, a significant step in combating the polio epidemic.",
                "The era of communications satellites begins with the successful launch of the first artificial satellite for global communication.",
                "The hula-hoop becomes a popular toy and exercise equipment in the United States."
            ],
            1959: [
                "Fidel Castro gains power in Cuba after the Cuban Revolution, leading to significant political changes in the country.",
                "Ford's Edsel, a highly anticipated automobile model, is judged a commercial failure, impacting the automotive industry.",
                "Volvo introduces safety belts (seatbelts) in its vehicles, contributing to automotive safety standards."
            ],
            1960: [
                "Unrest continues in Algeria as the struggle for independence from French colonial rule intensifies.",
                "Hurricane Donna devastates the U.S. East Coast and Puerto Rico, causing significant destruction and loss of life.",
                "The artificial kidney is introduced, revolutionizing the treatment of kidney diseases through dialysis.",
                "Lunch counter sit-ins begin as part of the civil rights movement, challenging segregation and discrimination.",
                "Brasilia, the planned capital of Brazil, officially opens for business, symbolizing modern urban planning.",
                "The birth control pill becomes available for sale in the United States, revolutionizing contraception and family planning.",
                "The first weather satellite is launched, enhancing weather forecasting and monitoring capabilities.",
                "The popularity of portable transistor radios begins, transforming the way people listen to music and news.",
                "The U.S. public debt reaches $284 billion, reflecting economic challenges and government expenditures.",
                "The U.S. resident population reaches 179.3 million, indicating continued population growth."
            ],
            1961: [
                "President Dwight D. Eisenhower warns against the influence of the military-industrial complex in his farewell address, highlighting concerns about the growing defense industry.",
                "The Leakeys, a family of paleoanthropologists, discover some of the earliest human remains, providing insights into human evolution.",
                "The Berlin Wall is erected by East Germany, dividing the city and symbolizing the Cold War's division of Europe.",
                "The Peace Corps is established by President John F. Kennedy, promoting international volunteer service and cultural exchange.",
                "The Bay of Pigs invasion, a failed U.S.-backed attempt to overthrow Fidel Castro's regime, takes place in Cuba.",
                "Valium, a popular tranquilizer and anti-anxiety medication, is introduced, influencing psychiatric treatment."
            ],
            1962: [
                "The Cuban missile crisis brings the world to the brink of nuclear war as the United States and the Soviet Union engage in a tense standoff over missile installations in Cuba.",
                "Gallium-arsenide semiconductor lasers are developed, advancing laser technology and telecommunications.",
                "The first satellite link between the United States and the United Kingdom is established, improving global communication.",
                "Polaroid introduces color instant film, allowing for instant color photography."
            ],
            1963: [
                "An enormous civil rights demonstration takes place in Washington, D.C., where Dr. Martin Luther King Jr. delivers his famous \"I Have a Dream\" speech.",
                "President John F. Kennedy is tragically assassinated in Dallas, Texas, leading to a period of national mourning and investigation.",
                "A coup in Vietnam removes President Ngo Dinh Diem, contributing to political instability in the region.",
                "A cold wave sweeps across the United States, resulting in the deaths of 150 people and highlighting the dangers of extreme weather conditions.",
                "Hurricane Flora causes the deaths of 7,000 people in Haiti and Cuba, underscoring the destructive power of hurricanes.",
                "Mob actions become increasingly common in the Southern United States, reflecting social tensions and resistance to civil rights."
            ],
            1964: [
                "The Aswan Dam becomes operational, providing hydroelectric power and water resources in Egypt.",
                "The Beatles become enormously popular, revolutionizing music and popular culture.",
                "The United States accidentally releases a kilogram of plutonium into the atmosphere, raising concerns about nuclear safety.",
                "Jawaharlal Nehru, the first Prime Minister of India, passes away, leading to political changes in India.",
                "The Verrazano-Narrows Bridge, with a span of 4,260 feet, is completed, connecting Staten Island and Brooklyn in New York.",
                "President Lyndon B. Johnson signs the Civil Rights Act into law, marking a significant step in the civil rights movement.",
                "The Tonkin Gulf Resolution is passed by the U.S. Congress, authorizing military actions in Vietnam.",
                "3-D laser-holography is introduced, advancing holographic technology and imaging.",
                "The Moog synthesizer is introduced, revolutionizing electronic music production.",
                "The Federal Trade Commission (FTC) requires health warnings on cigarette packaging, acknowledging the health risks of smoking."
            ],
            1965: [
                "Malcolm X, a prominent civil rights activist, is assassinated, leading to debates about his legacy and contributions.",
                "Race riots erupt in the Watts neighborhood of Los Angeles, highlighting racial tensions and inequality in the United States.",
                "Pope Paul VI issues a declaration disassociating Jews from guilt for the crucifixion of Jesus Christ, fostering interfaith dialogue.",
                "A great electrical blackout affects northeastern states in the United States, emphasizing the vulnerability of electrical systems.",
                "Kevlar, a strong and lightweight synthetic material, is introduced, with applications in various industries, including body armor.",
                "Radial tires are introduced, improving vehicle safety and performance.",
                "IBM introduces its word processor, revolutionizing document preparation and office work."
            ],
            1966: [
                "The Cultural Revolution begins in China, leading to significant social and political upheaval under Mao Zedong's leadership.",
                "Opposition to the Vietnam War increases, with growing protests against U.S. involvement in Southeast Asia.",
                "A sniper kills 12 people at the University of Texas at Austin, prompting discussions about gun control and campus safety.",
                "Miniskirts are introduced as a fashion trend, challenging traditional dress norms and reflecting cultural changes.",
                "Edward Brooke becomes the first African American to be elected as a U.S. Senator by popular vote, marking a milestone in U.S. politics.",
                "Dolby-A noise reduction technology is introduced, improving audio recording and playback quality.",
                "Skateboards are introduced as a popular recreational activity for youth.",
                "The concept of \"body counts\" is introduced as a metric in Vietnam War reports, reflecting the measurement of enemy casualties.",
                "Bell-bottom pants are introduced as a distinctive fashion style."
            ],
            1967: [
                "The Six-Day War takes place in the Middle East, resulting in significant territorial changes and geopolitical shifts.",
                "The \"Summer of Love\" is a cultural phenomenon marked by countercultural movements, music festivals, and social experimentation.",
                "Thurgood Marshall becomes the first African American Supreme Court justice, making history in the U.S. judicial system.",
                "A tragic fire in the Apollo 1 spacecraft claims the lives of three astronauts during a pre-launch test, leading to safety improvements in space exploration.",
                "The United States experiences the loss of its 500th aircraft over Vietnam, underscoring the challenges of aerial warfare in the conflict.",
                "Race riots erupt in Newark, New Jersey, leaving 26 people dead in four days of violence and unrest.",
                "Detroit experiences race riots that result in 43 deaths and significant property damage, highlighting racial tensions in urban centers.",
                "Antiwar protests against the Vietnam War accelerate, with growing opposition to U.S. military involvement.",
                "The \"body count\" metric becomes a regular feature in Vietnam War reports, quantifying the number of enemy casualties.",
                "Law enforcement seizes 209 pounds of heroin in Georgia, reflecting ongoing efforts to combat drug trafficking.",
                "Bell-bottom pants become a prominent fashion trend, symbolizing the fashion of the era."
            ],
            1968: [
                "The Tet Offensive in Vietnam stuns the civilian population in the United States, raising questions about the progress of the war.",
                "Dr. Martin Luther King Jr., a civil rights leader, is assassinated, leading to nationwide mourning and protests against racial injustice.",
                "Black riots erupt in various U.S. cities, reflecting deep-seated social and racial tensions.",
                "Student revolts and protests take place in Paris and around the world, advocating for political and social change.",
                "Senator Robert F. Kennedy is tragically assassinated during his presidential campaign, altering the political landscape.",
                "A B-52 bomber carrying four hydrogen bombs crashes in a Greenland bay, raising concerns about nuclear accidents.",
                "Soviet forces quash a liberalizing government in Czechoslovakia, demonstrating Soviet influence in Eastern Europe.",
                "Spain officially voids a 1492 law that banned Jews, reflecting changing attitudes toward religious tolerance.",
                "The Democratic National Convention in Chicago faces protests and clashes with antiwar demonstrators.",
                "Apollo 8 astronauts become the first humans to orbit the Moon, marking a significant achievement in space exploration."
            ],
            1969: [
                "Skyjackings to Cuba continue, reflecting a trend of hijackings for political and personal motives.",
                "Barnard College in New York City begins to admit men, marking a milestone in gender integration in higher education.",
                "The first artificial heart implant is performed, paving the way for advancements in organ transplantation and medical technology.",
                "Anti-Vietnam War demonstrations take place in more than 40 cities across the United States on the same weekend, illustrating widespread opposition to the war.",
                "The Woodstock Music & Art Fair becomes a cultural icon, symbolizing the counterculture movement and music of the era.",
                "Approximately 250,000 protesters march on Washington, D.C., demanding an end to the Vietnam War and social change.",
                "Apollo 11 successfully lands on the Moon, with astronauts Neil Armstrong and Buzz Aldrin becoming the first humans to walk on the lunar surface.",
                "A snowstorm of the decade closes New York City, disrupting daily life and transportation.",
                "The My Lai massacre, which took place in 1968, is revealed to the public, sparking outrage and investigations into war crimes.",
                "The Boeing 747 jumbo jet is introduced, revolutionizing long-distance air travel with its large passenger capacity.",
                "An oil spill fouls Santa Barbara beaches in California, raising environmental awareness and concerns.",
                "The Concorde Mach 2 jetliner conducts its first flight, representing a technological leap in supersonic aviation."
            ],
            1970: [
                "The concept of \"radical chic\" becomes popular, reflecting a fascination with political activism and social change.",
                "A Palestinian group hijacks five airplanes in a coordinated operation, drawing international attention to the Palestinian-Israeli conflict.",
                "Charles de Gaulle, the former President of France, passes away, marking the end of an era in French politics.",
                "The Asbury Park riots result in the shooting of 46 people, highlighting issues of racial tension and urban unrest.",
                "Members of the radical activist group known as the \"Weathermen\" are arrested for a bomb plot, raising concerns about domestic terrorism.",
                "Tuna is recalled from the market due to mercury contamination, leading to food safety awareness.",
                "Bar codes are introduced as a technology for product identification and inventory management.",
                "Floppy disks are introduced as a storage medium for computer data, revolutionizing data transfer and storage.",
                "Windsurfing is introduced as a recreational water sport, combining elements of sailing and surfing.",
                "The U.S. public debt reaches $370 billion, reflecting economic challenges and government spending.",
                "The U.S. resident population reaches 203.3 million, indicating demographic growth."
            ],
            1971: [
                "A powerful earthquake in Los Angeles claims the lives of 51 people and causes significant damage to the city.",
                "A strong reaction against drug use in the armed forces intensifies, leading to anti-drug policies and enforcement.",
                "Hot pants are introduced as a fashion trend, characterized by short, tight-fitting shorts for women.",
                "The Pentagon Papers, a classified government report, are printed by newspapers, revealing government secrets and decisions related to the Vietnam War.",
                "Liquid crystal displays (LCDs) are introduced as a technology for displaying digital information in calculators and screens."
            ],
            1972: [
                "Ten European nations become members of the European Common Market, promoting economic integration and cooperation.",
                "U.S. President Richard Nixon makes a historic visit to China, marking a thaw in U.S.-China relations.",
                "Burglars are caught inside the Democratic Party's Watergate headquarters, leading to the Watergate scandal and political investigations.",
                "A tragic terrorist attack during the Munich Olympics results in the massacre of 11 Israeli athletes by Palestinian militants.",
                "Airline anti-hijacking procedures are established in the United States to enhance aviation security.",
                "Electronic pocket calculators are introduced, simplifying mathematical calculations and becoming portable tools.",
                "The Pong video game is introduced, pioneering the video game industry and electronic entertainment."
            ],
            1973: [
                "The last manned mission to the Moon, Apollo 17, takes place, marking the end of the Apollo program and lunar exploration.",
                "An oil embargo is imposed by oil-producing nations, leading to an energy crisis and fuel shortages in many countries.",
                "The Bosporus Bridge, with a span of 3,524 feet, is completed in Istanbul, Turkey, connecting Europe and Asia.",
                "Recombinant DNA technology is introduced, allowing scientists to manipulate and modify DNA, leading to advancements in biotechnology."
            ],
            1974: [
                "Patty Hearst, the granddaughter of publisher William Randolph Hearst, is kidnapped by the Symbionese Liberation Army (SLA), leading to a high-profile kidnapping case.",
                "A widespread gasoline shortage occurs in the United States, causing long lines at gas stations and highlighting energy dependency.",
                "Richard Nixon resigns from the Presidency of the United States in the wake of the Watergate scandal, making him the first U.S. President to resign from office.",
                "A series of tornadoes kills 315 people in the United States in two days, underscoring the destructive power of severe weather.",
                "The Green Revolution, an agricultural technology initiative, is introduced, leading to increased food production and global agricultural advancements."
            ],
            1975: [
                "South Vietnam falls to North Vietnamese forces, marking the end of the Vietnam War and leading to the reunification of Vietnam.",
                "Cambodia falls to the Khmer Rouge regime, resulting in a period of mass atrocities and social upheaval.",
                "Civil war erupts in Beirut, Lebanon, leading to a protracted conflict and instability in the region.",
                "Atari video games, including the iconic game Pong, are introduced, contributing to the growth of the video game industry."
            ],
            1976: [
                "Concerns about the extinction of animal species become a prominent public issue, leading to conservation efforts.",
                "Mao Tse-tung, the founding father of the People's Republic of China, passes away, marking a significant moment in Chinese history.",
                "Hurricane Lizzie devastates Mexico, resulting in the tragic loss of 2,500 lives.",
                "The Cray-1 supercomputer is introduced, representing a major advancement in high-performance computing."
            ],
            1977: [
                "The Trans-Alaskan oil pipeline becomes operational, facilitating the transportation of oil from Alaska to the continental United States.",
                "Three Israeli settlements are approved on the West Bank, contributing to the ongoing Israeli-Palestinian conflict.",
                "Optical fiber telephone lines are introduced, revolutionizing long-distance communication with improved speed and capacity.",
                "The Orient Express, a famous luxury train service, makes its last trip, marking the end of an era in train travel.",
                "Protesters attempt to halt the construction of the Seabrook nuclear power plant, reflecting concerns about nuclear energy."
            ],
            1978: [
                "An agreement is reached for the Panama Canal to be controlled by Panama, ending U.S. control over the strategic waterway.",
                "Proposition 13, a California ballot initiative, wins approval and triggers a nationwide trend of reduced capital expenditures.",
                "The exchange rate reaches 1 U.S. dollar equaling 175 Japanese yen, impacting international trade and currency markets.",
                "A tragic air collision over San Diego claims the lives of 150 people, raising questions about aviation safety.",
                "The Jonestown mass suicide occurs, resulting in the deaths of 909 people following the orders of cult leader Jim Jones.",
                "The world witnesses the birth of the first test-tube baby in London, a significant milestone in reproductive medicine."
            ],
            1979: [
                "The Shah of Iran flees the country amid growing unrest and revolution, leading to the Iranian Revolution.",
                "The Three Mile Island nuclear power plant experiences a partial meltdown, causing concerns about nuclear safety and environmental impact.",
                "Anastasio Somoza is ousted from power in Nicaragua, marking a turning point in the Nicaraguan Revolution.",
                "The U.S. embassy in Tehran is seized by Iranian militants, and hostages are held, leading to a diplomatic crisis known as the Iran hostage crisis.",
                "Soviet forces enter Afghanistan, initiating the Soviet-Afghan War and a protracted conflict in the region.",
                "The Rubik's Cube, a popular puzzle toy, is introduced and becomes a global sensation.",
                "Sony introduces the Walkman, a portable cassette player that revolutionizes personal music listening."
            ],
            1980: [
                "The price of an ounce of gold reaches $802 in the United States, reflecting economic challenges and fluctuations in the precious metals market.",
                "The United States experiences the highest inflation rate in 33 years, impacting the economy and consumer purchasing power.",
                "Banking deregulation policies are implemented, leading to changes in the financial industry and increased competition.",
                "The eruption of Mount St. Helens in Washington State results in the deaths of over 50 people and significant environmental damage.",
                "A hostage rescue mission in Iran fails, further intensifying the Iran hostage crisis.",
                "Solidarity, a trade union in Poland, gains recognition, challenging communist authorities and leading to political changes.",
                "A gold rush in the Amazon rainforest attracts prospectors and environmental concerns.",
                "Dolby-C noise reduction technology is introduced, enhancing audio quality in cassette tapes and other audio recordings.",
                "The U.S. public debt reaches $908 billion, reflecting fiscal challenges and government spending.",
                "The U.S. resident population reaches 226.5 million, indicating continued demographic growth."
            ],
            1981: [
                "Iran releases the embassy hostages, ending the 444-day-long Iran hostage crisis and improving U.S.-Iran relations.",
                "Millions of workers in Poland participate in strikes, demanding workers' rights and political reforms.",
                "The U.S. public debt reaches one trillion dollars, marking a significant fiscal milestone.",
                "An Israeli raid successfully destroys an Iraqi nuclear reactor, raising concerns about nuclear proliferation in the Middle East.",
                "The Humber Bridge, with a span of 4,626 feet, is completed in the United Kingdom, becoming one of the world's longest suspension bridges.",
                "Widespread marches and rallies against nuclear weapons and arms take place in Europe, reflecting global concerns about nuclear disarmament.",
                "The CDC notes a strange immune-system disease, later identified as AIDS, marking the beginning of a major public health crisis."
            ],
            1982: [
                "The world experiences a worldwide oil glut, leading to fluctuations in oil prices and changes in the global energy market.",
                "The Falklands War erupts between the United Kingdom and Argentina, resulting in territorial conflicts and military operations.",
                "An airliner crashes into the Potomac River bridge, resulting in the tragic deaths of 78 passengers and crew members.",
                "An oil rig sinks off Newfoundland, Canada, causing the loss of 84 lives and highlighting the dangers of offshore drilling.",
                "A major airliner crash in New Orleans claims the lives of 149 people, raising concerns about aviation safety.",
                "Approximately 800,000 people participate in a march against nuclear weapons in New York City, advocating for disarmament.",
                "Israeli forces reach Beirut, Lebanon, during the Lebanon War, leading to significant developments in the ongoing conflict."
            ],
            1983: [
                "The assassination of Benigno \"Ninoy\" Aquino Jr. occurs upon his arrival in Manila, leading to political turmoil in the Philippines.",
                "Widespread protests against missile deployments take place in Europe, reflecting concerns about the arms race and nuclear weapons.",
                "The world population is estimated to reach 4.7 billion, highlighting global demographic trends."
            ],
            1984: [
                "The legalization of VCR taping is implemented in the United States, addressing copyright and intellectual property issues.",
                "The Iran-Iraq war escalates to involve oil tankers in the Persian Gulf, impacting regional stability and oil markets.",
                "Reports emerge of Indonesian death squads allegedly responsible for the deaths of approximately 4,000 people, raising human rights concerns.",
                "Continued battles and conflicts persist in Beirut, Lebanon, contributing to the city's instability.",
                "The isolation of the AIDS virus represents a significant breakthrough in understanding the disease.",
                "A federal estimate indicates that there are approximately 350,000 homeless individuals in the United States, prompting discussions on homelessness.",
                "Research suggests that passive inhalation of cigarette smoke can cause diseases, leading to increased awareness of the dangers of secondhand smoke.",
                "A massive demonstration in Manila, Philippines, involving around 900,000 participants occurs, prompting President Reagan to reflect on economic conditions.",
                "An additional historical event or invention for this year: The Apple Macintosh personal computer is introduced, revolutionizing the computer industry with its graphical user interface."
            ],
            1985: [
                "Kidnappings continue to be a pressing issue in Beirut, affecting the safety of foreign nationals and journalists.",
                "Mikhail Gorbachev is selected as the Chairman of the USSR, marking the beginning of significant political reforms in the Soviet Union.",
                "Actor Rock Hudson's hospitalization for AIDS raises awareness of the disease in the entertainment industry.",
                "France sinks the Greenpeace vessel Rainbow Warrior in a controversial act of sabotage.",
                "A devastating earthquake strikes Mexico City, resulting in the tragic loss of 25,000 lives and widespread destruction.",
                "The U.S. trade balance becomes negative, reflecting trade deficits and economic challenges.",
                "Terrorism emerges as a widespread tactic employed by various splinter groups, posing security threats globally.",
                "The Achille Lauro cruise ship is hijacked, leading to the murder of a passenger and international tensions.",
                "Massive federal spending continues to drive economic expansion in the United States.",
                "The U.S. public debt reaches $1.82 trillion, doubling since 1980 as fiscal concerns grow."
            ],
            1986: [
                "The Challenger space shuttle experiences a tragic explosion, resulting in the loss of the entire crew and suspending NASA's manned space program for several years.",
                "The English Channel tunnel project receives approval, paving the way for a major transportation link between the United Kingdom and mainland Europe.",
                "The Chernobyl nuclear disaster unfolds, with dozens of heroes sacrificing themselves to contain the disaster, and experts anticipate long-term health impacts from the released atomic cloud.",
                "The emergence of a crack cocaine epidemic in the United States raises concerns about drug addiction and its social consequences.",
                "An additional historical event or invention for this year: The Hubble Space Telescope is launched into orbit, revolutionizing astronomical observation."
            ],
            1987: [
                "The Iran-Iraq War results in approximately one million casualties, highlighting the devastating toll of the prolonged conflict.",
                "The Dow Jones Industrial Average experiences a significant drop of 508 points in one day, known as \"Black Monday,\" impacting financial markets.",
                "In the United States, there are 13,468 reported AIDS-related deaths, underlining the severity of the AIDS epidemic.",
                "Arabs living within Israel initiate a general resistance movement, contributing to tensions in the region.",
                "The number of VCRs in the United States reaches 50 million, indicating widespread adoption of the technology."
            ],
            1988: [
                "The term \"Greenhouse Effect\" becomes widely used in discussions about climate change and global warming, raising environmental awareness.",
                "A Pan-Am jetliner explodes over Lockerbie, Scotland, with 259 people aboard, leading to investigations into the bombing and its perpetrators.",
                "An Armenian earthquake kills 25,000 people and leaves 400,000 homeless, prompting international relief efforts.",
                "RU-486, a controversial medication used for medical abortions, is introduced, sparking debates about reproductive rights.",
                "Widespread drought conditions affect the United States, impacting agriculture and water resources.",
                "The number of reported AIDS cases in the United States exceeds 60,000, underscoring the continued spread of the epidemic.",
                "Estimates suggest that the United States has spent $51.6 billion on illegal drugs this year, highlighting the challenges of drug-related issues."
            ],
            1989: [
                "The U.S. intensifies its \"war on drugs\" with increased efforts to combat drug trafficking and substance abuse.",
                "Political stress and significant changes take place in the Soviet Union, leading to political transformations and the eventual dissolution of the USSR.",
                "The U.S.S. Iowa experiences a turret explosion, resulting in the tragic loss of 42 lives and investigations into the incident.",
                "Hurricane Hugo strikes, leaving 71 people dead and causing widespread devastation in the affected areas.",
                "The Salman Rushdie affair begins, centered around the publication of Rushdie's novel \"The Satanic Verses\" and the subsequent fatwa issued against him.",
                "The U.S. conducts a military invasion of Panama, leading to the toppling of General Manuel Noriega's regime.",
                "Tiananmen Square demonstrations in Beijing, China, lead to a pro-democracy movement and a government crackdown, resulting in significant unrest.",
                "Federally insured bank losses in the United States are estimated at a staggering $500 billion, raising concerns about the stability of the financial sector.",
                "Compact discs (CDs) become the dominant playback medium in the United States, revolutionizing the music industry with digital audio technology."
            ],
            1990: [
                "Iraq's invasion of Kuwait triggers international condemnation, and the United States organizes an expeditionary force to oppose the invasion, setting the stage for the Gulf War.",
                "The South African government lifts emergency decrees, signaling political changes in the country.",
                "The U.S. public debt reaches $3.23 trillion, reflecting fiscal challenges and government spending.",
                "The Hubble Space Telescope encounters technical issues, leading to a space shuttle mission to correct its optics.",
                "The United States is estimated to have spent approximately $40 billion on illegal drugs this year, highlighting the persistent issue of drug-related problems.",
                "The U.S. resident population reaches 248.7 million, indicating ongoing demographic changes and growth."
            ],
            1991: [
                "The Gulf War results in the deaths of at least 50,000 Iraqis and significant destruction during the conflict in the Middle East.",
                "Iraq releases approximately 40 million gallons of crude oil into the Persian Gulf, leading to environmental and ecological disasters in the region.",
                "The Oakland Hills fire in California burns around 3,000 homes and claims dozens of lives, emphasizing the destructive power of wildfires.",
                "Massive volcanic eruptions of Mt. Pinatubo on Luzon have far-reaching impacts on climate and air travel.",
                "A coup attempt is foiled in the USSR, while Arab-Israeli talks continue in the Middle East.",
                "By the end of May, AIDS-related deaths in the United States total 113,426, highlighting the ongoing AIDS epidemic.",
                "Imported automobile sales account for one-third of the U.S. market, reflecting changing consumer preferences.",
                "The USSR dissolves into its constituent republics, and Mikhail Gorbachev resigns from his leadership position, marking the end of an era in Soviet history.",
                "Approximately one-fifth of sub-Saharan college graduates are believed to be HIV-positive, underlining the global impact of the AIDS crisis."
            ],
            1992: [
                "Economic recession grips industrial nations, resulting in increased homelessness and widespread reports of mass layoffs.",
                "Riots erupt in Los Angeles and other U.S. cities following the verdict in the Rodney King trial, resulting in 52 deaths and over $1 billion in damages.",
                "The U.S. military is deployed to aid famine relief efforts amid the civil war in Somalia, highlighting humanitarian crises in conflict zones.",
                "Tens of thousands of people are massacred during \"ethnic cleansing\" in the former Yugoslavia, underscoring the brutality of the Balkan conflict.",
                "Hurricanes strike Florida, Louisiana, and Hawaii, causing dozens of deaths and leaving thousands homeless, emphasizing the destructive power of natural disasters.",
                "Major earthquakes in Southern California and Egypt cause extensive damage and disrupt communities.",
                "An estimated 13 million people are now infected with the HIV virus, highlighting the global scale of the AIDS epidemic.",
                "The Czech Republic and Slovakia separate, marking significant changes in the political landscape of Eastern Europe."
            ],
            1993: [
                "Terrorists bomb the World Trade Center in New York, resulting in casualties and raising concerns about domestic terrorism.",
                "The FBI lays siege to the Branch Davidians near Waco, Texas, and 80 individuals ultimately lose their lives in the incident.",
                "Bill Clinton becomes the first Democratic President since Jimmy Carter, marking a change in U.S. political leadership.",
                "Strife and conflict continue in Bosnia, contributing to the complex and protracted Balkan Wars.",
                "North Korea withdraws from the nuclear nonproliferation treaty, raising concerns about nuclear proliferation.",
                "U.S. troops are withdrawn from Somalia, reflecting shifts in U.S. foreign policy.",
                "Congress votes to close over 130 U.S. military bases, leading to changes in the nation's defense infrastructure.",
                "U.S. unemployment rates decline, reflecting improvements in the labor market.",
                "The U.S. national debt reaches $4.35 trillion, emphasizing ongoing fiscal challenges."
            ],
            1994: [
                "The North American Free Trade Agreement (NAFTA) agreement is ratified by all participating parties, promoting trade and economic cooperation in North America.",
                "The CIA's Aldrich Ames is exposed as a Russian spy, highlighting intelligence breaches within U.S. agencies.",
                "The Anglican Church ordains its first female priests, marking a historic moment in religious leadership.",
                "South Africa holds its first universal-suffrage election, signaling the end of white minority rule and apartheid.",
                "Israel and the Palestine Liberation Organization (PLO) sign a self-rule accord, aiming for peace and autonomy in the Middle East.",
                "O.J. Simpson is charged in connection with two murders, leading to a high-profile trial and discussions on race, justice, and celebrity.",
                "Fifty years since World War II Normandy landings, commemorations take place to remember the D-Day invasion and its significance.",
                "A professional baseball strike disrupts the sport's season, raising questions about labor relations in professional sports.",
                "The United States intervenes in Haiti and successfully restores Jean-Bertrand Aristide to the presidency, addressing political turmoil in the country."
            ],
            1995: [
                "The Shoemaker-Levy 9 comet cluster collides with Jupiter, providing a rare astronomical spectacle.",
                "A devastating terrorist bomb attack targets the Oklahoma City federal building, resulting in the tragic loss of 161 lives.",
                "Approximately one in ten people in the United States is connected to the internet, marking the growing influence of the World Wide Web.",
                "O.J. Simpson is acquitted of murder charges in a highly publicized trial, sparking debates and discussions about the legal system and justice.",
                "Peace initiatives make progress in Northern Ireland, Bosnia, and the Middle East, fostering hope for conflict resolution.",
                "The assassination of Israeli Prime Minister Yitzhak Rabin leads to a period of mourning and uncertainty in Israel.",
                "General Colin Powell declines to run for the U.S. presidency, affecting the political landscape and potential candidates.",
                "The U.S. federal debt reaches a significant milestone, surpassing $5 trillion, raising concerns about fiscal responsibility."
            ],
            1996: [
                "U.S. federal workers return to work following a budget crisis, highlighting the impact of government shutdowns on public services.",
                "A bomb explodes at the Atlanta Olympic Games, resulting in one fatality and raising security concerns at major international events.",
                "Earth experiences a rise in its recent average surface temperature, contributing to discussions about climate change and global warming.",
                "Minnesota faces one of its coldest winters in nearly a century, with extreme cold weather affecting the region.",
                "Mount Everest climbing deaths continue to rise, underscoring the risks and challenges of high-altitude mountaineering.",
                "Islamic rebels capture Kabul, leading to political changes and conflict in Afghanistan.",
                "The struggle over abortion continues in the U.S. Senate, reflecting ongoing debates about reproductive rights and legislation.",
                "Copyright piracy remains a source of friction between the United States and China, impacting intellectual property rights.",
                "The U.S. national debt surpasses $5.2 trillion, highlighting long-term fiscal challenges.",
                "The United States experiences economic prosperity, with positive economic indicators and growth.",
                "Efforts to control immigration and drug addiction face criticism and challenges in their implementation.",
                "Timothy McVeigh is held in connection with the Oklahoma City bombing, one of the deadliest domestic terrorist attacks in U.S. history.",
                "The Unabomber suspect, Ted Kaczynski, is indicted, leading to legal proceedings and discussions about domestic terrorism."
            ],
            1997: [
                "The Haitian ferry Pride of la Gonave sinks, resulting in a tragic maritime disaster with over 200 casualties.",
                "New AIDS infections are estimated to exceed 3 million, highlighting the ongoing global health crisis.",
                "Approximately 5.8 million people have died from AIDS-related illnesses, underscoring the magnitude of the HIV/AIDS pandemic.",
                "The United States has an estimated resident population of approximately 275 million, reflecting demographic changes.",
                "Approximately 40% of the U.S. population is now connected to the internet, marking a significant milestone in the digital age.",
                "President Bill Clinton faces heavy scrutiny and political pressure regarding allegations of sexual misconduct, leading to a national conversation.",
                "The Dow-Jones average surpasses 8,000 points in July, indicating stock market growth and economic stability.",
                "Tobacco companies admit that tobacco is addictive, leading to legal and public health implications.",
                "Comet Hale-Bopp passes nearby in March, offering a celestial spectacle visible from Earth.",
                "Hong Kong reverts to Chinese sovereignty, marking a historic moment in international relations.",
                "NASA's Ames Research Center establishes a department of astrobiology, advancing the study of life beyond Earth.",
                "The world mourns the death of Diana, Princess of Wales, in a tragic auto crash, triggering global expressions of grief and remembrance.",
                "Media mogul Ted Turner donates $1 billion to the United Nations, making a significant philanthropic contribution to international causes."
            ],
            1998: [
                "President Bill Clinton faces allegations of perjury and obstruction of justice, leading to a cloud of controversy and legal proceedings.",
                "The U.S. economic expansion shows signs of slowing, raising concerns about economic stability and growth.",
                "El Niño weather patterns lead to heavy rains in California and violent storms across the Midwest, impacting weather and agriculture.",
                "Storms cause significant damage in Europe, affecting infrastructure and communities.",
                "Tornadoes strike Alabama, resulting in the loss of 34 lives and causing destruction in affected areas.",
                "Ted Kaczynski pleads guilty to the Unabomber attacks, acknowledging his involvement in a series of domestic bombings.",
                "The U.S. federal budget shows a small surplus for the first time in 30 years, indicating progress in fiscal management.",
                "Rwanda executes 22 individuals for their roles in the genocide, marking a significant moment in the pursuit of justice.",
                "Iraq appears to achieve successful outcomes in ending UN weapons inspections, raising concerns about international security.",
                "Russia experiences economic and social turmoil, reflecting challenges in the post-Soviet era.",
                "Chicago O’Hare International Airport records approximately 70 million passenger arrivals and departures in 1997, highlighting its significance as a major transportation hub."
            ],
            1999: [
                "President Bill Clinton is impeached by the House of Representatives, triggering a historic impeachment trial in the Senate.",
                "The U.S. economy experiences a surge, with the Dow Jones average finishing above 11,000 points for the first time in history.",
                "The United States faces very large balance of payment deficits, raising concerns about international trade and economic stability.",
                "Violent crime in the United States reaches its lowest level since 1973, reflecting positive trends in public safety.",
                "The American Medical Association (AMA) approves a union for medical doctors, addressing labor issues within the medical profession."
            ],
            2000: [
                "The U.S. stock market experiences a burst of bubbles, leading to discussions about the stock market's impact on social security.",
                "A Russian nuclear submarine sinks in the Barents Sea, resulting in the tragic loss of 118 lives and raising questions about submarine safety.",
                "An Air France Concorde crashes into a hotel, resulting in the tragic deaths of 113 individuals and marking a significant aviation disaster.",
                "Mexico's Institutional Revolutionary Party (PRI) loses the presidency for the first time in 71 years, signifying a political shift in Mexico.",
                "Edward Gorey, acclaimed author and illustrator, passes away at the age of 75, leaving behind a legacy of unique and imaginative works.",
                "George W. Bush is elected as the President of the United States, shaping the country's political landscape and policies."
            ],
            2001: [
                "A series of coordinated terrorist attacks kills approximately 3,000 people in New York and Virginia, leading to significant changes in security and international relations.",
                "The submarine U.S.S. Greenville surfaces underneath a Japanese trawler, resulting in the tragic loss of 9 lives and international attention.",
                "New observations of \"dark energy\" and \"dark matter\" force a re-evaluation of previously held cosmological theories, reshaping our understanding of the universe.",
                "The solar-powered aircraft Helios reaches an altitude of 96,500 feet, demonstrating the potential of renewable energy in aviation.",
                "Approximately 55% of U.S. households now contain computers, signifying the growing presence of technology in homes.",
                "Senate and House offices are closed due to anthrax contamination, resulting in heightened concerns about bioterrorism threats.",
                "U.S. armed forces enter Afghanistan as part of the global response to terrorism, marking the beginning of a significant military campaign."
            ],
            2002: [
                "President George W. Bush identifies an \"axis of evil,\" shaping U.S. foreign policy and international perceptions.",
                "North Korea reports that it has secretly produced nuclear bombs, intensifying concerns about nuclear proliferation.",
                "Enormous accounting frauds and business bankruptcies come to light in the United States, leading to financial scandals and corporate reforms.",
                "Piracy is blamed, rather than quality, for the continued decline in sales of recorded music and music videos worldwide, impacting the music industry.",
                "The Euro becomes the official currency of multiple European countries, solidifying the Eurozone's economic integration.",
                "The war crimes trial of Slobodan Milosevic begins, addressing allegations of human rights abuses during the Balkan conflicts."
            ],
            2003: [
                "An enormous power outage affects the northeastern United States and eastern Canada during the summertime, revealing vulnerabilities in electrical infrastructure.",
                "Europe experiences an unprecedented heatwave, with more than 11,000 deaths in France alone attributed to extreme temperatures above 105°F.",
                "Primatologists discover a previously unknown species of ape in the northern Congo, resembling a cross between a gorilla and a chimpanzee, but larger, expanding our knowledge of primate diversity.",
                "The Galileo space probe is deliberately crashed into Jupiter, concluding its fourteen-year mission exploring the outer planets of our solar system.",
                "A mysterious monolith is discovered in a remote desert, sparking intrigue and speculation about its origin and purpose.",
                "The first privately funded spacecraft successfully reaches orbit, marking a milestone in commercial space exploration.",
                "The European Space Agency's Mars Express mission confirms the presence of water ice on Mars, increasing the likelihood of future human exploration."
            ],
            2004: [
                "Terrorist attacks on four rush hour trains result in the tragic deaths of 191 people in Madrid, Spain, and a siege of a school in Beslan, Northern Ossetia, leads to the loss of 335 lives and injuries to at least 700 people.",
                "The largest passenger ship afloat, named the Queen Mary 2 by Her Majesty Queen Elizabeth II, sets off on its maiden voyage, symbolizing advancements in maritime technology.",
                "Taipei 101, the world's tallest skyscraper at 509 meters, opens to the public, representing architectural and engineering achievements.",
                "The Hubble Space Telescope captures stunning images of distant galaxies, providing valuable insights into the cosmos.",
                "A breakthrough in stem cell research offers new possibilities for regenerative medicine and disease treatment.",
                "Google goes public in a highly anticipated initial public offering, transforming the tech industry and investment landscape.",
                "The European Space Agency's Rosetta spacecraft successfully lands a probe on a comet's surface, advancing our understanding of cometary bodies."
            ],
            2005: [
                "Hurricane Katrina makes landfall along the U.S. Gulf Coast, resulting in the tragic loss of over 1,800 lives and significant damage to communities.",
                "The Virgin Atlantic Global Flyer breaks the world record for the fastest solo flight around the world, pushing the boundaries of aviation.",
                "A leap second is added to the end of the year, fine-tuning our understanding of time and precision.",
                "The Kyoto Protocol enters into force, marking a global commitment to address climate change.",
                "YouTube is launched, revolutionizing online video sharing and content creation.",
                "The Cassini-Huygens mission successfully lands a probe on Saturn's moon Titan, providing valuable data about this enigmatic world."
            ],
            2006: [
                "North Korea claims to have conducted its first nuclear test, raising concerns about nuclear proliferation and international security.",
                "The 250th anniversary of the birth of Wolfgang Amadeus Mozart is celebrated, honoring the legacy of a prolific composer and musician.",
                "Twitter is founded, shaping the way people communicate and share information in the digital age.",
                "NASA's New Horizons spacecraft embarks on a mission to Pluto, promising new discoveries about the distant dwarf planet.",
                "Researchers achieve the first successful cloning of a mammal from an adult cell, opening new possibilities in genetics and biotechnology.",
                "The International Space Station expands with the addition of new modules, enhancing scientific research in space."
            ],
            2007: [
                "Russia declares the resumption of strategic bomber flight exercises, signaling military assertiveness on the global stage.",
                "Harry Potter and the Deathly Hallows is released and becomes the fastest-selling book in publishing history, captivating readers worldwide.",
                "Apple releases the iPhone, revolutionizing the smartphone industry and changing the way people interact with technology.",
                "China's Chang'e-1 lunar probe successfully enters lunar orbit, marking a significant milestone in China's space exploration efforts.",
                "Live Earth concerts are held across the world to raise awareness about climate change and environmental conservation.",
                "Researchers discover a new species of deep-sea creature in the Mariana Trench, shedding light on Earth's most extreme environments."
            ],
            2008: [
                "Bernard Madoff is arrested for committing the largest financial fraud in history, exposing vulnerabilities in the financial sector.",
                "Barack Obama is elected as the 44th President of the United States, making history as the first President of African-American origin.",
                "The Wilkins Ice Shelf in Antarctica disintegrates, raising concerns about climate change and its impact on polar regions.",
                "Lehman Brothers goes bankrupt, triggering a global financial crisis and reshaping the world's economic landscape.",
                "Pirate activity increases off the coast of Somalia, drawing international attention to maritime security issues.",
                "The Large Hadron Collider (LHC) at CERN becomes operational, enabling groundbreaking experiments in particle physics."
            ],
            2009: [
                "The Icelandic banking system collapses, highlighting vulnerabilities in global financial markets and banking systems.",
                "An outbreak of the H1N1 influenza strain, 'Swine Flu,' reaches pandemic proportions, affecting global public health and healthcare systems.",
                "The longest total solar eclipse of the 21st century takes place on July 22, lasting up to 6 minutes and 38.8 seconds, captivating skywatchers across Asia and the Pacific Ocean.",
                "The Kepler Space Telescope is launched to search for exoplanets, revolutionizing our understanding of planets beyond our solar system.",
                "The Large Hadron Collider (LHC) at CERN achieves record energy levels, enabling experiments to explore fundamental particles and the early universe.",
                "The Copenhagen Climate Summit brings world leaders together to address climate change and set emissions targets for the future."
            ],
            2010: [
                "The Deepwater Horizon oil platform explodes in the Gulf of Mexico, leading to the tragic deaths of eleven oil workers and a seven-month-long oil spill, highlighting environmental risks associated with offshore drilling.",
                "The Eyjafjallajökull volcano erupts beneath an Icelandic ice cap, spewing ash into the atmosphere and disrupting air travel across Europe, revealing vulnerabilities in global transportation.",
                "Hundreds of thousands of secret American diplomatic cables are released by the website WikiLeaks, sparking debates about transparency, security, and international relations.",
                "Apple introduces the iPad, revolutionizing the tablet computer market and changing the way people consume digital content.",
                "Scientists create the first synthetic organism with a human-made genetic code, opening new possibilities in biotechnology.",
                "The United Nations adopts the 2030 Agenda for Sustainable Development, setting ambitious goals for global sustainability and development."
            ],
            2011: [
                "The Iraq War is declared over by the United States, marking a significant milestone in U.S. foreign policy.",
                "Japan is hit by a 9.1 magnitude earthquake, followed by a devastating tsunami that adds to the death toll and triggers a nuclear crisis in four coastal nuclear power plants.",
                "The global population is judged to have reached seven billion, underscoring the challenges and opportunities of demographic growth.",
                "Osama bin Laden, the figurehead of Al-Qaeda, is killed by American special forces in Pakistan, leading to discussions about the impact on counterterrorism efforts.",
                "Street vendor Mohamed Bouazizi sets himself on fire in Tunisia, sparking a revolutionary movement that leads to the overthrow of the Tunisian government and similar revolutions across the Middle East, known as the Arab Spring.",
                "NASA's Juno spacecraft is launched on a mission to study Jupiter's composition and evolution, providing insights into the solar system's history.",
                "Scientists discover evidence of water on Mars, raising the possibility of past or present life on the Red Planet."
            ],
            2012: [
                "The Diamond Jubilee of Queen Elizabeth II is celebrated, commemorating her 60-year reign as the monarch of the United Kingdom and other Commonwealth realms.",
                "The Arab Spring continues to unfold, shaping political transitions and unrest in several countries across the Middle East and North Africa.",
                "The century's second and last solar transit of Venus occurs, offering a rare celestial event for astronomers and skywatchers.",
                "The Tokyo Skytree, the tallest self-supporting tower in the world at 634 meters, opens to the public, showcasing architectural and engineering excellence.",
                "CERN announces the discovery of the Higgs Boson, often referred to as the 'god particle,' providing insights into fundamental particles and the nature of the universe.",
                "Austrian skydiver Felix Baumgartner becomes the first person to break the sound barrier without machine assistance, achieving this feat with a 24-mile jump to Earth at Roswell, New Mexico.",
                "Curiosity, NASA's Mars rover, successfully lands on the Martian surface, embarking on a mission to explore the Red Planet's geology and search for signs of past life."
            ],

            
            # ... (další roky a události)
        }
        return events.get(year, [])
        
    @commands.command(aliases=["randomLoot","randomloot"])
    async def cloot(self, ctx):
        items = ["A Mysterious Journal", "A Cultist Robes", "A Whispering Locket", "A Mysterious Puzzle Box", "A Map of the area", "An Ornate dagger", "Binoculars", "An Old journal", "A Gas mask", "Handcuffs", "A Pocket watch", "A Police badge", "A Vial of poison", "A Rope (20 m)", "A Vial of holy water", "A Hunting knife", "A Lockpick", "A Vial of acid", "A Hammer", "Pliers", "A Bear trap", "A Bottle of poison", "A Perfume", "Flint and steel", "A Vial of blood", "A Round mirror", "A Pocket knife", "Matchsticks", "Cigarettes", "Sigars", "A Compass", "An Opium pipe", "A Vial of snake venom", "A Handkerchief", "A Personal diary", "A Wooden cross", "A Business card", "A Cultist's mask", "Cultist’s robes", "A Pocket watch", "A Bottle of absinthe", "A Vial of morphine", "A Vial of ether", "A Black candle", "A Flashlight", "A Baton", "A Bottle of whiskey", "A Bulletproof vest", "A First-aid kit", "A Baseball bat", "A Crowbar", "A Cigarillo case", "Brass knuckles", "A Switchblade knife", "A Bottle of chloroform", "Leather gloves", "A Sewing kit", "A Deck of cards", "Fishing Line", "An Axe", "A Saw", "A Rope (150 ft)", "A Water bottle", "A Lantern", "A Signaling mirror", "A Steel helmet", "A Waterproof cape", "A Colt 1911 Auto Handgun", "A Luger P08 Handgun", "A S&W .44 Double Action Handgun", "A Colt NS Revolver", "A Colt M1877 Pump-Action Rifle", "A Remington Model 12 Pump-Action Rifle", "A Savage Model 99 Lever-Action Rifle", "A Winchester M1897 Pump-Action Rifle", "A Browning Auto-5 Shotgun", "A Remington Model 11 Shotgun", "A Winchester Model 12 Shotgun", "A Beretta M1918 Submachine Gun", "An MP28 Submachine Gun", "Handgun Bullets (10)", "Handgun Bullets (20)", "Handgun Bullets (30)", "Rifle Bullets (10)", "Rifle Bullets (20)", "Rifle Bullets (30)", "Shotgun Shells (10)", "Shotgun Shells (20)", "Shotgun Shells (30)", "A Bowie Knife", "A Katana Sword", "Nunchucks", "A Tomahawk", "A Bayonet", "A Rifle Scope", "A Rifle Bipod", "A Shotgun Stock", "A Dynamite Stick", "A Dissecting Kit", "A Bolt Cutter", "A Hacksaw", "A Screwdriver Set", "A Sledge Hammer", "A Wire Cutter", "Canned Meat", "Dried Meat", "An Airmail Stamp", "A Postage Stamp", "A Camera", "A Chemical Test Kit", "A Codebreaking Kit", "A Geiger Counter", "A Magnifying Glass", "A Sextant", "Federal agent credentials", "Moonshine", "A Skeleton key", "A Can of tear gas", "A Trench coat", "Leather gloves", "A Fountain pen", "A Shoe shine kit", "A Straight razor", "Cufflinks", "A Snuff box", "A Perfume bottle", "Playing cards", "An Oil lantern", "A Mess kit", "A Folding shovel", "A Sewing kit", "A Grappling hook", "A Portable radio", "A Dice set", "Poker chips", "A Pipe", "Pipe tobacco", "A Hairbrush", "Reading glasses", "A Police whistle", "An Altimeter", "A Barometer", "A Scalpel", "A Chemistry set", "A Glass cutter", "A Trench periscope", "A Hand Grenade", "A Signal flare", "An Army ration", "A Can of kerosene", "A Butcher's knife", "A Pickaxe", "A Fishing kit", "An Antiseptic ointment", "Bandages", "A Cigarette Case", "A Matchbox", "A pair of Cufflinks", "A pair of Spectacles", "A pair of Sunglasses", "A set of Keys", "A tube of Lipstick", "A set of Hairpins", "A Checkbook", "An Address Book", "An Umbrella", "A pair of Gloves", "A Notebook", "A Gas cooker", "Rubber Bands", "A Water Bottle", "A Towel", "A Cigar Cutter", "A Magnifying Glass", "A Magnesium Flare", "A Hairbrush", "A Sketchbook", "A Police Badge", "A Fingerprinting Kit", "Lecture Notes", "A Measuring Tape", "Charcoal", "A Pencil Sharpener", "An Ink Bottle", "Research Notes", "A Crowbar", "A Fake ID", "A Stethoscope", "Bandages", "Business Cards", "A Leather-bound Journal", "A Prescription Pad", "Dog Tags", "A Pipe", "A Chocolate bar", "Strange bones", "A Prayer Book", "Surgical Instruments", "Fishing Lures", "Fishing Line", "Pliers", "A Bottle Opener", "A Wire Cutter", "A Wrench", "A Pocket Watch", "A Travel Guidebook", "A Passport", "Dental Tools", "A Surgical Mask", "A Bottle of red paint", "An Electricity cable (15 ft)", "A Smoke Grenade ", "A Heavy duty jacket", "A pair of Heavy duty trousers", "Motor Oil", "Army overalls", "A small scale", "A bottle of Snake Oil", "A Cane with a hidden sword", "A Monocle on a chain", "A Carved ivory chess piece", "Antique marbles", "A Bullwhip", "A Folding Fan", "A Folding Pocket Knife", "A Travel Chess Set", "A Pocket Book of Etiquette", "A Pocket Guide to Stars", "A Pocket Book of Flowers", "A Mandolin", "An Ukulele", "A Vial of Laudanum", "A Leather Bound Flask (empty)", "A Lock of Hair", "A Tobacco Pouch", "A flare gun", "A pipe bomb", "A Molotov cocktail", "An anti-personnel mine", "A machete", "A postcard", "A wristwatch", "A shovel", "A padlock", "A light chain (20 ft)", "A heavy chain (20 ft)", "A handsaw", "A telescope", "A water pipe", "A box of candles", "Aspirin (16 pills)", "Chewing Tobacco", "A Gentleman's Pocket Comb", "A Sailor's Knot Tying Guide", "A Leather Map Case", "A Camera", "Crystal Rosary Beads", "A Handmade Silver Bracelet", "Herbal Supplements", "A Bloodletting Tool", "A Spiritualist Seance Kit", "A Morphine Syringe", "A Bottle of Radioactive Water", "An Astrology Chart", "An Alchemy Kit", "A Mortar and Pestle", "A Scalpel", "An Erlenmeyer Flask", "A Chemistry Textbook", "Nautical Charts", "A Bottle of Sulfuric Acid", "Protective Gloves", "Safety Goggles", "A Kerosene Lamp", "Painkillers"]
        # Pravděpodobnost 50% na získání peněz
        has_money = random.choice([True, False, False, False])
        money = None
        if has_money:
            money = random.randint(1, 1000) / 100  # Peníze od 0.01 do 10.00
    
        # Náhodně vyber počet předmětů od 1 do 7
        num_items = random.randint(1, 7)
        # Náhodně vyber předměty
        chosen_items = random.sample(items, num_items)
    
        # Vytvoření embedu
        embed = discord.Embed(title="Random Loot", color=discord.Color.blue())
        for item in chosen_items:
            emoji = "\U0001F4E6"  # Emoji pro věc
            embed.add_field(name=f"{emoji} {item}", value='\u200b', inline=False)  # '\u200b' je prázdný znak
    
        if money is not None:
            emoji_money = "\U0001F4B5"  # Emoji pro peníze
            embed.add_field(name=f"{emoji_money} Money", value=f"${money:.2f}", inline=False)
    
        await ctx.send(embed=embed)
