import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from math import floor, ceil

data_filename = 'data/bike_test.csv'

with open(data_filename, 'r') as train_data:
    raw_test_data = pd.read_csv(train_data, header=0)

test_features = raw_test_data.drop('rent_freq', axis=1).drop('rent_place_num', axis=1).drop('rent_time', axis=1)
# create training labels list
test_labels = raw_test_data['rent_freq']

bst = xgb.Booster({'nthread': 4})  # init model
bst.load_model('bst/bike_20181210_140901%2Fmodel.bst')  # load data

dtest = xgb.DMatrix(test_features)
# train model
pred = bst.predict(dtest)

mse = mean_squared_error(test_labels, pred)
rmse = np.sqrt(mse)
print(rmse)
'''
successCnt = 0
for i in range(0, test_labels.size):
    isCorrect = round(pred[i]) == test_labels[i]
    # isCorrect = floor(pred[i]) == test_labels[i] or ceil(pred[i]) == test_labels[i]

    print(test_labels[i], pred[i], isCorrect)
    if isCorrect:
        successCnt += 1

print("Total : ", test_labels.size)     # 914400
print("Success : ", successCnt)     # 510871
print("Accuracy : ", successCnt / test_labels.size)     # 0.5586953193350831
'''




