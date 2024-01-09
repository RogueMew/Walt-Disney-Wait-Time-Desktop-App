import ctypes as windowsManager

def terminalMiniWIN():
    windowsManager.windll.user32.ShowWindow(windowsManager.windll.kernel32.GetConsoleWindow(), 6)