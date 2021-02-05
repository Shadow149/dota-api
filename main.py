import discord
import os
from keep_alive import keep_alive
from OpenDota import OpenDota
from HeroInfographic import HeroInfographic

client = discord.Client()

account_ids = [["ItsYourBoi", 196156934], ["Kormit", 134205395], ["dr.walrus", 214671946], ["ジョジョ", 92584067], ["Klaus", 234647899], ["Stimpy", 229669450], ["MarioSDVC", 210311685]]

COMMAND_PREFIX = "!"

@client.event
async def on_ready():
    print("I'm in")
    print(client.user)

async def create_image(message, player):
    await message.channel.send("LOADING...")

    inf = HeroInfographic(600, 780, 'layouts/HeroInfo_new.xml', 'styles/HeroInfo_new.css', player)

    try:
        inf.initialise_variables()
        img = inf.create()
        img.save("info.png","png")
        await message.channel.send(file=discord.File('info.png'))
    except Exception as e: 
        print(str(e))
        await message.channel.send("Error, Maybe the match is not processed yet, please wait.")

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

            create_image(message, info_player)
                

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

                create_image(message, info_player)

    elif command[0] == COMMAND_PREFIX+"game" and command[1].isdigit():
        for account in account_ids:
            if message.author.name == account[0]:
                steam_id = account[1]

        if steam_id != None:
            od = OpenDota()
            match = od.get_match(int(command[1]))
            m_id = ""
            m_id = match.matchId
            #match = od.get_match_from_file("test_data.txt")
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


keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
print(client.run(token))
