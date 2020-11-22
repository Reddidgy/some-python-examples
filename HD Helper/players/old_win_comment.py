bot_message_text += '===============================\n\n\n\n'
bot_message_text += '*Level:* ' + str(cl_loser.level) + ' ' + '*EXP:* [ ' + str(cl_loser.exp) + ' / ' + str(cl_loser.max_exp) + ' ]' + '\n'
bot_message_text += ':hearts:: ' + str(was_loser_hp) + ' _- ' + str(winnnerattack) + '_' + '\n'

bot_message_text += ':crossed_swords:: ' + str(cl_winner.attack) + ' '
bot_message_text += ':shield:: ' + str(cl_winner.deffend) + (tab*8) + ' '
bot_message_text += ':crossed_swords:: ' + str(cl_loser.attack) + ' '
bot_message_text += ':shield:: ' + str(cl_loser.deffend) + '\n'
bot_message_text += "*Win:* " + str(cl_winner.wins) + ' ' + '*Lose:* ' + str(cl_winner.loses) + (tab*8)
bot_message_text += "*Win:* " + str(cl_loser.wins) + ' ' + '*Lose:* ' + str(cl_loser.loses)
