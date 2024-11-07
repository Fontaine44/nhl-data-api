import requests

NHL_API_1 = 'https://api.nhle.com'
NHL_API_2 = 'https://api-web.nhle.com/v1'

def get_teams():
    url = f"{NHL_API_1}/stats/rest/en/franchise?sort=fullName&include=lastSeason.id&include=firstSeason.id&include=teams"
    response = requests.get(url)
    return response.json()

def get_players(team_abbrev):
    url = f"{NHL_API_2}/roster/{team_abbrev}/20242025"
    response = requests.get(url)
    return response.json()

def get_games(team_abbrev):
    url = f"{NHL_API_2}/club-schedule-season/{team_abbrev}/20242025"
    response = requests.get(url)
    return response.json()