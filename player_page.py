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

		self.totals = self.all_tables.get('totals', pandas.DataFrame()).pipe(self.add_player_id).pipe(self.remap).pipe(self.create_composite_key).pipe(self.convert_nullcolumns_from_number)
		self.per_game = self.all_tables.get('per_game', pandas.DataFrame()).pipe(self.add_player_id)
		self.per_minute = self.all_tables.get('per_minute', pandas.DataFrame()).pipe(self.add_player_id)
		self.per_poss = self.all_tables.get('per_poss', pandas.DataFrame()).pipe(self.add_player_id)
		self.advanced = self.all_tables.get('advanced', pandas.DataFrame()).pipe(self.add_player_id)
		self.shooting = self.all_tables.get('shooting', pandas.DataFrame()).pipe(self.add_player_id)
		self.advanced_pbp = self.all_tables.get('advanced_pbp', pandas.DataFrame()).pipe(self.add_player_id)
		self.playoffs_totals = self.all_tables.get('playoffs_totals', pandas.DataFrame()).pipe(self.add_player_id)
		self.playoffs_per_game = self.all_tables.get('playoffs_per_game', pandas.DataFrame()).pipe(self.add_player_id)
		self.playoffs_per_minute = self.all_tables.get('playoffs_per_minute', pandas.DataFrame()).pipe(self.add_player_id)
		self.playoffs_per_poss = self.all_tables.get('playoffs_per_poss', pandas.DataFrame())
		self.playoffs_advanced = self.all_tables.get('playoffs_advanced', pandas.DataFrame())
		self.playoffs_shooting = self.all_tables.get('playoffs_shooting', pandas.DataFrame())
		self.playoffs_advanced_pbp = self.all_tables.get('playoffs_advanced_pbp', pandas.DataFrame())
		self.sim_thru = self.all_tables.get('sim_thru', pandas.DataFrame())
		self.sim_career = self.all_tables.get('sim_career', pandas.DataFrame())
		self.college = self.all_tables.get('college', pandas.DataFrame())
		self.leaderboard = self.all_tables.get('leaderboard', pandas.DataFrame())
		self.salaries = self.all_tables.get('salaries', pandas.DataFrame())
		
	def add_player_id(self,df):
		if df.empty:
			return df
		else:
			df['player_id'] = self.player_id
			return df

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

	def remap(self,df):
		''' Convert Bref names to friendlier db names '''
		remap = {'Season': 'season'
						, 'Age' : 'age'
						, 'Tm' : 'team'
						, 'Lg' : 'league'
						, 'Pos' : 'position'
						, 'G' : 'games_played'
						, 'GS' : 'games_started'
						, 'MP' : 'minutes_played'
						, 'FG' : 'field_goals'
						, 'FGA' : 'field_goals_attempted'
						, 'FG%' : 'field_goal_percentage'
						, '3P' : 'three_point_fg_made'
						, '3PA' : 'three_point_fg_attempted'
						, '3P%' : 'three_point_percentage'
						, '2P' : 'two_point_fg_made'
						, '2PA' : 'two_point_fg_attempted'
						, '2P%' : 'two_point_fg_percentage'
						, 'eFG%' : 'effective_fg_percentage'
						, 'FT' : 'ft_made'
						, 'FTA' : 'ft_attempted'
						, 'FT%' : 'ft_percentage'
						, 'ORB' : 'offensive_rebounds'
						, 'DRB' : 'defensive_rebounds'
						, 'TRB' : 'total_rebounds'
						, 'AST' : 'assists'
						, 'STL' : 'steals'
						, 'BLK' : 'blocks'
						, 'TOV' : 'turnovers'
						, 'PF' : 'personal_fouls'
						, 'PTS' : 'points'}

		return df.rename(columns=remap)


	def create_composite_key(self,df):
		composite_columns_1 = ['player_id','season','team']
		composite_columns_2 = ['player_id','Season','Tm']

		if 'id' in df.columns:
			print('ID column already exists for table')

		elif sum([1 if x in df.columns else 0 for x in composite_columns_1]) == 3:
			df['id'] = df.apply(lambda x: '%s - %s - %s' % tuple([x[val] for val in composite_columns_1]), axis=1) 

		elif sum([1 if x in df.columns else 0 for x in composite_columns_2]) == 3:
			df['id'] = df.apply(lambda x: '%s - %s - %s' % tuple([x[val] for val in composite_columns_2]), axis=1)

		else:
			print('Unable to create composite key, columns not found')
		
		return df

	def convert_nullcolumns_from_number(self,df):
		return df.where(pandas.notnull,None)