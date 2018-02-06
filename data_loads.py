from db_tables import session, Players, Player_Season_Totals, Player_Gamelog_Totals
from player_page import player_page
from player_gamelog_page import player_career_gamelog
from logs import log_client
from get_players import get_players_dataframe


def get_all_player_ids():
    return [x.id for x in session.query(Players).all()]


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


def insert_player_career_gamelog(player_id):
    pcg = player_career_gamelog(player_id)
    game_list = [Player_Gamelog_Totals(**game) for game in pcg.career_gamelog.to_dict(orient='records')]
    for game in game_list:
        session.add(game)

    try:
        session.commit()
        return None

    except:
        log_client.captureException()
        session.rollback()
        return 'Error'


def insert_career_gamelog_list(list_of_player_ids):
    for player_id in list_of_player_ids:

        if session.query(Player_Gamelog_Totals).filter(Player_Gamelog_Totals.player_id == player_id).all() != []:
            print('%s already exists' % player_id)
            continue

        try:
            outcome = insert_player_career_gamelog(player_id)
            if outcome == 'Error':
                log_client.captureMessage('Unable to insert gamelogs for %s' % player_id)
        except:
            log_client.captureException()
