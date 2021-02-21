import discord
import os
from keep_alive import keep_alive
from OpenDota import OpenDota
from HeroInfographic import HeroInfographic
from TeamInfographic import TeamInfographic

client = discord.Client()

account_ids = [["ItsYourBoi", 196156934], ["Kormit", 134205395], ["dr.walrus", 214671946], ["ジョジョ", 92584067], ["Klaus", 234647899], ["Stimpy", 229669450], ["MarioSDVC", 210311685]]

COMMAND_PREFIX = "!"

ERROR_MESSAGE = "Error, please check the command is correct"

@client.event
async def on_ready():
    print("I'm in")
    print(client.user)

async def create_hero_image(message, player):
    await message.channel.send("LOADING...")

    inf = HeroInfographic(600, 820, 'layouts/HeroInfo_new.xml', 'styles/HeroInfo_new.css', player)

    # try:
    completed = inf.initialise_variables()
    if completed:
        img = inf.create()
        img.save("info.png","png")
    await message.channel.send(file=discord.File('info.png'))
    # except Exception as e: 
    #     print(str(e))
    #     await message.channel.send(ERROR_MESSAGE)

async def create_team_image(message, players, team):
    await message.channel.send("LOADING...")

    inf = TeamInfographic(2500, 850, 'layouts/TeamInfo.xml', 'styles/TeamInfo.css', players, team)

    # try:
    inf.initialise_variables()
    img = inf.create()
    img.save("info.png","png")
    await message.channel.send(file=discord.File('info.png'))
    # except Exception as e: 
    #     print(str(e))
    #     await message.channel.send(ERROR_MESSAGE)

async def create_discord_scoreboard(message, match):
    m_id = ""
    m_id = match.matchId
    players = match.get_players()

    embed=discord.Embed(title="Match ID: "+ str(m_id))
    embed.description = match.get_winning_team() + " Win!"

    embed.add_field(name="Radiant", value="\u200b", inline=True)
    embed.add_field(name="Dire", value="\u200b", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)

    for i in range(0,5):
        name = players[i].hero
        value = "NW: " + str(players[i].get_net_worth()) +"\n KDA: "+str(''.join(str(players[i].get_KDA())[1:-1]) +"\n CS: "+str(''.join(str(players[i].get_cs())[1:-1])))
        embed.add_field(name=name, value=value, inline=True)

        name = players[5+i].hero
        value = "NW: " + str(players[5+i].get_net_worth()) + "\n KDA: "+str(''.join(str(players[5+i].get_KDA())[1:-1]) +"\n CS: "+str(''.join(str(players[5+i].get_cs())[1:-1])))
        embed.add_field(name=name, value=value, inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        
    await message.channel.send(embed=embed)

@client.event
async def on_message(message):

    steam_id = None

    if message.author == client.user:
        return

    command = message.content.split(" ")
    if message.content == COMMAND_PREFIX+"game":
        for account in account_ids:
            if message.author.name == account[0]:
                steam_id = account[1]

        if steam_id != None:
            od = OpenDota()
            match = od.get_latest_match(steam_id)
            await create_discord_scoreboard(message, match)
            
    elif command[0] == COMMAND_PREFIX+"game" and command[1] == "info":
        for account in account_ids:
            if message.author.name == account[0]:
                steam_id = account[1]

        if steam_id != None:
            od = OpenDota()
            match = od.get_latest_match(steam_id)
            m_id = match.matchId
            players = match.get_players()

            hero = ' '.join(command[2:]).lower()
            info_player = None
            for player in players:
                if player.hero.lower() == hero:
                    info_player = player

            await create_hero_image(message, info_player)

    elif command[0] == COMMAND_PREFIX+"game" and command[1] == "teaminfo":
        for account in account_ids:
            if message.author.name == account[0]:
                steam_id = account[1]

        if steam_id != None:
            od = OpenDota()
            match = od.get_latest_match(steam_id)
            m_id = match.matchId
            players = match.get_players()

            team = ' '.join(command[2:]).lower()
            
            team_id = None

            if team == 'dire':
                team_id = 1
            elif team == 'radiant':
                team_id = 0

            await create_team_image(message, players, team_id)
                
    elif len(command) > 3:
        if command[0] == COMMAND_PREFIX+"game" and command[1].isdigit() and command[2] == "info":
            for account in account_ids:
                if message.author.name == account[0]:
                    steam_id = account[1]

            if steam_id != None:
                od = OpenDota()
                match = od.get_match(int(command[1]))
                m_id = match.matchId
                players = match.get_players()

                hero = ' '.join(command[3:]).lower()
                info_player = None
                for player in players:
                    if player.hero.lower() == hero:
                        info_player = player

                await create_hero_image(message, info_player)   

        elif command[0] == COMMAND_PREFIX+"game" and command[1].isdigit() and command[2] == "teaminfo":
            for account in account_ids:
                if message.author.name == account[0]:
                    steam_id = account[1]

            if steam_id != None:
                od = OpenDota()
                match = od.get_match(int(command[1]))
                m_id = match.matchId
                players = match.get_players()

                team = ' '.join(command[2:]).lower()
                
                team_id = None

                if team == 'dire':
                    team_id = 1
                elif team == 'radiant':
                    team_id = 0

                await create_team_image(message, players, team_id)   
            

    elif command[0] == COMMAND_PREFIX+"game" and command[1].isdigit():
        for account in account_ids:
            if message.author.name == account[0]:
                steam_id = account[1]

        if steam_id != None:
            od = OpenDota()
            match = od.get_match(int(command[1]))
            await create_discord_scoreboard(message, match)

    elif command[0] == COMMAND_PREFIX+"pastgames":
        if len(command) > 1:
            if len(message.mentions) > 0:
                for account in account_ids:
                    if message.mentions[0].name == account[0]:
                        steam_id = account[1]
        else:
            for account in account_ids:
                if message.author.name == account[0]:
                    steam_id = account[1]

        if steam_id != None:
            od = OpenDota()
            matches = od.get_last_x_matches_data_simple(5, steam_id)

            embed=discord.Embed(title="Past Games")

            for match in matches:
                embed.add_field(name=f"Match ID: {match[0]}", value=f"Hero: {match[1]}\nKDA: {match[2]} {match[3]} {match[4]}", inline=False)
            
            await message.channel.send(embed=embed)
keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
print(client.run(token))
