# SCAIE - Sistema Agente Conversacional Inteligente Empresarial

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0%2B-green)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-green)](https://vuejs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

SCAIE (Sistema Agente Conversacional Inteligente Empresarial) is an intelligent conversational agent platform designed for business automation, particularly focused on sales processes. The system combines CRM functionality with AI-powered conversations to provide a complete solution for automated customer engagement.

## 🌟 Key Features

- **CRM Functionality**: Contact management with interest level tracking
- **AI-Powered Conversational Agent**: Using Qwen (Alibaba's language model) for natural conversations
- **Multi-Platform Support**: Web, Telegram, and WhatsApp integration
- **Task Management**: Built-in task tracking for follow-ups
- **Analytics Dashboard**: KPIs and metrics visualization
- **RESTful API**: Well-documented API for integration
- **Omnipotent Agent**: Advanced agent with action processing and contact management capabilities

## 🏗️ Architecture

The system follows a modern client-server architecture:

- **Frontend**: Vue.js 3 with Tailwind CSS
- **Backend**: Python FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **AI Integration**: Qwen (Alibaba Cloud) via DashScope API
- **Deployment**: Docker-ready with Nginx configuration

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher (for frontend development)
- npm (Node Package Manager)

### Using the Complete Run Script (Recommended)

The easiest way to run the complete system is using our new comprehensive script:

```bash
# Make the script executable
chmod +x run_complete.sh

# Run the complete system
./run_complete.sh
```

This script will:
1. Set up a Python virtual environment
2. Install all backend and frontend dependencies
3. Build the frontend
4. Check environment configuration
5. Start the application on port 8003

### Manual Setup

If you prefer to set up the system manually:

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/Scaie024/scAIe.crm.git
   ```

2. **Navigate to the project directory**
   ```bash
   cd scaie_crm
   ```

3. **Set up Python virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

5. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

6. **Configure environment variables**
   Create a `.env` file in the `backend` directory with your configuration:
   ```env
   # Database Configuration
   DATABASE_URL=sqlite:///./scaie.db

   # Security Configuration
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # DashScope API Configuration (Qwen)
   # Get your key at: https://dashscope.aliyuncs.com/
   DASHSCOPE_API_KEY=your_dashscope_api_key_here

   # Qwen Model Configuration
   QWEN_MODEL=qwen-plus
   ```

7. **Run the application**
   ```bash
   cd backend/src/scaie
   python3 -m app.main
   ```

## 🖥️ Accessing the Application

Once the application is running, you can access:

- **Web Interface**: http://localhost:8003
- **API Documentation**: http://localhost:8003/docs
- **Health Check**: http://localhost:8003/health

## 🧪 Testing the Agent

You can test the agent functionality using the web interface chat or via API calls:

### Using the Web Interface
1. Navigate to http://localhost:8003
2. Go to the "Chat de Pruebas del Agente" section
3. Enter messages to interact with the agent

### Using the API
You can test the agent directly via API calls:

```bash
# Test the basic chat endpoint
curl -X POST http://localhost:8003/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola", "contact_info": {"phone": "+525512345678", "name": "Cliente de Prueba"}}'

# Test the omnipotent agent endpoint (recommended)
curl -X POST http://localhost:8003/api/omnipotent-agent/process-message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hola",
    "platform": "web",
    "contact_info": {
      "phone": "+525512345678",
      "name": "Cliente de Prueba"
    }
  }'
```

## 📁 Project Structure

```
scaie_crm/
├── backend/
│   ├── src/scaie/
│   │   ├── app/
│   │   │   ├── api/          # API endpoints
│   │   │   ├── core/         # Core application components
│   │   │   ├── models/       # Database models
│   │   │   ├── schemas/      # Pydantic schemas
│   │   │   ├── services/     # Business logic services
│   │   │   └── main.py       # Application entry point
│   │   └── ...
│   ├── static/               # Built frontend files
│   ├── scaie.db              # SQLite database
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/       # Vue components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API service layer
│   │   └── ...
│   └── package.json          # Node.js dependencies
├── scripts/                  # Utility scripts
├── run_complete.sh           # Complete system run script
└── ...
```

## 🛠️ Development

### Backend Development

The backend is built with FastAPI and uses:
- SQLAlchemy for database operations
- SQLite as the default database
- Pydantic for data validation
- OAuth2 for authentication

### Frontend Development

The frontend is built with Vue.js 3 and uses:
- Vue Router for navigation
- Tailwind CSS for styling
- Fetch API for backend communication

To run the frontend in development mode:
```bash
cd frontend
npm run dev
```

## 🔧 Configuration

### Environment Variables

The system requires several environment variables to be set in the `backend/.env` file:

- `DASHSCOPE_API_KEY`: Your DashScope API key for Qwen access
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for JWT token generation
- `QWEN_MODEL`: The Qwen model to use (default: qwen-plus)

### Agent Configuration

The agent can be configured with:
- `AGENT_NAME`: The name of the agent
- `AGENT_PERSONALITY`: Personality traits of the agent
- `AGENT_TONE`: Communication tone
- `AGENT_GOAL`: Primary goal of the agent

## 📚 API Documentation

The complete API documentation is available at http://localhost:8003/docs when the application is running. It includes:
- All endpoints with examples
- Request/response schemas
- Authentication requirements
- Error codes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, please open an issue on the GitHub repository or contact the development team.