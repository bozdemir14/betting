import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from imblearn.over_sampling import SMOTE
from tqdm import tqdm
import joblib

# --- 1. Load Data ---
df = pd.read_csv('/Users/batumbp/Files/betting/_DENEME2/data/fikstur_feature_matrix_final.csv')

# --- 2. Prepare Inputs (Features) ---
# Define input columns and ensure correct data types for encoding
input_cols = ['Favorite_Odds', 'Favorite_Team', 'Lig', 'Season', 'Hafta']
for col in input_cols:
    df[col] = df[col].astype('category')

X_raw = df[input_cols]
target_cols = df.columns[11:] # Assuming features start at column 11

# --- 3. Prepare Data for Training (Use ALL data for final models) ---
# For evaluation, we'll still need a test set, but for deployment we train on everything
# Keep the split for evaluation purposes, but also train final models on full data

# Split for evaluation
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Save test indices for consistent evaluation
test_indices = test_df.index
pd.Series(test_indices).to_csv('/Users/batumbp/Files/betting/_DENEME2/results/test_indices.csv', index=False)

# For final models, use ALL data
X_full_raw = df[input_cols]

# --- 4. Fit Encoder on ALL Data (for deployment) ---
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
encoder.fit(X_full_raw)

# Save the fitted encoder
joblib.dump(encoder, '/Users/batumbp/Files/betting/_DENEME2/results/encoder.pkl')

# Transform data for evaluation
X_train_raw = train_df[input_cols]
X_test_raw = test_df[input_cols]
X_train_encoded = encoder.transform(X_train_raw)
X_test_encoded = encoder.transform(X_test_raw)

# Also prepare full dataset encoding for final models
X_full_encoded = encoder.transform(X_full_raw)

# --- 5. Loop, Train, and Evaluate Efficiently ---
model_results = []

for target_col in tqdm(target_cols, desc="Training models for each feature"):
    # Ensure target is a valid binary column
    if df[target_col].nunique() != 2:
        continue

    y_full = df[target_col]
    y_train = train_df[target_col]
    y_test = test_df[target_col]

    # Use SMOTE for significant minority classes, otherwise use class_weight
    min_class_count = y_train.value_counts().min()
    if min_class_count > 10:
        smote = SMOTE(random_state=42, k_neighbors=min(min_class_count - 1, 5))
        X_train_res, y_train_res = smote.fit_resample(X_train_encoded, y_train)
        eval_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    else:
        X_train_res, y_train_res = X_train_encoded, y_train
        eval_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1)

    # Train evaluation model
    eval_model.fit(X_train_res, y_train_res)
    
    # Train final model on ALL data (for predictions on new matches)
    min_class_count_full = y_full.value_counts().min()
    if min_class_count_full > 10:
        smote_full = SMOTE(random_state=42, k_neighbors=min(min_class_count_full - 1, 5))
        X_full_res, y_full_res = smote_full.fit_resample(X_full_encoded, y_full)
        final_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    else:
        X_full_res, y_full_res = X_full_encoded, y_full
        final_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1)
    
    final_model.fit(X_full_res, y_full_res)
    
    # Save the FINAL model (for making predictions on new matches)
    joblib.dump(final_model, f'/Users/batumbp/Files/betting/_DENEME2/results/models/{target_col.replace("/", "_")}.pkl')

    # Evaluate on test set using evaluation model
    y_pred = eval_model.predict(X_test_encoded)
    y_pred_proba = eval_model.predict_proba(X_test_encoded)[:, 1]

    # Calculate comprehensive metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc = roc_auc_score(y_test, y_pred_proba)
    
    # Class distribution info
    train_pos_rate = y_train.mean()
    test_pos_rate = y_test.mean()
    
    # Store results
    model_results.append({
        'Feature': target_col,
        'Accuracy': f"{accuracy:.4f}",
        'Precision': f"{precision:.4f}",
        'Recall': f"{recall:.4f}",
        'F1_Score': f"{f1:.4f}",
        'AUC': f"{auc:.4f}",
        'Train_Positive_Rate': f"{train_pos_rate:.4f}",
        'Test_Positive_Rate': f"{test_pos_rate:.4f}",
        'Test_Samples': len(y_test)
    })

    # Create a results DataFrame for this feature (evaluation predictions)
    predictions_df = pd.DataFrame({
        'true_label': y_test.values,
        'predicted_proba': y_pred_proba
    }, index=y_test.index)

    # Save the evaluation predictions
    predictions_df.to_csv(f'/Users/batumbp/Files/betting/_DENEME2/results/predictions/{target_col.replace("/", "_")}.csv')

# Save comprehensive model results
results_df = pd.DataFrame(model_results)
results_df.to_csv('/Users/batumbp/Files/betting/_DENEME2/results/model_results.csv', index=False)

print("Models trained on full data, evaluation results, and predictions saved.")