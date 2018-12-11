import datetime
import os

import pandas as pd
from google.cloud import storage
import xgboost as xgb

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./yangjae-8608241ce851.json"
# os.environ['PROJECT_ID'] = "yangjae-224512"
# os.environ['BUCKET_ID'] = "yangjae_storage"
# os.environ['REGION'] = "asia-east1"

# os.environ['PROJECT_ID'] = ""

# %env PROJECT_ID <YOUR_PROJECT_ID>
# %env BUCKET_ID <YOUR_BUCKET_ID>
# %env REGION <REGION>
# %env TRAINER_PACKAGE_PATH ./census_training
# %env MAIN_TRAINER_MODULE census_training.train
# %env JOB_DIR <gs://YOUR_BUCKET_ID/xgb_job_dir>


# TODO: REPLACE 'BUCKET_CREATED_ABOVE' with your GCS BUCKET_ID
BUCKET_ID = 'yangjae_storage'
# [END setup]

# ---------------------------------------
# 1. Add code to download the data from GCS (in this case, using the publicly hosted data).
# ML Engine will then be able to use the data when training your model.
# ---------------------------------------
# [START download-data]
data_filename = 'bike_train_1.csv'
data_filename2 = 'bike_train_2.csv'

# Public bucket holding the data
bucket = storage.Client().bucket('yangjae_storage')

# Path to the data inside the public bucket
data_dir = ''

# Download the data
blob = bucket.blob(''.join([data_dir, data_filename]))
blob.download_to_filename(data_filename)
blob2 = bucket.blob(''.join([data_dir, data_filename2]))
blob2.download_to_filename(data_filename2)
# [END download-data]

# ---------------------------------------
# This is where your model code would go. Below is an example model using the dataset.
# ---------------------------------------

# [START define-and-load-data]

# Load the training dataset
with open(data_filename, 'r') as train_data:
    raw_training_data = pd.read_csv(train_data, header=0)
with open(data_filename2, 'r') as train_data2:
    raw_training_data2 = pd.read_csv(train_data2, header=0)
raw_training_data.append(raw_training_data2, ignore_index=True)

# remove column we are trying to predict ('rent_freq') from features list
train_features = raw_training_data.drop('rent_freq', axis=1).drop('rent_place_num', axis=1).drop('rent_time', axis=1)
# create training labels list
train_labels = raw_training_data['rent_freq']

# [END define-and-load-data]

# [START load-into-dmatrix-and-train]
# load data into DMatrix object
dtrain = xgb.DMatrix(train_features, train_labels)
# train model
bst = xgb.train({'tree_method': 'exact'}, dtrain, 20)
# [END load-into-dmatrix-and-train]

# ---------------------------------------
# 2. Train and save the model to GCS
# ---------------------------------------
# [START export-to-gcs]
# Export the model to a file
model = 'model.bst'
bst.save_model(model)

# Upload the model to GCS
bucket = storage.Client().bucket(BUCKET_ID)
blob = bucket.blob('{}/{}'.format(
    datetime.datetime.now().strftime('bike_%Y%m%d_%H%M%S'),
    model))
blob.upload_from_filename(model)
# [END export-to-gcs]