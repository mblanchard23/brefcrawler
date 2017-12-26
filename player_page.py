import requests, pandas
from bs4 import BeautifulSoup
import sqlite3

baseurl = "http://www.basketball-reference.com/players/{firstletter}/{playerid}.html"

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

