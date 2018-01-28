''' Handlers for the Player List pages /players/{firstletter} 
	This only returns a small dataset on each player like Name, College, Draft Year'''

import pandas
import requests
import datetime
import os
from bs4 import BeautifulSoup

baseurl = "http://www.basketball-reference.com/players/{firstletter}/{playerid}.html"
players_url = "http://www.basketball-reference.com/players/{firstletter}/"
bref_date_transformation = lambda x: datetime.datetime.strptime(str(x),'%B %d, %Y').strftime('%Y-%m-%d') if pandas.notnull(x) else None

def validate_players_table(df):
    if df.columns.tolist() == ['Player', 'From', 'To', 'Pos', 'Ht', 'Wt', 'Birth Date', 'College']:
        return True
    else:
        return False


def player_id_creator(player_fullname):
    ''' Guess what player IDs should look like based on BasketBall References format
		ID format seems to use:
		{first five letters of the surname}
		+ {first two letters of forename}
		+ {counter}'''
    if len(player_fullname.split(' ')) < 2:
        return None
    else:
        return (player_fullname.split(' ')[1][:5] \
                + player_fullname.split(' ')[0][:2] \
                + '01').lower()


def check_player_ids_look_ok(df):
    ''' Check to see a good proportion of player IDs match
		what we'd expect them to be. Basketball Reference's player
		
	If 50% of calculated player_ids match, it's probably ok
	'''
    correctness_threshold = 0.5
    check_vector = df.apply(lambda x: x['player_id'] == player_id_creator(x['Player']), axis=1)
    return check_vector.value_counts().to_dict()[True] > len(check_vector) * correctness_threshold


def get_players_table(letter):
    ''' Return a BS Tag of all playes whose surname begins with letter '''
    req = requests.get(players_url.format(firstletter=letter))
    soup = BeautifulSoup(req.text, 'html.parser')
    tables = soup.find_all('table')
    table_lst = [x for x in tables if x.attrs.get('id') == 'players']
    if len(table_lst) == 1:
        return table_lst[0]  # If only one table detected
    else:
        print('Error: Unable to find player list for letter: %s' % letter)
        return None


def convert_HTML_players_table_to_df(t):
    ''' Returns a Pandas DataFrame from BS4 player table input from BREF'''

    ''' Create base table as seen on the site '''
    df = pandas.read_html(str(t))[0]
    assert validate_players_table(
        df), 'Player table format unexpected. Either table download failed or BR has changed its format'

    '''Enrichment past the basic table provided by Basketball Ref'''

    '''1. Identify Hall of Famers and remove the asterisk from their Names!'''
    df['hall_of_fame'] = df.Player.map(lambda x: '*' in x)
    df.Player = df.Player.map(lambda x: x.replace('*', ''))

    '''2. Grab Player IDs '''

    player_id_series = []
    for row in t.find_all('tr'):
        if row.th.attrs.get('data-append-csv'):
            player_id_series.append(row.th.attrs.get('data-append-csv'))

    if len(player_id_series) == len(df):
        df['player_id'] = player_id_series
        if check_player_ids_look_ok(df):
            return df
        else:
            print('Unable to parse Player IDs')
            df.drop('player_id', inplace=True)
            return df


def get_players_dataframe(letter):
    t = get_players_table(letter)
    df = convert_HTML_players_table_to_df(t)

    '''Rename BRef's columns to friendlier DB ones'''
    df.rename(columns={'player_id':'id'
                            ,'Player':'player_name'
                            ,'From':'year_from'
                            ,'To':'year_to'
                            ,'Pos':'position'
                            ,'Ht':'height'
                            ,'Wt':'weight'
                            ,'Birth Date':'birth_date'
                            ,'College':'college'
                            ,'hall_of_fame':'hall_of_fame'}
              ,inplace=True)
    df.birth_date = df.birth_date.map(bref_date_transformation)

    return df


def insert_all_players():
    letters_in_alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for letter in letters_of_alphabet:
        try:
            df = get_players_dataframe(letter)
            pass
        except:
            print('Letter not found: %s' % letter)