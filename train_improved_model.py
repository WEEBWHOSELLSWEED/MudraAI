import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import time
from data_loader import load_data, get_train_val_test_split
import json

def train_and_evaluate():
    X, y = load_data('data.pickle')
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = get_train_val_test_split(X, y)
    
    print("Training Improved Model (MLPClassifier)...")
    model = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42)
    
    start_time = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start_time
    
    # Evaluate
    start_time = time.time()
    y_pred = model.predict(X_test)
    infer_time = time.time() - start_time
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print(f"Results:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"Inference Time for {len(y_test)} samples: {infer_time:.4f}s")
    
    # Save the model
    with open('improved_model.p', 'wb') as f:
        pickle.dump({'model': model}, f)
        
    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'train_time': train_time,
        'inference_time_per_sample': infer_time / len(y_test)
    }
    
    with open('metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
        
    print("Saved improved_model.p and metrics.json")

if __name__ == '__main__':
    train_and_evaluate()
