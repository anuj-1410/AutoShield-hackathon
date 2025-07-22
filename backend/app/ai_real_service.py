"""
AutoShield Real AI Service
This service uses the actual trained ML model for fraud detection
"""

import os
import sys
import asyncio
import joblib
import pandas as pd
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Add ai-services to path
sys.path.append('../../ai-services')

logger = logging.getLogger(__name__)

class RealAIService:
    def __init__(self):
        self.model_version = "fraud_detection_v1.0"
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.model_loaded = False
        
        # Load the real ML model
        self._load_model()
    
    def _load_model(self):
        """Load the trained ML model components"""
        try:
            model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ai-services'))
            
            # Load model components
            self.model = joblib.load(os.path.join(model_dir, 'fraud_detection_model.pkl'))
            self.scaler = joblib.load(os.path.join(model_dir, 'feature_scaler.pkl'))
            self.feature_names = joblib.load(os.path.join(model_dir, 'feature_names.pkl'))
            
            self.model_loaded = True
            logger.info("✅ Real ML model loaded successfully")
            print("✅ Real ML model loaded successfully")
            print(f"📊 Model features: {len(self.feature_names)}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load ML model: {e}")
            print(f"❌ Failed to load ML model: {e}")
            raise RuntimeError("ML model is required for fraud detection. Please ensure model files exist.")
    
    async def predict_fraud(self, wallet_features: Dict) -> Dict:
        """
        Real AI prediction using trained ML model
        
        Args:
            wallet_features: Dictionary containing wallet feature data
            
        Returns:
            Dictionary with prediction results
        """
        if not self.model_loaded:
            raise RuntimeError("ML model not loaded")
        
        try:
            # Prepare model input - ensure all required features are present
            model_input = {}
            for feature_name in self.feature_names:
                model_input[feature_name] = wallet_features.get(feature_name, 0)
            
            logger.info(f"🔍 Running AI prediction with {len(model_input)} features")
            
            # Create DataFrame with correct feature order
            input_df = pd.DataFrame([model_input])
            
            # Make prediction
            if hasattr(self.model, 'predict_proba'):
                # For models that support probability
                if hasattr(self.model, 'coef_'):
                    # Scale features for linear models
                    input_scaled = self.scaler.transform(input_df)
                    prediction = self.model.predict(input_scaled)[0]
                    fraud_probability = self.model.predict_proba(input_scaled)[0][1]
                else:
                    # Tree-based models don't need scaling
                    prediction = self.model.predict(input_df)[0]
                    fraud_probability = self.model.predict_proba(input_df)[0][1]
            else:
                # Fallback for models without probability
                prediction = self.model.predict(input_df)[0]
                fraud_probability = 0.5
            
            # Determine risk level
            if fraud_probability > 0.8:
                risk_level = "HIGH"
            elif fraud_probability > 0.5:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"
            
            # Determine status based on prediction
            if prediction == 0:  # Not fraud
                if fraud_probability < 0.2:
                    status = "verified"
                else:
                    status = "unverified"
            else:  # Fraud detected
                status = "suspected"
            
            # Calculate confidence score (inverse of fraud probability for verified accounts)
            if status == "verified":
                confidence_score = round((1 - fraud_probability) * 100, 2)
            else:
                confidence_score = round(fraud_probability * 100, 2)
            
            # Generate risk factors based on features
            risk_factors = self._generate_risk_factors(wallet_features, fraud_probability)
            
            # Generate attestation hash for verified accounts
            attestation_hash = None
            if status == "verified":
                attestation_hash = self._generate_attestation_hash(
                    wallet_features.get('wallet_address', ''),
                    status,
                    confidence_score
                )
            
            result = {
                "prediction": int(prediction),
                "fraud_probability": float(fraud_probability),
                "risk_level": risk_level,
                "status": status,
                "confidence_score": confidence_score,
                "risk_score": int(fraud_probability * 100),
                "risk_factors": risk_factors,
                "attestation_hash": attestation_hash,
                "model_version": self.model_version,
                "analyzed_at": datetime.now().isoformat()
            }
            
            logger.info(f"🎯 AI Prediction completed: {status} ({confidence_score}% confidence)")
            return result
            
        except Exception as e:
            logger.error(f"❌ AI prediction failed: {e}")
            raise RuntimeError(f"AI prediction failed: {str(e)}")
    
    def _generate_risk_factors(self, wallet_features: Dict, fraud_probability: float) -> List[str]:
        """Generate human-readable risk factors based on wallet features"""
        risk_factors = []
        
        # High fraud probability
        if fraud_probability > 0.7:
            risk_factors.append("High ML fraud probability")
        elif fraud_probability > 0.5:
            risk_factors.append("Medium ML fraud probability")
        
        # Age-based risks
        wallet_age = wallet_features.get('wallet_age_days', 0)
        if wallet_age < 7:
            risk_factors.append("Very new account (less than 7 days)")
        elif wallet_age < 30:
            risk_factors.append("New account (less than 30 days)")
        
        # Transaction pattern risks
        tx_burstiness = wallet_features.get('tx_burstiness', 0)
        if tx_burstiness > 0.8:
            risk_factors.append("High transaction burstiness (bot-like behavior)")
        
        # Suspicious interactions
        suspicious_contracts = wallet_features.get('suspicious_contract_interactions', 0)
        if suspicious_contracts > 0:
            risk_factors.append(f"Interactions with {suspicious_contracts} suspicious contracts")
        
        # Failed transactions
        failed_txs = wallet_features.get('failed_transaction_count', 0)
        total_txs = wallet_features.get('total_transactions', 1)
        if failed_txs > 0 and (failed_txs / total_txs) > 0.1:
            risk_factors.append("High failure rate in transactions")
        
        # Dust transactions
        dust_txs = wallet_features.get('dust_transactions_count', 0)
        if dust_txs > total_txs * 0.5:
            risk_factors.append("High number of dust transactions")
        
        # New account connections
        new_account_ratio = wallet_features.get('received_from_new_accounts', 0)
        if new_account_ratio > 0.7:
            risk_factors.append("High interactions with new accounts")
        
        return risk_factors
    
    def _generate_attestation_hash(self, wallet_address: str, status: str, confidence: float) -> str:
        """Generate cryptographic attestation hash"""
        data = f"{wallet_address}:{status}:{confidence}:{self.model_version}:{datetime.now().isoformat()}"
        return "0x" + hashlib.sha256(data.encode()).hexdigest()
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        return {
            "model_loaded": self.model_loaded,
            "model_version": self.model_version,
            "feature_count": len(self.feature_names) if self.feature_names else 0,
            "model_type": str(type(self.model).__name__) if self.model else "None"
        }
