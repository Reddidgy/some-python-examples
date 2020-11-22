def Win(self, enemy):
    """Функция победы над врагом 'enemy'"""
    boost = PlayerCB[enemy].level  # берем буст EХР из лвла

    enemyattack = PlayerCB[enemy].attack - self.deffend  # берем урон от врага из его атаки минус броня

    if enemyattack <= 0:        # если атака врага за минусом защиты меньше чем 0
        enemyattack = 2

    # танцы с бубном на HP поинты

    if self.hp < enemyattack or self.hp == enemyattack: # если атака врага больше чем хп - сделать 0 хп
        self.hp = 0
    else:
        self.hp = self.hp - enemyattack                 # если нет - то отнять

    while boost != 0:
        self.exp = self.exp + 1
        boost = boost - 1
        if self.exp == self.max_exp:
            self.LevelUp()

    self.wins = self.wins + 1               # завершаем всё добавлением вина
    print(str(self.name) + ' выиграл')
    self.UpdatePlayerToFile()               # апдейтим всё в файл

    # конец функции победы

def Lose(self, enemy):
    """функция проигрыша персонажа"""
    enemyattack = PlayerCB[enemy].attack - self.deffend  # берем урон от врага из его атаки минус броня

    if enemyattack <= 0:        # если атака врага за минусом защиты меньше чем 0
        enemyattack = 2

    if self.hp < enemyattack or self.hp == enemyattack: # если атака врага больше чем хп - сделать 0 хп
        self.hp = 0
    else:
        self.hp = self.hp - enemyattack                 # если нет - то отнять

    self.loses = self.loses + 1               # завершаем всё добавлением вина
    print(str(self.name) + ' проиграл')
    self.UpdatePlayerToFile()
