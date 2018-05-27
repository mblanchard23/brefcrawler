"""Grab and parse shot chart data for each game
BREF's unique game_id is of the form YYYYMMDD0{3_letter_hometeam_abbreviation}
This lambda can generate a game_id from a player_gamelog
create_game_id = lambda x: str(x['date']).replace('-','') + '0' + (x['team'] if x['home_away'] == 'H' else x['opponent'] )
"""
import requests, pandas
from bs4 import BeautifulSoup


def get_boxscore_shotchart(game_id):
    base_url = 'https://www.basketball-reference.com/boxscores/shot-chart/{game_id}.html'

    req = requests.get(base_url.format(game_id=game_id))
    if req.status_code == 404:
        print('Game %s does not exist' % game_id)
        return None

    else:
        return req


def parse_shot_tag(shot_tag):
    if shot_tag.get('class')[0] != 'tooltip':
        return 'Something went wrong'

    shot_data = {'quarter': shot_tag.get('class')[1].split('-')[1]
        , 'player_id': shot_tag.get('class')[2][2:]
        , 'make': 1 if shot_tag.get('class')[3] == 'make' else 0
        , 'x_coord': shot_tag.get('style').split(';')[0][4:-2]
        , 'y_coord': shot_tag.get('style').split(';')[1][5:-2]
                 }

    tip = shot_tag.get('tip').split('<br>')
    shot_data['time_remaining'] = tip[0].split(', ')[1].split(' remaining')[0].zfill(7)
    shot_data['minutes_remaining'] = shot_data['time_remaining'].split(':')[0]
    shot_data['seconds_remaining'] = shot_data['time_remaining'].split(':')[1][:2]
    shot_data['deciseconds_remaining'] = shot_data['time_remaining'][-1]
    shot_data['distance'] = tip[1].split(' ')[-2]
    shot_data['shot_type'] = tip[1].split(' ')[-4].split('-')[0]
    shot_data['new_score'] = tip[2].split(' ')[-1]
    return shot_data


def parse_boxscore_shotchart(request_text):
    """Return a DataFrame of shots from a game"""
    soup = BeautifulSoup(request_text, 'html.parser')
    shot_charts = [x for x in soup.find_all('div') if 'shot-area' in x.get('class', [])]
    shots = shot_charts[0].find_all('div') + shot_charts[1].find_all('div')
    df = pandas.DataFrame(parse_shot_tag(x) for x in shots)
    return df


def get_game_shotdata_as_df(game_id):
    req = get_boxscore_shotchart(game_id)
    if not req:
        return None
    else:
        df = parse_boxscore_shotchart(req.text)
        df['game_id'] = game_id
        return df
