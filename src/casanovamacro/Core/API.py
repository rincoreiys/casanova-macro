import json
import requests

from  .Global import SERVER_ADDRESS, config

def patch(url:str, json:json):
    print(f"Test:Patch:URL is {SERVER_ADDRESS}/{url} and data is {json}")
    return requests.patch(f"{SERVER_ADDRESS}/{url}", json=json)

def post(url:str, json:json):
    print(f"Test:Patch:URL is {SERVER_ADDRESS}/{url} and data is {json}")
    return requests.post(f"{SERVER_ADDRESS}/{url}", json=json)


def get(url:str):
    return requests.get(f"{SERVER_ADDRESS}/{url}").json()


def update_character(json):
    response =  patch(f"character/{config.nickname}/update",json=json).json()
    print(f"Test:Updating character:{response}")