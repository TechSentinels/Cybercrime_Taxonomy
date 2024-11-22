import tensorflow as tf
import pickle
from tensorflow.keras.layers import Bidirectional,LSTM,Dense,Dropout,Embedding
from keras.initializers import GlorotUniform
from keras.regularizers import l2
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from tensorflow.keras.models import Sequential,load_model


# Reset the default graph
tf.compat.v1.reset_default_graph()
class LSTM_functions():

    def __init__(self):
        try:
            with open('artifacts\\label_encoder.pkl', 'rb') as f:
                self.loaded_encoder = pickle.load(f)
            with open('artifacts\\tokenizer.pkl', 'rb') as f:
                self.loaded_tokenizer = pickle.load(f)
        except FileNotFoundError:
            print("Error: Files not found. Please check the file paths.")
            # Handle the error, e.g., exit the program or provide a default behavior
        try:
            self.model = tf.keras.models.load_model("artifacts\\best_model.keras")
            #print(self.model.summary())
        except:
            print("Model not loaded properly")

    def load_and_predict(self, input_text):
        try:
            input_data = self.preprocess_text(input_text)
            prediction = self.model.predict(input_data)

            # Adjust post-processing based on your model's output format
            predicted_class = np.argmax(prediction)
            predicted_label = self.loaded_encoder.inverse_transform([predicted_class])[0]

            return predicted_label
        except AttributeError as e:
            print(f"AttributeError occurred: {e}")
            print("Please check if the model architecture and input data are compatible.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "An error occurred during prediction."

    def preprocess_text(self, input_text):
        input_sequence = self.loaded_tokenizer.texts_to_sequences([input_text])
        input_data = tf.keras.preprocessing.sequence.pad_sequences(input_sequence, maxlen=100)
        return np.array(input_data)