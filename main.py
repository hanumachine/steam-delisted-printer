import requests

API_KEY = ""
STEAM_ID = ""

def get_owned_games(api_key, steam_id):
    url = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return [game['appid'] for game in data['response']['games']]

def check_game_availability(appid):
    url = f'https://store.steampowered.com/api/appdetails?appids={appid}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data[str(appid)]['success'] and data[str(appid)]['data']['is_free'] is False and not data[str(appid)]['data']['is_dlc']

def main():
    owned_games = get_owned_games(API_KEY, STEAM_ID)
    unavailable_games = []

    for appid in owned_games:
        if not check_game_availability(appid):
            unavailable_games.append(appid)
            print(f"Game with AppID {appid} is no longer available for purchase.")

    if not unavailable_games:
        print("All games in the library are available for purchase.")
    else:
        print("List of games no longer available for purchase:", unavailable_games)

if __name__ == '__main__':
    main()