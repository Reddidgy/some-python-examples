import json

who_is_it_dict = {                  # словарь для создания второго файла с норм фамилией (на всякий)
    'UL84R0TMX' : 'ugarov',
    'UDAQQGJMS' : 'player1',
    'UCCA04GPL' : 'player2',
    'UAN9Q00BF' : 'player3',
    'UHJ777DQF' : 'player4',
    'UCH5KKE67' : 'player5',
    'UFC8XCJSV' : 'player6',
    'UGKSUVANM' : 'player7',
    'UK3T1E44B' : 'player8',
    'UM3U0T7PH' : 'player9',
    'U7568MABD' : 'player10',
    'UJGT1V9EW' : 'player11',
    'UCVUT24TT' : 'player12',
    'UCBLN44N6' : 'player13',
}

players_filename = 'players.json'
user = 'UK3T1E44B' # текущий пользователь в формате слака

# выгрузка всех персонажей из файла players.json
with open(players_filename, 'r', encoding='utf-8') as infile:
    l_players = json.load(infile)

for player in l_players:
    dict = {                # словарь для создания стандартного игрока
        'name': player,
        'public_name': '<@' + player + '>',
        'level':1,
        'hp':100,
        'attack':24,
        'deffend':16,
        'exp':0,
        'max_exp':2,
        'wins':0,
        'loses':0,
    }

    filename = 'players\\' + player + '.json'     # имя основного файла со словарем
    whofilename = 'players\\' + player + '-' + who_is_it_dict[player] + '.txt' # имя второго файла

    with open(filename, 'w', encoding='utf-8') as inGameFile:
        json.dump(dict, inGameFile)

    with open(whofilename, 'w', encoding='utf-8') as inFile:
        json.dump(whofilename, inFile)































###
