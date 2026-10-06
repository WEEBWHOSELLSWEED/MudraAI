import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def load_data(filepath='data.pickle'):
    """
    Loads static landmark features and labels from the pickle file.
    Performs validation and returns NumPy arrays.
    """
    with open(filepath, 'rb') as f:
        data_dict = pickle.load(f)
        
    X = np.array(data_dict['data'])
    y_raw = np.array(data_dict['labels'])
    
    # Encode labels if they are not integers
    le = LabelEncoder()
    y = le.fit_transform(y_raw)
    
    # In MudraAI, labels are string numbers '0', '1', '2' mapping to labels_dict.
    # But let's let LabelEncoder handle it, or we just map them directly to int.
    # The baseline expects y to be integers.
    try:
        y = np.array([int(l) for l in y_raw])
    except:
        pass # fallback to LabelEncoder
        
    return X, y

def get_train_val_test_split(X, y, test_size=0.2, val_size=0.1, random_state=42):
    """
    Splits the dataset into train, validation, and test sets.
    Prevents data leakage by ensuring strict splits.
    """
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Adjust val_size proportion relative to the remaining data
    val_ratio = val_size / (1.0 - test_size)
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_ratio, random_state=random_state, stratify=y_train_val
    )
    
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)

if __name__ == "__main__":
    X, y = load_data()
    print(f"Loaded {X.shape[0]} samples with {X.shape[1]} features.")
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = get_train_val_test_split(X, y)
    print(f"Train: {X_train.shape[0]}, Val: {X_val.shape[0]}, Test: {X_test.shape[0]}")
