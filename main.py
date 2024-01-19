import customtkinter
import requests as web
import pytz as timezone
import datetime as time
import subprocess as NonWindows
import ctypes as windowsManager
import json as json
import PySimpleGUI as psg
import platform as OperatingSystem
import os
class resorts:
    resortNames = [
        "Walt Disney World® Resort",
        "Tokyo Disney Resort",
        "Shanghai Disney Resort",
        "Disneyland Paris",
        "Disneyland Resort",
        "Hong Kong Disneyland Parks",
    ]


class Urls:
    Ride_Ids_URL = "https://api.themeparks.wiki/v1/entity/{}/children"
    Park_Time_URL = "https://api.themeparks.wiki/v1/entity/{}/schedule"
    Ride_Time_URL = "https://api.themeparks.wiki/v1/entity/{}/live"
    All_Park_Ids_URL = "https://api.themeparks.wiki/v1/destinations"
    Entity_Data_URL = "https://api.themeparks.wiki/v1/entity/{}"


class ParkIds:
    Park_Ids = {
        "Disneyland": "7340550b-c14d-4def-80bb-acdb51d49a66",
        "California Adventure": "disneycaliforniaadventurepark",
        "Magic Kingdom": "magickingdompark",
        "EPCOT": "epcot",
        "Hollywood Studios": "disneyshollywoodstudios",
        "Animal Kingdom": "disneysanimalkingdomthemepark",
        "Tokyo Disneyland": "tokyodisneyland",
        "Tokyo DisneySea": "tokyodisneysea",
        "Disneyland Paris": "dae968d5-630d-4719-8b06-3d107e944401",
        "Walt Disney Studios Park": "ca888437-ebb4-4d50-aed2-d227f7096968",
        "Hong Kong Disneyland": "bd0eb47b-2f02-4d4d-90fa-cb3a68988e3b",
        "Shanghai Disneyland": "shanghaidisneyland",
    }


class ParkTimeInfo:
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
    parkWantedTimeZone = None
    SpecialEvent = False
    completed = None

    parkOpened = ""
    parkTime = ""
    parkOperationOpen = ""
    parkOperationClosed = ""

    def parkStatusChecker():
        temp = web.get(
            Urls.Park_Time_URL.format(ParkIds.Park_Ids[userVariables.selected_Park])
        )
        currentTime = time.datetime.now(
            timezone.timezone(ParkTimeInfo.Park_TimeZones[userVariables.selected_Park])
        )
        temp = temp.json()
        if "schedule" in temp:
            ParkTimeInfo.parkTime = currentTime.strftime("%H:%M:%S")
            for tickets in temp["schedule"]:
                if (
                    str(tickets["date"]) == currentTime.strftime("%Y-%m-%d")
                    and tickets["type"] == "OPERATING"
                ):
                    currentTimeList = currentTime.strftime("%H:%M:%S").split(":")
                    ParkTimeInfo.parkOperationOpen = (
                        tickets["openingTime"]
                        .split("T")[-1]
                        .split("+")[0]
                        .split("-")[0]
                    )
                    ParkTimeInfo.parkOperationClosed = (
                        tickets["closingTime"]
                        .split("T")[-1]
                        .split("+")[0]
                        .split("-")[0]
                    )
                    closingTimeList = (
                        tickets["closingTime"]
                        .split("T")[-1]
                        .split("+")[0]
                        .split("-")[0]
                        .split(":")
                    )
                    openingTimeList = (
                        tickets["openingTime"]
                        .split("T")[-1]
                        .split("+")[0]
                        .split("-")[0]
                        .split(":")
                    )
                    if closingTimeList[0] == "00":
                        closingTimeList[0] = "24"
                    if (
                        (
                            int(openingTimeList[0])
                            < int(currentTimeList[0])
                            < int(closingTimeList[0])
                        )
                        or (
                            int(openingTimeList[0]) == int(currentTimeList[0])
                            and int(openingTimeList[1]) <= int(currentTimeList[1])
                        )
                        or (
                            int(closingTimeList[0]) == int(currentTimeList[0])
                            and int(closingTimeList[1]) > int(currentTimeList[1])
                        )
                        or (
                            closingTimeList[0] == "00"
                            and (
                                int(currentTimeList[0]) < int(openingTimeList[0])
                                or (
                                    int(currentTimeList[0]) == int(openingTimeList[0])
                                    and int(currentTimeList[1])
                                    < int(openingTimeList[1])
                                )
                            )
                        )
                    ):
                        ParkTimeInfo.parkOpened = "Open"
                    else:
                        ParkTimeInfo.parkOpened = "Closed"

    def resetData():
        ParkTimeInfo.parkWantedTimeZone = None
        ParkTimeInfo.SpecialEvent = False
        ParkTimeInfo.parkOpened = ""
        ParkTimeInfo.parkTime = ""
        ParkTimeInfo.parkOperationOpen = ""
        ParkTimeInfo.parkOperationClosed = ""


class menuOptions:
    Park_options = [
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
    Type_Options = ["Rides", "--DEV-- Shows --DEV--", "--WIP-- Restaurants --WIP--"]


class RideData:
    Ride_Names = []
    Ride_Ids = {}
    Ride_Name = ""
    Ride_Id = ""
    Ride_Closed = ""
    Ride_Status = ""
    selected_Ride = ""
    standby = ""
    single = ""
    boardingStart = ""
    boardingEnd = ""
    boardingState = ""
    boardingNext = ""
    boardingTime = ""
    lightningState = ""
    lightningStart = ""
    lightningEnd = ""
    lightningPrice = ""
    lightningCurrency = ""


class ShowData:
    # Show Vars
    Show_Names = []
    Show_Name = ""
    Show_Ids = ""
    Show_Times = []


class RestaurantData:
    Restaurant_Names = []
    Restaurant_Id = ""


class userVariables:
    selected_Park = ""
    selected_Type = ""
    selected_Ride = ""
    selected_RideId = ""


class UnixBasedSystems:
    def AppleLinuxMinimizeTerminal():
        NonWindows.run(["xdotool", "windowminimize", "$(xdotool getactivewindow)"])


class WindowsBasedSystems:
    def terminalMiniWIN():
        windowsManager.windll.user32.ShowWindow(
            windowsManager.windll.kernel32.GetConsoleWindow(), 6
        )


# App Items
app = customtkinter.CTk()
customtkinter.set_appearance_mode("system")


# App Funcs and Classes
class UtilityFuncs:
    def jasonCheck(text):
        try:
            text = text.text
            json.loads(text)
            return True
        except json.JSONDecodeError:
            return False

    def wifiCheck():
        try:
            web.get("https://google.com", timeout=5)
            return True
        except web.ConnectionError or web.ConnectTimeout:
            return False
    
    def MinimizeTerminal():
        if OperatingSystem.system() == "Linux" or OperatingSystem.system() == "Darwin":
            UnixBasedSystems.AppleLinuxMinimizeTerminal()
        elif OperatingSystem.system() == "Windows":
            WindowsBasedSystems.terminalMiniWIN()


class AttractionFuncs:
    parkJason = ""

    def jasonLoader():
        try:
            AttractionFuncs.parkJason = web.get(
                url=Urls.Ride_Ids_URL.format(
                    ParkIds.Park_Ids[userVariables.selected_Park]
                )
            )
            AttractionFuncs.parkJason.raise_for_status()
        except web.RequestException as e:
            print(f"error loading Json: {e}")
        if UtilityFuncs.jasonCheck(AttractionFuncs.parkJason) == False:
            TempVars.jasonLoads = False
            return
        else:
            AttractionFuncs.parkJason = AttractionFuncs.parkJason.json()
            TempVars.jasonLoads = True

    def NameAdder():
        for attractions in AttractionFuncs.parkJason["children"]:
            temp = web.get(url=Urls.Ride_Time_URL.format(attractions["id"]))
            if UtilityFuncs.jasonCheck(temp) == False:
                return
            if attractions["entityType"] == "ATTRACTION":
                temp = temp.json()
                if len(temp["liveData"]) <= 0:
                    RideData.Ride_Names.append(
                        "--Unknown Status-- " + attractions["name"]
                    )
                elif temp["liveData"][0]["status"] != "OPERATING":
                    RideData.Ride_Names.append("-- Closed -- " + attractions["name"])
                else:
                    RideData.Ride_Names.append(attractions["name"])
            elif attractions["entityType"] == "SHOW":
                temp = temp.json()
                if len(temp["liveData"]) <= 0:
                    ShowData.Show_Names.append(
                        "--Unknown Status-- " + attractions["name"]
                    )
                elif temp["liveData"][0]["status"] != "OPERATING":
                    ShowData.Show_Names.append(
                        "-- Not Running -- " + attractions["name"]
                    )
                else:
                    ShowData.Show_Names.append(attractions["name"])
            elif attractions["entityType"] == "RESTAURANT":
                temp = temp.json()
                if len(temp["liveData"]) <= 0:
                    RestaurantData.Restaurant_Names.append(
                        "--Unknown Status-- " + attractions["name"]
                    )
                elif temp["liveData"][0]["status"] != "OPERATING":
                    RestaurantData.Restaurant_Names.append(
                        "-- Closed -- " + attractions["name"]
                    )
                else:
                    RestaurantData.Restaurant_Names.append(attractions["name"])


class TempVars:
    TempParkSelection = customtkinter.StringVar()
    TempRideSelection = customtkinter.StringVar()
    TempErrorCheck = True


class ButtonFuncs:
    def SelectParkFunc():
        userVariables.selected_Park = TempVars.TempParkSelection.get()
        if userVariables.selected_Park != "":
            ParkTimeInfo.parkStatusChecker()
            firstScreenFuncs.removeWidgets()
            app.title(f"Wait Time App - {userVariables.selected_Park} - Loading...")
            if ParkTimeInfo.parkOpened == "Open":
                AttractionFuncs.jasonLoader()
                AttractionFuncs.NameAdder()
            secondScreenFuncs.screenInit()

    def BackMain():
        secondScreenFuncs.removeWidgets()
        firstScreenFuncs.screenInit()

    def SelectTypeFunc(type):
        userVariables.selected_Type = type
        secondScreenFuncs.removeWidgets()
        thirdScreen.screenInit()

    def backType():
        thirdScreen.removeWidgets()
        secondScreenFuncs.screenInit()

    def SelectRideFunc():
        userVariables.selected_Ride = TempVars.TempRideSelection.get()

        
        if userVariables.selected_Type == "Rides":
            WaitTimeFuncs.rideWaits()
            if TempVars.TempErrorCheck == True:
                thirdScreen.removeWidgets()
                fourthScreen.screenInit()
    def backRide():
        fourthScreen.removeWidgets()
        thirdScreen.screenInit()


class WaitTimeFuncs:
    def rideWaits():
        userVariables.selected_Ride = TempVars.TempRideSelection.get()
        for attractions in AttractionFuncs.parkJason["children"]:
            if attractions["name"] == userVariables.selected_Ride:
                userVariables.selected_RideId = attractions["id"]
                break
        temp = web.get(Urls.Ride_Time_URL.format(userVariables.selected_RideId))
        if UtilityFuncs.jasonCheck(temp) == False:
            psg.popup_error(
                f"Cannot Find any data on this particular {userVariables.selected_Type}\nThis could mean the data set is not JSON"
            )
            TempVars.TempErrorCheck = False
            return 
        temp = temp.json()
        if "liveData" not in temp:
            psg.popup_error(
                f"Cannot Find any data on this particular {userVariables.selected_Type}\nThis could mean the data set is down or the request is not running correctly"
            )
            TempVars.TempErrorCheck = False
            return 
        if "queue" not in temp["liveData"][0]:
            psg.popup_error(
                f"The {userVariables.selected_Type} is not responding with any data in terms of wait time"
            )
            TempVars.TempErrorCheck = False
            return
        temp = temp["liveData"][0]["queue"]
        if "STANDBY" in temp:
            RideData.standby = temp["STANDBY"]["waitTime"]
        if "SINGLE_RIDER" in temp:
            RideData.single = temp["SINGLE_RIDER"]["waitTime"]
        if "PAID_RETURN_TIME" in temp:
            if "price" in temp["PAID_RETURN_TIME"]:
                RideData.lightningCurrency = temp["PAID_RETURN_TIME"]["price"][
                    "currency"
                ]
                RideData.lightningPrice = temp["PAID_RETURN_TIME"]["price"]["amount"]
            RideData.lightningState = temp["PAID_RETURN_TIME"]["state"]
            RideData.lightningStart = temp["PAID_RETURN_TIME"]["returnStart"]
            RideData.lightningEnd = temp["PAID_RETURN_TIME"]["returnEnd"]
        if "BOARDING_GROUP" in temp:
            RideData.boardingState = temp["BOARDING_GROUP"]["allocationStatus"]
            RideData.boardingStart = temp["BOARDING_GROUP"]["currentGroupStart"]
            RideData.boardingEnd = temp["BOARDING_GROUP"]["currentGroupEnd"]
            RideData.boardingTime = temp["BOARDING_GROUP"]["estimatedWait"]
            RideData.boardingNext = temp["BOARDING_GROUP"]["nextAllocationTime"]

# App Screens
class firstScreenFuncs:
    def screenInit():
        app.title("Wait Time App")
        app.geometry("550x275")
        app.resizable(False,False)
        app.grid_columnconfigure((0, 1, 2), weight=1)
        app.grid_rowconfigure(
            (
                0,
                1,
                2,
            ),
            weight=1,
        )
        # Label
        mainTitle = customtkinter.CTkLabel(
            app, text="Welcome to the\nDisney Park Wait Time Tracker Desktop App"
        )
        mainTitle.grid(row=0, column=1, sticky="ew")
        # Park Selection
        ParkSelectionLabel = customtkinter.CTkLabel(app, text="Select a Park:")
        ParkSelectionLabel.grid(row=1, column=0, sticky="ew")
        ParkSelectionMenu = customtkinter.CTkOptionMenu(
            app, values=menuOptions.Park_options, variable=TempVars.TempParkSelection
        )
        ParkSelectionMenu.grid(row=1, column=1, sticky="ew")
        ParkSelectionButton = customtkinter.CTkButton(
            app, text="Select Park", command=ButtonFuncs.SelectParkFunc
        )
        ParkSelectionButton.grid(row=1, column=2)
        # Exit Button
        ExitButton = customtkinter.CTkButton(app, text="Exit",width=528, command=lambda: exit())
        ExitButton.grid(row=2, column=0, columnspan = 3,padx=0)

    def removeWidgets():
        for widgets in app.winfo_children():
            widgets.destroy()


class secondScreenFuncs:
    def screenInit():
        app.title(f"Wait Time App - {userVariables.selected_Park}")
        app.grid_columnconfigure((0, 1, 2), weight=1)
        app.grid_rowconfigure((0, 1, 2), weight=1)
        # Time
        ParkOpenHours = customtkinter.CTkLabel(
            app,
            text=f"Park Hours:\n{ParkTimeInfo.parkOperationOpen} - {ParkTimeInfo.parkOperationClosed}",
        )
        ParkOpenHours.grid(row=0, column=0)
        ParkOpened = customtkinter.CTkLabel(
            app, text=f"The park is {ParkTimeInfo.parkOpened}"
        )
        ParkOpened.grid(row=0, column=1)
        ParkTime = customtkinter.CTkLabel(
            app, text=f"Park Time: {ParkTimeInfo.parkTime}\n"
        )
        ParkTime.grid(row=0, column=2)
        # Type Buttons
        if ParkTimeInfo.parkOpened == "Open":
            RideButton = customtkinter.CTkButton(
                app, text="Rides", command=lambda: ButtonFuncs.SelectTypeFunc("Rides")
            )
            RideButton.grid(row=1, column=0)
            ShowButton = customtkinter.CTkButton(
                app, text="Shows", command=lambda: ButtonFuncs.SelectTypeFunc("Shows")
            )
            ShowButton.grid(row=1, column=1)
            RestaurantButton = customtkinter.CTkButton(
                app,
                text="Restaurant",
                command=lambda: ButtonFuncs.SelectTypeFunc("Restaurant"),
            )
            RestaurantButton.grid(row=1, column=2)
        else:
            ParkOpened.grid_forget()
            ClosedLabel = customtkinter.CTkLabel(
                app, text=f"{ParkTimeInfo.parkOpened}"
            )
            ClosedLabel.grid(row=1, column=0, sticky="ew", columnspan=3, padx=225)
        # Back Button
        BackButton = customtkinter.CTkButton(
            app, text="Back", command=ButtonFuncs.BackMain,width=264, 
        )
        BackButton.grid(row=2, column=0, sticky="ew", padx=0)

        # Exit Button
        ExitButton = customtkinter.CTkButton(app, text="Exit",width=264,  command=lambda: exit())
        ExitButton.grid(row=2, column=2, sticky="ew", padx=0)

    def removeWidgets():
        for widgets in app.winfo_children():
            widgets.destroy()


class thirdScreen:
    def screenInit():
        app.title(
            f"Wait Time App - {userVariables.selected_Park} - {userVariables.selected_Type}"
        )
        app.geometry("550x275")
        app.grid_columnconfigure((0, 1, 2), weight=1)
        app.grid_rowconfigure((0, 1, 2), weight=1)

        TypeLabel = customtkinter.CTkLabel(
            app, text=f"Select a {userVariables.selected_Type}:"
        )
        TypeLabel.grid(row=1, column=0)
        if userVariables.selected_Type == "Rides":
            RideChoiceMenu = customtkinter.CTkOptionMenu(
                app, variable=TempVars.TempRideSelection, values=RideData.Ride_Names
            )
        elif userVariables.selected_Type == "Shows":
            RideChoiceMenu = customtkinter.CTkOptionMenu(
                app, variable=TempVars.TempRideSelection, values=ShowData.Show_Names
            )
        elif userVariables.selected_Type == "Restaurants":
            RideChoiceMenu = customtkinter.CTkOptionMenu(
                app,
                variable=TempVars.TempRideSelection,
                values=RestaurantData.Restaurant_Names,
            )
        RideChoiceMenu.grid(row=1, column=1, columnspan=2)
        RideChoiceButton = customtkinter.CTkButton(
            app,
            text=f"Select {userVariables.selected_Type}",
            command=ButtonFuncs.SelectRideFunc,
        )
        RideChoiceButton.grid(row=1, column=3)
        # Back Button
        BackButton = customtkinter.CTkButton(
            app, text="Back", command=ButtonFuncs.backType, width=264
        )
        BackButton.grid(row=2, column=0, sticky="ew",columnspan=2, padx=0)
        #Seperator
        
        # Exit Button
        ExitButton = customtkinter.CTkButton(app, text="Exit", width=264,command=lambda: exit())
        ExitButton.grid(row=2, column=2,sticky="ew" , columnspan=2,padx=0)

    def removeWidgets():
        for widgets in app.winfo_children():
            widgets.destroy()


class fourthScreen:
    def screenInit():
        app.title(
            f"Wait Time App - {userVariables.selected_Park} - {userVariables.selected_Type}"
        )
        app.geometry("800x500")
        app.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        app.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Standby and Single Rider Frame
        standSingleFrame = customtkinter.CTkFrame(app)
        standSingleFrame.grid(row=0, column=0, columnspan=5, sticky="nsew")
        standSingleFrame.grid_columnconfigure((0, 1), weight=1)
        StandByLabel = customtkinter.CTkLabel(standSingleFrame, text=f"\nStandby Time (min)\n{RideData.standby}\n")
        StandByLabel.grid(row=0, column=0, padx=50)
        SingleLabel = customtkinter.CTkLabel(standSingleFrame, text=f"\nSingle Rider Wait Time (min)\n{RideData.single}\n")
        SingleLabel.grid(row=0, column=1, padx=50)

        # Lightning Lane Frame
        LightningFrame = customtkinter.CTkFrame(app)
        LightningFrame.grid(row=1, column=0, columnspan=5, sticky="nsew")
        LightningFrame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        LightningStatusLabel = customtkinter.CTkLabel(LightningFrame, text=f"\nLightning Lane Status\n{RideData.boardingState}\n")
        LightningPriceLabel = customtkinter.CTkLabel(LightningFrame, text=f"\nLightning Lane Price\n{RideData.lightningPrice} {RideData.lightningCurrency}\n")
        LightningStartLabel = customtkinter.CTkLabel(LightningFrame, text=f"\nLightning Lane Start Time\n{RideData.lightningStart}\n")
        LightningEndLabel = customtkinter.CTkLabel(LightningFrame, text=f"\nLightning Lane End Time\n{RideData.lightningEnd}\n")
        LightningStatusLabel.grid(row=1, column=0, padx=25)
        LightningPriceLabel.grid(row=1, column=1, padx=25)
        LightningStartLabel.grid(row=1, column=2, padx=25)
        LightningEndLabel.grid(row=1, column=3, padx=25)

        # Boarding Group Frame
        BoardingFrame = customtkinter.CTkFrame(app)
        BoardingFrame.grid(row=2, column=0, columnspan=5, sticky="nsew")
        BoardingFrame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        BoardingStatusLabel = customtkinter.CTkLabel(BoardingFrame, text=f"\nBoarding Group Status\n{RideData.boardingState}\n")
        BoardingStartLabel = customtkinter.CTkLabel(BoardingFrame, text=f"\nBoarding Group Start Time\n{RideData.boardingStart}\n")
        BoardingWaitLabel = customtkinter.CTkLabel(BoardingFrame, text=f"\nBoarding Group Wait Time\n{RideData.boardingTime}\n")
        BoardingNextLabel = customtkinter.CTkLabel(BoardingFrame, text=f"\nBoarding Group Next Time\n{RideData.boardingNext}\n")
        BoardingStatusLabel.grid(row=1, column=0, padx=10)
        BoardingStartLabel.grid(row=1, column=1, padx=10)
        BoardingWaitLabel.grid(row=1, column=2, padx=10)
        BoardingNextLabel.grid(row=1, column=3, padx=10)

        # Back Button
        BackButton = customtkinter.CTkButton(
            app, text="Back", command=ButtonFuncs.backRide
        )
        BackButton.grid(row=3, column=0, columnspan=5, sticky="ew")
        # Seperator
        Seperator = customtkinter.CTkLabel(app, text=" ")
        Seperator.grid(row=4, column=0, columnspan=5, sticky="ew")
        # Exit Button
        ExitButton = customtkinter.CTkButton(app, text="Exit", command=lambda: exit())
        ExitButton.grid(row=5, column=0, columnspan=5, sticky="ew")

    def removeWidgets():
        for widgets in app.winfo_children():
            widgets.destroy()

class AppInit:
    def App():
        if UtilityFuncs.wifiCheck():
            UtilityFuncs.MinimizeTerminal()
            firstScreenFuncs.screenInit()
            app.mainloop()
        else:
            psg.popup_error(
                "Having issues connecting to the internet\n Retry when you are connected",
                title="Error 404 - Connectivity Error",
            )

AppInit.App()