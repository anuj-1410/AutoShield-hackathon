"""
AutoShield Prediction Script
This script provides a command-line interface to test the fraud detection model
with sample wallet data.
"""

import pandas as pd
import joblib

# --- Load Model and Features ---
print("--- AutoShield Prediction Script ---")
try:
    print("\n[1/2] Loading trained model and features...")
    model = joblib.load('fraud_detection_model.pkl')
    scaler = joblib.load('feature_scaler.pkl')
    feature_names = joblib.load('feature_names.pkl')
    print("   > Model, scaler, and features loaded successfully.")
except FileNotFoundError as e:
    print(f"Error: Could not load model file - {e}. Please run train_model.py first.")
    exit()

def predict_wallet_fraud(wallet_data):
    """
    Predicts if a wallet is fraudulent based on its features.

    Args:
        wallet_data: A dictionary containing wallet features.

    Returns:
        A tuple containing the prediction and probability.
    """
    # Create a DataFrame with the correct feature order.
    sample_df = pd.DataFrame([wallet_data], columns=feature_names)
    
    # Scale features if the model requires it (e.g., Logistic Regression).
    if hasattr(model, 'coef_'):
        sample_scaled = scaler.transform(sample_df)
        prediction = model.predict(sample_scaled)[0]
        probability = model.predict_proba(sample_scaled)[0][1]
    else:
        prediction = model.predict(sample_df)[0]
        probability = model.predict_proba(sample_df)[0][1]
    
    return int(prediction), float(probability)

def main():
    """Main function to run a test prediction."""
    print("\n[2/2] Running a test prediction with a sample suspicious wallet...")
    
    # Define a sample wallet with suspicious characteristics.
    suspicious_wallet = {
        'wallet_age_days': 10, 'total_transactions': 200, 'total_incoming_transactions': 100,
        'total_outgoing_transactions': 100, 'unique_counterparties': 5, 'is_contract_creator': 0,
        'average_transaction_value': 0.1, 'max_transaction_value': 1.0, 'min_transaction_value': 0.001,
        'median_transaction_value': 0.05, 'std_transaction_value': 0.2, 'average_time_between_transactions': 0.1,
        'tx_frequency_per_day': 20.0, 'peak_tx_in_24h': 80, 'contract_interaction_count': 2,
        'erc20_token_count': 1, 'nft_count': 0, 'token_airdrops_received': 10,
        'tx_burstiness': 0.95, 'recurrent_tx_to_same_address': 30, 'received_from_new_accounts': 0.8,
        'suspicious_contract_interactions': 5, 'dust_transactions_count': 50, 'failed_transaction_count': 15,
        'average_gas_fee_paid': 0.001, 'is_burn_address_interactor': 1, 'creation_year': 2024,
        'creation_month': 1, 'creation_day_of_week': 5, 'has_contract_interaction': 1,
        'days_to_first_contract': 1
    }
    
    # Make a prediction.
    prediction, probability = predict_wallet_fraud(suspicious_wallet)
    
    # Display the results.
    print("\n--- Prediction Result ---")
    print(f"Wallet Data: Sample Suspicious Wallet")
    print(f"Prediction: {'FRAUDULENT' if prediction == 1 else 'LEGITIMATE'}")
    print(f"Fraud Probability: {probability:.2%}")
    print("-------------------------")

if __name__ == "__main__":
    main()
