''' Get Per Season Level data from the Player Page '''
import requests, pandas
from bs4 import BeautifulSoup, Comment


def getpp(player_id):
	baseurl = "http://www.basketball-reference.com/players/{firstletter}/{playerid}.html"
	return requests.get(baseurl.format(firstletter=player_id[:1],playerid=player_id))





def test(player_id):
	return get_player_data(player_id)

class player_page:
	def __init__(self,player_id):
		self.player_id = player_id

		self.all_tables = self.get_player_data()
		
		self.totals = self.all_tables.get('totals', pandas.DataFrame())
		self.per_game = self.all_tables.get('per_game', pandas.DataFrame())
		self.per_minute = self.all_tables.get('per_minute', pandas.DataFrame())
		self.per_poss = self.all_tables.get('per_poss', pandas.DataFrame())
		self.advanced = self.all_tables.get('advanced', pandas.DataFrame())
		self.shooting = self.all_tables.get('shooting', pandas.DataFrame())
		self.advanced_pbp = self.all_tables.get('advanced_pbp', pandas.DataFrame())
		self.playoffs_totals = self.all_tables.get('playoffs_totals', pandas.DataFrame())
		self.playoffs_per_game = self.all_tables.get('playoffs_per_game', pandas.DataFrame())
		self.playoffs_per_minute = self.all_tables.get('playoffs_per_minute', pandas.DataFrame())
		self.playoffs_per_poss = self.all_tables.get('playoffs_per_poss', pandas.DataFrame())
		self.playoffs_advanced = self.all_tables.get('playoffs_advanced', pandas.DataFrame())
		self.playoffs_shooting = self.all_tables.get('playoffs_shooting', pandas.DataFrame())
		self.playoffs_advanced_pbp = self.all_tables.get('playoffs_advanced_pbp', pandas.DataFrame())
		self.sim_thru = self.all_tables.get('sim_thru', pandas.DataFrame())
		self.sim_career = self.all_tables.get('sim_career', pandas.DataFrame())
		self.college = self.all_tables.get('college', pandas.DataFrame())
		self.leaderboard = self.all_tables.get('leaderboard', pandas.DataFrame())
		self.salaries = self.all_tables.get('salaries', pandas.DataFrame())
		
	def get_player_page_as_request(self): 
		baseurl = "http://www.basketball-reference.com/players/{firstletter}/{playerid}.html"
		return requests.get(baseurl.format(firstletter = self.player_id[0]
								,playerid = self.player_id))


	def get_tables_from_html(self,reqtext):
		''' Take Basketball Reference player page and return {TableName:DataFrame}
			dictionary'''
		soup = BeautifulSoup(reqtext,'html.parser')
		''' Parse data tables out of HTML on page'''
		tables = soup.findAll('table')
		html_df_dict = {}
		for t in tables:
			df = pandas.read_html(str(t))[0]
			df.drop([q for q in df.columns if type(q) == str and  'Unnamed:' in q]
					, inplace=True
					, axis=1) 
			
			html_df_dict[t.get('id')] = df

		''' Parse the remaining tables out of commented HTML'''
		comments = soup.findAll(text=lambda text: isinstance(text, Comment))
		table_soups = []
		commented_df_dict = {}
		for c in comments:
			commentsoup = BeautifulSoup(c,'html.parser')
			table_soups += commentsoup.findAll('table')

		for t in table_soups:
			df = pandas.read_html(str(t))[0]
			try:
				df.drop(index=df[df.Season=='Career'].index,inplace=True)
			except:
				pass
			# If we still have the Unnamed columns popping up, add this back in...

			df.drop([q for q in df.columns if type(q) == str and  'Unnamed:' in q]
					, inplace=True
					, axis=1) 
			
			commented_df_dict[t.get('id')] = df

		return {**html_df_dict, **commented_df_dict}


	def get_player_data(self):
		req = getpp(self.player_id)
		return self.get_tables_from_html(req.text)

