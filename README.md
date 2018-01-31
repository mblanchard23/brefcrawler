# Scrapes Basketball Reference for Data
A few Python classes to scrape data from Basketball Reference
Requires BeautifulSoup, requests and pandas

### Classes
*player_page()* 
Takes Basketball Reference player ID from and returns an object with the Pandas tables from a player's page. The Totals table is only full reliable at the moment
```python
from player_page import player_page
jalen = player_page('roseja01')
jalen.totals[['season','age','games_played','points']]

0   1994-95  22.0            81     663
1   1995-96  23.0            80     803
2   1996-97  24.0            66     482
3   1997-98  25.0            82     771
4   1998-99  26.0            49     542
5   1999-00  27.0            80    1457
6   2000-01  28.0            72    1478
7   2001-02  29.0            83    1696
8   2001-02  29.0            53     982
9   2001-02  29.0            30     714
10  2002-03  30.0            82    1816
11  2003-04  31.0            66    1022
12  2003-04  31.0            16     212
13  2003-04  31.0            50     810
14  2004-05  32.0            81    1495
15  2005-06  33.0            72     887
16  2005-06  33.0            46     557
17  2005-06  33.0            26     330
18  2006-07  34.0            29     108
```

### Caching Data in SQL Stores
Supported using SQLAlchemy + whatever DBC. E.g. To load MySQL using pymysql on Python3, run
```bash
$ export BREF_DB_URI="mysql+pymysql://user:pass@{hostname}:{port number}/{db_name}"
```

#### Initiate Data Store
The database needs to be initiated before anything can be done
```python
from db_tables import Base, engine
Base.metadata.create_all(engine)
```

#### Inserting Players from BR's player lists
```python
from data_loads import insert_all_players
insert_all_players() # May take a while
```

#### Inserting Player Season Totals from a player page
```python
from data_loads import insert_player_season_totals
insert_player_season_totals('roseja01') # Adds Jalen's season stats to the DB
```
