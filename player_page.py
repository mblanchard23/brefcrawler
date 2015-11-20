import requests
from bs4 import BeautifulSoup

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

def tablify(soup_table,delimiter=",",qualifier=None):
	#Converts a HTML table into a character separated table. Option to set delimiter and cell qualifier
	table_out = ''

	if not qualifier:
		for row in soup_table.find_all('tr'):
			row_string = ''
			for cell in row.find_all('td'):
				row_string += ifnull2(cell.strings) + delimiter
			table_out += row_string[0:len(row_string)-len(delimiter)] + '\n'

		return table_out

	else:
		for row in soup_table.find_all('tr'):
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
				row_string = ifnull(row.a['href']) + delimiter
				for cell in row.find_all('td'):
					row_string += qualifier + cell.string + qualifier + delimiter
				table_out += row_string[0:len(row_string)-len(delimiter)] + '\n'
			else:
				continue
		return table_out


def cycle():
	a = ''
	alphabet = 'bcd'
	for letter in alphabet:
		a += player_tablify(get_players(letter))

