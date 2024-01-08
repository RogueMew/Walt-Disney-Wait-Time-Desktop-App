import requests as web
import PySimpleGUI as psg 
def internetConnectionTest():
    try:
        test = web.get("https://google.com", timeout= 5)
        return True
    except web.ConnectionError or web.ConnectTimeout:
        return False