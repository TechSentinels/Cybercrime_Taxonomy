import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import re
from nltk import WordNetLemmatizer

class NaiveBayesClassifier:
    def __init__(self):
        try:
            with open('artifacts\\label_encoder.pkl', 'rb') as f:
                self.loaded_encoder = pickle.load(f)
            with open('artifacts\\tfidf_vectorizer.pkl', 'rb') as f:
                self.loaded_vectorizer = pickle.load(f)
            with open('artifacts\\naive_bayes_model.pkl', 'rb') as f:
                self.loaded_model = pickle.load(f)
        except FileNotFoundError:
            print("Error: Files not found. Please check the file paths.")
            # Handle the error, e.g., exit the program or provide a default behavior

    def load_and_predict(self, input_text):
        try:
            input_data = self.preprocess_text(input_text)
            print(input_data)
            print(self.loaded_model)
            prediction = self.loaded_model.predict(input_data)
            predicted_label = self.loaded_encoder.inverse_transform(prediction)[0]
            return predicted_label
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "An error occurred during prediction."

    def preprocess_text(self, input_text):
        def preprocess_text(text):
            # Lower Casing
            if not isinstance(text, str):
                text = str(text)
            text = text.lower()
            text=re.sub("[^a-zA-Z]"," ",text)
            # Tokenization
            #tokens = word_tokenize(text)
            tokens = text.split()

            # Remove stop words and numbers
            tokens = [word for word in tokens if word not in stopwords_list]
            # Lemmatization
            lemmatizer = WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(word) for word in tokens]\

            return " ".join(tokens)
        input_text=preprocess_text(input_text)
        input_data = self.loaded_vectorizer.transform([input_text])
        return input_data