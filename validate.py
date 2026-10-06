import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import json
import warnings

warnings.filterwarnings('ignore')

import os

data_pickle_path = os.environ.get('DATA_PICKLE', 'data.pickle')
if not os.path.exists(data_pickle_path) and os.path.exists(r"D:\datasets\handsign_dataset\data.pickle"):
    data_pickle_path = r"D:\datasets\handsign_dataset\data.pickle"

if os.path.exists(data_pickle_path):
    with open(data_pickle_path, 'rb') as f:
        data_dict = pickle.load(f)
    X = np.array(data_dict['data'])
    y = np.array([int(l) for l in data_dict['labels']])
    print(f'Total samples: {X.shape[0]}')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f'Test samples: {X_test.shape[0]}')
else:
    print(f'Note: {data_pickle_path} not found (external dataset). Performing dummy feature test on models.')
    X_test = np.random.rand(10, 42)
    y_test = None

try:
    rf_dict = pickle.load(open('model.p', 'rb'))
    rf_model = rf_dict['model']
    rf_pred = rf_model.predict(X_test)
    if y_test is not None:
        print(f'Random Forest Accuracy: {accuracy_score(y_test, rf_pred):.4f}')
        print(f'RF Precision: {precision_score(y_test, rf_pred, average="weighted", zero_division=0):.4f}')
        print(f'RF Recall: {recall_score(y_test, rf_pred, average="weighted", zero_division=0):.4f}')
        print(f'RF F1: {f1_score(y_test, rf_pred, average="weighted", zero_division=0):.4f}')
    else:
        print(f'Random Forest Model: Loaded & inference functional (predicted {len(rf_pred)} samples).')
except Exception as e:
    print(f'RF Error: {e}')

try:
    mlp_dict = pickle.load(open('improved_model.p', 'rb'))
    mlp_model = mlp_dict['model']
    mlp_pred = mlp_model.predict(X_test)
    if y_test is not None:
        print(f'MLP Accuracy: {accuracy_score(y_test, mlp_pred):.4f}')
        print(f'MLP Precision: {precision_score(y_test, mlp_pred, average="weighted", zero_division=0):.4f}')
        print(f'MLP Recall: {recall_score(y_test, mlp_pred, average="weighted", zero_division=0):.4f}')
        print(f'MLP F1: {f1_score(y_test, mlp_pred, average="weighted", zero_division=0):.4f}')
    else:
        print(f'MLP Model: Loaded & inference functional (predicted {len(mlp_pred)} samples).')
except Exception as e:
    print(f'MLP Error: {e}')

with open('static/representatives.json', 'r') as f:
    reps = json.load(f)
print(f'Representatives count: {len(reps)}')
hello_rep = reps.get('Hello', [])
print(f'Representative Hello shape: {len(hello_rep)}')
