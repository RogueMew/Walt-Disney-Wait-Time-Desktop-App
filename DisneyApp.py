import tkinter as AppWindow
from tkinter import font
import requests
import json
import datetime
import pytz
import os
from PIL import ImageTk, Image

Park_TimeZones = {
    "Disneyland": "America/Los_Angeles",
    "California Adventure": "America/Los_Angeles",
    "Magic Kingdom": "America/New_York",
    "EPCOT": "America/New_York",
    "Hollywood Studios": "America/New_York",
    "Animal Kingdom": "America/New_York",
    "Tokyo Disneyland": "Asia/Tokyo",
    "Tokyo DisneySea": "Asia/Tokyo",
    "Disneyland Paris": "Europe/Paris",
    "Walt Disney Studios Park": "Europe/Paris",
    "Hong Kong Disneyland": "Asia/Hong_Kong",
    "Shanghai Disneyland": "Asia/Shanghai",
}
Park_Ids = {
    "Disneyland": "7340550b-c14d-4def-80bb-acdb51d49a66",
    "California Adventure": "832fcd51-ea19-4e77-85c7-75d5843b127c",
    "Magic Kingdom": "75ea578a-adc8-4116-a54d-dccb60765ef9",
    "EPCOT": "47f90d2c-e191-4239-a466-5892ef59a88b",
    "Hollywood Studios": "288747d1-8b4f-4a64-867e-ea7c9b27bad8",
    "Animal Kingdom": "1c84a229-8862-4648-9c71-378ddd2c7693",
    "Tokyo Disneyland": "3cc919f1-d16d-43e0-8c3f-1dd269bd1a42",
    "Tokyo DisneySea": "67b290d5-3478-4f23-b601-2f8fb71ba803",
    "Disneyland Paris": "dae968d5-630d-4719-8b06-3d107e944401",
    "Walt Disney Studios Park": "ca888437-ebb4-4d50-aed2-d227f7096968",
    "Hong Kong Disneyland": "bd0eb47b-2f02-4d4d-90fa-cb3a68988e3b",
    "Shanghai Disneyland": "ddc4357c-c148-4b36-9888-07894fe75e83",
}
options = [
    "Select Option",
    "Disneyland",
    "California Adventure",
    "Magic Kingdom",
    "EPCOT",
    "Hollywood Studios",
    "Animal Kingdom",
    "Tokyo Disneyland",
    "Tokyo DisneySea",
    "Disneyland Paris",
    "Walt Disney Studios Park",
    "Hong Kong Disneyland",
    "Shanghai Disneyland",
]

# Window Setup
root = AppWindow.Tk()

WindowData = {
    "WindowHeight": root.winfo_screenheight() - 75,
    "WindowWidth": root.winfo_screenwidth(),
    "WindowTitle": "Disney Park Wait Time App",
}


root.geometry("{}x{}+0+0".format(WindowData["WindowWidth"], WindowData["WindowHeight"]))
root.title(WindowData["WindowTitle"])
root.resizable(True, True)
root.config(bg="Light Blue")


# Variables

current_directory = os.getcwd()

Park_Selected = AppWindow.StringVar()
Park_Selected.set("Select Option")
PreviousPage = None
Ride_Ids_URL = "https://api.themeparks.wiki/v1/entity/{}/children"
Park_Time_URL = "https://api.themeparks.wiki/v1/entity/{}/schedule"
Park_Current_Date_Label = "The Date at {} is {}"
photo = None
Photo_Path = "{} Photo.png"
Fonts = {
    "Date": font.Font(size=13, family="cursive"),
    "Menu Buttons": font.Font(size=30, family="cursive"),
    "Park Name": font.Font(size=18, family="cursive"),
}


# JSON Loader And Readers
def JSONLooader(Park_Chosen):
    global Park_JSONRAW
    Park_JSONRAW = requests.get(Ride_Ids_URL.format(Park_Ids[Park_Chosen]))
    global Park_JSONRef
    Park_JSONRef = Park_JSONRAW.json()


def JSON_Finder(type):
    firstItem = Park_JSONRef["children"]

    for rides in firstItem:
        Ride_ID = rides["id"]
        Ride_Name = rides["name"]
        Ride_Type = rides["entityType"]

        WaitTime_URL = "https://api.themeparks.wiki/v1/entity/{}/live".format(Ride_ID)
        RideWaitJSONRAW = requests.get(WaitTime_URL)
        RideWaitJSON = RideWaitJSONRAW.json()

        if type == "ride":
            if Ride_Type == "ATTRACTION" and len(RideWaitJSON["liveData"]) > 0:
                RideWaitJSON = RideWaitJSON["liveData"][0]
                Ride_Status = RideWaitJSON["status"]
                output = "\nName: {}\nType: {}\nStatus: {}\n".format(
                    Ride_Name, Ride_Type, Ride_Status
                )
                print("===========================================================")
                print(output)
                if Ride_Status == "OPERATING":
                    if "queue" in RideWaitJSON:
                        if "STANDBY" in RideWaitJSON["queue"]:
                            Ride_Standby = RideWaitJSON["queue"]["STANDBY"]["waitTime"]
                            if Ride_Standby is None:
                                Ride_Standby_Output = "Standby Wait Time: {}\n".format(
                                    Ride_Standby
                                )
                                print(Ride_Standby_Output)
                            else:
                                Ride_Standby_Output = (
                                    "Standby Wait Time: {} minutes\n".format(
                                        Ride_Standby
                                    )
                                )
                                print(Ride_Standby_Output)

                        if "SINGLE_RIDER" in RideWaitJSON["queue"]:
                            Ride_Single = RideWaitJSON["queue"]["SINGLE_RIDER"][
                                "waitTime"
                            ]
                            if Ride_Single is None:
                                Ride_Single_Output = (
                                    "Single Rider Wait Time: {}\n".format(Ride_Single)
                                )
                                print(Ride_Single_Output)
                            else:
                                Ride_Single_Output = (
                                    "Single Rider Wait Time: {} minutes\n".format(
                                        Ride_Single
                                    )
                                )
                                print(Ride_Single_Output)

                        if "PAID_RETURN_TIME" in RideWaitJSON["queue"]:
                            Ride_Lightning_State = RideWaitJSON["queue"][
                                "PAID_RETURN_TIME"
                            ]["state"]
                            print("\nLightning Lane State: {}")
                            if Ride_Lightning_State == "AVAILABLE":
                                Ride_Lightning_Start = RideWaitJSON["queue"][
                                    "PAID_RETURN_TIME"
                                ]["returnStart"]
                                Ride_Lightning_End = RideWaitJSON["queue"][
                                    "PAID_RETURN_TIME"
                                ]["returnEnd"]
                                Ride_Lightning_Price = str(
                                    RideWaitJSON["queue"]["PAID_RETURN_TIME"]["price"][
                                        "amount"
                                    ]
                                ).split("00")[0]
                                Ride_Lightning_Output = "\nLightning Lane Price: ${}\nLightning Lane Time Group Start: {}\nLightning Lane Time Group End: {}\n".format(
                                    Ride_Lightning_Price,
                                    Ride_Lightning_Start,
                                    Ride_Lightning_End,
                                )
                                print(Ride_Lightning_Output)

                        if "RETURN_TIME" in RideWaitJSON["queue"]:
                            Ride_ReturnTime_State = RideWaitJSON["queue"][
                                "RETURN_TIME"
                            ]["state"]
                            Ride_ReturnTime_State_Output = (
                                "Return Time Status: {}".format(Ride_ReturnTime_State)
                            )
                            print(Ride_ReturnTime_State_Output)

                            if Ride_ReturnTime_State != "FINISHED":
                                Ride_ReturnTime_Start = str(
                                    RideWaitJSON["queue"]["RETURN_TIME"]["returnStart"]
                                ).split("T")[-1]
                                Ride_ReturnTime_End = str(
                                    RideWaitJSON["queue"]["RETURN_TIME"]["returnEnd"]
                                ).split("T")[-1]
                                Ride_ReturnTime_Time_Output = "Return Time Start: {}\nReturn Time End: {}\n".format(
                                    Ride_ReturnTime_Start, Ride_ReturnTime_End
                                )
                                print(Ride_ReturnTime_Time_Output)

                        if "BOARDING_GROUP" in RideWaitJSON["queue"]:
                            BOARDING_GROUP_Allocation = RideWaitJSON["queue"][
                                "BOARDING_GROUP"
                            ]["allocationStatus"]
                            if BOARDING_GROUP_Allocation == "AVAILABLE":
                                BOARDING_GROUP_Current_Start = str(
                                    RideWaitJSON["queue"]["BOARDING_GROUP"][
                                        "currentGroupStart"
                                    ]
                                ).split("T")[-1]
                                BOARDING_GROUP_Current_End = str(
                                    RideWaitJSON["queue"]["BOARDING_GROUP"][
                                        "currentGroupEnd"
                                    ]
                                ).split("T")[-1]
                                BOARDING_GROUP_Wait = RideWaitJSON["queue"][
                                    "BOARDING_GROUP"
                                ]["estimatedWait"]
                                if BOARDING_GROUP_Wait is None:
                                    BOARDING_GROUP_Output = "Boarding Groups Allocation Status: {}\nCurrent Group Start Time: {}\nCurrent Group End Time: {}\nCurrent Wait Time: {}\n".format(
                                        BOARDING_GROUP_Allocation,
                                        BOARDING_GROUP_Current_Start,
                                        BOARDING_GROUP_Current_End,
                                        BOARDING_GROUP_Wait,
                                    )
                                    print(BOARDING_GROUP_Output)
                                else:
                                    BOARDING_GROUP_Output = "Boarding Groups Allocation Status: {}\nCurrent Group Start Time: {}\nCurrent Group End Time: {}\nCurrent Wait Time: {} minutes\n".format(
                                        BOARDING_GROUP_Allocation,
                                        BOARDING_GROUP_Current_Start,
                                        BOARDING_GROUP_Current_End,
                                        BOARDING_GROUP_Wait,
                                    )
                                    print(BOARDING_GROUP_Output)

        if type == "restaurant":
            if Ride_Type == "RESTAURANT":
                output = "\nName: {}\nType: {}\n".format(Ride_Name, Ride_Type)
                print("===========================================================")
                print(output)

            if Ride_Type == "RESTAURANT" and len(RideWaitJSON["liveData"]) > 0:
                RideWaitJSON = RideWaitJSON["liveData"][0]
                Ride_Status = RideWaitJSON["status"]
                if Ride_Status == "OPERATING":
                    if "queue" in RideWaitJSON:
                        if "STANDBY" in RideWaitJSON["queue"]:
                            Ride_Standby = RideWaitJSON["queue"]["STANDBY"]["waitTime"]
                            if Ride_Standby is None:
                                Ride_Standby_Output = "Standby Wait Time: {}\n".format(
                                    Ride_Standby
                                )
                            else:
                                Ride_Standby_Output = (
                                    "Standby Wait Time: {} minutes\n".format(
                                        Ride_Standby
                                    )
                                )
                            print(Ride_Standby_Output)
                        if "diningAvailability" in RideWaitJSON:
                            for Partysize in RideWaitJSON["diningAvailability"]:
                                sizeOfParty = Partysize["partySize"]
                                PartyWait = Partysize["waitTime"]
                                PartyOutput = "-------------------\nParty Size: {}\nWait for Party size: {} minutes\n"
                        if "operatingHours" in RideWaitJSON:
                            OperatingTimeOpened = RideWaitJSON["operatingHours"][0][
                                "startTime"
                            ]
                            OperatingTimeClosed = RideWaitJSON["operatingHours"][0][
                                "endTime"
                            ]
                            OperatingOutput = "\nOpened: {}\nClosed: {}\n".format(
                                OperatingTimeOpened, OperatingTimeClosed
                            )
                            print(OperatingOutput)


def Time_Getter(Park_Chosen):
    global Park_Time_JSONRaw
    Park_Time_JSONRaw = requests.get(Park_Time_URL.format(Park_Ids[Park_Chosen]))
    global Park_Time_JSONRef
    Park_Time_JSONRef = Park_Time_JSONRaw.json()
    global Park_Current_Date
    Park_Current_Date = datetime.datetime.now(
        pytz.timezone(Park_TimeZones[Park_Chosen])
    ).strftime("%Y-%m-%d")


# Button Functions
def Exit_Command():
    root.quit()


def Select_Park_Button():
    if Park_Selected.get() != "Select Option":
        global PreviousPage
        global photo
        PreviousPage = "Main"
        root.title("{} Directory".format(Park_Selected.get()))
        Park_Menus.place_forget()
        Park_Selected_Button.place_forget()
        Back_Button_Main.place(
            width=60, height=30, x=WindowData["WindowWidth"] - 120, y=0
        )

        JSONLooader(Park_Selected.get())
        Park_Name_Label.config(
            text="{} Menu".format(Park_Selected.get()), bg="Light Blue"
        )
        Park_Name_Label.place(x=0, y=0)
        photo = Image.open(
            os.path.join(os.getcwd(), "Photos", Photo_Path.format(Park_Selected.get()))
        )
        photo = photo.resize((560, 315))
        photo = ImageTk.PhotoImage(photo)
        Park_Photo.create_image(0, 0, anchor=AppWindow.NW, image=photo)
        Park_Photo.place(x=WindowData["WindowWidth"] - 560, y=30)
        Ride_Button.place(x=WindowData["WindowWidth"] / 4 - 60, y=40)
        Shows_Button.place(x=WindowData["WindowWidth"] / 4 - 60, y=140)
        Restaurants_Button.place(x=WindowData["WindowWidth"] / 4 - 60, y=240)


def Back_Button_Command(PreviousPage):
    if PreviousPage == "Main":
        root.title(WindowData["WindowTitle"])
        Park_Selected.set("Select Option")
        Park_Menus.place(
            width=180,
            height=60,
            x=WindowData["WindowWidth"] / 2 - 90,
            y=WindowData["WindowHeight"] - 400,
        )
        Park_Selected_Button.place(
            width=120,
            height=60,
            x=WindowData["WindowWidth"] / 2 - 60,
            y=WindowData["WindowHeight"] - 300,
        )
        Current_Date_Label.pack_forget()
        Back_Button_Main.place_forget()
        Park_Photo.place_forget()
        Current_Date_Label.place_forget()
        Park_Name_Label.place_forget()
        Ride_Button.place_forget()
        Shows_Button.place_forget()
        Restaurants_Button.place_forget()
    if PreviousPage == "Back":
        Select_Park_Button()


def Menu_Button_Command(Type_chosen):
    JSON_Finder(Type_chosen)


# Button Definers
Exit_Button = AppWindow.Button(root, text="Exit", command=lambda: Exit_Command())
Park_Selected_Button = AppWindow.Button(
    root, text="Select Park", command=lambda: Select_Park_Button()
)
Back_Button_Main = AppWindow.Button(
    root, text="Back", command=lambda: Back_Button_Command("Main")
)
Back_Button_Menu = AppWindow.Button(
    root, text="Back", command=lambda: Back_Button_Main("Menu")
)
Ride_Button = AppWindow.Button(
    root,
    text="Rides",
    font=Fonts["Menu Buttons"],
    width=10,
    command=lambda: Menu_Button_Command("ride"),
)
Restaurants_Button = AppWindow.Button(
    root,
    text="Restaurants",
    font=Fonts["Menu Buttons"],
    command=lambda: Menu_Button_Command("restaurant"),
)
Shows_Button = AppWindow.Button(
    root, text="Shows", font=Fonts["Menu Buttons"], width=10
)

# Menu Definers
Park_Menus = AppWindow.OptionMenu(root, Park_Selected, *options)
# Labels
Current_Date_Label = AppWindow.Label(root, text="", font=Fonts["Date"])
Park_Name_Label = AppWindow.Label(root, font=Fonts["Park Name"])
Park_Photo = AppWindow.Canvas(root, width=560, height=315)
# Initial Setup
Exit_Button.place(
    width=60,
    height=30,
    x=WindowData["WindowWidth"] - 60,
    y=0,
)
Park_Menus.place(
    width=180,
    height=60,
    x=WindowData["WindowWidth"] / 2 - 90,
    y=WindowData["WindowHeight"] - 400,
)
Park_Selected_Button.place(
    width=120,
    height=60,
    x=WindowData["WindowWidth"] / 2 - 60,
    y=WindowData["WindowHeight"] - 300,
)

# Removed Items
Park_Menus.place()
root.mainloop()
