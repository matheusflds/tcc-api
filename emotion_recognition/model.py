import pandas as pd
from random import randint

class LstmConvModel:
  @staticmethod
  def predict(documents):
    scores = [(randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100)) for _ in documents]
    return pd.DataFrame(scores, columns=['joy','fear','anger','sadness'])