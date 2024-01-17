import requests as web
import data as data
import PySimpleGUI as psg
import json as jason


ParkjasonRaw = ""
ParkJasonRefined = ""
firstItem = "" 

def isValidJason(text):
    try:
        jason.loads(text)
        return True
    except jason.JSONDecodeError:
        return False
def JSONLooader(Park):
    global ParkjasonRaw, ParkJasonRefined
    ParkjasonRaw = web.get(data.Ride_Ids_URL.format(data.Park_Ids[Park]))
    ParkJasonRefined = ParkjasonRaw.json()
def NameAdder(Type):
    for rideNames in ParkJasonRefined["children"]:
        if Type == "Rides" and rideNames["entityType"] == "ATTRACTION":
            temp = web.get(data.Ride_Time_URL.format(rideNames["id"]))
            temp = temp.json()
            if len(temp["liveData"]) > 0:
                if temp["liveData"][0]["status"] != "OPERATING":
                    data.Ride_Name.append(" --Closed-- " + rideNames["name"] + " --Closed--")
                else:
                    data.Ride_Name.append(rideNames["name"])
            else:
                data.Ride_Name.append("--Unknown Status-- " + rideNames["name"] + " --Unknown Status--")
        if Type == "--WIP-- Shows --WIP--" and rideNames["entityType"] == "SHOW":
            temp = web.get(data.Ride_Time_URL.format(rideNames["id"]))
            temp = temp.json()
            if len(temp["liveData"]) > 0:
                if temp["liveData"][0]["status"] != "OPERATING":
                    data.Ride_Name.append(" --Not Running-- " + rideNames["name"] + " --Not Running--")
                else:
                    data.Ride_Name.append(rideNames["name"])
            else:
                data.Ride_Name.append("--Unknown Status-- " + rideNames["name"] + " --Unknown Status--")

def waitTimeGetter(ride):
    firstItem = ParkJasonRefined["children"]
    for rides in firstItem:
        if rides["name"] == ride:
            data.Ride_Ids = rides["id"]
            break
    temp = web.get(data.Ride_Time_URL.format(data.Ride_Ids)) 
    if len(temp.text) > 0:
        temp = temp.json()
        if len(temp["liveData"]) > 0:
            if temp["liveData"][0]["status"] == "OPERATING":
                if "queue" in temp["liveData"][0]:
                    if "STANDBY" in temp["liveData"][0]["queue"]:
                        data.standby = temp["liveData"][0]["queue"]["STANDBY"]["waitTime"]
                    
                    if "SINGLE_RIDER" in temp["liveData"][0]["queue"]:
                        data.single = temp["liveData"][0]["queue"]["SINGLE_RIDER"]["waitTime"]

                    if "PAID_RETURN_TIME" in temp["liveData"][0]["queue"] and temp["liveData"][0]["queue"]["PAID_RETURN_TIME"]["state"] == "AVAILABLE":
                        data.lightningState = temp["liveData"][0]["queue"]["PAID_RETURN_TIME"]["state"]
                        if "returnStart" in temp["liveData"][0]["queue"]["PAID_RETURN_TIME"]:
                            data.lightningStart = temp["liveData"][0]["queue"]["PAID_RETURN_TIME"]["returnStart"]
                        if "returnEnd" in temp["liveData"][0]["queue"]["PAID_RETURN_TIME"]:
                            data.lightningEnd = temp["liveData"][0]["queue"]["PAID_RETURN_TIME"]["returnEnd"]
                        if "price" in temp["liveData"][0]["queue"]["PAID_RETURN_TIME"]:
                            data.lightningPrice = temp["liveData"][0]["queue"]["PAID_RETURN_TIME"]["price"]["amount"]
                            data.lightningCurrency = temp["liveData"][0]["queue"]["PAID_RETURN_TIME"]["price"]["currency"]
                    
                    if "BOARDING_GROUP" in temp["liveData"][0]["queue"] and "allocationStatus" in temp["liveData"][0]["queue"]["BOARDING_GROUP"]:
                        data.boardingState = temp["liveData"][0]["queue"]["BOARDING_GROUP"]["allocationStatus"]
                        if "currentGroupStart" in temp["liveData"][0]["queue"]["BOARDING_GROUP"]:
                            data.boardingStart = temp["liveData"][0]["queue"]["BOARDING_GROUP"]["currentGroupStart"]
                        if "currentGroupEnd" in temp["liveData"][0]["queue"]["BOARDING_GROUP"]:
                            data.boardingEnd = temp["liveData"][0]["queue"]["BOARDING_GROUP"]["currentGroupEnd"]
                        if "nextAllocationTime" in temp["liveData"][0]["queue"]["BOARDING_GROUP"]:
                            data.boardingNext = temp["liveData"][0]["queue"]["BOARDING_GROUP"]["nextAllocationTime"]
                        if "estimatedWait" in temp["liveData"][0]["queue"]["BOARDING_GROUP"]:
                            data.boardingTime = temp["liveData"][0]["queue"]["BOARDING_GROUP"]["estimatedWait"]
                else:
                    data.Ride_Status = "Open" 
            elif temp["liveData"][0]["status"] != "OPERATING":
                psg.popup_error("The Ride is closed or not reporting data")
        else:
            psg.popup_error("The Ride has no data that can be read")    
    else:
        psg.popup_error("The Ride has no data that can be read")
def showTimeGetter(show):
    firstItem = ParkJasonRefined["children"]
    for show in firstItem:
        if show["name"] == show:
            data.Show_Ids = show["id"]
            break
    temp = web.get(data.Ride_Time_URL.format(data.Show_Ids))
    if len(temp.text) > 0 and isValidJason(temp.text):
        temp = temp.json()

        if "liveData" in temp:
            if len(temp["liveData"]) > 0:
                if "showTimes" in temp["liveData"][0]:
                    for Times in temp["liveData"][0]["showtimes"]:
                        data.Show_Times.append(Times["startTime"].split("T")[-1].split("-+")[0])
                        print("Done")
                else:
                    psg.popup_error("The Show has no data that can be read")  
            else:
                psg.popup_error("The Show has no data that can be read")
        else:
            psg.popup_error("The Show has no data that can be read")
    else:
        psg.popup_error("The Show has no data that can be read")
