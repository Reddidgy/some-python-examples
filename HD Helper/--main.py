import os
import slack
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import json
from random import *

"""Конфиги для google sheets & drive"""
scope = [
    "https://spreadsheets.google.com/feeds",
    'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds) # авторизация по кредам в переменную
sheet = client.open('Python Google spreadsheet').sheet1 # открыть нужную таблицу
message_from_bot = False # переменная для определения чье сообщение прилетело бота или человека
#cap_data = sheet.get_all_records() # получить все записи в переменную data

# Переменная API токена из винды
client = slack.WebClient(token=os.environ["SLACK_API_TOKEN"])

#################
""" VARIABLES """
#################
LOG_FILE = 'log.txt'
players_filename = 'players.json'   # файл списка всех персонажей
player_filename = ''                # переменная для файла каждого персонажа
l_players = []                      # массив для игроков из файла players.json
PlayerCB = {}   # PlayerClassBank - здесь хранятся игроки с нужными функциями
# PlayerCB.update({user:Player(user)})   # добавление нового героя с именем user
# print(PlayerCB[user])   пример где находится сам герой и его вызов
# для того чтобы вывести его характеристики print(PlayerCB[user].level) - вывод "1" если уровень первый
dict_player = {} # переменная для функции UpdatePlayerToFile класса Player
# символ табуляции внутри скобок '	'

########################
""" END OF VARIABLES """
########################

##################################
""" GAME CLASSES AND FUNCTIONS """
##################################

class Player:
    """Класс игрок"""

    def __init__(self, name, public_name, level, hp, attack, deffend, exp, max_exp, wins, loses):
        """Функция инициализации игрока из файла каждого игрока"""
        self.name = name
        self.public_name = public_name
        self.level = level
        self.hp = hp
        self.attack = attack
        self.deffend = deffend
        self.exp = exp
        self.max_exp = max_exp
        self.wins = wins
        self.loses = loses

    def PlayerRegister(self, name, level = 1, hp = 100, attack = 7, deffend = 3, exp = 0, max_exp = 2, wins = 0, loses = 0):
        ############ НЕ ИСПОЛЬЗУЕТСЯ ##############
        """Функция регистрации игрока 1го лвла"""
        self.name = name
        self.public_name = public_name
        self.level = level
        self.hp = hp
        self.attack = attack
        self.deffend = deffend
        self.exp = exp
        self.max_exp = max_exp
        self.wins = wins

    def UpdatePlayerToFile(self):
        """Функция для записи всех изменений в JSON файл игрока"""

        dict_player = {                 # создает словарь из значений текущего класса
            'name' : self.name,
            'public_name' : self.public_name,
            'level' : self.level,
            'hp' : self.hp,
            'attack' : self.attack,
            'deffend' : self.deffend,
            'exp' : self.exp,
            'max_exp' : self.max_exp,
            'wins' : self.wins,
            'loses' : self.loses,
        }
        player_filename = 'players\\' + self.name + '.json'    # строим имя файла персонажа из имени класса
        with open(player_filename, 'w', encoding='utf-8') as infile:    # открываем файл игрока для записи
            json.dump(dict_player, infile)

    def Win(self, loser):
        """Функция победы над врагом 'loser'"""
        boost = PlayerCB[loser].level  # берем буст EХР из лвла
        gain_exp = boost

        while boost != 0:
            self.exp = self.exp + 1
            boost = boost - 1
            if self.exp == self.max_exp:
                self.LevelUp()

        self.wins = self.wins + 1               # завершаем всё добавлением вина
        print(str(self.name) + ' выиграл')
        self.UpdatePlayerToFile()               # апдейтим всё в файл

        return gain_exp

        # конец функции победы

    def Lose(self):
        """функция проигрыша персонажа"""

        self.loses = self.loses + 1               # завершаем всё добавлением вина
        print(str(self.name) + ' проиграл')
        self.UpdatePlayerToFile()


    def LevelUp(self, time=1):
        for i in range(0,time):
            self.level = self.level + 1
            self.attack = self.attack + 2
            self.deffend = self.deffend + 2
            self.exp = 0
            self.max_exp = self.level * 2
        self.UpdatePlayerToFile()

def Fight(attacker, cl_attacker, deffender, cl_deffender):
    """Функция драки атакера и дефендера"""

    """РАСЧЕТ АТАКИ """

    # Рандомно делаем от нижнего порога до верхнего атаки и отнимаем защиту
    min_attack = cl_attacker.attack // 10 # погрешность вниз
    max_attack = cl_attacker.attack // 10 # погрешность вверх
    attacker_attack = randint(cl_attacker.attack - min_attack, cl_attacker.attack + max_attack)
    # окончательная посчитанная атака атакующего
    attacker_attack = attacker_attack - cl_deffender.deffend

    min_attack = cl_deffender.attack // 10 # погрешность вниз
    max_attack = cl_deffender.attack // 10 # погрешность вверх
    deffender_attack = randint(cl_deffender.attack - min_attack, cl_deffender.attack + max_attack)
    # окончательная посчитанная атака защитника
    deffender_attack = deffender_attack - cl_attacker.deffend
    print(deffender_attack)
    if deffender_attack <= 0:        # если атака проигравшего за минусом защиты меньше чем 0
            deffender_attack = 2
    if attacker_attack <= 0:        # если атака проигравшего за минусом защиты меньше чем 0
            attacker_attack = 2

    """РАСЧЕТ РАНДОМА"""
    fight_random = randint(1,10)
    if fight_random >= 5:
        winner = attacker               # победа атакующего
        cl_winner = cl_attacker
        winnnerattack = attacker_attack
        loser = deffender
        cl_loser = cl_deffender
        loserattack = deffender_attack // 2
    else:
        winner = deffender               # победа защищающегося
        cl_winner = cl_deffender
        winnnerattack = attacker_attack
        loser = attacker
        cl_loser = cl_attacker
        loserattack = attacker_attack // 2

    """РАСЧЕТ ХП"""
    if cl_winner.hp <= loserattack: # если атака проигравшего больше чем хп - сделать 0 хп
        was_winner_hp = cl_winner.hp
        was_winner_lvl = cl_winner.level
        cl_winner.hp = 0
    else:
        was_winner_lvl = cl_winner.level
        was_winner_hp = cl_winner.hp
        cl_winner.hp = cl_winner.hp - loserattack                 # если нет - то отнять

    if cl_loser.hp <= winnnerattack:
        was_loser_hp = cl_loser.hp
        cl_loser.hp = 0
    else:
        was_loser_hp = cl_loser.hp
        cl_loser.hp = cl_loser.hp - winnnerattack                 # если нет - то отнять

    tab = '	'
    cl_loser.Lose()
    bot_message_text = ':crossed_swords:' + cl_deffender.public_name + '[*' + str(cl_deffender.level) + 'lvl*] was attacked by ' + cl_attacker.public_name + '[*' + str(cl_attacker.level) + 'lvl*]!' + ':crossed_swords:' +  '\n\n'
    win_exp = str(cl_winner.Win(loser))
    bot_message_text += '*Fight:*\n'
    bot_message_text += cl_loser.public_name + ' received *' + str(winnnerattack) + ' damage* and was defeated.\n'
    bot_message_text += cl_winner.public_name + ' received *' + str(loserattack) + ' damage* but wins the batle and obtains *' + str(win_exp) + ' EXP*.' + '\n\n'
    bot_message_text += '*Stats:*\n'

    bot_message_text += str(cl_winner.public_name) + ' : ' + '*Level:* ' + str(cl_winner.level) + '	' + '*EXP:* [ ' + str(cl_winner.exp) + ' / ' + str(cl_winner.max_exp) + ' ]	'
    bot_message_text += ':hearts:: ' + str(was_winner_hp) + ' _- ' + str(loserattack) + '_	'
    bot_message_text += "*Win:* " + str(cl_winner.wins) + ' ' + '*Lose:* ' + str(cl_winner.loses)  + '\n\n'

    bot_message_text += str(cl_loser.public_name) + ' : ' + '*Level:* ' + str(cl_loser.level) + '	' + '*EXP:* [ ' + str(cl_loser.exp) + ' / ' + str(cl_loser.max_exp) + ' ]	'
    bot_message_text += ':hearts:: ' + str(was_loser_hp) + ' _- ' + str(winnnerattack) + '_	'
    bot_message_text += "*Win:* " + str(cl_loser.wins) + ' ' + '*Lose:* ' + str(cl_loser.loses)  + '\n'
    if was_winner_lvl < cl_winner.level:
        bot_message_text += '\n\n' + cl_winner.public_name + ' *Congratulations!* You have reached *Level ' + str(cl_winner.level) + '*!\n'
    else:
        pass




    return bot_message_text
    pass

def TestUpload(client, channel,text):
    client.chat_postMessage(
    channel=channel,
    blocks=
    [
		{
			"type": "image",
			"title": {
				"type": "plain_text",
				"text": "image1",
				"emoji": True
			},
			"image_url": "https://media.giphy.com/media/uudzUtVcsLAoo/giphy.gif",
			"alt_text": "image1"
		}
	]
)

def GameInit():
    # выгрузка всех персонажей из файла players.json
    with open(players_filename, 'r', encoding='utf-8') as infile:
        l_players = json.load(infile)

    # выгрузка данных каждого персонажа в класс из массива l_players
    # для каждого имени в массиве l_players выгруженном из файла players.json
    for i in l_players:
        player_filename = 'players\\' + i + '.json'    # строим имя каждого файла
        with open(str(player_filename), 'r') as infile:    # открываем каждый файл для чтения
            tempPlayer = json.load(infile)                              # выгружаем словарь из каждого файла в времянку
            PlayerCB.update({i:Player(tempPlayer['name'],tempPlayer['public_name'],tempPlayer['level'],tempPlayer['hp'],
                tempPlayer['attack'],
                tempPlayer['deffend'],
                tempPlayer['exp'],
                tempPlayer['max_exp'],
                tempPlayer['wins'],
                tempPlayer['loses'],
                )})
        # добавляем КЛАСС в словарь всех игроков {PlayerCB}

    return l_players
        # теперь есть класс для каждого игрока с выгруженными данными из файлов

def PlayerStat(player_name):
    """Функция для вывода статы. Возвращает готовое сообщение для бота"""

    # name = str(name)
    # stat_user = PlayerCB[name]
    temp_line = '----------------------------------------\n'
    temp_public_name = '*Player:* ' + str(PlayerCB[player_name].public_name) + '\n'
    temp_level = '*Level:* ' + str(PlayerCB[player_name].level) + '    '
    temp_exp = '*EXP:* [ ' + str(PlayerCB[player_name].exp) + ' / ' + str(PlayerCB[player_name].max_exp) + ' ]' + '\n'
    temp_hp = ':hearts:: ' + str(PlayerCB[player_name].hp) + ' / ' + '100' + '\n'
    temp_attack = ':crossed_swords:: ' + str(PlayerCB[player_name].attack) + '    '
    temp_deffend = ':shield:: ' + str(PlayerCB[player_name].deffend) + '\n'
    temp_win_loose = "*Win:* " + str(PlayerCB[player_name].wins) + '    ' + '*Lose:* ' + str(PlayerCB[player_name].loses) + '\n'

    bot_message_text = temp_public_name + temp_line + temp_level + temp_exp + temp_hp + temp_attack + temp_deffend + temp_win_loose + temp_line
    return bot_message_text

def GameHelp():
    bot_message_text = "Game commands:\n`game stat`\n`game attack`"
    return bot_message_text

#########################################
""" END OF GAME CLASSES AND FUNCTIONS """
#########################################

def LogMessages(payload, user, text):  # функция логирования принимает текст для принта и пэйлоад для логгинга
    try:
        with open(LOG_FILE, 'a',encoding='utf-8') as in_log_file:
            log_var_to_write = ''
            temp_log = str(payload).split(',')
            for i in temp_log:
                log_var_to_write = log_var_to_write + str(i) + '\n'
            log_var_to_write = log_var_to_write + '===========================================\n'
            log_var_to_print = str(user) + ': ' + str(text)
            print(log_var_to_print)
            in_log_file.write(log_var_to_write)
        return log_var_to_write
    except Exception as e:
        print(e)


def BotMessage(web_client, channel, text):
    text = str(text)
    web_client.chat_postMessage(
        channel=channel,
        text=text
    )
def debug():
    print('!!!!!!!!!!!! DEBUG !!!!!!!!!!!!')
def EmployeeSearch(employee_search):
    ### Переменные из открытой таблицы и для поиска в EmployeeSearch()
    last_name_row = sheet.col_values(14)
    first_name_row = sheet.col_values(13)
    company_row = sheet.col_values(12)
    team_row = sheet.col_values(8)
    office_row = sheet.col_values(3)
    level_row = sheet.col_values(2)

    sheet_index = -1 # Переменная для счета индекса
    office_index = 0 # Переменная для индекса офиса (из-за объединения столбцов)
    team_index = 0 # Переменная для индекса офиса (из-за объединения столбцов)
    level_index = 0 # Переменная для индекса этажа (из-за объединения столбцов)
    found_employee = [] # Массив для найденных поиском сотрудников
    temp_office_index = 0 # Временная переменная индекса для расчета офиса
    temp_team_index = 0 # Временная переменная индекса для расчета команды
    temp_level_index = 0 # Временная переменная индекса для расчета этажа

    # Начало поиска по таблице
    for i in last_name_row:
        if sheet_index == len(office_row) - 1:
            pass
        else:
            sheet_index = sheet_index + 1
        #print('sheet index is ' + str(sheet_index))
        if employee_search.lower() in i.lower():
            found_office_row = False # Переменная для окончания процесса поиска
            found_team_row = False # Переменная для окончания процесса поиска
            found_level_row = False # Переменная для окончания процесса поиска

            ## Логика поиска ячейки этажа ##
            temp_level_index = sheet_index          # Создание временной переменной индекса этажа
            if level_row[temp_level_index] == '':   # если ячейка этажа пустая, запускается цикл перемещения по ячейке вверх
                while found_level_row == False:             # т.к. значение в объединенных ячейках находятся наверху
                    if level_row[temp_level_index] != '':   # __если ячейка не пустая, то активируем переменную found_level_row
                        found_level_row = True              # и назначем верный индекс этажа
                        level_index = temp_level_index
                    else:
                        temp_level_index = temp_level_index - 1     # __елсе ячейка пустая перемещаемся в минус
                found_level_row = False                              #  по индексу и вверх по таблице
            else:
                found_level_row = True                              # _елсе сразу на нужной ячейке - временный индекс
                level_index = temp_level_index                      # становится верным для этажа

            ## Логика поиска ячейки офиса ##                        # идентично логике этажей
            temp_office_index = sheet_index
            if office_row[temp_office_index] == '':
                while found_office_row == False:
                    if office_row[temp_office_index] != '':
                        found_office_row = True
                        office_index = temp_office_index
                    else:
                        temp_office_index = temp_office_index - 1
                found_office_row = False
            else:
                found_office_row = True
                office_index = temp_office_index

            ## Логика поиска ячейки команды ##                      # идентично логике этажей и офиса
            temp_team_index = sheet_index
            if team_row[temp_team_index] == '':
                while found_team_row == False:
                    if team_row[temp_team_index] != '':
                        found_team_row = True
                        team_index = temp_team_index
                    else:
                        temp_team_index = temp_team_index - 1
                found_team_row = False
            else:
                found_team_row = True
                team_index = temp_team_index
            new_employee = ('Employee:' +       # начало построения переменной для найденного сотрудника
            str(first_name_row[sheet_index]) +  # в переменную new_employee
            ' ' +
            str(last_name_row[sheet_index]) +
            "\nCompany:" +
            str(company_row[sheet_index]) +
            "\nTeam:" +
            str(team_row[team_index]) +
            "\nOffice:" +
            str(office_row[office_index]) +
            " Floor:" +
            str(level_row[level_index]))

            found_employee.append(new_employee) # найденного сотрудника добавляем в массив found_employee[]
        else:
            pass
    if found_employee == []:                    # если массив остался пустым ретурнаем НоФоунд месседж
        bot_message_text = 'I can not find "' + employee_search + '" in the capacity! Sorry dude!'
        return bot_message_text
    else:                                       # елсе массив не пустой
        bot_message_text = ''
        found_employee_index = 0                # переменная для подсчета индекса в массиве found_employee[]
        last_employee_index = len(found_employee) - 1
        for i in found_employee:
            bot_message_text = bot_message_text + '------------------------------------------------\n' + i + '\n'
            if found_employee_index == last_employee_index:
                bot_message_text = bot_message_text + '------------------------------------------------\n'
            found_employee_index = found_employee_index + 1
        return bot_message_text                 # возвращаем наполненный сотрудниками месседж для бота

####################################
""" END OF CLASSES AND FUNCTIONS """
####################################


######################
""" ТЕЛО ПРОГРАММЫ """
######################
l_players = GameInit()
print('Slack bot is ready to work!')
                                        # тестирую трай
@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    command_message = False         # переменная для проверки команда или дичь
    bot_message_text = ''           # Переменная для будущего текста бота и функции BotMessage
    message_from_bot = False
    data = payload['data']          # вся дата из полученного месседжа
    web_client = payload['web_client']  #
    rtm_client = payload['rtm_client']
    received_message = data.get('text', [])     # Текст сообщения в переменной received_message
    # проверяем 2 этих параметра в шапку channel_id & thread_ts
    channel_id = data['channel']        # если первый кусок == loc и частей больше одной, но меньше 5
    thread_ts = data['ts']


    if 'subtype' in data:                       # Проверка subtype для определения чье сообщение бот/человек
        if data['subtype'] == 'bot_message':
            message_from_bot = True
    message_from_bot = False
    if 'user' in data:
        user = data['user']
        message_from_bot = False
        LastLog = LogMessages(payload, user, received_message)     # Если от человека - логировать
    else:
        message_from_bot = True
        user = 'NoUser'

    ############################################
    """БОЛЬШЕ ОДНОГО СЛОВА ФУНКЦИИ ИЛИ ХЕЛП"""
    ############################################
    if ' ' in received_message:       # если есть пробел, разбить received_message
        message_parts = received_message.split(' ')                 # и поместить в виде списка в message_parts

        if message_parts[0].lower() == 'cmes':
            """функция отправки сообщения в канал с ботом. Use: `cmes text`"""
            command_message = True
            channel_id = 'CNXHFGMEW'
            thread_ts = data['ts']
            bot_message_text = received_message[5:]
            web_client.chat_postMessage(
                channel=channel_id,
                text=bot_message_text,
            )

        if message_parts[0].lower() == 'dmes':
            """ Функция отправки в личку человеку """
            command_message = True
            channel_id = str(message_parts[1][2:-1])
            thread_ts = data['ts']
            word_counter = -1
            if message_parts[1][:2] == '<@':
                for word in message_parts:
                    word_counter = word_counter + 1
                    if word_counter == 0 or word_counter == 1:
                        pass
                    elif word_counter == 2:
                        bot_message_text = word
                    else:
                        bot_message_text = bot_message_text + ' ' + word
                web_client.chat_postMessage(
                    channel=channel_id,
                    text=bot_message_text,
                )
                print('Message sent to ' + str(message_parts[1]))
            else:
                print('Wrong using of dmes')

        ####################
        """ FUNCTION LOC """
        ####################

        if message_parts[0].lower() == 'loc':
            """Проверка на функцию loc"""
            command_message = True

            try:
                """Проверка для функции loc (Искать по фамилии или по номеру офиса)"""
                second_word = int(message_parts[1])
            except:
                VAR_LOC_OFFICE = False
            else:
                VAR_LOC_OFFICE = True

            if VAR_LOC_OFFICE == True:
                '''ПОИСК ПО ОФИСУ'''
                if second_word >= 200 and second_word < 1000:
                    print('ну че сучка. Погнали искать по номеру офиса')
                else:
                    print('такого офиса нет браток!')

            else:
                '''ПОИСК ПО ФАМИЛИИ'''
                if len(message_parts[1]) > 2:       # если второй кусок (фамилия) больше двух символов
                    employee_search = message_parts[1]  # помещаем фамилию в переменную поиска employee_search
                    bot_message_text = EmployeeSearch(employee_search)  # текст для бота = выполнение функции поиска по фамилии выше
                    BotMessage(web_client, channel_id, bot_message_text)    # функция отправки ботосообщения
                else:                                               # если символов меньше двух
                    bot_message_text = 'Please use more than 2 symbols in employee last name.' # отправляем мессагу "сделай больше двух символов"
                    BotMessage(web_client, channel_id, bot_message_text)

        #########################
        """ END OF CHECKS LOC """
        #########################

        ######################
        """ GAME FUNCTIONS """
        ######################

        if message_parts[0].lower() == 'game':
            command_message = True
            wrong_game_channel = False
            """Проверка на тег game"""

            if user not in l_players:       # проверка на нахождение пользователя в игре
                    if user == 'NoUser':
                        pass
                    else:
                        bot_message_text = '<@' + user + ">, you dont play this game! Try `reg` command"   # елсе нет в списке
                        BotMessage(web_client, channel_id, bot_message_text)
            else:
                if message_parts[1].lower() == 'attack':
                    """Функция атаки игрока"""

                    if channel_id != 'CNXHFGMEW':
                        if user == 'UL84R0TMX' or user == 'UCVUT24TT' or user == 'UCBLN44N6':
                            wrong_game_channel = False
                        else:
                            wrong_game_channel = True

                    if len(message_parts) == 2:             # в команде атак 2 слова
                        bot_message_text = "For attack use `game attack @anybody`"   # елсе нет в списке
                        BotMessage(web_client, channel_id, bot_message_text)

                    elif len(message_parts) == 3:           # в команде атак 3 слова

                            if message_parts[2][:2] == '<@': # проверяем, что в третьем слове пользователь
                                player_name = str(message_parts[2][2:-1])

                                if player_name in l_players:    # если игрок в [l_players]


                                    attacker = user
                                    deffender = player_name
                                    cl_attacker = PlayerCB[attacker]
                                    cl_deffender = PlayerCB[deffender]
                                    print(user + ' пробует атаковать ' + player_name)

                                    if wrong_game_channel:          # если верный канал
                                        bot_message_text = "You have to use *#hd_bot_test* channel for this command!"   # елсе нет в списке
                                        BotMessage(web_client, channel_id, bot_message_text)
                                    else:

                                        if cl_attacker.hp == 0 or cl_deffender.hp == 0:
                                            '''Проверка хп противников'''

                                            if cl_attacker.hp == 0:
                                                bot_message_text = cl_attacker.public_name + " you have *0 hp* and you can't attack right now! Cya tomorrow!"
                                                BotMessage(web_client, channel_id, bot_message_text)

                                            if cl_deffender.hp == 0:
                                                bot_message_text = cl_deffender.public_name + " have *0 hp* and can't be attacked. Try tomorrow!"
                                                BotMessage(web_client, channel_id, bot_message_text)
                                        else:
                                            print('У противников достаточно хп. Можно начинать расчеты победы или поражения')
                                            bot_message_text = Fight(attacker, cl_attacker, deffender, cl_deffender)
                                            BotMessage(web_client, channel_id, bot_message_text)

                                else:
                                    bot_message_text = '<@' + player_name + "> dont play this game! "   # елсе не пользователь
                                    BotMessage(web_client, channel_id, bot_message_text)
                                    pass
                            else:
                                bot_message_text = "For attack use `game attack @anybody`"   # елсе нет в списке [l_players]
                                BotMessage(web_client, channel_id, bot_message_text)
                                pass
                    else:
                        bot_message_text = GameHelp()   # елсе нет в списке
                        BotMessage(web_client, channel_id, bot_message_text)

                elif message_parts[1] == 'stat':
                    """Функция статистики для игроков"""

                    if len(message_parts) == 2:
                        """Статистика игрока, с которого написано"""
                        bot_message_text = PlayerStat(user)
                        BotMessage(web_client, channel_id, bot_message_text)

                    if len(message_parts) == 3:
                        """СТАТА ДРУГОГО ИГРОКА"""

                        if message_parts[2][:2] == '<@':        # если третье слово - имя игрока
                            player_name = str(message_parts[2][2:-1])
                            if player_name in l_players:        # если имя игрока в [l_players]
                                #print(PlayerCB[player_name])
                                bot_message_text = PlayerStat(player_name)  # формируем сообщение со статой для выбранного пользователя
                                BotMessage(web_client, channel_id, bot_message_text)
                            else:
                                bot_message_text = '<@' + player_name + "> dont play this game! "   # елсе нет в списке
                                BotMessage(web_client, channel_id, bot_message_text)
                        else:                                                                       # елсе не понял третье слово
                            bot_message_text = "You can't use this command like this.\nPlease try `game stat @anybody`"
                            BotMessage(web_client, channel_id, bot_message_text)

                # если ничего во втором слове не похоже на годноту.

                else:
                    bot_message_text = GameHelp() # отправляем мессагу "сделай больше двух символов"
                    BotMessage(web_client, channel_id, bot_message_text)

        #############################
        """ END OF GAME FUNCTIONS """
        #############################

        if message_parts[0] == "#":     # комменты, чтобы бот не флудил
            command_message = True
            pass

    else:
        #########################
        """ ONE WORD COMMANDS """
        #########################

        if received_message == 'test':
            command_message = True
            bot_message_text = 'ti test'
            TestUpload(web_client, channel_id,bot_message_text)


        # Хелпа для лок функции
        if received_message == 'loc':
            command_message = True
            bot_message_text = '*loc-command* can help to find first/company/team names, office number and floor.\nFor using you should type "loc - ru_last_name".\nAlso you can use just part of last name\n\n*For example:*`loc Коровин` or `loc одег`'
            BotMessage(web_client, channel_id, bot_message_text)

        # Хелпа для game функции
        if received_message == 'game':
            command_message = True
            bot_message_text = GameHelp()
            BotMessage(web_client, channel_id, bot_message_text)
        ### ЛАСТ ЛОГ ОТПРАВКА ###
        if received_message == 'admin_last_log':
            command_message = True
            bot_message_text = LastLog
            BotMessage(web_client, channel_id, bot_message_text)
        # Хелп мессага
        if received_message == 'help':
            command_message = True
            bot_message_text = "I don't know what is help. But you can try to use `loc`,`game` commands."
            BotMessage(web_client, channel_id, bot_message_text)

    #######################################################################
    # если ничего не подошло - отправляем, что ничего не поняли
    if command_message == False and message_from_bot == False:
        print('No command message')

        '''bot_message_text = "I can't understand your language. Take it easy and type `help` dude."
        BotMessage(web_client, channel_id, bot_message_text)'''

slack_token = os.environ["SLACK_API_TOKEN"]     # выдираем переменную SLACK_API_TOKEN из винды
rtm_client = slack.RTMClient(token=slack_token) # назначаем клиент в переменную rtm_client
rtm_client.start()                              # запускаем клиент

############################
""" КОНЕЦ ТЕЛО ПРОГРАММЫ """
############################


















### EOF ###

















'''  <<<< payload >>>>
            #text=f"Hi <@{user}>!",
{
    'rtm_client': <slack.rtm.client.RTMClient object at 0x03054D30>,
    'web_client': <slack.web.client.WebClient object at 0x03F8F230>,
    'data': {
        'client_msg_id': '5b90c45b-1d23-43e1-84ae-169fe0f7f0a3',
        'suppress_notification': False,
        'text': 'HUILO',
        'user': 'UL84R0TMX',
        'team': 'T0259C89T',
        'user_team': 'T0259C89T',
        'source_team': 'T0259C89T',
        'channel': 'DNUU6F1L3',
        'event_ts': '1570579648.004200',
        'ts': '1570579648.004200'
    }    xoxb-2179416333-776958321795-cWcDATKtmKC6NLDs0Hv5OMlA
}
'''
