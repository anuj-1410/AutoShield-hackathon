"""
AutoShield Model Training Script
This script loads the wallet fraud dataset, preprocesses the data, trains multiple
machine learning models, and saves the best-performing model for inference.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
import joblib

def main():
    """Main function to run the model training pipeline."""
    print("--- AutoShield Model Training Started ---")

    # 1. Load the Dataset
    print("\n[1/5] Loading dataset: wallet_fraud_dataset.csv...")
    try:
        df = pd.read_csv('wallet_fraud_dataset.csv')
    except FileNotFoundError:
        print("Error: wallet_fraud_dataset.csv not found. Please place it in the ai-services directory.")
        return

    # 2. Preprocess Data and Engineer Features
    print("[2/5] Preprocessing data and engineering features...")
    df['account_creation_timestamp'] = pd.to_datetime(df['account_creation_timestamp'])
    df['first_contract_interaction_timestamp'] = pd.to_datetime(df['first_contract_interaction_timestamp'], errors='coerce')
    df['creation_year'] = df['account_creation_timestamp'].dt.year
    df['creation_month'] = df['account_creation_timestamp'].dt.month
    df['creation_day_of_week'] = df['account_creation_timestamp'].dt.dayofweek
    df['has_contract_interaction'] = (~df['first_contract_interaction_timestamp'].isna()).astype(int)
    df['days_to_first_contract'] = (df['first_contract_interaction_timestamp'] - df['account_creation_timestamp']).dt.days
    df['days_to_first_contract'] = df['days_to_first_contract'].fillna(-1)

    features_to_drop = ['wallet_address', 'account_creation_timestamp', 'first_contract_interaction_timestamp']
    df_ml = df.drop(columns=features_to_drop)

    X = df_ml.drop('is_fake_account', axis=1)
    y = df_ml['is_fake_account']
    feature_names = list(X.columns)
    print(f"   > Found {len(feature_names)} features.")

    # 3. Split Data and Scale Features
    print("[3/5] Splitting data and scaling features...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 4. Train the Model (Random Forest selected for performance)
    print("[4/5] Training RandomForestClassifier model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    auc_score = roc_auc_score(y_test, y_pred_proba)
    print(f"   > Model training complete. AUC Score: {auc_score:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # 5. Save the Model, Scaler, and Feature Names
    print("[5/5] Saving model, scaler, and feature names...")
    joblib.dump(model, 'fraud_detection_model.pkl')
    joblib.dump(scaler, 'feature_scaler.pkl')
    joblib.dump(feature_names, 'feature_names.pkl')
    print("   > Files saved successfully: fraud_detection_model.pkl, feature_scaler.pkl, feature_names.pkl")

    print("\n--- AutoShield Model Training Completed ---")

if __name__ == "__main__":
    main()
