import PySimpleGUI as psg
import data as data
import Functions as func
import Windows as win
import testWifi as wifitest
import windowsMinimizeTerminal as Windows
import LinuxDarwinMinimizeWindow as AppleLinux
import platform as OperatingSystem
import scheduleDetector as parkTime


if OperatingSystem.system() == "Linux" or OperatingSystem.system() == "Darwin":
    AppleLinux.AppleLinuxMinimizeTerminal()
elif OperatingSystem.system() == "Windows":
    Windows.terminalMiniWIN()

if wifitest.internetConnectionTest() == False:
    psg.popup_error("Could not connect to the internet\nConnect to a network an reboot the app",title="Error 404")
    exit()

window = psg.Window("Disney Park App Tracker", layout= win.layoutStack(1),)

while True:
    event, values = window.read()

    if event == psg.WIN_CLOSED or event == "Exit":
        break
    
    if event == "Select Park":
        data.selected_Park = values["-Park-"]

        
        data.selected_Park = values["-Park-"]
        if data.selected_Park != "Select Option":
            func.JSONLooader(data.selected_Park)
            parkTime.parkStatusChecker()
            if data.parkOpened == "Open":
                window.close()
                window = psg.Window("{} Attraction Menu".format(values["-Park-"]), layout=win.layoutStack(2))
            if data.parkOpened == "Closed":
                window.close()
                window = psg.Window("{} Attraction Menu".format(values["-Park-"]), layout=win.layoutStack(5))
    
    if event == "Back to Park Selection":
        window.close()
        window = psg.Window("Disney Park App Tracker", layout=win.layoutStack(1))
    
    if event == "Back to Type Selection":
        window.close()
        window = psg.Window("{} Attraction Menu".format(data.selected_Park), layout= win.layoutStack(2))
    
    if event == "Select Type":
        selected_Type = values["-Type-"] 
        if selected_Type == "--WIP-- Restaurants --WIP--":
            psg.popup_error("This Function is A work in progress")
        func.NameAdder(selected_Type)
        window.close()
        window = psg.Window("{} {} Choices".format(data.selected_Park, selected_Type), layout=win.layoutStack(3))
        

    
    if event == "Select Attraction":
        data.selected_Ride = values["-Ride-"]
        if selected_Type == "Rides":
            func.waitTimeGetter(data.selected_Ride)
            window.close()
            window = psg.Window("{} Wait Times".format(data.selected_Ride),layout=win.layoutStack(4))
        elif selected_Type == "--WIP-- Shows --WIP--":
            func.showTimeGetter(data.selected_Ride)
    
    if event == "Back to {} Selection".format(data.selected_Type):
        window.close()
        window = psg.Window("{} {} Choices".format(data.selected_Park, data.selected_Type), layout=win.layoutStack(3))
window.close()