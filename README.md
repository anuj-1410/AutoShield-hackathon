# AutoShield - Decentralized Account Verification Platform

AutoShield is a comprehensive Web3 security platform that combines AI-powered fake account detection with blockchain-based verification to protect decentralized ecosystems from fraud and social engineering attacks.

## 🚀 Features

- **AI-Powered Detection**: Advanced machine learning models with 97%+ accuracy
- **Blockchain Verification**: Immutable on-chain attestations and verification records
- **Real-time Processing**: Sub-second verification with instant results
- **Privacy Preserving**: Zero personal data collection, only public blockchain analysis
- **Developer Friendly**: Easy integration with REST APIs and smart contract interfaces
- **Community Driven**: Decentralized governance and community feedback integration

## 🏗️ Project Structure

```
autoshield-dapp/
├── 📁 frontend/                    # Next.js Web Application
│   ├── 📁 app/                     # Next.js App Router
│   ├── 📁 components/              # React components
│   ├── 📁 hooks/                   # Custom React hooks
│   ├── 📁 lib/                     # Frontend utilities
│   ├── 📁 public/                  # Static assets
│   ├── 📁 styles/                  # CSS styles
│   └── package.json                # Frontend dependencies
│
├── 📁 backend/                     # Python Backend API
│   ├── 📁 app/                     # FastAPI application
│   │   ├── 📁 api/                 # API endpoints
│   │   ├── 📁 core/                # Core configurations
│   │   ├── 📁 models/              # Database models
│   │   ├── 📁 services/            # Business logic
│   │   └── 📁 utils/               # Utility functions
│   └── requirements.txt            # Python dependencies
│
├── 📁 smart-contracts/             # Blockchain Smart Contracts
│   ├── 📁 contracts/               # Solidity contracts
│   ├── 📁 scripts/                 # Deployment scripts
│   ├── 📁 test/                    # Contract tests
│   └── package.json                # Smart contract dependencies
│
├── 📁 ai-services/                 # AI/ML Services
│   ├── 📁 models/                  # ML model files
│   ├── 📁 training/                # Training scripts
│   ├── 📁 inference/               # Inference engines
│   └── requirements.txt            # AI dependencies
│
├── 📁 tests/                       # Integration tests
├── 📁 docs/                        # Documentation
├── 📁 config/                      # Configuration files
└── start-autoshield.ps1            # PowerShell startup script
```

## 🚀 Quick Start

### Prerequisites
- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/autoshield-dapp.git
   cd autoshield-dapp
   ```

2. **Install frontline dependencies**
   ```bash
   # Install frontend dependencies
   cd frontend && npm install
   
   # Install backend dependencies
   cd ../backend && pip install -r requirements.txt
   ```

3. **Start the application**
   
   **Option A: Start both services with PowerShell script**
   ```powershell
   .\start-autoshield.ps1 -All
   ```
   
   **Option B: Start services individually**
   
   Terminal 1 (Backend):
   ```bash
   cd backend/app
   python main_simple.py
   ```
   
   Terminal 2 (Frontend):
   ```bash
   cd frontend
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs

## 📖 API Endpoints

### Verification
- `POST /api/v1/verification/analyze` - Analyze wallet address
- `GET /api/v1/verification/status/{address}` - Get verification status

### Analytics
- `GET /api/v1/analytics/system-stats` - System statistics
- `GET /api/v1/analytics/daily-stats` - Daily statistics

### Admin
- `GET /api/v1/admin/flagged-accounts` - Get flagged accounts
- `POST /api/v1/admin/flagged-accounts/{address}/review` - Review flagged account

## 🧪 Testing

Run tests for different components:

```bash
# Backend tests
cd tests && python test_backend.py

# Frontend tests
cd frontend && npm run test
```

## 🔧 Configuration

The application uses environment variables for configuration. Create a `.env` file in the `config/` directory:

```env
# Application
DEBUG=true
SECRET_KEY=your-secret-key-here

# Database (optional)
DATABASE_URL=postgresql://user:password@localhost:5432/autoshield

# Blockchain
BLOCKCHAIN_RPC_URL=http://localhost:8545
CONTRACT_ADDRESS=
PRIVATE_KEY=

# AI/ML
AI_CONFIDENCE_THRESHOLD=0.7

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600
```

## 🔐 Security Features

- **Rate Limiting**: API rate limiting to prevent abuse
- **Input Validation**: Comprehensive input validation
- **CORS Protection**: Cross-origin request protection
- **Security Headers**: Security headers for enhanced protection
- **Wallet Validation**: Ethereum address validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

For support, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for Web3 Security**
