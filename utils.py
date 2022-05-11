## Import in the Clarifai gRPC based objects needed
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2
from emoji import emojize
from random import choice, randint
from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings

# emoji
def get_smile(user_data):
    # запоминание smile для пользователя
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data['emoji']

# чьё число больше
def play_raund_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Ваше число {user_number}, моё число {bot_number}, вы выиграли'
    elif user_number == bot_number:
        message = f'Ваше число {user_number}, моё число {bot_number}, ничья'
    else:
        message = f'Моё число {bot_number}, ваше число {user_number}, вы проиграли'
    return message

# клавиатура
def main_keyboard():
    return ReplyKeyboardMarkup(
        [['Пришли картинку', KeyboardButton('Мои координаты', request_location=True)]]
    )
############## clarifai распознование картинки
def has_object_on_image(file_name, object_name):
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    # кортеж
    metadata = (('authorization', f'Key {settings.CLARIFAI_API_KEY}'),)

    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)

    request = service_pb2.PostModelOutputsRequest(
        model_id = 'aaa03c23b3724a16a56b629203edc62c',
        inputs = [
            resources_pb2.Input(
                data=resources_pb2.Data(image=image)
            )
        ])

    response = app.PostModelOutputs(request, metadata=metadata)
    #print(response)
    return check_response_for_object(response, object_name)

def check_response_for_object(response, object_name):
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == object_name and concept.value >= 0.9:
                return True
    else:
        print(f'ошибка распознования картинки {response.outputs[0].status.details}')

    return False
#############
if __name__ == '__main__':
    print(has_object_on_image('images/cat.jpg', 'cat'))
    print(has_object_on_image('images/image.jpg', 'car'))
    print(has_object_on_image('images/image2.jpg', 'cat'))