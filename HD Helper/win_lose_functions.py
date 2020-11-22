    def Win(self, loser):
        """Функция победы над врагом 'loser'"""
        boost = PlayerCB[loser].level  # берем буст EХР из лвла

        while boost != 0:
            self.exp = self.exp + 1
            boost = boost - 1
            if self.exp == self.max_exp:
                self.LevelUp()

        self.wins = self.wins + 1               # завершаем всё добавлением вина
        print(str(self.name) + ' выиграл')
        self.UpdatePlayerToFile()               # апдейтим всё в файл

        # конец функции победы

    def Lose(self):
        """функция проигрыша персонажа"""

        self.loses = self.loses + 1               # завершаем всё добавлением вина
        print(str(self.name) + ' проиграл')
        self.UpdatePlayerToFile()
