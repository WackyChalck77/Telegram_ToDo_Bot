import telebot
import random
token = "6834706220:AAHXrVeWDsR114e95vetj9XROEhgGTT_pI8"
bot = telebot.TeleBot(token)

HELP = """
Доступны следущие команды:
/help - вызов справки
/add - добавить задачу
/list - вывести список задач
/random - случайная задача
/exit - выход из программы
/print_all - печать всех задач
"""
tasks={}
RANDOM_TASKS = [
    "Закупить товар", "сходить на футбол", "почитать книгу", "посмотреть фильм"
]

def add_todo(date, category, task):
  #Проверка даты в словаре
  if date in tasks:
    tasks[date].append({'task':task,'category':category} )
  else:
    tasks[date] = []
    tasks[date].append({'task':task, 'category':category})
  print(tasks[date])

@bot.message_handler(commands=["add"])
def add(message):
    input_command=message.text.split(maxsplit=3)
    date=input_command[1].lower()
    category=input_command[2]
    task=input_command[3]
    if len(task) <= 3:
        print("ошибка")
        bot.send_message(message.chat.id, "задача содержит слишком мало символов, повторите ввод")
    else:
        add_todo(date,category,task)
        bot.send_message(message.chat.id, "задача "+task+" добавлена на дату "+date+" с категорией @"+category)
#    bot.send_message(message.chat.id, "работает?")

@bot.message_handler(commands=["random"])
def random_add(message):
    date="сегодня"
    task=random.choice(RANDOM_TASKS)
    category="random"
    add_todo(date,category,task)
    bot.send_message(message.chat.id, "задача ["+task+"] добавлена на дату "+date)

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=["list"])
def list_(message):
    input_command=message.text.split(maxsplit=1)
    date=input_command[1].lower()
    if date in tasks:
        text_listed=date+"\n"
        inner_dict=tasks.get(date)
        for task in inner_dict:
            text_listed=text_listed + " [] - "+ task['task'] +" @"+ task['category'] + "\n"
            print(text_listed)
        bot.send_message(message.chat.id,text_listed)
    else:
        bot.send_message(message.chat.id,"на выбранную дату задачи отсутствуют")

@bot.message_handler(commands=["print_all"])
def print_all_(message):
    for date in tasks:
        text_listed=""
        inner_dict=tasks[date]
        for task in inner_dict:
            text_listed=text_listed + date + " [] - "+ task['task'] +" @"+ task['category'] + "\n"
            print(text_listed)
        bot.send_message(message.chat.id,text_listed)

bot.polling(none_stop=True)
