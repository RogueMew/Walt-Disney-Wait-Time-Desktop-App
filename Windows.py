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
            [psg.Text("Select Attraction Type:"), psg.OptionMenu(data.Ride_Name, key="-Type-"), psg.Button("Select Type")]
        ]
        return layout3