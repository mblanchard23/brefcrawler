from db_tables import session, Players, Player_Season_Totals
from player_page import player_page
from logs import log_client
from get_players import get_players_dataframe

''' Players List '''


def insert_players(session, lst):
    ''' Inserts a lst of player dicts'''
    for player in lst:
        try:
            p = Players(**player)
            session.add(p)
            session.commit()
        except:
            print('%s already exists, skipping' % p.player_name)
            session.rollback()
            continue

    return None


def insert_all_players():

    letters_of_alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for letter in letters_of_alphabet:
        try:
            df = get_players_dataframe(letter)
            insert_players(session, df.to_dict(orient='records'))

        except:
            print('Letter not found: %s' % letter)


''' Player Season Totals '''


def insert_player_season_totals(player_id):
    pp = player_page(player_id)
    lst = pp.totals.to_dict(orient='records')
    error_lst = []
    for season_summary in lst:
        pst = Player_Season_Totals(**season_summary)

        session.add(pst)

        try:
            session.commit()
        except:
            session.rollback()

    if error_lst:
        log_client.captureMessage(str(error_lst))


def insert_list_player_season_totals(list_of_player_ids):
    for player_id in list_of_player_ids:
        try:
            insert_player_season_totals(player_id)
        except:
            log_client.captureMessage('Insert Failed for {player_id}'.format(player_id=player_id))
