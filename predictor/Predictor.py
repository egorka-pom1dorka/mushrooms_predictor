from tensorflow.keras.models import load_model
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
from predictor.DataHolder import DataHolder


class Predictor:
    _WIDTH = 300
    _HEIGHT = 300
    _VALID_PREDICTION_MIN_PERCENT = 65
    _INVALID_PREDICTION_PERCENT = 40

    def __init__(self, model_file_path, data_file_path):
        self.model = load_model(model_file_path)
        self.dataHolder = DataHolder(data_file_path)

    def predict(self, img_path):
        predicted_values = self._get_predicted_values(img_path)
        return self._get_predictions(predicted_values)

    def _get_predicted_values(self, img_path):
        img_tensor = self._load_image(img_path)
        prediction = self.model.predict(img_tensor)
        return prediction[0]

    def _load_image(self, img_path, show=False):
        img = image.load_img(img_path, target_size=(self._WIDTH, self._HEIGHT))
        img_tensor = image.img_to_array(img)
        img_tensor = np.expand_dims(img_tensor, axis=0)
        img_tensor /= 255.

        if show:
            plt.imshow(img_tensor[0])
            plt.axis('off')
            plt.show()

        return img_tensor

    def _get_predictions(self, predicted_values):
        max_v = max(predicted_values)
        percent = int(round(max_v * 100))

        if percent <= self._INVALID_PREDICTION_PERCENT:
            return []

        if percent >= self._VALID_PREDICTION_MIN_PERCENT:
            index = list(predicted_values).index(max_v)
            return [self._get_prediction(index, percent)]

        predictions = []

        for value in predicted_values:
            percent = int(round(value * 100))

            if percent > self._INVALID_PREDICTION_PERCENT:
                index = list(predicted_values).index(value)
                predictions.append(self._get_prediction(index, percent))

        return predictions

    def _get_prediction(self, mushroom_index, percent):
        mushroom_data = self.dataHolder.get_by_index(mushroom_index)

        return {
            'mushroom_data': mushroom_data,
            'predicted_value': percent
        }
