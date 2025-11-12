import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, recall_score, precision_score
from sklearn.preprocessing import OneHotEncoder
from imblearn.over_sampling import SMOTE
from tqdm import tqdm
import numpy as np

# Load the data
df = pd.read_csv('/Users/batumbp/Files/betting/_DENEME2/fikstur_feature_matrix_final.csv')

# Inputs: Favorite_Odds, Favorite_Team, Lig, Season, Hafta
input_cols = ['Favorite_Odds', 'Favorite_Team', 'Lig', 'Season', 'Hafta']

# Convert Favorite_Odds to string for one-hot encoding
df['Favorite_Odds'] = df['Favorite_Odds'].astype(str)

# One-hot encode the inputs
encoder = OneHotEncoder(sparse_output=False, drop='first')  # drop first to avoid multicollinearity
encoded_inputs = encoder.fit_transform(df[input_cols])
encoded_df = pd.DataFrame(encoded_inputs, columns=encoder.get_feature_names_out(input_cols))

X = encoded_df

# Target columns: from column 11 onwards
target_cols = df.columns[11:]

results = []

for target_col in tqdm(target_cols, desc="Processing features"):
    # Ensure target is numeric
    if df[target_col].dtype == 'bool':
        df[target_col] = df[target_col].astype(int)
    elif df[target_col].dtype == 'object':
        continue
    
    y = df[target_col]
    
    if y.nunique() != 2:
        continue
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Check if we can use SMOTE (minority class > 10)
    min_class_count = y_train.value_counts().min()
    if min_class_count > 10:
        smote = SMOTE(random_state=42)
        X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    else:
        X_train_res, y_train_res = X_train, y_train
        model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    
    model.fit(X_train_res, y_train_res)
    
    # Predict
    y_pred = model.predict(X_test)
    
    # Recall for True
    recall_true = recall_score(y_test, y_pred, pos_label=1)
    precision_true = precision_score(y_test, y_pred, pos_label=1, zero_division=0)
    results.append((target_col, recall_true, precision_true))

# Sort by recall for True
results.sort(key=lambda x: x[1], reverse=True)
print("\nTop 5 features by recall for True:")
for col, rec, prec in results[:5]:
    print(f'{col}: Recall {rec:.4f}, Precision {prec:.4f}')

# Save all results to CSV
results_df = pd.DataFrame(results, columns=['Feature', 'Recall_True', 'Precision_True'])
results_df.to_csv('/Users/batumbp/Files/betting/_DENEME2/model_results.csv', index=False)
print("Results saved to model_results.csv")

# For top 5, print detailed metrics
print("\nDetailed metrics for top 5 features:")
for col, _, _ in results[:5]:
    y = df[col].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    min_class_count = y_train.value_counts().min()
    if min_class_count > 10:
        smote = SMOTE(random_state=42)
        X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    else:
        X_train_res, y_train_res = X_train, y_train
        model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    model.fit(X_train_res, y_train_res)
    y_pred = model.predict(X_test)
    print(f'\n{col}:')
    print(classification_report(y_test, y_pred, target_names=['False', 'True']))