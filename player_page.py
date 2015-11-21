import requests
from bs4 import BeautifulSoup
import sqlite3

baseurl = "http://www.basketball-reference.com/players/{firstletter}/{playerid}.html"
testurl = "http://www.basketball-reference.com/players/r/roseja01.html"
testid = "roseja01"



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

def ifnull(*args):
	for elem in args:
		if elem:
			return elem
		return 'null'

def ifnull2(generator):
	for string in generator:
		if not string:
			return null
		else:
			return string
		# if elem:
		# 	return elem
		# return 'null'

def seasons_tablify(soup_table,delimiter=",",qualifier=None,player_id=None):
	#Converts a HTML table into a character separated table. Option to set delimiter and cell qualifier
	table_out = ''

	if not qualifier:
		for row in soup_table.find_all('tr'):
			if player_id:
				row_string = player_id + delimiter
			else:
				row_string = ''
			

			for cell in row.find_all('td'):
				row_string += ifnull2(cell.strings) + delimiter
			table_out += row_string[0:len(row_string)-len(delimiter)] + '\n'

		return table_out

	else:
		for row in soup_table.find_all('tr'):
			if player_id:
				row_string = qualifier + player_id + qualifier + delimiter
			else:
				row_string = ''
			for cell in row.find_all('td'):
				row_string += qualifier + ifnull(cell.string) + qualifier + delimiter
			table_out += row_string[0:len(row_string)-len(delimiter)] + '\n'

		return table_out


# Grab list of all players - Split this into separate

def get_players(letter):
	url = "http://www.basketball-reference.com/players/{letter}/"
	url = url.format(letter=letter)
	resp = requests.get(url)
	if resp.status_code == 200:
		soup = BeautifulSoup(resp.text,'html.parser')
		return soup # get_rid
		playertable = soup.find_all('table')[0].tbody 
		return playertable
	else:
		return None

def player_tablify(soup_table,delimiter=",",qualifier=None):
	#Used in grabbing all player details
	table_out = ''

	if not qualifier:
		for row in soup_table.tbody.find_all('tr'):
			if row.a:
				row_string = ifnull(row.a['href'].split('/')[-1][:-5]) + delimiter
				for cell in row.find_all('td'):
					row_string += ifnull(cell.string,'null') + delimiter
				table_out += row_string[0:len(row_string)-len(delimiter)] + '\n'
			else:
				continue
		return table_out

	else:
		for row in soup_table.tbody.find_all('tr'):
			if row.a:
				row_string = qualifier + ifnull(row.a['href'].split('/')[-1][:-5]) + qualifier + delimiter
				for cell in row.find_all('td'):
					row_string += qualifier + ifnull(cell.string) + qualifier + delimiter
				table_out += row_string[0:len(row_string)-len(delimiter)] + '\n'
			else:
				continue
		return table_out

def tbt(table,delimiter=','):
	table = table.split('\n')
	for i,v in enumerate(table):
		table[i] = v.split(delimiter)
	return table


def create_player_SQL_table():
	conn = sqlite3.connect('db.sqlite')
	c = conn.cursor()
	alphabet = 'abcdefghijklmnopqrstuvwyz'
	for letter in alphabet:
		print "Grabbing players for %s" % letter.upper()
		ht_table = get_players(letter)
		delim_table = player_tablify(ht_table,delimiter='\t')
		player_lst = tbt(delim_table,'\t')
		print "%d players found" % len(player_lst)
		succeeded = 0
		failed = 0

		for item in player_lst:
			if len(item) == 9:
				c.execute("insert into players values(?,?,?,?,?,?,?,?,?)",item)
				succeeded += c.rowcount
			else:
				failed += 1
		
		print "%d inserts succeeded\n%d inserts failed" % (succeeded,failed)
		conn.commit()

def c():
	conn = sqlite3.connect('db.sqlite')
	return conn.cursor()

def insert_player(player_id):
	conn = sqlite3.connect('db.sqlite')
	c = conn.cursor()

	seasons_insert = 'insert into season_stats values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)' 
	player = player_page(player_id)
	lst = tbt(seasons_tablify(player.totals,player_id=player.player_id))
	rows_inserted = 0
	for season in lst:
		if len(season) > 1:
			c.execute(seasons_insert,season)
			rows_inserted += c.rowcount
	conn.commit()	
	c.close()
	return rows_inserted