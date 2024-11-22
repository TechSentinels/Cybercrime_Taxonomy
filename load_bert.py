from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import pickle
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

class BertClassifier:
    def __init__(self, model_name="artifacts\distilbert-finetuned-imdb-multi-class"):
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased',do_lower_case=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        with open('artifacts\\label_encoder.pkl', 'rb') as f:
             self.Encoder= pickle.load(f)

       
    def preprocess(self, text):
        tokenized_input = self.tokenizer(text, truncation=True, padding="max_length", max_length=128, return_tensors='pt')
        #input_ids = tokenized_input['input_ids']
        #attention_mask = tokenized_input['attention_mask']
        #return tf.convert_to_tensor([input_ids]), tf.convert_to_tensor([attention_mask])
        return tokenized_input
    def predict(self, text):
        inputs = self.preprocess(text)
        with torch.no_grad():  # Disable gradient calculation during inference
            outputs = self.model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)
        predicted_labels = torch.argmax(probs, dim=1)
        return (self.Encoder.inverse_transform(predicted_labels))
    #def predict(self, text):
        #inputs = self.preprocess(text)
        #outputs = self.model(inputs)
        #logits = outputs.logits
       # predicted_class_id = tf.argmax(logits, axis=-1)
        #return predicted_class_id.numpy()[0]


class BertClassifierMultiLabel:
    def __init__(self, model_name="artifacts\distilbert-finetuned-multi-class"):
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased',do_lower_case=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        with open('artifacts\\label_encoder.pkl', 'rb') as f:
             self.Encoder= pickle.load(f)
        with open('artifacts\\MultiLabelBinarizer.pkl', 'rb') as f:
             self.multilabel= pickle.load(f)
       
    def preprocess(self, text):
        tokenized_input = self.tokenizer(text, truncation=True, padding="max_length", max_length=128, return_tensors='pt')
        #input_ids = tokenized_input['input_ids']
        #attention_mask = tokenized_input['attention_mask']
        #return tf.convert_to_tensor([input_ids]), tf.convert_to_tensor([attention_mask])
        return tokenized_input
    def predict(self, text):
        inputs = self.preprocess(text)
        with torch.no_grad():  # Disable gradient calculation during inference
            outputs = self.model(**inputs)
        #probs = torch.softmax(outputs.logits, dim=1)
        sigmoid = torch.nn.Sigmoid()
        probs = sigmoid(outputs.logits[0].cpu())
        preds = np.zeros(probs.shape)
        preds[np.where(probs>=0.3)] = 1
        return self.multilabel.inverse_transform(preds.reshape(1,-1))