import discord
from discord.ext import commands
import ctypes
from settings import allowed_user_id, allowed_channel_id, bot_token

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    channel = bot.get_channel(allowed_channel_id)
    if channel:
        await channel.send(f"Self Safety Triggered. <@{allowed_user_id}>")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "hc":
        await message.channel.send("Healthy")

    if (
        message.content.lower() in ["l", "lock"]
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
    ):
        print(message.author.id)
        print(message.channel.id)
        ctypes.windll.user32.LockWorkStation()
        await message.channel.send("Computer locked.")


bot.run(str(bot_token))
