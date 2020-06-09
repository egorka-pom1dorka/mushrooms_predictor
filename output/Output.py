from gtts import gTTS
import base64


class Output:
    @staticmethod
    def get_greeting_message():
        return 'Привет, я бот, который угадывает виды грибов по фотографии. ' \
               'Пришли мне фотографию и я попробую угадать, что эа гриб на ней, но для начала ' \
               'выбери пункт в каком виде тебе лучше получать предсказания от меня '

    @staticmethod
    def get_change_response_type_message(current_type, available_types):
        return 'Ты изменил тип сообщений с предсказаниями на %s. ' \
               'Ты можешь поменять его в любое время, написав %s' \
               % (current_type, ' или '.join(list(map(lambda x: '/' + x, available_types))))

    @staticmethod
    def get_undefined_message():
        return 'Ничего не понимаю, думай прежде, чем что-то делать'

    def get_prediction_message(self, predictions):
        if len(predictions) == 0:
            return self._get_unrecognized_message()

        if len(predictions) == 1:
            return self._get_sure_message(predictions[0])

        return self._get_unsure_message(predictions)

    @staticmethod
    def _get_unrecognized_message():
        return 'Не могу распознать этот гриб, попробуй загрузить другую фотографию. ' \
               'Если результат повторяется - значит я еще не научилась расспознать грибы даного типа'

    def _get_sure_message(self, prediction):
        value = prediction['predicted_value']
        mushroom = prediction['mushroom_data']
        return 'Я уверена на %s процентов, что это ' % value + self._get_message_about_mushroom(mushroom)

    def _get_unsure_message(self, predictions):
        message = 'Не уверена в ответе, думаю, что это что-то из этого: '

        for prediction in predictions:
            mushroom = prediction['mushroom_data']
            message += self._get_message_about_mushroom(mushroom)

        return message

    @staticmethod
    def _get_message_about_mushroom(mushroom):
        types = list(map(lambda x: x.lower(), mushroom['types']))

        return '%s или %s. Этот гриб относится к типам: %s. ' \
               % (mushroom['name_ru'], mushroom['name_lat'], ', '.join(types))

    @staticmethod
    def get_more_message(command):
        return 'Чтобы узнать больше напиши %s' % command

    @staticmethod
    def generate_audio(text, out_file):
        tts = gTTS(text, lang="ru")
        tts.save(out_file)

    def get_easter_egg_message_value(self):
        return self._decode('0LbQvtC/0LA=')

    def get_easter_egg_message_response(self):
        return self._decode('0YHRitC10LvQsCDRgtGA0YPRgdGL')

    @staticmethod
    def _decode(message):
        base64_bytes = message.encode('utf8')
        message_bytes = base64.b64decode(base64_bytes)
        return message_bytes.decode('utf8')
