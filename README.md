# Call of Cthulhu by Chaosium .inc
To be able to play Call of Cthulhu you will need Keepers Rulebook, Call of Cthulhu Starter set or Pulp of Cthulhu published by Chaosium .inc

[Call of Cthulhu Keeper Rulebook](https://www.chaosium.com/call-of-cthulhu-keeper-rulebook-hardcover/)

[Call of Cthulhu Starter Set](https://www.chaosium.com/call-of-cthulhu-starter-set/)

[Pulp Cthulhu](https://www.chaosium.com/pulp-cthulhu-hardcover/)

# Cthulhu Cog Install
!repo add senpaicz https://github.com/SenpaiCZ/RedBot

!cog install senpaicz CthulhuCog

# Cthulhu Cog Info
🐙 Elevate Your Call of Cthulhu RPG Experience with the Cthulhu Discord Cog! 🤖🎲

Attention all tabletop RPG enthusiasts! I'm thrilled to introduce the Cthulhu Discord Cog, your ultimate companion for immersive Call of Cthulhu gaming sessions. Designed to streamline and enhance your gameplay, this COG brings a range of features to your fingertips.

🎮 Seamlessly Manage Sessions: With intuitive commands, effortlessly roll dice, perform skill checks, and handle character actions—all within the Discord environment.

🕵️‍♂️ Create Investigators on the Fly: Generate investigator characters with ease, complete with random stats, backstories, and even inventory management.

🔍 Quick References at Your Fingertips: Access valuable game information, including skill lists, occupations, historical context, NPC generation, and more.

📜 Enhance the Storytelling: Unleash your creativity with the ability to generate random names and NPCs, injecting spontaneity into your narratives.

Whether you're a Keeper masterfully crafting the storyline or an investigator navigating through the mysteries, the Cthulhu Discord Cog is your trusty ally, making the Call of Cthulhu RPG smoother and more captivating than ever before.

Step into the realm of eldritch horrors and gripping narratives with the Cthulhu Discord Cog. Level up your Call of Cthulhu gameplay and embark on unforgettable adventures with the power of Discord and this versatile COG. Uncover the unknown and challenge the cosmic horrors that await!

# To-Do list
- Automatic Chase
- Beasts and Gods
- Magic
- Traveltime between cities
- Cars, horses and other trasport
- More random stuff and info :)

# Generate random name with !cname male/female

![Generating random name](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/randomName.jpg)

# Create Investigator

![Create Investigator](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/newInv.jpg)

# Generate random character stats

![Generating random character stats](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/autoChar.jpg)

# Change skill or stat

![Edit stat of your character](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/cstat%20STR.jpg)

![Edit skill of your character](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/cstat%20Listen.jpg)

# After filling all requered stat bot will calculate HP, MP, SAN, MOV, Damage Bonus and Build and save them to your investigator.

![Autofill](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/cstat%20POW%20calculate.jpg)

# Show character stats

![Show character stats](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/myChar1.jpg)

![Show character stats](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/myChar2.jpg)

![Show character stats](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/myChar3.jpg)

# Roll die or multiple

![Roll die](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/d%203D6.jpg)

# Check for skill

![Roll for skill](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/d%20Listen.jpg)

![Roll for skill](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/db%20Listen.jpg)

![Roll for skill](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/dp%20Listen.jpg)

# Using luck for rolls (max is 10 LUCK)

![Using luck](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/d%20Listen%20Use%20luck.jpg)

![using luck](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/d%20Listen%20Used%20luck.jpg)

# Inventory and backstory

![Generate random backstory](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/Inventory%20and%20backstory.jpg)

# Generate random NPC

![Generated random NPC](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/cNPC.jpg)

# Rename skill

![Rename skill](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/renameSkill.jpg)

# Delete investigator

![Delete Investigator](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/img/deleteInvestigator.jpg)

# Cthulhu Cog Commands

| Command                                  | Description                                 |
|------------------------------------------|---------------------------------------------|
| !coc / !cthulhuhelp                                  | Show all commands in discord with examples and descriptions.                    |
| !d YDX                                   | Roll dice (e.g. !d 3D6)                     |
| !d <skill>                               | Roll D100 against a skill (e.g. !d Listen)                |
| !db <skill>                              | Roll D100 against a skill with a bonus      |
| !dp <skill>                              | Roll D100 against a skill with a penalty    |
| !newInv name                                  | Create a new investigator                   |
| !autoChar                                | Generate random stats for an investigator if your stats are 0   |
| !mychar                                  | Show stats and skills                       |
| !cstat statName                       | Edit investigator stats                     |
| !cskill skillName                     | Edit investigator skills                    |
| !deleteInvestigator                      | Delete your investigator (you will be prompted to confirm deletion)                   |
| !mb                                      | Show backstory and inventory                |
| !cb category - item                   | Add a record to backstory or inventory     |
| !rb category itemID                | Delete a record from backstory or inventory|
| !cname male/female                     | Generate a random name                      |
| !cNPC male/female                      | Generate an NPC                             |
| !skillinfo skillName                  | Get info about a specific skill (without name of the skill you will get list of skills)            |                    |
| !coccupations occupationName          | Get info about a specific occupation (without name you will get list of occupations)       |
| !gbackstory                              | Generate a random backstory (it will not be saved to your investigator)                 |
| !cyear year                            | Historical information about a year         |
| !firearms name                            | Information about firearms in CoC from 1920s and modern (without name you will get list of weapons)        |
| !cloot                       | Generate random loot from 1920 (25% for money being inclooded)        |
| !rskill skill1 skill2                    | Rename skill to your liking. If your language is English you can rename Language (own) to English. You can also use 3 custom skills.    |
| !showUserData                  | Debug command. Shows raw data saved for user who calls the command (stats, skill, backstory).  |

# Change Log

31st August 2023 - New Features and Enhancements

**Automatic Calculations:** After filling in all the required stats, the system now automatically calculates HP, MP, LUCK, MOV, BUILD, and Damage Bonus. This streamlines the process and ensures accurate character progression.

**Simplified Language (own) and Dodge:** Language (own) and Dodge stats will now be automatically populated as you fill in other related stats, reducing manual input.

**MAX_MP and MAX_HP:** Introducing MAX_MP and MAX_HP stats that are automatically updated upon calculation. You can edit these values just like regular stats.

These enhancements aim to make character management more efficient and provide you with a smoother gameplay experience. Enjoy your adventures in the world of Cthulhu!
