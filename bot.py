""" обработчик текстовых сообщений """
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

# сбор логгов в файл bot.log
logging.basicConfig(filename='bot.log', level=logging.INFO)

# proxy
PROXY = {'proxy_url': settings.PROXY_URL,
        'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD }}

# функция ответов
def callback(update, context):
   print('Вызван /start')
   update.message.reply_text('Привет пользователь') # ответ пользователю

def talk_to_me(update, context):
   text = update.message.text
   print(text)
   update.message.reply_text(text)

# подключение бота
def main():
   # данные бота
   mybot = Updater(settings.API_KEY, use_context=True)

   # обработчики
   dp = mybot.dispatcher
   dp.add_handler(CommandHandler('start', callback)) # start-comand
   dp.add_handler(MessageHandler(Filters.text, talk_to_me))

   logging.info('Логин стартовал')
   mybot.start_polling() # стучится к серваку за обновлениями 
   mybot.idle() # ручное закрытие
   
if __name__ == '__main__':
   main()
