import PySimpleGUI as psg
import data as data
import Functions as func

def layoutStack(layoutWanted):
    if layoutWanted == 1:
        layout1 = [
            [psg.Text("Disney Park App Tracker"),  psg.Button("Exit")],
            [psg.Text("Select Park:"), psg.OptionMenu(data.Park_options, key="-Park-"), psg.Button("Select Park")]
        ]
        return layout1
    if layoutWanted == 2:
        layout2 = [
            [psg.Text("Disney Park App Tracker"), psg.Button("Back to Park Selection"), psg.Button("Exit")],
            [psg.Text("Select Attraction Type:"), psg.OptionMenu(data.Type_Options, key="-Type-"), psg.Button("Select Type")]
        ]
        return layout2
    if layoutWanted == 3:
        layout3 = [
            [psg.Text("Disney Park App Tracker"), psg.Button("Back to Type Selection"),psg.Button("Exit")],
            [psg.Text("Select Attraction Type:"), psg.OptionMenu(data.Ride_Name, key="-Ride-"), psg.Button("Select Attraction")]
        ]
        return layout3
    if layoutWanted == 4:
        layout4 = [
            [psg.Text("{} Wait Times".format(data.selected_Ride)), psg.Button("Back to {} Selection".format(data.selected_Type)), psg.Button("Exit")],
            [psg.Text("Stand By Wait Time: {}".format(data.standby), background_color="white", key="-Standby-", text_color="Black"), psg.Text("Single Rider Wait Time: {}".format(data.single), background_color="white", key="-Single-",text_color="Black")],
            [psg.Text("Lightning Lanes Available: {}".format(data.lightningState), background_color="white",text_color="Black"),psg.Text("Lightning Lane Price: {} {}".format(data.lightningPrice, data.lightningCurrency), background_color="white",text_color="Black"), psg.Text("Lightning Lane Return Time Start: {}".format(data.lightningStart), background_color="white",text_color="Black"), psg.Text("Lightning Lane Time End: {}".format(data.lightningEnd), background_color="white", text_color="Black")]
        ]
        return layout4