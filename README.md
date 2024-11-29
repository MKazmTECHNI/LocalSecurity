# LocalSecurity

With smart homes, and remote safety controls it's only fair to also code smart computers innit?

LocalSecurity is an (unfinished) tool that lets users remotely control their computer through commands sent via Discord. Whether you’re looking to monitor your system or manage essential settings, LocalSecurity is designed to offer seamless control with security in mind.

---

## 🚀 Features

- **Remote Monitoring**:
  - **View Camera & Screen**: One `?` and you get this moment images of infront of your camera and your monitor.
- **System Control**:
  - **Proccess Management**: Close unwanted proccesses remotly.
  - **Adjust Brightness & Volume**: Control display brightness and system volume.
- **Security**:
  - **Remote Lock**: Instantly lock your computer to protect your data.
  - **Remote Shutdown**: If you can't ensure that someone won't just log back in you can shutdown it.

---

## 🌐 Planned Features

- **Desktop App**: Control and monitor your computer through a dedicated desktop application.
- **Mobile Support**: Access controls from your mobile device for added convenience.

---

If you have any idea for new command or how to improve code, I'd appreciate texting me!

The app is OpenSource (like every should be) so feel free to bend it to your liking!

# How to get started and install it?

1. Setup **your** discord bot on `Discord developer portal`
2. Paste it's token into `settings_blank.py`
3. Add it to your desired **discord server**
4. Copy **channel ID** of channel you want to send commands from, and your **user ID**
5. Paste it into `settings_blank.py`
6. Change file name to `settings.py`
7. Run `pip install discord.py` and `pip install opencv-python` in your terminal
8. Throw script into Windows Autostart
9. Run the program! (`main.py`)

Commands are under command `help` but I'll also paste them here

| Short           | options     | Explanation                                        | examples       |
| --------------- | ----------- | -------------------------------------------------- | -------------- |
| help            |             | sends help command... obviously                    | help           |
| l / lock        |             | logs out of current user                           | l              |
| shut / shutdown |             | shutdowns computer...                              | shut           |
| ?               |             | sends screenshot and camera shot of current moment | ?              |
| proc / proccess | k/kill name | kills proccess with given name                     | proc k discord |
| v / volume      | number      | changes volume                                     | v 100          |
| b / brightness  | number      | changes brightness                                 | b 100          |

Created by MKazm ;p
