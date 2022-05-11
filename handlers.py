from glob import glob
import os
from random import choice

from utils import get_smile, has_object_on_image, play_raund_numbers, main_keyboard
from settings import USER_EMOJI
# запуск бота и приветствие со смайликом
def callback(update, context):
    print('Вызван /start')
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f'Привет пользователь {context.user_data["emoji"]}',
        reply_markup = main_keyboard()
    )

# спроси меня
def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text # ввод пользователя
    print(text)
    update.message.reply_text(f'{text} {context.user_data["emoji"]}',
        reply_markup = main_keyboard()
   )

# проверка ввода пользователя и приведение к числу
def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_raund_numbers(user_number)
        except (TypeError, ValueError):
            message = 'Введите целое число'
    else:
        message = 'Введите число'
    update.message.reply_text(message, reply_markup = main_keyboard())

# вывод картинок 
def send_image_picture(update, context):
    image_photo_list = glob('images/*')
    image_photo_filename = choice(image_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(image_photo_filename, 'rb'),
        reply_markup = main_keyboard()
    )

def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f'Ваши координаты {coords} {context.user_data["emoji"]}',
        reply_markup=main_keyboard()
    )
    print(coords)

def check_user_picture(update, context):
    update.message.reply_text('Обрабатываем фото')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads', f'{update.message.photo[-1].file_id}.png')
    photo_file.download(file_name)
    update.message.reply_text('Файл сохранен')
    if has_object_on_image(file_name, object_name='cat'):
        update.message.reply_text('Обнаружен котик, добавляю в библиотеку')
        os.makedirs('images', exist_ok=True)
        new_file_name = os.path.join('images', f'cat_{photo_file.file_id}.jpg')
        os.rename(file_name, new_file_name)
    else:
        os.remove(file_name)
        update.message.reply_text(f'Котика нету {USER_EMOJI[-1]})')