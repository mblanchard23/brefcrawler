# basketball-reference-crawler
A few Python classes to scrape data from Basketball Reference
Requires BeautifulSoup & Python requests
### Methods & Classes
*player_page()* 
Class takes a Basketball Reference player ID from and returns an object with the tables from a player's page. The object has a player_data dictionary attribute which stores the tables on the player page using the following keys:
```python
player_data = {	"totals": ""
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
		,"salaries": ""}

```
*tablify(soup_table,delimiter,qualifier)*
Turns a soup HTML table into a delimited string. Defaults to comma delimited and no qualifier

### Examples
Get player salary table
``` python
# Get Jalen's salaries
jalen = player_page('roseja01')
jalen.player_data['salaries'] #Returns Jalen's salary by year

```

Get a comma delimited table  
``` python
jalen = player_page('roseja01')
print tablify(jalen.totals)
# 1994-95,22,DEN,NBA,SF,81,37,1798,227,500,.454,36,114,.316,191,386,.495,.490,173,234,.739,57,160,217,389,65,22,160,206,663
# 1995-96,23,DEN,NBA,SG,80,37,2134,290,604,.480,32,108,.296,258,496,.520,.507,191,277,.690,46,214,260,495,53,39,234,229,803
# 1996-97,24,IND,NBA,SF,66,6,1188,172,377,.456,21,72,.292,151,305,.495,.484,117,156,.750,27,94,121,155,57,18,107,136,482
# 1997-98,25,IND,NBA,SF,82,0,1706,290,607,.478,25,73,.342,265,534,.496,.498,166,228,.728,28,167,195,155,56,14,132,171,771
# 1998-99,26,IND,NBA,SF,49,1,1238,200,496,.403,17,65,.262,183,431,.425,.420,125,158,.791,34,120,154,93,50,15,72,128,542
# 1999-00,27,IND,NBA,SF,80,80,2978,563,1196,.471,77,196,.393,486,1000,.486,.503,254,307,.827,42,345,387,320,84,49,188,234,1457
# 2000-01,28,IND,NBA,SF,72,72,2943,567,1242,.457,59,174,.339,508,1068,.476,.480,285,344,.828,37,322,359,435,65,43,211,230,1478
# 2001-02,29,TOT,NBA,SF,83,83,3153,663,1458,.455,89,246,.362,574,1212,.474,.485,281,335,.839,43,330,373,355,78,45,201,251,1696
# 2001-02,29,IND,NBA,SF,53,53,1937,387,871,.444,52,146,.356,335,725,.462,.474,156,186,.839,29,220,249,197,45,29,105,148,982
# 2001-02,29,CHI,NBA,SF,30,30,1216,276,587,.470,37,100,.370,239,487,.491,.502,125,149,.839,14,110,124,158,33,16,96,103,714
# 2002-03,30,CHI,NBA,SF,82,82,3351,642,1583,.406,133,359,.370,509,1224,.416,.448,399,467,.854,68,283,351,395,72,23,285,271,1816
# 2003-04,31,TOT,NBA,PG-SF,66,64,2497,383,952,.402,69,202,.342,314,750,.419,.439,187,231,.810,34,232,266,329,51,22,208,184,1022
# 2003-04,31,CHI,NBA,SF,16,14,529,75,200,.375,23,54,.426,52,146,.356,.433,39,51,.765,7,57,64,56,12,4,37,45,212
# 2003-04,31,TOR,NBA,PG,50,50,1968,308,752,.410,46,148,.311,262,604,.434,.440,148,180,.822,27,175,202,273,39,18,171,139,810
# 2004-05,32,TOR,NBA,SF,81,65,2710,527,1159,.455,108,274,.394,419,885,.473,.501,333,390,.854,44,232,276,209,63,10,180,190,1495
# 2005-06,33,TOT,NBA,SF-SG,72,45,1983,290,685,.423,59,172,.343,231,513,.450,.466,248,318,.780,28,183,211,181,30,13,115,156,887
# 2005-06,33,TOR,NBA,SF,46,22,1236,180,446,.404,31,115,.270,149,331,.450,.438,166,217,.765,15,114,129,113,20,10,65,101,557
# 2005-06,33,NYK,NBA,SG,26,23,747,110,239,.460,28,57,.491,82,182,.451,.519,82,101,.812,13,69,82,68,10,3,50,55,330
# 2006-07,34,PHO,NBA,SF,29,0,246,38,86,.442,21,47,.447,17,39,.436,.564,11,12,.917,3,20,23,16,5,2,9,22,108


```
