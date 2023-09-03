# bot.py

import os
import re

import discord
from discord.ext import commands, buttons

import dotenv
import env
#import d2, d4, d6, d8, d12, d20
#from d20 import roll
#import d2, d4, d6, d8, d12, d20, d100
import die

ints = discord.Intents.default()
ints.message_content = True


dotenv.load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = env.TOKEN
#client = discord.Client(intents=ints)


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = ints)
        self.added = False
        self.synced = False

    async def on_ready(self):
        if not self.synced:
            await tree.sync(guild=discord.Object(1144036249565397022))
            self.synced = True
        if not self.added:
            self.added = True

client = aclient()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    cmd = message.content
    name = message.author.name
    channel = message.channel
    tokens = re.split(r' ', cmd)
    reply = lambda x : channel.send(x, reference=message)
    n = len(tokens)
    if n == 0:
        return
    t0 = tokens[0]
    if len(t0) <= 2 or t0[0] != '/' or t0[1] != 'd':
        return
    if t0[1] == '0':
        await reply(f'{name}\'s die has a leading 0')
        return
    try:
        args = [int(tokens[1+i]) for i in range(0, n-1)]
    except:
        await reply(f'{name}, something wasn\t numeric')
        return
    #print(f'Tokens = {str(tokens)}')
    s = False
    m = 0
    try:
        if len(t0) == 3:
            if t0[2] == 's':
                await reply(f'{name}, bad command')
                return
            else:
                m = int(t0[2])
        elif len(t0) == 4:
            if t0[3] == 's':
                s = True
                m = int(t0[2])
            else:
                m = int(t0[2])*10+int(t0[3])
        elif len(t0) == 5:
            if t0[4] == 's':
                s = True
                m = int(t0[2])*10+int(t0[3])
            else:
                m = int(t0[2])*100+int(t0[3])*10+int(t0[4])
        elif len(t0) == 6:
            if t0[5] == 's':
                s = True
                m = int(t0[2])*100+int(t0[3])*10+int(t0[4])
            else:
                await reply(f'{name}, unsupported command')
                return
        else:
            await reply(f'{name}, unsupported command')
            return
    except ValueError:
        await reply(f'{name}, bad command')
        return
    except:
        await reply(f'{name}, uncaught exception')
        return
    #print(f's = {s}, m = {m}')

    if n == 1:
        if s:
            await reply(f'{name}, you need an argument')
        else:
            roll = die.roll(m)
            await reply(f'{name} rolled {roll}/{m}')
        return
    elif n == 2:
        t1 = 0
        try:
            t1 = int(tokens[1])
        except ValueError:
            await reply(f'{name}, {tokens[1]} is not a number')
            return
        line = ''
        if s:
            if t1 > 100:
                await reply(f'{name}, at most 100 rolls.')
                return
            rolls = die.rolls(t1,m)
            line = f'{name} rolled {str(rolls)}/{m}'
            line = line + f' (for a sum of {sum(rolls)})'
        else:
            line = f'{name} rolled {die.roll(m,t1)}/{m}'
        await reply(line)
        return
    elif n == 3:
        if not s:
            await reply(f'{name}, too many arguments.')
            return
        t1 = 0
        t2 = 0
        if len(tokens[1]) == 0:
            await reply(f'{name}? Empty argument.')
            return
        elif len(tokens[1]) > 2 and tokens[1][0] == '0':
            await reply(f'{name}, {tokens[1]} starts with 0')
            return
        if len(tokens[2]) == 0:
            await reply(f'{name}? Empty argument.')
            return
        elif len(tokens[2]) > 2 and tokens[2][0] == '0':
            await reply(f'{name}, {tokens[2]} starts with 0',
                    reference=message)
            return

        try:
            t1 = int(tokens[1])
        except ValueError:
            await reply(f'{name}, {tokens[1]} is not a number')
            return
        if t1 > 100:
            await reply(f'{name}, at most 100 rolls.')
            return
        try:
            t2 = int(tokens[2])
        except ValueError:
            await reply(f'{name}, {tokens[2]} is not a number')
            return

        rolls = die.rolls(t1, m, t2)
        line = f'{name} rolled {str(rolls)}/{m}'
        line = line + f' (for a sum of {sum(rolls)})'
        await reply(line)
        return

    return


tree = discord.app_commands.CommandTree(client)

@tree.command(name="name", description="description")
async def slash_command(interaction: discord.Interaction):
    await interaction.response.send_message("command")

@tree.command(description='Roll 1 d20.', guild=discord.Object(1144036249565397022))
async def roll20(interaction: discord.Interaction):
    await interaction.response.send_message(f'User rolled a {d20.roll()} out of 20')


client.run(TOKEN)
