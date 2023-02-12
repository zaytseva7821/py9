import random
import telebot
import requests

bot = telebot.TeleBot("", parse_mode=None)

num = 0
count = 0
culc = False
game = False

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Погода', 'Калькулятор', 'Игра', '/stop')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, 'Привет!', reply_markup=keyboard1)

@bot.message_handler(commands=['stop'])
def stop(message):
    global culc
    culc = False
    global game
    game = False
    count = 0
    bot.reply_to(message, 'Хорошо')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Погода":
        data = requests.get("https://wttr.in/?format=3")
        bot.reply_to(message, data.text)
    elif message.text == "Калькулятор":
        global culc 
        culc = True
        bot.reply_to(message, "Теперь я могу решать выражения. Чтобы меня остановить, нажмите /stop")
    elif culc == True:
        bot.reply_to(message, eval(message.text))
    elif message.text == "Игра":
        global game 
        game = True
        global num
        bot.reply_to(message, "Я загадал число в диапазоне от 1 до 1000. Твоя задача угадать это число. Я буду лишь говорить, твое число больше или меньше загаданного. Чтобы выйти из игры нажми /stop")
        num = random.randint(1,1000)
        print(num)
    elif game == True:
        global count
        count +=1
        if int(message.text) > num:
            bot.reply_to(message, "Твое число больше загаданного")
        elif int(message.text) == num:
            bot.reply_to(message, f"Ты угадал! Тебе понадобилось {count} попыток")
            game = False
	    count = 0
        elif int(message.text) < num:
            bot.reply_to(message, "Твое число меньше загаданного")
    else:
        print(f'{message.from_user.first_name}: "{message.text}"')
        bot.reply_to(message, message.text)

bot.infinity_polling()

