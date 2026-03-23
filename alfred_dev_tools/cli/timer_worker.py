import json
import subprocess
import sys
import time


def _show_dialog(message):
    script = f"""
tell application "System Events"
    activate
    repeat 5 times
        beep
        delay 0.7
    end repeat
    display dialog {json.dumps(message)} with title "计时结束" buttons {{"确定"}} default button "确定"
end tell
"""
    subprocess.run(["osascript", "-e", script], check=False)


def main():
    seconds = int(sys.argv[1])
    message = sys.argv[2]

    time.sleep(seconds)
    _show_dialog(message)
