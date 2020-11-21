# pip install gspread oauth2client
#row = sheet.row_values(3) # получить в переменную значения строк
#col = sheet.col_values(3) # получить в переменную значения столбцов
#cell = sheet.cell(1,2).value # 1 - номер строки 2 - номер столбца получить переменную ячейки
#insertRow = ['hello', 5, 'red', 'blue'] # Определить список для будущей строки
#sheet.insert_row(insertRow, 7) # добавляет строку сдвигая всё вниз
#sheet.update_cell(2,2, 'Changed!')

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
scope = [
    "https://spreadsheets.google.com/feeds",
    'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open('Python Google spreadsheet').sheet1 # открыть нужную таблицу
data = sheet.get_all_records() # получить все записи в переменную data

last_name_row = sheet.col_values(14)
first_name_row = sheet.col_values(13)
company_row = sheet.col_values(12)
team_row = sheet.col_values(8)
office_row = sheet.col_values(3)
level_row = sheet.col_values(2)

employee_search = input('Employe Last name:')
sheet_index = 0 # Переменная для счета индекса
office_index = 0 # Переменная для индекса офиса (из-за объединения столбцов)
team_index = 0 # Переменная для индекса офиса (из-за объединения столбцов)
level_index = 0 # Переменная для индекса этажа (из-за объединения столбцов)
found_employee = [] # Массив для найденных поиском сотрудников
temp_office_index = 0 # Временная переменная индекса для расчета офиса
temp_team_index = 0 # Временная переменная индекса для расчета команды
temp_level_index = 0 # Временная переменная индекса для расчета этажа
#print(office_row)
for i in last_name_row:
    if employee_search.lower() in i.lower():
        found_office_row = False # Переменная для окончания процесса поиска
        found_team_row = False # Переменная для окончания процесса поиска
        found_level_row = False # Переменная для окончания процесса поиска

        ## Логика поиска ячейки этажа ##
        temp_level_index = sheet_index
        if level_row[temp_level_index] == '':
            while found_level_row == False:
                if level_row[temp_level_index] != '':
                    found_level_row = True
                    level_index = temp_level_index
                else:
                    temp_level_index = temp_level_index - 1
            found_level_row = False
        else:
            found_level_row = True
            level_index = temp_level_index

        ## Логика поиска ячейки офиса ##
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

        ## Логика поиска ячейки команды ##
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

        new_employee = ('Сотрудник:' +
        str(first_name_row[sheet_index]) +
        ' ' +
        str(last_name_row[sheet_index]) +
        "\nCompany:" +
        str(company_row[sheet_index]) +
        "\nTeam:" +
        str(team_row[team_index]) +
        "\nOffice:" +
        str(office_row[office_index]) +
        " Этаж:" +
        str(level_row[level_index]))

        found_employee.append(new_employee)



        sheet_index = sheet_index + 1
    else:
        sheet_index = sheet_index + 1
bot_message = ''
found_employee_index = 0
last_employee_index = len(found_employee) - 1
for i in found_employee:
    bot_message = bot_message + '----------------\n' + i + '\n'
    if found_employee_index == last_employee_index:
        bot_message = bot_message + '----------------\n'
    found_employee_index = found_employee_index + 1

print(bot_message)







































#### EOF
