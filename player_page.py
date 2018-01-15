''' Get Per Season Level data from the Player Page '''

import requests, pandas
from bs4 import BeautifulSoup
import sqlite3

def get_tables_from_html_text(ht_as_bs_tag):
	tables = ['<table class' + x for x in  str(ht_as_bs_tag).split('<table class')]
	t2 = [t.split('</table>')[0] + '</table>' for t in tables]
	soups = [BeautifulSoup(t,'html.parser') for t in t2]
	soup_dict = {q.table.get('id'):pandas.read_html(str(q)) for q in soups if q}
	dataframes = [pandas.read_html(t) for t in t2] 
	return soups, dataframes, soup_dict

def get_player_tables(player_id):
	baseurl = "http://www.basketball-reference.com/players/{firstletter}/{playerid}.html"
	req = requests.get(baseurl.format(firstletter=player_id[:1],playerid=player_id))
	return get_tables_from_html_text( BeautifulSoup(req.text,'html.parser'))

def get_player_html(player_id):
	baseurl = "http://www.basketball-reference.com/players/{firstletter}/{playerid}.html"
	return requests.get(baseurl.format(firstletter=player_id[:1],playerid=player_id))



def test():
	return get_player_tables('bryanko01')

class player_page:

	def __init__(self,player_id):
		self.player_id = player_id
		self.player_data = {
		"totals": ""
		,"per_game": ""
		,"per_minute": ""
		,"per_poss": ""
		,"advanced": ""
		,"shooting": ""
		,"advanced_pbp": ""
		,"playoffs_totals": ""
		,"playoffs_per_game": ""
		,"playoffs_per_minute": ""
		,"playoffs_per_poss": ""
		,"playoffs_advanced": ""
		,"playoffs_shooting": ""
		,"playoffs_advanced_pbp": ""
		,"sim_thru": ""
		,"sim_career": ""
		,"college": ""
		,"leaderboard": ""
		,"salaries": ""
		}

		self.player_url = baseurl.format(firstletter=player_id[0],playerid=player_id)
		resp = requests.get(self.player_url)
		if resp.status_code == 200:
			resp = resp.text
		else:
			resp = None

		self.all = resp

		soup = BeautifulSoup(resp.encode('utf8'),'html.parser')
		tables = soup.find_all('table')

		for item in tables:
			try:
				tablename = item['id']
				
			except KeyError:
				continue

			self.player_data[tablename] = item.tbody
		self.totals = self.player_data['totals'] #Special attribute for the totals table

