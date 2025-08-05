# Project Structure and Organization

## Overview

This document describes the organization of the scAIe CRM project, a FastAPI + Vue.js application with AI agent capabilities for automated sales conversations.

## Directory Structure

```
scaie_crm/
├── backend/                 # FastAPI backend application
│   ├── src/                 # Main source code
│   │   └── scaie/           # Main application package
│   │       ├── app/         # Core application code
│   │       │   ├── api/     # API endpoints
│   │       │   ├── core/    # Core configurations
│   │       │   ├── models/  # Database models
│   │       │   ├── schemas/ # Pydantic schemas
│   │       │   ├── services/ # Business logic services
│   │       │   └── static/  # Static files (frontend build)
│   │       ├── init_db.py   # Database initialization script
│   │       └── migrate_contacts.py # Contact migration utility
│   ├── tests/               # Backend tests
│   └── test_db.py           # Database testing utilities
├── config/                  # Configuration files
├── docs/                    # Documentation
│   ├── development/         # Development documentation
│   ├── deployment/          # Deployment guides
│   ├── api/                 # API documentation
│   └── user_guide/          # User guides
├── frontend/                # Vue.js frontend application
│   ├── src/                 # Frontend source code
│   │   ├── components/      # Vue components
│   │   ├── pages/           # Page components
│   │   ├── router/          # Vue Router configuration
│   │   ├── services/        # API service clients
│   │   ├── utils/           # Utility functions
│   │   ├── App.vue          # Root Vue component
│   │   └── main.js          # Frontend entry point
│   └── [config files]       # Build and package configuration
├── scripts/                 # Utility and deployment scripts
└── README.md                # Main project documentation
```

## Backend Structure

The backend is built with FastAPI and follows a modular architecture:

### Core Components

1. **API Endpoints** (`app/api/endpoints/`)
   - Individual endpoint files for different features
   - Each file contains routes related to a specific domain

2. **Models** (`app/models/`)
   - Database models using SQLAlchemy ORM
   - Define the data structure and relationships

3. **Schemas** (`app/schemas/`)
   - Pydantic models for request/response validation
   - Data serialization and deserialization

4. **Services** (`app/services/`)
   - Business logic implementation
   - Integration with external services (AI, Telegram, WhatsApp)

5. **Core** (`app/core/`)
   - Database configuration
   - Security and application core settings

### Key Services

- **LLM Service**: Integration with Qwen AI models
- **Omnipotent Agent**: Main AI agent implementation
- **Telegram Service**: Integration with Telegram Bot API
- **WhatsApp Service**: Integration with Facebook Graph API
- **Contact Service**: Contact management operations

## Frontend Structure

The frontend is built with Vue.js 3 and follows a component-based architecture:

### Components Organization

1. **Feature-based Components** (`src/components/`)
   - Components organized by feature (agent, chat, contacts, dashboard)
   - Shared components for common UI elements

2. **Pages** (`src/pages/`)
   - Top-level page components that compose features
   - Route-linked views

3. **Services** (`src/services/`)
   - API client implementations
   - Service functions for backend communication

4. **Utilities** (`src/utils/`)
   - Composable functions for Vue 3 Composition API
   - Helper functions and utilities

## Scripts and Configuration

### Deployment Scripts (`scripts/`)

- `build_and_run.sh`: Build and run the complete application
- `deploy.sh`: Deployment automation
- `run_with_ngrok.sh`: Run with ngrok for external access
- Service start scripts for different environments

### Configuration Files (`config/`)

- Docker configuration for containerization
- Nginx configuration for reverse proxy
- Production deployment configurations

## Documentation

Documentation is organized in the `docs/` directory:
- Development guides and technical documentation
- Deployment instructions and configuration guides
- API documentation (to be expanded)
- User guides (to be expanded)

## Best Practices Implemented

1. **Separation of Concerns**: Clear separation between API, business logic, and data layers
2. **Modular Design**: Feature-based organization for both frontend and backend
3. **Scalable Architecture**: Designed to support multiple messaging platforms
4. **AI Integration**: Built-in LLM capabilities with configurable agents
5. **Database Management**: SQLAlchemy ORM with migration support
6. **Testing Ready**: Structured to support unit and integration tests