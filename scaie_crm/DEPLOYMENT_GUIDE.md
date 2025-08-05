# SCAIE Deployment Guide

This guide explains how to deploy and run the SCAIE (Sistema Agente Conversacional Inteligente Empresarial) application using the provided scripts.

## 📋 Prerequisites

Before deploying the application, ensure you have the following installed:

- Python 3.8 or higher
- Node.js 14 or higher (for frontend development)
- npm (Node Package Manager)

## 🚀 Deployment Process

The deployment process has been simplified with three main scripts:

### 1. Setup Script (`setup.sh`)

This script prepares the environment by:

- Creating a Python virtual environment
- Installing all required backend dependencies
- Installing frontend dependencies (if npm is available)

**Usage:**
```bash
./setup.sh
```

This script only needs to be run once, or when dependencies are updated.

### 2. Run Script (`run_app.sh`)

This script starts the SCAIE application:

- Checks for required configuration files
- Ensures the database is available
- Terminates any existing processes on port 8003
- Starts the application server

**Usage:**
```bash
./run_app.sh
```

The application will be available at:
- Web Interface: http://localhost:8003
- API Documentation: http://localhost:8003/docs
- Health Check: http://localhost:8003/health

To stop the application, press `Ctrl+C`.

### 3. Full Deployment Script (`deploy_simple.sh`)

This is a comprehensive script that handles the complete deployment process:

- Environment setup
- Dependency installation
- Frontend building
- Database initialization
- Application startup

**Usage:**
```bash
./deploy_simple.sh
```

## ⚙️ Configuration

### Environment Variables

Before running the application, you need to configure the environment variables in the `backend/.env` file:

```env
# Database Configuration
DATABASE_URL=sqlite:///./scaie.db

# Qwen API Configuration (required for AI features)
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# Agent Configuration
AGENT_NAME=SCAI
AGENT_PERSONALITY="amigable, profesional, directo, conversacional, natural"
AGENT_TONE="profesional y directo"
AGENT_GOAL="ayudar a las empresas a ser más eficientes con inteligencia artificial y automatización de procesos"

# LLM Parameters
TEMPERATURE=0.8
MAX_TOKENS=1024
TOP_P=0.9
TOP_K=30

# Skip authentication for testing
SKIP_AUTH=true
```

**Important:** You must obtain a DashScope API key from [Alibaba Cloud DashScope](https://dashscope.console.aliyuncs.com/) for the AI features to work.

## 🧪 Testing the Application

Once the application is running, you can test it in several ways:

### 1. Web Interface

Open your browser and navigate to http://localhost:8003 to access the web interface.

### 2. API Endpoints

Use curl or any HTTP client to test the API endpoints:

```bash
# Test health check
curl http://localhost:8003/health

# List contacts
curl http://localhost:8003/api/contacts/

# Process a message with the AI agent
curl -X POST http://localhost:8003/api/omnipotent-agent/process-message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "platform": "web", "contact_info": {"name": "Test User", "phone": "123456789"}}'
```

### 3. API Documentation

Visit http://localhost:8003/docs to access the interactive API documentation.

## 🛠️ Troubleshooting

### Common Issues and Solutions

1. **Port already in use**
   - The run script automatically terminates processes on port 8003
   - If issues persist, manually kill the process:
     ```bash
     lsof -i :8003
     kill -9 <process_id>
     ```

2. **Missing dependencies**
   - Run the setup script again:
     ```bash
     ./setup.sh
     ```

3. **Database errors**
   - Delete the existing database file and restart:
     ```bash
     rm backend/scaie.db
     ./run_app.sh
     ```

4. **Frontend not loading**
   - Ensure you've built the frontend:
     ```bash
     cd frontend
     npm install
     npm run build
     cd ..
     cp -r frontend/dist/* backend/static/
     ```

## 📁 Project Structure

```
scaie_crm/
├── backend/
│   ├── src/scaie/app/        # Main application code
│   ├── static/               # Static files
│   ├── scaie.db              # SQLite database
│   └── .env                  # Environment configuration
├── frontend/                 # Vue.js frontend
├── setup.sh                  # Environment setup script
├── run_app.sh                # Application run script
├── deploy_simple.sh          # Full deployment script
├── README.md                 # Project documentation
└── DEPLOYMENT_GUIDE.md       # This file
```

## 🔒 Security Considerations

1. Keep your DashScope API key secure and never commit it to version control
2. Use environment variables for all sensitive configuration
3. In production, disable `SKIP_AUTH` and implement proper authentication
4. Regularly update dependencies to patch security vulnerabilities

## 🔄 Updating the Application

To update the application:

1. Pull the latest changes from the repository
2. Run the setup script to update dependencies:
   ```bash
   ./setup.sh
   ```
3. Restart the application:
   ```bash
   ./run_app.sh
   ```

## 📞 Support

For issues not covered in this guide, please:

1. Check the application logs for error messages
2. Verify all environment variables are correctly set
3. Ensure all dependencies are properly installed
4. Confirm the database is properly initialized