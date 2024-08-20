import requests
import json
from database import registerUserDB
from database import fetchStartdataDB

api_key = ''

def getSteamData():
    # Your Steam API key
    steam_id = '76561198050659307'

    # URL for the GetPlayerSummaries API endpoint
    url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}'

    # Make the request
    response = requests.get(url)

    if response.status_code == 200:

        # Parse the JSON response
        player_summary = response.json()


        # Output the result
        print(player_summary['response']['players'][0]['personastate'])
        return player_summary['response']['players'][0]['personastate']
    else: 
        print("Failed to request from Steam")


def getUserInfo(steam_id: str, discord_id):
    # Your Steam API key

    # URL for the GetPlayerSummaries API endpoint
    url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}'

    # Make the request
    response = requests.get(url)

    if response.status_code == 200:

        # Parse the JSON response
        player_summary = response.json()
        registerUserDB(player_summary, discord_id, steam_id)

       
        
    else: 
        print("Failed to request from Steam")


