Ride_Ids_URL = "https://api.themeparks.wiki/v1/entity/{}/children"
Park_Time_URL = "https://api.themeparks.wiki/v1/entity/{}/schedule"
Ride_Time_URL = "https://api.themeparks.wiki/v1/entity/{}/live"
All_Park_Ids_URL = "https://api.themeparks.wiki/v1/destinations"
Entity_Data_URL = "https://api.themeparks.wiki/v1/entity/{}"


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
    "California Adventure": "disneycaliforniaadventurepark",
    "Magic Kingdom": "magickingdompark",
    "EPCOT": "epcot",
    "Hollywood Studios": "disneyshollywoodstudios",
    "Animal Kingdom": "disneysanimalkingdomthemepark",
    "Tokyo Disneyland": "tokyodisneyland",
    "Tokyo DisneySea": "tokyodisneysea",
    "Disneyland Paris": "dae968d5-63d-4719-8b6-3d17e94441",
    "Walt Disney Studios Park": "ca888437-ebb4-4d50-aed2-d227f7096968",
    "Hong Kong Disneyland": "bd0eb47b-2f02-4d4d-90fa-cb3a68988e3b",
    "Shanghai Disneyland": "shanghaidisneyland",
}
Park_options = [
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
resortNames = [
    "Walt Disney World® Resort",
    "Tokyo Disney Resort",
    "Shanghai Disney Resort",
    "Disneyland Paris",
    "Disneyland Resort",
    "Hong Kong Disneyland Parks",
]


parkWantedTimeZone = None
SpecialEvent = False
completed = None

parkOpened = ""
parkTime = ""
parkOperationOpen = ""
parkOperationClosed = ""

Type_Options = ["Rides", "--DEV-- Shows --DEV--", "--WIP-- Restaurants --WIP--"]


# Ride Vars
Ride_Name = []
Ride_Ids = ""
Ride_Closed = ""

Ride_Status = ""

selected_Park = ""
selected_Type = ""
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

#Restaruant Vars






#Show Vars
Show_Name = ""
Show_Ids = ""
Show_Times = []