""" обработчик текстовых сообщений """
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from handlers import (callback, guess_number, send_image_picture, user_coordinates,
                        check_user_picture, talk_to_me)

import settings

# сбор логгов в файл bot.log
logging.basicConfig(filename='bot.log',
   # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
   level=logging.INFO
   )

# PROXY = {
#    'proxy_url': settings.PROXY_URL,
#    'urllib3_proxy_kwargs': {
#       'username': settings.PROXY_USERNAME,
#       'password': settings.PROXY_PASSWORD
#       }
#    }

# подключение бота
def main():
   # данные бота
   mybot = Updater(settings.API_KEY, use_context=True) # request_kwargs=PROXY

   # обработчики
   dp = mybot.dispatcher
   dp.add_handler(CommandHandler('start', callback)) # вызов функции запуска /start
   dp.add_handler(CommandHandler('guess', guess_number)) #вызов функции игры /guess
   dp.add_handler(CommandHandler('image', send_image_picture))
   dp.add_handler(MessageHandler(Filters.regex('^(Пришли картинку)$'), send_image_picture))
   dp.add_handler(MessageHandler(Filters.location, user_coordinates))
   dp.add_handler(MessageHandler(Filters.photo, check_user_picture))
   dp.add_handler(MessageHandler(Filters.text, talk_to_me)) #

   logging.info('Login') # вывод логов
   mybot.start_polling() # стучится к серваку за обновлениями 
   mybot.idle() # ручное закрытие

# для импорта
if __name__ == '__main__':
   main()
