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


# Generate random name with !cname male/female

![Generating random name](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/name.jpg)

# Generate random character stats

![Generating random character stats](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/autochar.jpg)

# Change skill or stat

![Edit skill of your character](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/cskill.jpg)

# Show character stats

![Show character stats](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/mcs1.jpg)

![Show character stats](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/mcs2.jpg)

![Show character stats](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/mcs3.jpg)

# Roll die or multiple

![Roll 3D6](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/d.jpg)

# Check for skill

![Roll for skill](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/d%20listen.jpg)

# Using luck for rolls (in this example its roll with bonus die)

![Using luck](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/use%20luck.jpg)

![using luck](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/use%20luck%202.jpg)

# Generate random NPC

![Generated random NPC](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/random%20npc.jpg)

# Get info about skills

![List of skills](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/skillinfo.jpg)
![Show occult skill](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/skillinfo%20occult.jpg)

# Get info about occupations

![List of occupations](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/occupations.jpg)
![Get info about librarian](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/occupations%20librarian.jpg)

# Get info about year

![Year info](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/year%201923.jpg)

# Generate backstory

![Generate random backstory](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/backstory%20generator.jpg)

# Show information about firearms

![Firearms information](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/firearms.jpg)

![Firearms information](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/firearms2.jpg)

# Random loot generator

![Loot generator](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/loot%20generator.jpg)

# Cthulhu Cog Commands

| Command                                  | Description                                 |
|------------------------------------------|---------------------------------------------|
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
| !rb category - itemID                | Delete a record from backstory or inventory|
| !cname male/female                     | Generate a random name                      |
| !cNPC male/female                      | Generate an NPC                             |
| !skillinfo skillName                  | Get info about a specific skill (without name of the skill you will get list of skills)            |                    |
| !coccupations occupationName          | Get info about a specific occupation (without name you will get list of occupations)       |
| !gbackstory                              | Generate a random backstory (it will not be saved to your investigator)                 |
| !cyear year                            | Historical information about a year         |
| !firearms name                            | Information about firearms in CoC from 1920s and modern (without name you will get list of weapons)        |
| !cloot                       | Generate random loot from 1920 (25% for money being inclooded)        |
| !rskill                    | Rename skill to your liking. If your language is English you can rename Language (own) to English. You can also use 3 custom skills.    |
| !showUserData                  | Debug command. Shows raw data saved for user who calls the command (stats, skill, backstory).  |

