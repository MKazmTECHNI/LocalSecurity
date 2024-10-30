import discord
from discord.ext import commands
import ctypes
import psutil

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

    if (
        message.content.lower() == "help"
        and allowed_user_id == message.author.id
        and allowed_channel_id == message.channel.id
    ):
        await message.channel.send(
            """
help - sends this command... obviously.
l / lock - logs out of current user 
shut / shutdown - shutdowns computer...
proc / proccess k / kill name - kills proccess with given name (for example. proc k discord) 
            """
        )

        # LOCKING COMPUTER
    if (
        message.content.lower() in ["l", "lock"]
        and allowed_user_id == message.author.id
        and allowed_channel_id == message.channel.id
    ):
        # actual function \/
        ctypes.windll.user32.LockWorkStation()
        await message.channel.send("Computer locked.")

        # SHUTDOWN COMPUTER
    if (
        message.content.lower() in ["shut", "shutdown"]
        and allowed_user_id == message.author.id
        and allowed_channel_id == message.channel.id
    ):
        # actual function \/
        ctypes.windll.shutdown(1, 0, 0)
        await message.channel.send("Computer shutting down.")

    # PROCCESS / PROC FUNCTIONALITY
    elif (
        message.content.lower().startswith("process")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
        or message.content.lower().startswith("proc")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
    ):
        try:
            command, *args = message.content.lower().split(" ")[1:]
            if command == "kill" and args:
                process_name = args[0]
                process = [
                    proc
                    for proc in psutil.process_iter()
                    if process_name in proc.name().lower()
                ]
                for proc in process:
                    proc.terminate()
                if process:
                    print(f"{process_name} has been closed successfully.")
                else:
                    print(f"{process_name} is not running.")

                await message.channel.send(f"Killed {process_name} process")
            else:
                await message.channel.send("Please select process to be killed.")

            # Potential errors
        except Exception as e:
            await message.channel.send(e)


bot.run(str(bot_token))
