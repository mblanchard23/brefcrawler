import boto3, os, json
from db_tables import Players, session
from data_loads import insert_player_season_gamelog
import time

assert os.environ.get('sqs_bref_url') is not None, 'Unable to find SQS Queue URL. Load sqs_bref_url into ENV'

try:
    boto_session = boto3.Session(profile_name='brefsqs')
except:
    print('Unable to locate SQS credentials. Add to aws credentials under [brefsqs] profile')

sqs = boto_session.client('sqs')

def send_json_message(message_body):
    response = sqs.send_message(QueueUrl=os.environ.get('sqs_bref_url')
                                , MessageBody=message_body
                                , MessageGroupId='bref')
    return response


def pop_message():
    response = sqs.receive_message(QueueUrl=os.environ.get('sqs_bref_url'))
    if response.get('ResponseMetadata', {}).get('HTTPStatusCode') != 200:
        print('Message Failed')
        raise SystemError('Unable to retrieve SQS Data')
    else:
        message = response.get('Messages', [])
        if not message:
            print('Empty Queue')
            return None
        assert len(message) == 1, "Number of messages does != 1. Set the request to only return a single message"
        message_body = message[0].get('Body')
        message_id = message[0].get('ReceiptHandle')
        sqs.delete_message(QueueUrl=os.environ.get('sqs_bref_url')
                           , ReceiptHandle=message_id)
        print(message_body)
        return json.loads(message_body)


def get_latest_season():
    from sqlalchemy import func
    return session.query(func.max(Players.year_to)).all()[0][0]


def get_this_seasons_players(current_season=get_latest_season()):
    players = session.query(Players).filter(Players.year_to == current_season).all()
    player_list = [{'player_id': x.id, 'season': current_season} for x in players]
    return player_list


def add_daily_update_to_queue():
    # By default, only update players registered to play in the present season
    player_list = get_this_seasons_players()
    for player in player_list:
        send_json_message(message_body=json.dumps(player))

    return player_list


def poll_queue():
    while True:
        player = pop_message()
        insert_player_season_gamelog(**player)
        time.sleep(5)

