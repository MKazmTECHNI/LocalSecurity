import discord
from discord.ext import commands
import ctypes
import psutil
from PIL import ImageGrab
from io import BytesIO
import cv2
import time
from pynput.keyboard import Controller, Key
import time
import subprocess



from settings import allowed_user_id, allowed_channel_id, bot_token

# Define Windows API functions and constants for volume control
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
keyboard = Controller()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


keys = {
    "space": Key.space,
    "ctrl": Key.ctrl,
    "alt": Key.alt,
    "tab": Key.tab,
    "caps": Key.caps_lock,
    "backspace": Key.backspace,
    "esc": Key.esc,
    "escape": Key.esc,
    "back": Key.backspace,
    "enter": Key.enter,
    "del": Key.delete,
    "delete": Key.delete,
    "up": Key.up,
    "down": Key.down,
    "right": Key.right,
    "left": Key.left,
    "page_up": Key.page_up,
    "page_down": Key.page_down,
    "win": Key.cmd,
    "cmd": Key.cmd,
    "f1":Key.f1,
    "f2":Key.f2,
    "f3":Key.f3,
    "f4":Key.f4,
    "f5":Key.f5,
    "f6":Key.f6,
    "f7":Key.f7,
    "f8":Key.f8,
    "f9":Key.f9,
    "f10":Key.f10,
    "f11":Key.f11,
    "f12":Key.f12,
}

def get_key(key_to_press):
    for key, value in keys.items():
        if key == key_to_press:
            return value
    return key_to_press


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
cmd = executes simple commands and sends u feedback (for example. 'cmd echo Hello')
py = executes simple scripts and sends u feedback (for example. 'py print("Hello")')
pa = pauses current song
skip = skips current song
prev = rewinds current song
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
            key_to_press = get_key(command_parts[2])

            # I don't really know what could I explain here...
            if command == "press" or command == "p":
                keyboard.press(key_to_press)
                keyboard.release(key_to_press)
                await message.channel.send(f"Pressed {command_parts[2]}")
            elif command == "down" or command == "d":
                keyboard.press(key_to_press)
                await message.channel.send(f"Pressed down {command_parts[2]}")
            elif command == "up" or command == "u":
                keyboard.release(key_to_press)
                await message.channel.send(f"Pressed up {command_parts[2]}")
            elif command == "write" or command == "w":
                keyboard.write(key_to_press)  # Write everything after 'key write'
                await message.channel.send(f"Written '{command_parts[2]}'")
            elif command == "hotkey" or command == "hk":
                hotkey_parts = command_parts[2].split()
                try:
                    for key in hotkey_parts:
                        keyboard.press(get_key(key))
                    for key in hotkey_parts: 
                        keyboard.release(get_key(key))
                    await message.channel.send(f"Pressed '{command_parts[2]}'")
                except Exception as e:
                    await message.channel.send(f"Error pressing hotkey: {e}")
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

# some commands to songies (songs)
    if (
        message.content.lower().startswith("pause")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
        or message.content.lower().startswith("pa")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
    ):
        keyboard.press(Key.media_play_pause)
        keyboard.release(Key.media_play_pause)
        await message.channel.send("Music paused")
    if (
        message.content.lower().startswith("skip")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
    ):
        keyboard.press(Key.media_next)
        keyboard.release(Key.media_next)
        await message.channel.send("Song skipped!")
    if (
        message.content.lower().startswith("prev")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
        or message.content.lower().startswith("prev")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
    ):
        keyboard.press(Key.media_previous)
        keyboard.release(Key.media_previous)
        await message.channel.send("Song reverted!")

    
    # CMD FUNCTIONALITY
    if (
        message.content.lower().startswith("cmd")
        and allowed_user_id == message.author.id
        and allowed_channel_id == message.channel.id
    ):
        try:
            command = message.content[len("cmd "):]  # Extract command after 'cmd'
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            output = result.stdout if result.stdout else result.stderr
            if len(output) > 2000:  # Discord message limit
                await message.channel.send("Output too long. Sending as a file.")
                output_buffer = BytesIO(output.encode("utf-8"))
                output_buffer.seek(0)
                await message.channel.send(
                    file=discord.File(fp=output_buffer, filename="cmd_output.txt")
                )
            else:
                await message.channel.send(f"```\n{output}\n```")
        except Exception as e:
            await message.channel.send(f"Error executing command: {e}")

      # PYTHON EXECUTION FUNCTIONALITY
    elif (
        message.content.lower().startswith("py")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
    ):
        try:
            code_to_execute = message.content.split(" ", 1)[1]
            
            # Capture output
            import io
            import contextlib
            
            output_buffer = io.StringIO()
            with contextlib.redirect_stdout(output_buffer):
                exec(code_to_execute, {"__builtins__": __builtins__})

            # Get the output
            output = output_buffer.getvalue().strip()
            output_buffer.close()

            # Send the output to Discord
            if output:
                await message.channel.send(f"```\n{output}\n```")
            else:
                await message.channel.send("Code executed successfully with no output.")
        
        except Exception as e:
            await message.channel.send(f"Error executing Python code: {e}")

    if (
        message.content.lower().startswith("at")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
        or message.content.lower().startswith("alttab")
        and message.author.id == allowed_user_id
        and message.channel.id == allowed_channel_id
    ):
        times = message.content.lower().split()[1]
        if times.isdigit():
            keyboard.press("alt")
            for i in range(int(times)):
                keyboard.press("tab")
            keyboard.release("tab")
            keyboard.release("alt")
            await message.channel.send(f"Alt-tabbed {times} times")
        else:
            await message.channel.send("Please provide a valid number of times to alt-tab.")
        




bot.run(str(bot_token))