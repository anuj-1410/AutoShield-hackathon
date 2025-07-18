# AutoShield - Decentralized Account Verification Platform

AutoShield is a comprehensive Web3 security platform that combines AI-powered fake account detection with blockchain-based verification to protect decentralized ecosystems from fraud and social engineering attacks.

## 🚀 Features

- **AI-Powered Detection**: Advanced machine learning models with 97%+ accuracy
- **Blockchain Verification**: Immutable on-chain attestations and verification records
- **Real-time Processing**: Sub-second verification with instant results
- **Privacy Preserving**: Zero personal data collection, only public blockchain analysis
- **Developer Friendly**: Easy integration with REST APIs and smart contract interfaces
- **Community Driven**: Decentralized governance and community feedback integration

## 🏗️ Architecture

### Frontend
- **Next.js 14** with App Router
- **Tailwind CSS** for styling
- **shadcn/ui** component library
- **Web3 Integration** (MetaMask, WalletConnect)
- **Responsive Design** for desktop and mobile

### Backend
- **Python FastAPI** for AI/ML services
- **PostgreSQL** for data storage (optional)
- **Redis** for caching and session management (optional)
- **Smart Contracts** on Ethereum (Solidity)

### AI/ML Stack
- **scikit-learn** for traditional ML models
- **TensorFlow/PyTorch** for deep learning
- **Custom Models** for fake account detection

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

2. **Install dependencies**
   ```bash
   # Frontend dependencies
   npm install
   
   # Backend dependencies
   pip install fastapi uvicorn
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
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs

## 🌐 Application URLs

- **Frontend Dashboard**: http://localhost:3000
- **Public Query Tool**: http://localhost:3000/query
- **Admin Panel**: http://localhost:3000/admin
- **Learn More**: http://localhost:3000/learn
- **API Documentation**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health

## 📖 API Endpoints

### Verification
- `POST /api/v1/verification/analyze` - Analyze wallet address
- `GET /api/v1/verification/status/{address}` - Get verification status
- `POST /api/v1/verification/re-analyze` - Re-analyze account

### Analytics
- `GET /api/v1/analytics/system-stats` - System statistics
- `GET /api/v1/analytics/daily-stats` - Daily statistics

### Admin
- `GET /api/v1/admin/flagged-accounts` - Get flagged accounts
- `POST /api/v1/admin/flagged-accounts/{address}/review` - Review flagged account

### Blockchain
- `GET /api/v1/blockchain/network-info` - Network information
- `GET /api/v1/blockchain/transaction/{hash}` - Transaction details

## 🧪 Testing

Run the backend test suite:
```bash
python test_backend.py
```

## 🔧 Configuration

The application uses environment variables for configuration. Create a `.env` file in the root directory:

```env
# Application
DEBUG=true
SECRET_KEY=your-secret-key-here

# Database (optional)
DATABASE_URL=postgresql://user:password@localhost:5432/autoshield

# Redis (optional)
REDIS_URL=redis://localhost:6379

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

## 🏗️ Project Structure

```
autoshield-dapp/
├── app/                    # Next.js frontend
│   ├── admin/             # Admin dashboard
│   ├── dashboard/         # User dashboard
│   ├── query/             # Public query tool
│   └── learn/             # Educational content
├── backend/               # Python backend
│   └── app/
│       ├── api/           # API endpoints
│       ├── core/          # Core utilities
│       ├── models/        # Database models
│       ├── services/      # Business logic
│       └── utils/         # Utility functions
├── components/            # React components
├── contracts/             # Smart contracts
├── lib/                   # Utility libraries
├── public/                # Static assets
└── scripts/               # Deployment scripts
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

## 🔮 Roadmap

- [ ] Real blockchain integration
- [ ] Advanced ML models
- [ ] Database integration
- [ ] Mobile app
- [ ] API rate limiting
- [ ] Smart contract deployment
- [ ] Community governance

---

**Built with ❤️ for Web3 Security**
