import os
import requests
import subprocess
import sys

# Configuration
GITHUB_REPO = "https://raw.githubusercontent.com/username/repository/branch/"  # Replace with your repo
FILES_TO_CHECK = ["file1.py", "file2.py"]  # List of files to check
AUTOSTART_DIR = os.path.expanduser("~/.config/autostart")  # For Linux
# For Windows: AUTOSTART_DIR = os.path.join(os.getenv('APPDATA'), 'Microsoft\Windows\Start Menu\Programs\Startup')


def download_file(filename):
    url = GITHUB_REPO + filename
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {filename}")


def setup_autostart(filename):
    # Create a .desktop file for Linux
    if sys.platform.startswith("linux"):
        with open(os.path.join(AUTOSTART_DIR, f"{filename}.desktop"), "w") as f:
            f.write(
                f"""
[Desktop Entry]
Type=Application
Exec=python3 {os.path.abspath(filename)}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name={filename}
"""
            )
    # Add Windows autostart logic if needed here


def main():
    for filename in FILES_TO_CHECK:
        if not os.path.isfile(filename):
            download_file(filename)
            setup_autostart(filename)
            subprocess.Popen(["python", filename])  # Start the downloaded file
            sys.exit(0)
        else:
            # Optionally check if files have changed
            response = requests.head(GITHUB_REPO + filename)
            remote_size = int(response.headers.get("Content-Length", 0))
            local_size = os.path.getsize(filename)
            if remote_size != local_size:
                download_file(filename)
                setup_autostart(filename)
                subprocess.Popen(["python", filename])  # Start the downloaded file
                sys.exit(0)


if __name__ == "__main__":
    main()
