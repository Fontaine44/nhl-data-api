import requests

NHL_API_1 = 'https://api.nhle.com'
NHL_API_2 = 'https://api-web.nhle.com/v1'

TEAMS = [
    "ANA", "BOS", "BUF", "CGY", "CAR", "CHI", "COL", "CBJ", "DAL", "DET", "EDM", "FLA", "LAK", "MIN", "MTL", "NSH", "NJD", "NYI", "NYR", "OTT", "PHI", "PIT", "SJS", "SEA", "STL", "TBL", "TOR", "UTA", "VAN", "VGK", "WSH", "WPG"
]

def get_teams():
    url = f"{NHL_API_1}/stats/rest/en/franchise?sort=fullName&include=lastSeason.id&include=firstSeason.id&include=teams"
    response = requests.get(url)
    franchises = response.json()['data']
    filtered_teams = []

    for franchise in franchises:
        teams = franchise['teams']
        for team in teams:
            if team['triCode'] in TEAMS:
                filtered_teams.append(
                    {
                        'id': team['id'],
                        'fullName': team['fullName'],
                        'triCode': team['triCode']
                    }
                )

    return { 'teams': filtered_teams }

def get_players(team_abbrev):
    url = f"{NHL_API_2}/roster/{team_abbrev}/20242025"
    response = requests.get(url)
    return response.json()

def get_games(team_abbrev):
    url = f"{NHL_API_2}/club-schedule-season/{team_abbrev}/20242025"
    response = requests.get(url)
    return response.json()