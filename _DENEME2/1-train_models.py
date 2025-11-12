import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, confusion_matrix
from sklearn.preprocessing import OneHotEncoder
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

# --- 3. Split Data ONCE (to prevent data leakage) ---
# We split the raw data first, including the target columns
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Save test indices for consistent splitting in analysis script
test_indices = test_df.index
pd.Series(test_indices).to_csv('/Users/batumbp/Files/betting/_DENEME2/results/test_indices.csv', index=False)

X_train_raw = train_df[input_cols]
X_test_raw = test_df[input_cols]

# --- 4. Fit Encoder ONLY on Training Data ---
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
encoder.fit(X_train_raw)

# Save the fitted encoder
joblib.dump(encoder, '/Users/batumbp/Files/betting/_DENEME2/results/encoder.pkl')

# Transform both training and test sets
X_train_encoded = encoder.transform(X_train_raw)
X_test_encoded = encoder.transform(X_test_raw)

# --- 5. Loop, Train, and Evaluate Efficiently ---
results = []
for target_col in tqdm(target_cols, desc="Training models for each feature"):
    # Ensure target is a valid binary column
    if train_df[target_col].nunique() != 2:
        continue

    y_train = train_df[target_col]
    y_test = test_df[target_col]

    # Use SMOTE for significant minority classes, otherwise use class_weight
    min_class_count = y_train.value_counts().min()
    if min_class_count > 10:
        smote = SMOTE(random_state=42, k_neighbors=min(min_class_count - 1, 5))
        X_train_res, y_train_res = smote.fit_resample(X_train_encoded, y_train)
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    else:
        X_train_res, y_train_res = X_train_encoded, y_train
        model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1)

    model.fit(X_train_res, y_train_res)
    joblib.dump(model, f'/Users/batumbp/Files/betting/_DENEME2/results/models/{target_col.replace("/", "_")}.pkl')
    y_pred = model.predict(X_test_encoded)

    # --- 6. Calculate and Store Comprehensive Metrics ---
    precision = precision_score(y_test, y_pred, pos_label=1, zero_division=0)
    recall = recall_score(y_test, y_pred, pos_label=1, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
    else:
        # Handle cases with only one class
        if cm.shape == (1, 1):
            if y_test.iloc[0] == 1:
                tn, fp, fn, tp = 0, 0, 0, cm[0, 0]
            else:
                tn, fp, fn, tp = cm[0, 0], 0, 0, 0
        else:
            tn, fp, fn, tp = 0, 0, 0, 0  # Fallback
    num_bets = tp + fp

    results.append({
        'Feature': target_col,
        'Precision': precision,
        'Recall': recall,
        'Bets_Placed': num_bets,
        'True_Positives': tp,
        'False_Positives': fp
    })

# --- 7. Save Results ---
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by='Precision', ascending=False)
results_df.to_csv('/Users/batumbp/Files/betting/_DENEME2/results/model_results.csv', index=False)

print("Model results saved to 'results/model_results.csv'")
print("\nTop 5 features by Precision:")
print(results_df.head(5).to_string())