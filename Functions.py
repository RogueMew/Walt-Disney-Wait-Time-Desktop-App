import requests
import data as data

Ride_Ids_URL = "https://api.themeparks.wiki/v1/entity/{}/children"
Park_Time_URL = "https://api.themeparks.wiki/v1/entity/{}/schedule"
Ride_Time_URL = "https://api.themeparks.wiki/v1/entity/{}/live"

ParkjasonRaw = ""
ParkJasonRefined = ""
firstItem = "" 

def JSONLooader(Park):
    global ParkjasonRaw, ParkJasonRefined
    ParkjasonRaw = requests.get(Ride_Ids_URL.format(data.Park_Ids[Park]))
    ParkJasonRefined = ParkjasonRaw.json()
    print("Completed")

def NameAdder(Type):
    firstItem = ParkJasonRefined["children"]
    for rideNames in firstItem:
        data.Ride_Name.append(rideNames["name"])
        data.Ride_Ids.append({"{}".format(rideNames["name"]) : "{}".format(rideNames["id"])})