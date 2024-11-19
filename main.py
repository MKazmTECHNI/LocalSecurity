import requests
import hashlib
import os
import sys
import subprocess

# Constants
URL = "https://raw.githubusercontent.com/MKazmTECHNI/LocalSecurity/main/main.py"
FILENAME = os.path.join(os.getcwd(), "main.py")


def download_script():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(
            f"Failed to download script. HTTP Status: {response.status_code}"
        )


def get_file_hash(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def update_and_rerun():
    try:
        with open(__file__, "r") as current_file:
            current_script = current_file.read()

        downloaded_script = download_script()

        current_hash = get_file_hash(current_script)
        downloaded_hash = get_file_hash(downloaded_script)

        if current_hash != downloaded_hash:
            print("Script has changed. Updating and restarting...")

            with open(FILENAME, "w") as file:
                file.write(downloaded_script)

            subprocess.Popen([sys.executable, FILENAME])
            sys.exit(0)  # Exit the current script after launching the new one
        else:
            print("Script is up-to-date. Continuing execution...")

    except Exception as e:
        print(f"Error during update check: {e}")
        sys.exit(1)


update_and_rerun()
print("Running main script...")

import discord
from discord.ext import commands
import ctypes
import psutil
import wmi
import pyautogui
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
proc/proccess k/kill name - kills proccess with given name (for example. 'proc k discord') 
k/key press/p,down,up,write,hotkey keys - mimics computer keys (try it yourself)
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

        # KEYING FUNCTIONALITY

    elif (
        message.content.lower().startswith("k")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
        or message.content.lower().startswith("key")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
    ):
        try:
            command_parts = message.content.lower().split(
                " ", 2
            )  # Split only the first two times
            command = command_parts[1]

            # I don't really know what could I explain here...
            if command == "press" or command == "p":
                pyautogui.keyDown(command_parts[2])
                pyautogui.keyUp(command_parts[2])
                await message.channel.send(f"Pressed {command_parts[2]}")
            elif command == "down":
                pyautogui.keyDown(command_parts[2])
                await message.channel.send(f"Pressed down {command_parts[2]}")
            elif command == "up":
                pyautogui.keyUp(command_parts[2])
                await message.channel.send(f"Pressed up {command_parts[2]}")
            elif command == "write" or command == "w":
                pyautogui.write(command_parts[2])  # Write everything after 'key write'
                await message.channel.send(f"Written '{command_parts[2]}'")
            elif command == "hotkey" or command == "hk":
                hotkey_parts = command_parts[2].split()
                pyautogui.hotkey(*hotkey_parts)
                await message.channel.send(f"Pressed '{command_parts[2]}'")
            else:
                await message.channel.send("Choose one of key commands")

        except IndexError:
            await message.channel.send("Not enough arguments")

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
