import os
from random import *

WORDS = {}
FILE_ISNOT_OKAY = True
FILE = 'file.txt' # Добавлена для удобного тестирования
INPUTFILE = True # Добавлена для удобного тестирования
WCOUNT = 0 # Переменная для счетчика слов и процентного отображения загрузки


#################
### FUNCTIONS ###
#################

# Функция из винды для очистки экрана
def cls():
    os.system('CLS')

# Для дебаг комментария
def debug(x=''):
    print('DEBUG ' + x)

def stopline():
    input("============STOPLINE============")

def dsline(y=''):
    debug(y)
    stopline()

########################
### END OF FUNCTIONS ###
########################

# До тех пор пока не выбран файл
while FILE_ISNOT_OKAY:
    try:
        if INPUTFILE:
            FILE = input("Введите название файла с расширением, соблюдая регистр. \nНапример file.txt : ")
        # Пробуем открыть файл
        f = open(FILE)
    # Ловля ошибки нот екзиста файла
    except FileNotFoundError:
        cls()
        print('Файл ' + FILE + ' не найден! Попробуйте еще раз!')
    else:
        # Фолсим переменную, чтобы идти дальше
        FILE_ISNOT_OKAY = False

# Читает содержимое файла, убирает переводы строк, убирает пробелы и помещает всё
# в переменную a в виде списка отдельных слов
a = f.read().rstrip().split()

# Применяем цикл для каждого слова в списке а
for word in a:
    WCOUNT = WCOUNT + 1
    PCOUNT = round((WCOUNT * 100) / len(a))
    word = word.lower()
    print(word)
    ### КОД СЧЕТЧИКА ###
    # 78449 = 100
    # WCOUNT = x %
    #
    #
    #
    ### КОНЕЦ КОДА СЧЕТЧИКА ###
    # Запускаем трай, чтобы избежать ошибок, на которые поф
    try:
        # Если слово начинается со скобки или кавычки - убираем лишний символ
        while word[0] == "(" or word[0] == '"' or word[0] =="'":
            word = word[1:]
        # Если слово заканчивается знаком препинания - убиваем его
        while word[-1] == "." or word[-1] == "," or word[-1] == '"' or word[-1] == ')' or word[-1] == ':' or word[0] =="'" or word[0] ==";" or word[0] =="!" or word[0] =="?" or word[0] =="-":
            word = word[:-2]
        if word == "":
            continue
        # Если длина слова больше одного символа - оно наше
        if len(word) > 1:
            # Если слова нет в словаре слов - помещаем со значением 1
            if word not in WORDS:
                #print(word)
                WORDS.update({word:1})
            # Если слово есть, то прибавляем к значению + 1, для подсчета
            else:
                WORD_COUNT = WORDS.get(word)
                # Функция добавления в словарь с добавлением 1
                #print(word)
                WORDS.update({word:WORD_COUNT+1})
    except:
        # Если ошибка - ничего не делаем и продолжаем
        pass

# Закрываем файл
f.close()

# Открываем файл для нашего словаря
o = open('out.txt', 'w')

# Для каждого слова в словаре WORDS
for i in WORDS:
    # В переменную recword добавляем само слово и счет этого слова в книге (Через таб для гугл таблицы)
    recword = str(i) + '	' + str(WORDS.get(i)) + '\n'
    # Записываем каждое слово в оутпут файл
    o.write(recword)
# Закрываем файл

o.close()
cls()
print("Анализ файла успешно завершен!")
print("Результаты анализа файла " + FILE + " находятся - в файле out.txt")
print("Можно поместить их в EXCEL или GOOGLE DOC таблицу для сортировки")
print("Нажмие Ентер для завершения программы...")
input()
