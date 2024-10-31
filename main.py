import discord
from discord.ext import commands
import ctypes
import psutil
import wmi
from PIL import ImageGrab
from io import BytesIO
import cv2


from settings import allowed_user_id, allowed_channel_id, bot_token

# Define Windows API functions and constants for volume control
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{bot.user} has successfully connected to Discord!")
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
? - sends screenshot and camera shot of current moment
proc / proccess k / kill name - kills proccess with given name (for example. 'proc k discord') 
v/volume number = changes volume (for example. 'v 100' (sets volume to 100%))
b/brightness number = changes brightness (for example. 'b 100' (sets brightness to 100%)))
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

    # SCREENSHOT FUNCTIONALITY
    if (
        message.content.lower() == "?"
        and allowed_user_id == message.author.id
        and allowed_channel_id == message.channel.id
    ):
        user32.SetProcessDPIAware()
        screenshot = ImageGrab.grab()

        # Save the screenshot to a BytesIO object (so you dont have to save img locally)
        image_buffer = BytesIO()
        screenshot.save(image_buffer, format="PNG")
        image_buffer.seek(0)  # Move to the start of the BytesIO buffer

        await message.channel.send(
            file=discord.File(fp=image_buffer, filename="screenshot.png")
        )
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:  # ret = bool if retrieved frame successfully
            # Encode frame as PNG image
            _, encoded_image = cv2.imencode(
                ".png", frame, [cv2.IMWRITE_PNG_COMPRESSION, 9]
            )
            # Save it to BytesIO buffer
            image_buffer = BytesIO(encoded_image.tobytes())
            image_buffer.seek(0)
            # Send image from buffer without saving locally
            await message.channel.send(
                file=discord.File(fp=image_buffer, filename="camerashot.png")
            )
        else:
            await message.channel.send("Failed to capture image")

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

            # Potential error handling (report if it appears pls)
        except Exception as e:
            await message.channel.send(e)

        # CONTROLING BRIGHTNESS
    elif (
        message.content.lower().startswith("b")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
        or message.content.lower().startswith("brightness")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
    ):
        try:
            level = int(message.content.lower().split(" ")[1])
            if level < 0 or level > 100:
                await message.channel.send("Brightness must be between 0 and 100")
                return

            wmi_service = wmi.WMI(namespace="wmi")
            methods = wmi_service.WmiMonitorBrightnessMethods()[0]

            methods.WmiSetBrightness(level, 0)

            await message.channel.send(f"Brighness set to {level}")
        except ValueError:
            await message.channel.send(
                "Please provide a valid volume level between 0 and 100."
            )

        # CONTROLING VOLUME
    if (
        message.content.lower().startswith("v")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
        or message.content.lower().startswith("volume")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
    ):
        try:
            level = int(message.content.lower().split(" ")[1])
            if level < 0 or level > 100:
                await message.channel.send("Volume must be between 0 and 100")
                return

            level = max(0, min(level, 100))
            volume = int((level / 100) * 65535)
            ctypes.windll.winmm.waveOutSetVolume(0, volume + (volume << 16))
            await message.channel.send(f"Volume set to {level}")

        except ValueError:
            await message.channel.send(
                "Please provide a valid volume level between 0 and 100."
            )


bot.run(str(bot_token))
