from bs4 import BeautifulSoup
from get_players import
def create_cached_player_page():
    with open('player_page_html_data.html','wb')


def get_cached_player_page():
    f = open('player_page_html_data.html','rb')
    soup = BeautifulSoup(f.read())
    return soup


