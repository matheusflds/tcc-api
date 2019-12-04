import os
import pickle
import pandas as pd
from pathlib import Path
from tensorflow.keras.preprocessing.sequence import pad_sequences

from nlp.utils import preprocess
from .models.sentiment_analysis_model import sentiment_analysis_model
from .models.emotion_recognition_model import emotion_recognition_model

class SentimentAnalysis:
  @staticmethod
  def process(documents):
    # scores = [randint(0, 100) for _ in documents]
    # return pd.DataFrame(scores, columns=['polarity'])
    data_path = Path(os.path.abspath(__file__), '../model_data').resolve()

    tokenizer_path = data_path.joinpath('tokenizer.pickle')
    with tokenizer_path.open('rb') as file:
      tokenizer = pickle.load(file)

    cleaned_data = preprocess(documents, stemming=True)

    sequences = [text.split() for text in cleaned_data]
    list_tokenized = tokenizer.texts_to_sequences(sequences)

    input_dim = tokenizer.num_words
    embedding_dim = 100
    input_length = 30

    x_data = pad_sequences(list_tokenized, maxlen=input_length)

    sa_weights_path = data_path.joinpath('sentiment_analysis_weights.h5')
    model = sentiment_analysis_model(input_length,
                                     input_dim,
                                     embedding_layer=None,
                                     embedding_dim=embedding_dim)
    model.load_weights(sa_weights_path.as_posix())
    sa_results = model.predict_classes(x_data)

    encoder_path = data_path.joinpath('emotion_classes_encoder.pickle')
    with encoder_path.open('rb') as file:
      encoder = pickle.load(file)

    er_weights_path = data_path.joinpath('emotion_recognition_weights.h5')
    model = emotion_recognition_model(input_length,
                                      input_dim,
                                      num_classes=4,
                                      embedding_layer=None,
                                      embedding_dim=embedding_dim)
    model.load_weights(er_weights_path.as_posix())
    er_results = model.predict_classes(x_data)

    results = pd.get_dummies(er_results)
    results.columns = encoder.classes_
    results['polarity'] = sa_results

    return results
