import subprocess as NonWindows

def AppleLinuxMinimizeTerminal():
    NonWindows.run(["xdotool", "windowminimize", "$(xdotool getactivewindow)"])