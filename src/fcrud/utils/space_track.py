import requests
import json
# import xlsxwriter
import time
from datetime import datetime
import os

uriBase = "https://www.space-track.org"
requestLogin = "/ajaxauth/login"
requestCmdAction = "/basicspacedata/query"
requestFindStarlinks = "/class/tle_latest/NORAD_CAT_ID/>40000/ORDINAL/1/OBJECT_NAME/STARLINK~~/format/json/orderby/NORAD_CAT_ID%20asc"
requestOMMStarlink1 = "/class/omm/NORAD_CAT_ID/"
requestOMMStarlink2 = "/orderby/EPOCH%20asc/format/json"

configUsr = os.getenv('SLTRACK_USERNAME')
configPwd = os.getenv('SLTRACK_PASSWORD')
siteCred = {'identity': configUsr, 'password': configPwd}



def login():
    with requests.Session() as session:
        resp = session.post(uriBase + requestLogin, data=siteCred)
        r = session.get("https://www.space-track.org/basicspacedata/modeldef/class/launch_site/format/json")
        return r


def launch_site():
    with requests.Session() as session:
        resp = session.post(uriBase + requestLogin, data=siteCred)
        r = session.get(f"{uriBase}{requestCmdAction}/class/launch_site/format/json")
        return r.json()


def boxscore():
    with requests.Session() as session:
        resp = session.post(uriBase + requestLogin, data=siteCred)
        r = session.get(f"https://www.space-track.org/basicspacedata/query/class/boxscore/format/json")
        return r.json()


def satcat():
    with requests.Session() as session:
        resp = session.post(uriBase + requestLogin, data=siteCred)
        r = session.get(f"https://www.space-track.org/basicspacedata/query/class/satcat/format/json")
        return r.json()


def basic_space_data(class_name: str):
    with requests.Session() as session:
        resp = session.post(uriBase + requestLogin, data=siteCred)
        r = session.get(f"https://www.space-track.org/basicspacedata/query/class/{class_name}/format/json")
        return r.json()
