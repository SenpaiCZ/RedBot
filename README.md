# SenpaiCZ Cogs for RedBot
Its my first cog i ever made from scratch. If you find any issue let me know via discord @senpaicz.



# Call of Cthulhu by Chaosium .inc
To be able to play Call of Cthulhu you will need Keepers Rulebook, Call of Cthulhu Starter set or Pulp of Cthulhu published by Chaosium .inc

[Call of Cthulhu Keeper Rulebook](https://www.chaosium.com/call-of-cthulhu-keeper-rulebook-hardcover/)

[Call of Cthulhu Starter Set](https://www.chaosium.com/call-of-cthulhu-starter-set/)

[Pulp Cthulhu](https://www.chaosium.com/pulp-cthulhu-hardcover/)

# Cthulhu Cog Install
!repo add senpaicz https://github.com/SenpaiCZ/RedBot

!cog install senpaicz CthulhuCog

# Cthulhu Cog Info
The Cthulhu Discord Cog is a versatile companion for your tabletop role-playing sessions based on the popular Call of Cthulhu game. With its intuitive commands, you can easily roll dice, perform skill checks, create new investigators, generate random stats and backstories, and manage your character's inventory. The bot also provides a wealth of information, including lists of skills and occupations, historical details about specific years, and the ability to generate random names and NPCs. Whether you're a Keeper or a player, this bot enhances your Call of Cthulhu experience by streamlining tasks and providing quick access to essential game mechanics.


Generate random name with !cname male/female

![Generating random name](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/name.jpg)

Generate random character stats

![Generating random character stats](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/autochar.jpg)

Show character stats

![Show character stats](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/mcs1.jpg)

![Show character stats](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/mcs2.jpg)

![Show character stats](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/mcs3.jpg)

Roll die or multiple

![Roll 3D6](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/d.jpg)

Using luck for rolls

![Using luck](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/use%20luck.jpg)

![using luck](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/use%20luck%202.jpg)

Check for skill

![Roll for skill](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/d%20listen.jpg)

Change skill

![Edit skill of your character](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/cskill.jpg)

Generate random NPC

![Generated random NPC](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/random%20npc.jpg)

Get info about skills

![List of skills](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/skillinfo.jpg)
![Show occult skill](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/skillinfo%20occult.jpg)

Get info about occupations

![List of occupations](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/occupations.jpg)
![Get info about librarian](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/occupations%20librarian.jpg)

Get info about year

![Year info](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/year%201923.jpg)

Generate backstory

![Generate random backstory](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/backstory%20generator.jpg)

Show information about firearms

![Firearms information](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/firearms.jpg)

![Firearms information](https://github.com/SenpaiCZ/RedBot/blob/SenpaiCogs/src-images/firearms2.jpg)

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

