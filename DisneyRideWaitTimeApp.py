import PySimpleGUI as psg
import data as data
import Functions as func
import Windows as win
<<<<<<< Updated upstream
=======
import testWifi as wifitest

if wifitest.internetConnectionTest() == False:
    psg.popup_error("Could not connect to the internet\nConnect to a network an reboot the app",title="Error 404")
    exit()
>>>>>>> Stashed changes

window = psg.Window("Disney Park App Tracker", layout= win.layoutStack(1),)

while True:
    event, values = window.read()
    print(f"Event: {event}, Values: {values}")

    if event == psg.WIN_CLOSED or event == "Exit":
        break
    
    if event == "Select Park":
<<<<<<< Updated upstream
        selected_Park = values["-Park-"]
        if selected_Park != "Select Option":
            func.JSONLooader(selected_Park)
=======
        data.selected_Park = values["-Park-"]
        if data.selected_Park != "Select Option":
            func.JSONLooader(data.selected_Park)
>>>>>>> Stashed changes
            window["-Park-"].update('')
            window.close()
            window = psg.Window("{} Attraction Menu".format(values["-Park-"]), layout=win.layoutStack(2))
    
    if event == "Back to Park Selection":
        window.close()
        window = psg.Window("Disney Park App Tracker", layout=win.layoutStack(1))
    
    if event == "Back to Type Selection":
        window.close()
<<<<<<< Updated upstream
        window = psg.Window("{} Attraction Menu".format(selected_Park), layout= win.layoutStack(2))
=======
        window = psg.Window("{} Attraction Menu".format(data.selected_Park), layout= win.layoutStack(2))
    
>>>>>>> Stashed changes
    if event == "Select Type":
        selected_Type = values["-Type-"]
        func.NameAdder(selected_Type)
        window.close()
<<<<<<< Updated upstream
        window = psg.Window("{} {} Choices".format(selected_Park, selected_Type), layout=win.layoutStack(3))
=======
        window = psg.Window("{} {} Choices".format(data.selected_Park, data.selected_Type), layout=win.layoutStack(3))
    
    if event == "Select Attraction":
        data.selected_Ride = values["-Ride-"]
        func.waitTimeGetter(data.selected_Ride)
        window.close()
        window = psg.Window("{} Wait Times".format(data.selected_Ride),layout=win.layoutStack(4))
    
    if event == "Back to {} Selection".format(data.selected_Type):
        window.close()
        window = psg.Window("{} {} Choices".format(data.selected_Park, data.selected_Type), layout=win.layoutStack(3))
        
        
>>>>>>> Stashed changes


            


window.close()