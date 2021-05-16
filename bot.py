# Library Import
import discord
from discord.errors import ClientException
from discord.ext import commands
import os
import json
import asyncio
from discord_slash import SlashCommand, SlashContext

# Gets all the servers custom prefixes.
def getPrefixes(client, message):
    guild = message.guild.id
    data = json.loads(open("./json/serverConfig.json", "r").read())
    return data[str(guild)]["prefix"]

# Sets prefix, intents and the client variable.
intents = discord.Intents(members=True, guilds=True, emojis=True, messages=True, reactions=True)
client = commands.Bot(command_prefix=getPrefixes, help_command=None, intents=intents)
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True)

# Loads all the commands
def LoadFolder(folder: str):
    for filename in os.listdir(f"./{folder}"): # Just loads all the commands in the General folder
        if filename.endswith(".py"):           # To make your own commands just copy the template file.
            client.load_extension(f"{folder}.{filename[:-3]}")

def UnloadFolder(folder: str):
    for filename in os.listdir(f"./{folder}"):
        if filename.endswith(".py"):
            client.unload_extension(f"{folder}.{filename[:-3]}")

for folder in ["Administration", "Economy", "General", "Moderation", "Developer"]:
    LoadFolder(folder)

# Reloads the bot without restarting it.
@client.command()
async def reload(ctx):
    for folder in ["Administration", "Economy", "General", "Moderation", "Developer"]:
        try:
            UnloadFolder(folder)
        except:
            pass
        
        try:
            LoadFolder(folder)
        except:
            pass

    await ctx.message.add_reaction("✅")

try:
    client.run("") # Put your own token here (Don't share it!)
except ClientException:
    print("Token is invalid. Please enter a new one")