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
                "APP": ":sparkles:",
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
                            if self.player_stats[user_id]["STR"] != 0 and self.player_stats[user_id]["DEX"] != 0 and self.player_stats[user_id]["CON"] != 0 and self.player_stats[user_id]["EDU"] != 0 and self.player_stats[user_id]["APP"] != 0 and self.player_stats[user_id]["SIZ"] != 0 and self.player_stats[user_id]["LUCK"]:
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
            1890: [
                "First entirely steel-framed building erected in Chicago.",
                "First electric tube railway in London.",
                "British cruiser, Serpent, wrecked in storm off coast of Spain, 167 lost.",
                "Sitting Bull killed in Sioux uprising.",
                "First ice-cream sundae.",
                "U.S. resident population is 62.9 million."
            ],
            1891: [
                "Devastating quake levels 20,000 structures and kills 25,000 people in Japan.",
                "First practical hydroelectric station.",
                "Electric torch adopted in England."
            ],
            1892: [
                "Fires and floods create a human hell in Oil City, Pennsylvania, with 130 dead.",
                "Cholera vaccine developed.",
                "Cape-Johannesburg railroad completed.",
                "Crown top for bottles invented.",
                "Diesel engine patented."
            ],
            1893: [
                "Floods, pushed by hurricane winds, devastate the U.S. South Atlantic coast, resulting in 2000 deaths.",
                "World Exposition in Chicago.",
                "First practical roll film.",
                "Shredded wheat cereal invented."
            ],
            1894: [
                "War breaks out between China and Japan.",
                "Minnesota forest fire kills 480 people.",
                "Captain Dreyfus exiled to Devil’s Island.",
                "First wireless communication."
            ],
            1895: [
                "Roentgen discovers X-rays.",
                "Cigarette-making machine invented.",
                "The Lumieres open their Cinematographie."
            ],
            1896: [
                "Klondike gold rush begins.",
                "Addressograph patents confirmed.",
                "Ford’s first motorcar.",
                "Periscopes for submarines invented.",
                "First modern Olympic Games held in Athens."
            ],
            1897: [
                "Mimeo stencils are invented.",
                "First cathode ray tube."
            ],
            1898: [
                "Tropical cyclone hits southern U.S., resulting in hundreds of deaths.",
                "2446 U.S. soldiers die in the Spanish-American War.",
                "Disc recordings become practical.",
                "Commercial aspirin appears.",
                "Kellogg’s Corn Flakes introduced.",
                "Tubular flashlight invented."
            ],
            1899: [
                "Windsor Hotel in New York goes up in flames, causing millions in damage and 14 deaths.",
                "Rutherford discovers alpha and beta particles.",
                "General adoption of typewriters underway."
            ],
            1900: [
                "Pier re, steamer Rio de Janeiro wrecked in San Francisco harbor, 128 lives lost.",
                "The great Galveston hurricane kills 6,000 people.",
                "Mine explosion kills 200 in Utah.",
                "Boxer Rebellion occurs in China.",
                "Kodak “Brownie” camera introduced.",
                "Count Zeppelin launches 420-foot airship.",
                "U.S. public debt is $1.263 billion.",
                "U.S. resident population is 76 million."
            ],
            1901: [
                "President McKinley is assassinated.",
                "Two serious typhoid outbreaks occur in the U.S.",
                "Queen Victoria dies.",
                "Human blood groups classified.",
                "First transatlantic wireless communication."
            ],
            1902: [
                "Boer War.",
                "Mt. Pelée eruption kills 40,000 on Martinique.",
                "First steam-turbine-driven passenger ship.",
                "Modern macadam developed.",
                "First alum-dried powdered milk.",
                "Puffed cereals introduced.",
                "First Teddy bear created.",
                "First Caruso gramophone recording.",
                "Economical hydrogenated fats make fats for soap and cooking plentiful."
            ],
            1903: [
                "Fire at Iroquois Theatre in Chicago, worst theater fire in U.S. history (602 dead).",
                "Wright Brothers successfully fly the first heavier-than-air powered aircraft.",
                "First fluorescent light developed.",
                "Postal meter invented.",
                "Center-frame motorcycle engine introduced."
            ],
            1904: [
                "Eden Colorado train derails into flood, resulting in 96 deaths.",
                "Broadway subway opens in NYC.",
                "Thermos flask patented.",
                "Tracks (as opposed to wheels) first appear on farm machinery.",
                "Kapok life belts introduced.",
                "Russo-Japanese War begins."
            ],
            1905: [
                "Cullinan diamond (3,000 carats) found, largest to that date.",
                "Steam turbines become standard for the British navy.",
                "Abortive revolution in Russia.",
                "Electric motor horn invented.",
                "Chemical foam fire extinguisher created.",
                "Special Theory of Relativity proposed."
            ],
            1906: [
                "Earthquake and fire devastate San Francisco, 28,818 houses destroyed and 700 announced killed.",
                "U.S. troops occupy Cuba until 1909.",
                "Lusitania and Mauretania launched.",
                "Jukebox introduced.",
                "Mass-production of marine outboard motors begins."
            ],
            1907: [
                "West Virginian coal mine explosion kills 361.",
                "Rasputin gains great influence in Czarist Russia.",
                "Animated cartoons introduced.",
                "Electric washing machine invented.",
                "Household detergent introduced.",
                "Upright vacuum cleaner created."
            ],
            1908: [
                "Minkowski formulates his 4-dimensional geometry.",
                "Paper cups for drinking introduced."
            ],
            1909: [
                "Robert E. Peary reaches the North Pole.",
                "Hurricane in Louisiana and Mississippi kills 350.",
                "First powered flight across the English Channel.",
                "Double-decker buses introduced in the U.K."
            ],
            1910: [
                "Landslide buries workers in the Norman open-pit mine in Virginia, MN.",
                "Wellington, WA trains swept away by avalanche, killing 96.",
                "Murray and Hjort undertake the first deep-sea research expedition.",
                "Radio-direction finder introduced.",
                "Spring-operated mouse trap invented.",
                "Incorporation of the Boy Scouts of America.",
                "U.S. resident population is 92 million."
            ],
            1911: [
                "Forty tons of dynamite explode at Communipaw terminal, NJ, killing 30.",
                "Triangle Shirtwaist Factory fire in New York City leaves 145 dead.",
                "Zapata arrives in Mexico City, but the battles have just begun.",
                "Revolution in China leads to the republic under Sun Yat-sen.",
                "Electric frying pan introduced.",
                "Norwegian explorer Roald Amundsen reaches South Pole."
            ],
            1912: [
                "Titanic rams iceberg, 1,517 passengers and crew are lost.",
                "Wilson’s cloud chamber leads to the detection of protons and electrons.",
                "Cellophane patented.",
                "Saville Row creates what will be named the “trench coat” in WWI.",
                "Cadillac shows the first electric self-starter for automobiles.",
                "Two self-service grocery stores open in California."
            ],
            1913: [
                "The Balkan War begins.",
                "British steamer Calvadas lost in a blizzard in the Sea of Marmara, 200 lost.",
                "Wilson inaugurated as President of the U.S.",
                "Electric starters for motorcycles introduced.",
                "Vitamin A discovered.",
                "Income tax and popular election of senators added to U.S. Constitution."
            ],
            1914: [
                "The Great War begins.",
                "First air raids.",
                "First use of the Panama Canal.",
                "Canadian Pacific steamship Empress of India sunk in collision with the Storstad in the St. Lawrence River, 1,024 lost."
            ],
            1915: [
                "Lusitania sunk by German submarine, 1,199 lost, consternation and anger follow in the United States.",
                "Enormous and unprecedented casualties in the Great War.",
                "Cereal flakes are marketed.",
                "Chlorine gas used as a weapon.",
                "Gas mask invented.",
                "The zipper is patented."
            ],
            1916: [
                "Some 700,000 die in the battle of Verdun.",
                "One million die in the battle of the Somme.",
                "U.S. polio epidemic kills 7,000 and leaves 27,000 youngsters paralyzed.",
                "Gallipoli.",
                "Easter uprising.",
                "Jutland.",
                "Mechanical windshield wipers invented.",
                "General Theory of Relativity proposed.",
                "Pershing’s raid in Mexico."
            ],
            1917: [
                "United States enters WWI.",
                "The Russian Revolution unfolds and the Bolsheviks seize power.",
                "Mustard gas used in warfare.",
                "Ford mass-produces tractors.",
                "Steamer Castalia wrecked on Lake Superior, 22 men lost.",
                "Pennsylvania munitions plant explosion kills 133.",
                "1,600 dead in ship collision and explosion in Halifax, Nova Scotia."
            ],
            1918: [
                "WWI ends.",
                "Russian Civil War.",
                "Regular U.S. airmail service established.",
                "World influenza epidemic kills 21.6 million.",
                "U.S.S. Cyclops disappears after leaving Barbados.",
                "Powered flight reaches 150+ mph and 30,000+ feet.",
                "Electric clocks introduced."
            ],
            1919: [
                "Prohibition enacted in U.S.",
                "First transatlantic flight (1,880 miles in 16:12 hours).",
                "Grease-guns invented.",
                "Parachutes introduced."
            ],
            1920: [
                "Prohibition in effect in U.S.",
                "The Bolsheviks consolidate power in Russia.",
                "Earthquake in Gansu province, China, kills 200,000.",
                "First radio broadcasting station goes on the air.",
                "Teabags introduced.",
                "U.S. public debt is $24.3 billion.",
                "Women’s suffrage ratified.",
                "U.S. resident population is 105.7 million."
            ],
            1921: [
                "Rorschach devises his inkblot tests.",
                "Inflation of the German Mark begins.",
                "KDKA broadcasts sports.",
                "Capek coins the word “robot.”"
            ],
            1922: [
                "Revival and growth of the Ku Klux Klan.",
                "British dirigible AR-2 breaks in two, killing 62.",
                "Insulin is isolated.",
                "First practical postal franking machine.",
                "Soviet May Day slogans omit “world revolution.”",
                "Water-skiing invented.",
                "Mussolini marches on Rome."
            ],
            1923: [
                "Teapot Dome scandal rocks Harding administration.",
                "Big fire in Berkeley, CA destroys 600 buildings, causes $10 million in damage, and 60 deaths.",
                "German Mark stabilized.",
                "Continuing Klan violence in Georgia.",
                "Nazi putsch in Munich fails.",
                "King Tut’s tomb opened.",
                "Whooping-cough vaccine developed."
            ],
            1924: [
                "Leopold and Loeb convicted of the kidnap slaying of Bobby Franks.",
                "Paper egg cartons developed.",
                "Kleenex introduced."
            ],
            1925: [
                "W. Pauli formulates Exclusion Principle.",
                "I.G. Farben formed.",
                "Sun Yat-sen dies.",
                "In Midwest, 792 die from tornadoes in one day.",
                "U.S. dirigible Shenandoah breaks apart, killing 14.",
                "German SS formed.",
                "Scopes “Monkey Trial.”",
                "Aerial commercial crop-dusting introduced."
            ],
            1926: [
                "Dr. Goddard fires his first liquid-fuel rocket.",
                "Lightning starts a massive explosion at the U.S. Naval ammunition dump, Lake Denmark NJ—85 million in damages and 30 dead.",
                "Hurricane through Florida and Alabama leaves 243 dead.",
                "Chiang Kai-Shek stages coup in Canton.",
                "Trotsky expelled from Politburo.",
                "Rolex waterproof watch introduced."
            ],
            1927: [
                "Charles A. Lindbergh flies solo and non-stop between NYC-Paris.",
                "The Jazz Singer first feature-length sound film.",
                "First remote jukebox.",
                "Pop-up toaster introduced.",
                "Sacco and Vanzetti executed, later cleared by proclamation in 1977."
            ],
            1928: [
                "Television experiments.",
                "Southern Florida hurricane kills 1,836.",
                "Byrd expedition sails to Antarctica.",
                "Teletypes come into use.",
                "Waterproof cellophane developed.",
                "Geiger counter introduced.",
                "Vitamin C discovered."
            ],
            1929: [
                "Great stock market crash on 24 Oct.",
                "Graf Zeppelin circles the world.",
                "Russian passenger steamer Volga struck by remnant WWI mine in the Black Sea, 31 lost.",
                "16mm color film developed.",
                "Scotch tape introduced.",
                "Tune-playing automobile horn invented."
            ],
            1930: [
                "Technocracy movement at its highest.",
                "Flash bulb ends flash powder explosions at press conferences.",
                "First frozen foods marketed.",
                "Bathysphere invented.",
                "Cyclotron invented.",
                "Pluto discovered.",
                "Telescopic umbrella introduced.",
                "U.S. public debt now $16.18 billion.",
                "U.S. resident population now 122.8 million."
            ],
            1931: [
                "German millionaire support builds for Nazi Party.",
                "British Navy mutiny at Invergordon.",
                "Empire State Building formally opens.",
                "Al Capone imprisoned.",
                "Alka-Seltzer introduced.",
                "Electric razor introduced.",
                "George Washington Bridge (3,500 feet) completed."
            ],
            1932: [
                "Gandhi arrested.",
                "British submarine goes down in English Channel.",
                "Roosevelt elected President in landslide.",
                "Mussolini drains Pontine Marshes.",
                "Lindbergh baby kidnapped.",
                "First car radios introduced.",
                "First Gallup Poll conducted.",
                "Mars Bars introduced.",
                "Invention of zoom lens.",
                "Zippo lighter introduced."
            ],
            1933: [
                "Hitler named Chancellor of Germany.",
                "Japan withdraws from League of Nations.",
                "U.S. abandons gold standard.",
                "Long Beach quake kills 123.",
                "Hundreds die in Cuban rebellion.",
                "Freed Gandhi weighs 90 pounds.",
                "First German concentration camp (Dachau) established.",
                "Day-Glo pigments introduced.",
                "The game Monopoly published.",
                "Fluorescent lights introduced commercially."
            ],
            1934: [
                "Economic depression deepens as starvation and unrest spread in U.S.",
                "Drought extends from New York State to California.",
                "Sandino assassinated by Somoza supporters.",
                "San Francisco general strike ends.",
                "Huey Long assumes dictatorship of Louisiana.",
                "First commercial launderette established."
            ],
            1935: [
                "Increasingly severe dust storms batter the High Plains and Midwest of the U.S.",
                "First Pan-Am Clipper departs San Francisco for China.",
                "Social Security system enacted.",
                "Huey Long assassinated.",
                "Mao’s Long March concludes in Yenan.",
                "First passenger flight for the DC-3.",
                "Mass-market paperback books introduced.",
                "Richter earthquake scale developed.",
                "Tape recorder retailed."
            ],
            1936: [
                "Nazis enter Rhineland.",
                "Italy conquers Ethiopia.",
                "Spanish Civil War.",
                "U.S. heat wave kills 3,000.",
                "Dust-bowl conditions continue.",
                "Jesse Owens wins 4 gold medals at Berlin Olympics.",
                "Axis powers sign pact.",
                "Boulder Dam in operation.",
                "First Volkswagen introduced."
            ],
            1937: [
                "Gas explosion kills 294 in Texas school.",
                "Hindenburg dirigible explodes with loss of 36.",
                "8 Soviet generals die in Stalinist purges.",
                "DuPont patents nylon.",
                "Japanese sink U.S. gunboat Panay.",
                "Golden Gate Bridge (4,200 feet) completed.",
                "First supermarket carts introduced.",
                "Buchenwald concentration camp opens."
            ],
            1938: [
                "Mexico expropriates all foreign oil holdings.",
                "Germans enter Austria unopposed.",
                "Kristallnacht.",
                "Electric steam iron with thermostat invented.",
                "Instant coffee introduced.",
                "Nylon introduced.",
                "Ball-point pen patented.",
                "Prototype of photocopy machine developed.",
                "Major German-American Bund rally at Madison Square Garden.",
                "Arrests of Jews throughout Germany and Austria."
            ],
            1939: [
                "Germany annexes the Czechs.",
                "Madrid falls to Franco.",
                "U.S. submarine Squalus sinks with loss of 26 hands.",
                "French submarine Phoenix sinks with loss of 63.",
                "Two IRA bombs in London.",
                "Cellophane wrappers first appear in stores.",
                "Annexation of Baltic states.",
                "Germany invades Poland, and France and Britain declare war.",
                "Rockefeller Center opens.",
                "DDT introduced.",
                "Yellow-fever vaccine developed.",
                "Radar technology developed and deployed."
            ],
            1940: [
                "Finland surrenders to Soviets.",
                "Nazis strike at Denmark and Norway.",
                "Churchill becomes Prime Minister.",
                "Holland and Belgium fall.",
                "Dunkirk evacuation.",
                "Thousands die in Russo-Finnish War.",
                "German blitzkrieg to Channel.",
                "Bombings in Germany and England kill tens of thousands.",
                "Roosevelt elected for third term.",
                "Automatic gearbox for automobiles introduced.",
                "Inflatable life vests introduced.",
                "Radar operational and deployed in Britain.",
                "Artificial insemination developed.",
                "Penicillin produced in quantity.",
                "U.S. public debt now $42.97 billion.",
                "U.S. resident population now 131.7 million."
            ],
            1941: [
                "Aerial battle of Britain joined.",
                "Lend-Lease policy enacted.",
                "U.S. institutes military draft.",
                "About 2,500 die in Japanese raid on Pearl Harbor.",
                "Coconut Grove (Boston) nightclub fire kills 491.",
                "Jeep adopted as general-purpose military vehicle.",
                "Germans invade Soviet Union."
            ],
            1942: [
                "Singapore and Philippines fall.",
                "Major carrier battle off Midway Island.",
                "German siege of Leningrad continues.",
                "Crimea falls.",
                "Doolittle raid on Tokyo.",
                "Battle of Stalingrad joined.",
                "U.S. lands on Guadalcanal.",
                "Allies land in North Africa.",
                "Atomic fission achieved.",
                "Bazooka introduced.",
                "Napalm introduced."
            ],
            1943: [
                "Some 190,000 Germans and greater numbers of Soviet soldiers and civilians die at Stalingrad.",
                "Germans surrender at Stalingrad.",
                "Warsaw Ghetto uprising.",
                "Germany defeated in the biggest tank battle (Kursk) in history.",
                "Allies land in Sicily.",
                "Mussolini deposed then reseated by Germans.",
                "Allies invade Italy.",
                "Soviets crack Dnieper River line.",
                "Marshall Islands falls.",
                "29 die in Detroit race riots.",
                "Ball-point pens gain first acceptance.",
                "Aqualung invented.",
                "LSD synthesized."
            ],
            1944: [
                "De Gaulle is Free-French commander-in-chief.",
                "Continuing massive air raids on Germany.",
                "Crimea freed.",
                "Allies take Rome.",
                "D-Day landings in Normandy.",
                "Marianas under attack.",
                "Paris falls to Allies.",
                "Roosevelt re-elected for fourth term.",
                "Mass killings in Nazi concentration camps revealed.",
                "V-1 and V-2 missiles hit London.",
                "MacArthur returns to Philippines.",
                "Battle of the Bulge.",
                "Hurricane kills 46 along East Coast, and 344 more at sea.",
                "Ringling Bros. tent fire kills 168.",
                "Ammunition explosion kills 322 at Port Chicago, CA.",
                "Nerve gas developed."
            ],
            1945: [
                "Some 130,000 die in Dresden firebombing.",
                "60,000 die from nuclear blast at Nagasaki, and other mass bombings kill hundreds of thousands more in Japan.",
                "Total casualties of WWII are estimated at 50 million people.",
                "Europe and Japan need 15 years to effect significant recovery.",
                "U.S. war-related dead total 405,399.",
                "Auschwitz liberated.",
                "Yalta conference.",
                "Iwo Jima falls.",
                "Remagen Bridge taken.",
                "Roosevelt dies.",
                "Mussolini executed.",
                "Hitler commits suicide.",
                "Full extent of Nazi death camps revealed.",
                "Berlin falls.",
                "Churchill resigns.",
                "Battle of Okinawa.",
                "United Nations formed.",
                "Potsdam conference.",
                "Japan surrenders.",
                "Korea partitioned.",
                "Jackie Robinson becomes the first modern African-American major leaguer.",
                "Nuremberg war-crime trials.",
                "Tupperware introduced."
            ],
            1946: [
                "Chicago hotel fire kills 58.",
                "ENIAC computer unveiled by War Department.",
                "Churchill proclaims Iron Curtain.",
                "Violence continues in Palestine.",
                "Labor strikes dot U.S.",
                "Chinese Civil War renewed.",
                "Smoking said to cause lung cancer.",
                "Uprising in Vietnam.",
                "Chester F. Carlson unveils 'xerography'.",
                "Bikini swimsuits introduced.",
                "Espresso coffee machines invented."
            ],
            1947: [
                "U.S. gives up attempts to broker a peace in China.",
                "Religious strife in India.",
                "Marshall Plan advanced.",
                "Last New York streetcar retired.",
                "India and Pakistan independent.",
                "Polaroid Land Camera introduced.",
                "House committee looks for subversives in films."
            ],
            1948: [
                "Gandhi assassinated.",
                "Communist coup in Czechoslovakia.",
                "Civil war continues in the Palestine Mandate.",
                "Berlin airlift starts.",
                "State of Israel recognized and war continues.",
                "200-inch telescope at Mt. Palomar.",
                "New York subway fare doubles to ten cents.",
                "Kinsey Report on sex.",
                "Scrabble introduced.",
                "Solid-body electric guitar developed.",
                "Velcro invented.",
                "Transistor developed at Bell Labs.",
                "33 1/3 long-playing records introduced."
            ],
            1949: [
                "Chinese Communists take Peking.",
                "NATO organized.",
                "Berlin blockade concludes.",
                "German Federal Republic created.",
                "Red scare continues in U.S.",
                "USSR explodes nuclear device.",
                "Nationalist Chinese forces retreat to Taiwan.",
                "Indonesia achieves independence.",
                "Cable television introduced.",
                "Color television tube developed.",
                "Key-starting auto ignitions introduced."
            ],
            1950: [
                "One-piece windshield for Cadillacs.",
                "RCA announces color television.",
                "French appeal for aid against the Viet Minh.",
                "U.S. blizzards kill hundreds.",
                "Thousands die as Korean War begins.",
                "Inchon landings.",
                "China enters the Korean War.",
                "Gussie Moran sports lace underwear at Wimbledon.",
                "Diners’ Club card introduced.",
                "Xerox 914 commercial copier introduced.",
                "U.S. public debt now $256 billion.",
                "U.S. resident population is now 150.7 million."
            ],
            1951: [
                "MacArthur stripped of all commands.",
                "50 die in U.S. plane crash.",
                "Color television transmitted from Empire State Building.",
                "Hydrogen bomb tests at Eniwetok.",
                "Truce talks in Korea.",
                "Cinerama introduced.",
                "Chrysler introduces power steering.",
                "3-color stoplights for autos introduced."
            ],
            1952: [
                "Queen Elizabeth II accedes to British throne.",
                "Worst U.S. bus crash kills 28.",
                "French submarine La Sybille disappears in Mediterranean with 49 aboard.",
                "U.S. polio epidemic kills 3,300 and affects 57,000 children.",
                "Walk/Don’t Walk lighted pedestrian signs in New York City.",
                "GM offers built-in air conditioning in some 1953 cars.",
                "Eva Peron dies.",
                "Transistorized hearing aid introduced.",
                "Hydrogen bomb announced.",
                "Videotape introduced."
            ],
            1953: [
                "Joseph Stalin dies.",
                "Storms off North Sea kill 200 in Britain.",
                "DNA described as double helix in form.",
                "Pius XII approves of psychoanalysis in therapy.",
                "Rosenbergs executed.",
                "East Berlin uprising quashed.",
                "Korean armistice.",
                "U.S. flight to suburbs noted.",
                "Kennedy-Bouvier marriage.",
                "Expedition searches for yeti.",
                "Measles vaccine introduced."
            ],
            1954: [
                "Nautilus is first atomic-powered submarine.",
                "Army-McCarthy hearings.",
                "Murrow takes on McCarthy.",
                "Dien Bien Phu falls.",
                "First H-bomb exploded.",
                "Supreme Court orders school integration.",
                "North and South Vietnam established.",
                "Retractable ball-point pen introduced.",
                "Silicon transistor developed."
            ],
            1955: [
                "Missile with atomic warhead exploded in Nevada test.",
                "Hurricane Diane kills 184.",
                "Albert Einstein dies.",
                "Warsaw Pact treaty signed.",
                "Rebellion in Algeria.",
                "Mickey Mouse Club debuts on television.",
                "Air-to-air guided missile introduced.",
                "Disneyland opens."
            ],
            1956: [
                "Over 10,000 Mau-Mau rebels killed in 4 years.",
                "Bus boycott in Montgomery.",
                "Suburbs boom in U.S.",
                "Khrushchev denounces Stalin.",
                "Nasser seizes Suez Canal.",
                "Hungarian Revolt.",
                "Teon Company formed.",
                "Go-karts introduced."
            ],
            1957: [
                "Smoking shown to promote cancer.",
                "Nike Hercules atomic warheads to defend U.S. cities from enemy aircraft.",
                "Sputnik shocks U.S.",
                "Mackinac Straits Bridge (3,800 feet) completed."
            ],
            1958: [
                "Elvis Presley drafted.",
                "90 die in Chicago school fire.",
                "Nautilus sails across North Pole under the ice.",
                "Faubus closes Little Rock’s high schools.",
                "Pan Am inaugurates first 707 jet service to Paris.",
                "Sabin polio vaccine introduced.",
                "Communications satellite introduced.",
                "Hula-hoop introduced."
            ],
            1959: [
                "Castro gains power in Cuba.",
                "Ford’s Edsel judged a failure.",
                "Volvo introduces safety belts."
            ],
            1960: [
                "Unrest continues in Algeria.",
                "Hurricane Donna devastates U.S. East Coast and Puerto Rico, claiming 165 lives.",
                "Artificial kidney introduced.",
                "Lunch counter sit-ins begin.",
                "Brasilia (the first public-relations city) is open for business.",
                "Birth control pill goes on sale in U.S.",
                "First weather satellite.",
                "Popularity of portable transistor radios begins.",
                "U.S. public debt now $284 billion.",
                "U.S. resident population is now 179.3 million."
            ],
            1961: [
                "Eisenhower warns against military-industrial complex.",
                "The Leakeys find earliest human remains.",
                "Berlin Wall erected.",
                "Peace Corps established.",
                "Bay of Pigs landing in Cuba.",
                "Valium introduced."
            ],
            1962: [
                "Cuban missile crisis nearly brings nuclear war.",
                "Gallium-arsenide semiconductor laser developed.",
                "First satellite link between the U.S. and the UK.",
                "Polaroid color film introduced."
            ],
            1963: [
                "Enormous civil rights demonstration in Washington.",
                "Kennedy assassinated.",
                "Coup in Vietnam removes Diem.",
                "Cold wave in U.S. kills 150.",
                "Hurricane Flora kills 7,000 in Haiti and Cuba.",
                "Mob actions increasingly common in the South."
            ],
            1964: [
                "Aswan Dam in service.",
                "Beatles enormously popular.",
                "U.S. accidentally releases a kilo of plutonium into atmosphere.",
                "Nehru dies.",
                "Verrazano-Narrows Bridge (4,260 feet) completed.",
                "LBJ signs Civil Rights Act.",
                "Tonkin Gulf resolution.",
                "3-D laser-holography introduced.",
                "Moog synthesizer introduced.",
                "FTC requires health warning on cigarettes."
            ],
            1965: [
                "Malcolm X assassinated.",
                "Race riots in Watts.",
                "Pope disassociates Jews from guilt for the crucifixion of Jesus.",
                "Great Northeastern states’ electrical blackout.",
                "Kevlar introduced.",
                "Radial tires introduced.",
                "IBM word processor introduced."
            ],
            1966: [
                "Cultural Revolution in China.",
                "Opposition to Vietnam War increases.",
                "Sniper kills 12 at U. Texas.",
                "Miniskirts introduced.",
                "First black Senator elected by popular vote.",
                "Dolby-A introduced.",
                "Skateboards introduced.",
                "Body counts introduced."
            ],
            1967: [
                "The Six-Day War.",
                "The Summer of Love.",
                "First black Supreme Court justice appointed.",
                "3 astronauts die in Apollo fire.",
                "U.S. loses 500th plane over Vietnam.",
                "Newark race riots leave 26 dead in four days.",
                "31 deaths in Detroit race riots.",
                "Antiwar protests accelerate.",
                "Body count now a regular feature of Vietnam reports.",
                "209 pounds of heroin seized in Georgia.",
                "Bell bottoms introduced."
            ],
            1968: [
                "Tet Offensive stuns civilian United States.",
                "Martin Luther King assassinated.",
                "Black riots.",
                "Student revolt in Paris.",
                "Robert Kennedy assassinated.",
                "B-52 carrying four H-bombs crashes in a Greenland bay.",
                "Soviets quash liberalizing Czech government.",
                "Spain voids 1492 law banning Jews.",
                "Democrats’ convention in Chicago battles protesters.",
                "Apollo 8 astronauts orbit the Moon."
            ],
            1969: [
                "Skyjackings to Cuba continue.",
                "Barnard women integrate men’s dorm.",
                "First artificial heart implant.",
                "Anti-Vietnam War demonstrations in more than 40 cities on same weekend.",
                "Woodstock.",
                "250,000 protesters march on capital.",
                "Apollo 11 lands on the Moon.",
                "Snowstorm of the decade closes New York City.",
                "My Lai massacre revealed to have taken place in 1968.",
                "Boeing 747 jumbo jet.",
                "Oil spill fouls Santa Barbara beaches.",
                "First flight of Concorde Mach 2 jetliner."
            ],
            1970: [
                "Radical chic.",
                "Palestinian group hijacks five planes.",
                "De Gaulle dies.",
                "46 shot in Asbury Park riots.",
                "\"Weathermen\" arrested for bomb plot.",
                "Tuna recalled as mercury-contaminated.",
                "Bar codes introduced.",
                "Floppy disks introduced.",
                "Windsurfing introduced.",
                "U.S. public debt now $370 billion.",
                "U.S. resident population is now 203.3 million."
            ],
            1971: [
                "Quake in Los Angeles kills 51.",
                "Reaction against drug use in armed forces at full tide.",
                "Hot pants introduced.",
                "Pentagon Papers printed.",
                "Liquid crystal displays introduced."
            ],
            1972: [
                "Ten members in European Common Market.",
                "Nixon in China.",
                "Burglars caught in Democrats’ Watergate headquarters.",
                "11 Israelis massacred at Olympics.",
                "Airline anti-hijacking procedures established in U.S.",
                "Electronic pocket calculators introduced.",
                "Pong video game introduced."
            ],
            1973: [
                "Last trip to Moon.",
                "Oil embargo.",
                "Bosporus Bridge (3,524 feet) completed.",
                "Recombinant DNA introduced."
            ],
            1974: [
                "Patty Hearst is kidnapped by Symbionese Liberation \"Army\".",
                "Widespread gasoline shortage in U.S.",
                "Nixon resigns from Presidency.",
                "Tornadoes kill 315 in two days in U.S.",
                "Green Revolution agricultural technology introduced."
            ],
            1975: [
                "South Vietnam falls.",
                "Cambodia falls.",
                "Civil war in Beirut.",
                "Atari video games introduced."
            ],
            1976: [
                "Extinction of animal species a public concern.",
                "Mao Tse-tung dies.",
                "Hurricane Lizzie leaves 2,500 dead in Mexico.",
                "Cray I supercomputer introduced."
            ],
            1977: [
                "Trans-Alaskan oil pipeline in operation.",
                "Three Israeli settlements approved on West Bank.",
                "Optical fiber telephone line introduced.",
                "Last trip of Orient Express.",
                "Protesters try to stop Seabrook nuclear power plant."
            ],
            1978: [
                "Panama Canal to be controlled by Panama.",
                "Proposition 13 wins in California, heralding decline of capital expenditures across the nation.",
                "1 U.S. dollar equals 175 Japanese yen.",
                "Air collision over San Diego kills 150.",
                "909 die in Jonestown mass suicide.",
                "First test-tube baby born in London."
            ],
            1979: [
                "The Shah flees Iran.",
                "3-Mile Island nuclear power plant leak.",
                "Somoza ousted in Nicaragua.",
                "U.S. embassy in Tehran seized and hostages held.",
                "Soviets enter Afghanistan.",
                "Rubik’s cube introduced.",
                "Sony Walkman introduced."
            ],
            1980: [
                "An ounce of gold reaches $802 U.S.",
                "U.S. inflation rate highest in 33 years.",
                "Banking deregulated.",
                "Mt. St. Helens WA eruption kills 50+.",
                "Hostage rescue fails in Iran.",
                "Solidarity recognized in Poland.",
                "Gold rush in the Amazon.",
                "Dolby-C.",
                "U.S. public debt now $908 billion.",
                "U.S. resident population is now 226.5 million."
            ],
            1981: [
                "Iran releases embassy hostages.",
                "Millions in Poland on strike.",
                "U.S. public debt reaches one trillion dollars.",
                "Israeli raid destroys Iraqi nuclear reactor.",
                "Humber Bridge (4,626 feet) completed.",
                "Widespread marches and rallies against nuclear weapons and arms in Europe.",
                "Strange immune-system disease noted by CDC."
            ],
            1982: [
                "Worldwide oil glut.",
                "War for Falkland Islands.",
                "Airliner smashes into Potomac bridge, kills 78.",
                "84 die as Newfoundland oil rig sinks.",
                "New Orleans airliner crash kills 149.",
                "800,000 march against nuclear weapons in New York City.",
                "Israeli incursion reaches Beirut; PLO moves to Tunisia."
            ],
            1983: [
                "Aquino assassinated upon arriving in Manila.",
                "Widespread missile protests in Europe.",
                "World population estimated at 4.7 billion."
            ],
            1984: [
                "VCR taping legalized in U.S.",
                "Iran-Iraq war now involves oil tankers in Persian Gulf.",
                "Indonesian death squads reportedly kill some 4,000 people.",
                "Battles in Beirut continue.",
                "AIDS virus isolated.",
                "Federal estimate of 350,000 homeless in U.S.",
                "Passive inhalation of cigarette smoke held to cause disease.",
                "900,000 march in Manila; President Reagan asks if you’ve ever had it so good."
            ],
            1985: [
                "Kidnappings continue in Beirut.",
                "Gorbachev chosen as USSR chairman.",
                "Rock Hudson hospitalized for AIDS.",
                "France sinks Greenpeace vessel.",
                "Quake devastates Mexico City leaving 25,000 dead.",
                "U.S. trade balance now negative.",
                "Terrorism becomes widespread tactic of splinter groups.",
                "Achille Lauro hijacking and murders.",
                "Massive federal spending continues to fuel economic expansion.",
                "U.S. public debt now $1.82 trillion, doubled since 1980."
            ],
            1986: [
                "Challenger shuttle explosion effectively shuts down NASA manned program for several years.",
                "English Channel tunnel project okayed.",
                "At Chernobyl, dozens of heroes sacrifice themselves to contain the disaster and in the years to come, experts expect 24,000 deaths to be influenced by the released atomic cloud.",
                "Crack cocaine epidemic in U.S."
            ],
            1987: [
                "One million dead in Iran-Iraq War.",
                "Dow average loses 508 points in one day.",
                "This year 13,468 AIDS deaths in U.S.",
                "Arabs within Israel begin general resistance.",
                "50 million VCRs in U.S."
            ],
            1988: [
                "The term “Greenhouse Effect” is widely used.",
                "Pan-Am jetliner explodes over Lockerbie, Scotland, 259 aboard.",
                "Armenian earthquake kills 25,000 and leaves 400,000 homeless.",
                "RU-486.",
                "Widespread drought in U.S.",
                "U.S. AIDS cases top 60,000.",
                "U.S. estimated to have spent $51.6 billion on illegal drugs this year."
            ],
            1989: [
                "The U.S. \"war on drugs\" intensifies.",
                "Political stress in the Soviet Union.",
                "U.S.S. Iowa’s turret explodes, killing 42.",
                "Hurricane Hugo leaves 71 dead.",
                "Salman Rushdie affair begins.",
                "Panama invasion topples Noriega.",
                "Tiananmen Square demonstrations in Beijing.",
                "Federally insured bank losses in U.S. estimated at $500 billion dollars.",
                "CDs become dominant playback medium in the United States."
            ],
            1990: [
                "Iraq invades Kuwait, and U.S. organizes expeditionary force in opposition.",
                "South African government lifts emergency decrees.",
                "U.S. public debt at $3.23 trillion.",
                "Hubble telescope fiasco.",
                "U.S. estimated to have spent $40 billion on illegal drugs this year.",
                "U.S. resident population now 248.7 million."
            ],
            1991: [
                "Gulf War kills at least 50,000 Iraqis.",
                "Iraq releases 40 million gallons of crude oil into the Persian Gulf, and leaves some 600 oil wells afire.",
                "Oakland Hills fire burns some 3,000 homes and leaves dozens dead.",
                "Massive eruptions of Mt. Pinatubo on Luzon.",
                "Coup foiled in USSR; Arab-Israeli talks.",
                "At the end of May, AIDS deaths in the U.S. total 113,426.",
                "Import auto sales now account for 1/3 of the U.S. market.",
                "USSR dissolves into constituent republics; Gorbachev resigns.",
                "One-fifth of sub-Saharan college graduates believed to be HIV+."
            ],
            1992: [
                "Economic recession in industrial nations, homelessness and mass layoffs widely reported.",
                "Rioting in Los Angeles and other U.S. cities over Rodney King verdict, 52 killed and damages over $1 billion.",
                "U.S. military deployed to aid against famine amid Somalia civil war.",
                "Tens of thousands massacred during \"ethnic cleansing\" in former Yugoslavia.",
                "Hurricanes in Florida, Louisiana, and Hawaii kill dozens and leave thousands homeless.",
                "Major earthquakes in Southern California and Egypt cause extensive damage.",
                "Estimated 13 million people now infected with HIV virus.",
                "Czechs and Slovaks separate."
            ],
            1993: [
                "Terrorists bomb NY World Trade Center.",
                "FBI lays siege to Branch Davidians near Waco, and 80 ultimately die.",
                "Clinton first Democratic President since Carter.",
                "Strife continues in Bosnia.",
                "North Korea withdraws from nuclear nonproliferation treaty.",
                "U.S. troops withdrawn from Somalia.",
                "Congress votes over 130 U.S. military bases closed.",
                "U.S. unemployment declines.",
                "U.S. national debt $4.35 trillion."
            ],
            1994: [
                "NAFTA agreement ratified by all parties.",
                "CIA’s Aldrich Ames found to be Russian spy.",
                "Anglican Church ordains first female priests.",
                "First universal-suffrage election in South Africa signals end of white dominance.",
                "Israel and PLO sign self-rule accord.",
                "O.J. Simpson charged in 2 murders.",
                "Fifty years since WWII Normandy landings.",
                "Professional baseball strike marks the decline of that sport.",
                "U.S. lands in Haiti and successfully returns Aristide to presidency."
            ],
            1995: [
                "Shoemaker-Levi 9 comet cluster hurls into Jupiter.",
                "Terrorist bomb smashes Oklahoma City federal building, killing 161.",
                "In the U.S., about one in ten are wired into the internet.",
                "O.J. Simpson acquitted of murder.",
                "Peace progresses in Northern Ireland, Bosnia, and Middle East.",
                "Rabin assassinated in Israel.",
                "Colin Powell declines to run for U.S. presidency.",
                "U.S. federal debt at $5 trillion."
            ],
            1996: [
                "U.S. federal workers return to work after budget crisis.",
                "One killed when bomb explodes at Atlanta Olympic Games.",
                "Earth’s recent average surface temperature rises to new high.",
                "Coldest winter in Minnesota in nearly a hundred years.",
                "Mt. Everest climbing deaths rise steadily.",
                "Islamic rebels capture Kabul.",
                "Abortion struggle continues in Senate.",
                "Copyright piracy continues friction between U.S. and China.",
                "U.S. national debt at $5.2 trillion.",
                "Prosperity reigns in U.S.",
                "Ill-conceived attempts to control immigration and drug-addiction.",
                "McVeigh held in Oklahoma City bombing.",
                "Kaczinski indicted as Unabomber suspect."
            ],
            1997: [
                "Haitian ferry Pride of la Gonave sinks with 200+ dead.",
                "New AIDS infections estimated at more than 3 million.",
                "Approximately 5.8 million now have died from the disease.",
                "Approx. 275 million residents of U.S.",
                "40% of the U.S. now connected to the internet.",
                "Clinton under heavy pressure concerning sexual conduct.",
                "Dow-Jones average breaks 8,000 in July.",
                "Tobacco companies admit that tobacco is addictive.",
                "Comet Hale-Bopp passes nearby in March.",
                "Hong Kong reverts to China.",
                "Ames Research Center to have department of astrobiology.",
                "Diana, Princess of Wales, dead in auto crash.",
                "Ted Turner gives $1 billion to United Nations."
            ],
            1998: [
                "Pres. Clinton under cloud from possible perjury and obstruction of justice.",
                "U.S. economic expansion shows signs of slowing.",
                "El Niño soddens California and sends violent storms across the Midwest.",
                "Storms in Europe.",
                "Tornadoes in Alabama kill 34.",
                "Kaczinski pleads guilty to unabombings.",
                "U.S. federal budget shows small surplus for the first time in 30 years.",
                "Rwanda executes 22 for genocide.",
                "Iraq wages apparently successful end to UN weapons inspections.",
                "Economic and social turmoil continue in Russia.",
                "Passenger arrivals and departures at Chicago O’Hare number 70 million in 1997."
            ],
            1999: [
                "Pres. Clinton impeached by the House, but the Senate acquits him.",
                "U.S. economy surges; Dow Jones average finishes above 11,000 for first time in history.",
                "Very large balance of payment deficits for U.S.",
                "Violent crime in U.S. has not been lower since 1973.",
                "AMA approves a union for medical doctors."
            ],
            2000: [
                "U.S. stock market bubbles burst, ending talk of linking social security with stocks and other financial instruments.",
                "Russian nuclear submarine sinks in Barents Sea, 118 die.",
                "Air France Concorde smashes into hotel, 113 die.",
                "Mexico’s PRI loses presidency for the first time in 71 years.",
                "Edward Gorey dies at 75.",
                "Bush elected U.S. president."
            ],
            2001: [
                "World population estimated at 6.2 billion.",
                "Combined terrorist attacks kill some 3,000 in New York and Virginia.",
                "Submarine U.S.S. Greenville surfaces underneath a Japanese trawler, killing 9.",
                "AIDS infections in previous year estimated at 5.3 million.",
                "Total AIDS deaths placed at 21.8 million.",
                "New observations of “dark energy” and “dark matter” force re-evaluation of previously held cosmology.",
                "Solar-powered aircraft Helios reaches 96,500 feet.",
                "Some 55% of U.S. households contain computers.",
                "Senate and House offices closed because of anthrax contamination, and at least 5 elsewhere die from it.",
                "U.S. armed forces enter Afghanistan."
            ],
            2002: [
                "President Bush perceives an axis of evil, and many listen carefully.",
                "North Korea reports that it has secretly produced nuclear bombs.",
                "The Euro becomes official currency of Austria, Belgium, Finland, France, Germany, Greece, Ireland, Italy, Luxembourg, the Netherlands, Portugal, and Spain.",
                "Milosevic war crimes trial begins.",
                "Enormous accounting frauds and subsequent U.S. business bankruptcies come to light.",
                "Piracy blamed, not quality, as sales of recorded music and music videos continue to drop across the world."
            ],
            2003: [
                "Enormous power outage betrays summertime northeast U.S. and eastern Canada.",
                "Europe swelters in unprecedented heat wave—deaths of more than 11,000 in France alone are attributed to extended European temperatures of above 105°F.",
                "The Galileo space probe is sent crashing into Jupiter, concluding its fourteen-year mission among the outer planets.",
                "Previously unknown to primatologists, a mysterious species of ape found in the northern Congo, resembling a cross between gorilla and chimpanzee, but larger than either."
            ],
            2004: [
                "Terrorists on 4 rush hour trains kill 191 people in Madrid; 335 people killed and at least 700 people injured when Russian forces end the siege of a school in Beslan, Northern Ossetia.",
                "The largest passenger ship afloat is named the Queen Mary 2 by Her Majesty Queen Elizabeth II, and sets off on its maiden voyage.",
                "The Hutton Inquiry in London announces that it is satisfied that the British Government did not 'sex up' the dossier presenting the case for going to war in Iraq.",
                "The CIA admits that prior to the invasion of Iraq there was no imminent threat from weapons of mass destruction.",
                "Mount St. Helens becomes active again.",
                "Taipei 101 opens, it is the world’s tallest skyscraper at 509 meters."
            ],
            2005: [
                "Hurricane Katrina makes landfall along the U.S. Gulf Coast, killing over 1,800 people.",
                "Virgin Atlantic Global Flyer breaks the world record for the fastest solo flight around the world.",
                "A leap second is added to end the year."
            ],
            2006: [
                "North Korea claims to have conducted its first nuclear test.",
                "The 250th anniversary of the birth of Wolfgang Amadeus Mozart is celebrated."
            ],
            2007: [
                "Russia declares the resumption of strategic bomber flight exercises.",
                "Harry Potter and the Deathly Hallows is released and becomes the fastest-selling book in publishing history."
            ],
            2008: [
                "Bernard Madoff is arrested for committing the largest financial fraud in history.",
                "Barack Obama is elected the 44th President of the United States and the first President of African-American origin.",
                "The Wilkins Ice Shelf in Antarctica disintegrates, leaving the entire shelf at risk of breakup.",
                "Lehman Brothers goes bankrupt and sparks the beginning of a global financial crisis. Pirate activity increases off the coast of Somalia."
            ],
            2009: [
                "The Icelandic banking system collapses.",
                "An outbreak of the H1N1 influenza strain, 'Swine Flu,' reaches pandemic proportions.",
                "The longest total solar eclipse of the 21st century takes place on 22nd July, lasting up to 6 minutes and 38.8 seconds, occurring over Asia and the Pacific Ocean."
            ],
            2010: [
                "The Deepwater Horizon oil platform explodes in the Gulf of Mexico, eleven oil workers die and oil spills from the uncapped well for seven months.",
                "The Eyjafjallajökull volcano erupts beneath an Icelandic ice cap, spewing ash into the atmosphere that shuts down air travel across Europe.",
                "Hundreds of thousands of secret American diplomatic cables are released by the website WikiLeaks."
            ],
            2011: [
                "The Iraq War is declared over by the United States.",
                "Japan is hit by a 9.1 magnitude earthquake, the subsequent tsunami adds to the death toll and causes a crisis in four coastal nuclear power plants.",
                "The global population is judged to have reached seven billion.",
                "Osama bin Laden, figurehead of Al-Qaeda, is killed by American special forces in Pakistan.",
                "Street vendor Mohamed Bouazizi sets himself on fire in Tunisia, his death inspiring a revolutionary movement that topples the Tunisian government; similar revolutions occur across the Middle East."
            ],
            2012: [
                "Diamond Jubilee of Queen Elizabeth II.",
                "Arab Spring.",
                "The century’s second and last solar transit of Venus occurs.",
                "Tokyo Skytree, the tallest self-supporting tower in the world (634 meters high), is opened to the public.",
                "CERN announces the discovery of the Higgs Boson ‘god particle’.",
                "Austrian skydiver, Felix Baumgartner, becomes the first person to break the sound barrier without machine assistance when he jumps 24 miles to earth at Roswell, New Mexico."
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
