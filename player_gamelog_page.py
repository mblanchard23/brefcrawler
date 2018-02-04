import requests, pandas
from bs4 import BeautifulSoup, Comment
from db_tables import Players, session


class player_season_gamelog:
    ''' Gamelog for player for season. If season is not specified, entire career
    gamelog is searched for. Requires player to exist as Player'''

    def __init__(self, player_id, season):
        self.player_id = player_id
        self.season = self.parse_season(season)
        self.get_gamelogs(player_id=self.player_id, season=self.season)

        self.season_gamelog = self.season_gamelog.pipe(self.filter_column_headers) \
            .pipe(self.rename_gamelog_headers) \
            .pipe(self.home_away) \
            .pipe(self.win_loss) \
            .pipe(self.create_primary_key)

        if not self.playoff_gamelog.empty:
            self.playoff_gamelog = self.playoff_gamelog.pipe(self.filter_column_headers) \
                .pipe(self.rename_gamelog_headers) \
                .pipe(self.home_away) \
                .pipe(self.win_loss) \
                .pipe(self.create_primary_key)

    def parse_season(self, season_value):
        assert type(season_value) in (int, str), 'Season format incorrect'

        if type(season_value) == int:
            return str(season_value)

        elif len(season_value) == 7 and '-' in season_value:
            return str(int(season_value[:4]) + 1)

        elif len(season_value) == 4:
            return season_value

        else:
            raise TypeError('Unknown season format')

    def get_gamelog_html(self, player_id, season):
        season = self.parse_season(season)  # Redundant
        url_format = 'https://www.basketball-reference.com/players/{first_letter}/{player_id}/gamelog/{season}'
        req = requests.get(url_format.format(first_letter=player_id[0]
                                             , player_id=player_id
                                             , season=season))
        return req.text

    def get_dataframe_dict_from_html(self, request_text):
        dataframe_dict = {}
        soup = BeautifulSoup(request_text, 'html.parser')
        tables = soup.find_all('table')

        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        table_soups = []
        for c in comments:
            commentsoup = BeautifulSoup(c, 'html.parser')
            table_soups += commentsoup.findAll('table')

        all_tables = tables + table_soups

        for table in all_tables:
            table_id = table.get('id')
            if table_id:
                df = pandas.read_html(str(table))[0]
                df['season'] = self.season
                dataframe_dict[table_id] = df

        self.season_gamelog = dataframe_dict.get('pgl_basic', pandas.DataFrame())
        self.playoff_gamelog = dataframe_dict.get('pgl_basic_playoffs', pandas.DataFrame)

        if not self.season_gamelog.empty:
            self.season_gamelog['game_type'] = 'season'

        if not self.playoff_gamelog.empty:
            self.playoff_gamelog['game_type'] = 'playoff'

        return None

    def add_season(self, df):
        df['season'] = self.season
        return

    def get_gamelogs(self, player_id, season):
        return self.get_dataframe_dict_from_html(self.get_gamelog_html(player_id, season))

    def filter_column_headers(self, df):
        if 'Rk' in df.columns:
            return df.drop(index=df[df.Rk.apply(lambda x: str(x) == 'Rk')].index)
        else:
            return df

    def rename_gamelog_headers(self, df):
        map = {'Rk': 'rank'
            , 'G': 'game_played'
            , 'Date': 'date'
            , 'Age': 'age'
            , 'Tm': 'team'
            , 'Unnamed: 5': 'home_away'
            , 'Opp': 'opponent'
            , 'Unnamed: 7': 'winlossmargin'
            , 'GS': 'games_started'
            , 'MP': 'minutes_played'
            , 'FG': 'field_goals'
            , 'FGA': 'field_goals_attempted'
            , 'FG%': 'field_goal_percentage'
            , '3P': 'three_point_fg_made'
            , '3PA': 'three_point_fg_attempted'
            , '3P%': 'three_point_percentage'
            , 'FT': 'ft_made'
            , 'FTA': 'ft_attempted'
            , 'FT%': 'ft_percentage'
            , 'ORB': 'offensive_rebounds'
            , 'DRB': 'defensive_rebounds'
            , 'TRB': 'total_rebounds'
            , 'AST': 'assists'
            , 'STL': 'steals'
            , 'BLK': 'blocks'
            , 'TOV': 'turnovers'
            , 'PF': 'personal_fouls'
            , 'PTS': 'points'
            , 'GmSc': 'game_score'
            , '+/-': 'plus_minus'}

        return df.rename(columns=map)

    def home_away(self, df):
        df['home_away'] = df.home_away.apply(lambda x: 'H' if pandas.isnull(x) else 'A')
        return df

    def win_loss(self, df):
        try:
            df['result'] = df.winlossmargin.apply(lambda x: x[0])
        except:
            df['result'] = None

        try:
            df['result_margin'] = df.winlossmargin.apply(lambda x: int(x.split('(')[1][:-1]))
        except:
            df['result_margin'] = None
        return df

    def create_primary_key(self, df):
        df['id'] = df.apply(lambda x: '%s - %s - %s' % (x['season'], x['game_type'], str(x['rank']).zfill(2)), axis=1)
        return df


class player_career_gamelog:
    def __init__(self, player_id):
        self.player_id = player_id
        self.player = session.query(Players).filter(Players.id == player_id).all()[0]
        self.career_seasons = range(self.player.year_from, self.player.year_to + 1)
        self.gamelog_list = []

        for season in self.career_seasons:
            psg = player_season_gamelog(player_id=self.player_id, season=season)
            if not psg.season_gamelog.empty:
                self.gamelog_list.append(psg.season_gamelog)

            if not psg.playoff_gamelog.empty:
                self.gamelog_list.append(psg.playoff_gamelog)

        self.career_gamelog = pandas.concat(self.gamelog_list)


def tommy_test():
    return get_dataframe_dict_from_html(request_text=get_gamelogs(player_id='heinsto01'
                                                                  , season=1962))


def kobe_test():
    return get_dataframe_dict_from_html(request_text=get_gamelogs(player_id='bryanko01'
                                                                  , season=2002))
