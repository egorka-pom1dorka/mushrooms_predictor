import telebot
import os
from output import Output
from predictor import Predictor

bot = telebot.TeleBot('%token%')
predictor = Predictor('./data/mushrooms.h5', './data/mushrooms.csv')
output = Output()

text_command = 'text'
audio_command = 'audio'
more_command = 'more'

available_response_types = {text_command: 'Текст', audio_command: 'Аудио'}
response_type = available_response_types['text']
last_prediction = None

keyboard_types = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_types.row(
    available_response_types[text_command], available_response_types[audio_command]
)


def get_change_type_message():
    type_keys = list(available_response_types.keys())
    return output.get_change_response_type_message(response_type, type_keys)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, output.get_greeting_message(), reply_markup=keyboard_types)


@bot.message_handler(commands=[text_command])
def text_command_message_handler(message):
    global response_type
    response_type = 'text'
    bot.send_message(message.chat.id, get_change_type_message())


@bot.message_handler(commands=[audio_command])
def audio_command_message_handler(message):
    global response_type
    response_type = 'audio'
    bot.send_message(message.chat.id, get_change_type_message())


@bot.message_handler(commands=[more_command])
def more_command_message_handler(message):
    if last_prediction is not None:
        bot.send_message(message.chat.id, last_prediction['mushroom_data']['description'])
    else:
        bot.send_message(message.chat.id, output.get_undefined_message())


@bot.message_handler(content_types=['text'])
def text_message_handler(message):
    if message.text == output.get_easter_egg_message_value():
        return bot.send_message(message.chat.id, output.get_easter_egg_message_response())

    type_keys = list(available_response_types.keys())
    type_values = list(available_response_types.values())

    if message.text in type_values:
        global response_type
        response_type = type_keys[type_values.index(message.text)]
        bot.send_message(message.chat.id, get_change_type_message())
    else:
        bot.send_message(message.chat.id, output.get_undefined_message())


@bot.message_handler(content_types=['photo'])
def send_prediction(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)

    base_path = './user_data/'
    image_path = base_path + file_id + ".jpg"
    downloaded_file = bot.download_file(file_info.file_path)

    with open(image_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    predictions = predictor.predict(image_path)
    prediction = output.get_prediction_message(predictions)
    global last_prediction

    if len(predictions) == 1:
        last_prediction = predictions[0]
        output_message = prediction + ' ' + output.get_more_message('/more')
    else:
        last_prediction = None
        output_message = prediction

    if response_type == 'audio':
        audio_path = base_path + file_id + ".mp3"
        output.generate_audio(output_message, audio_path)
        bot.send_audio(message.chat.id, open(audio_path, "rb"))
        os.remove(audio_path)
    else:
        bot.send_message(message.chat.id, output_message)

    os.remove(image_path)


bot.polling()
