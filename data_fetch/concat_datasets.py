import os
import pandas as pd

from pathlib import Path
from datetime import datetime

def concat_datasets(dataset_dir):
  DATASET_DIR = Path(dataset_dir).resolve()
  files = pd.Series([x for x in os.listdir(DATASET_DIR) if x.endswith('.csv')], 
                     name='files')
  if len(files) > 0:
    queries = files.str.extract(r'([#:a-zA-Z]\w+:?)', expand=False)
    for query in queries.unique():
      query_files = files[files.str.contains(query)]
      print('Found {} file(s) with query "'.format(len(query_files)) + query + '"')
      df = pd.DataFrame(columns=['id', 'date', 'user', 'text'])
      for filename in query_files:
        filepath = os.path.join(DATASET_DIR, filename)
        df = pd.concat([df, pd.read_csv(filepath, lineterminator='\n')])
        os.remove(filepath)

      now = datetime.now()
      timestamp = int(datetime.timestamp(now))
      name = query + '-' + str(timestamp) + '.csv'
      df.to_csv(os.path.join(DATASET_DIR, name), index=None)
  print('Done!')

if __name__ == '__main__':
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument('dataset_dir', type=str)

  args = parser.parse_args()
  concat_datasets(**vars(args))