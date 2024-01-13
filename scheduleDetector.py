import pytz as timezone
import datetime as time
import data as data
import requests as web

def parkStatusChecker():
    temp = web.get(data.Park_Time_URL.format(data.Park_Ids[data.selected_Park]))
    currentTime =  time.datetime.now(timezone.timezone(data.Park_TimeZones[data.selected_Park]))
    temp = temp.json()
    if "schedule" in temp:
        data.parkTime = currentTime.strftime("%H:%M:%S")
        for tickets in temp["schedule"]:
            if str(tickets["date"]) == currentTime.strftime("%Y-%m-%d") and tickets["type"] == "OPERATING":
                currentTimeList = currentTime.strftime("%H:%M:%S").split(":")
                data.parkOperationOpen = tickets["openingTime"].split("T")[-1].split("+")[0].split("-")[0]
                data.parkOperationClosed = tickets["closingTime"].split("T")[-1].split("+")[0].split("-")[0]
                closingTimeList = tickets["closingTime"].split("T")[-1].split("+")[0].split("-")[0].split(":")
                openingTimeList = tickets["openingTime"].split("T")[-1].split("+")[0].split("-")[0].split(":")
                if closingTimeList[0] == '00':
                    closingTimeList[0] = '24'
                if (
                    (int(openingTimeList[0]) < int(currentTimeList[0]) < int(closingTimeList[0])) or
                    (int(openingTimeList[0]) == int(currentTimeList[0]) and int(openingTimeList[1]) <= int(currentTimeList[1])) or
                    (int(closingTimeList[0]) == int(currentTimeList[0]) and int(closingTimeList[1]) > int(currentTimeList[1])) or
                    (closingTimeList[0] == '00' and (
                        int(currentTimeList[0]) < int(openingTimeList[0]) or
                        (int(currentTimeList[0]) == int(openingTimeList[0]) and int(currentTimeList[1]) < int(openingTimeList[1]))
                    ))
                ):
                    data.parkOpened = "Open"
                else:
                    data.parkOpened = "Closed"