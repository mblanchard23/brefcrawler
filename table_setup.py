def table_queries():
	players = """create table players(player_id varchar(255),Name varchar(255),Played_From int,Played_To int,Pos varchar(255),Ht varchar(255),Wt int,Birth_Date varchar(255),College varchar(255))"""

	season_stats = """create table season_stats
					(player_id varchar(255)
					,Season varchar(255)
					,Age int
					,Tm varchar(255)
					,Lg varchar(255)
					,Pos varchar(255)
					,G int
					,GS int
					,MP int
					,FG int
					,FGA int
					,FG_Percentage float
					,Three_Pointers_Made int
					,Three_Point_Attemps int
					,ThreeP_Percentage float
					,Two_Points_Made int
					,Two_Point_Attempts int
					,Two_Point_Percentage float
					,eFG_Percentage float
					,FT int
					,FTA int
					,FT_Percentage float
					,ORB int
					,DRB int
					,TRB int
					,AST int
					,STL int
					,BLK int
					,TOV int
					,PF int
					,PTS int)"""
	return [players,season_stats]

def create_tables():
	import sqlite3
	lst = table_queries()
	conn = sqlite3.connect('db.sqlite')
	c = conn.cursor()
	for query in lst:
		try:
			c.execute(query)
			conn.commit()
		except:
			print('Error')

	conn.close()

