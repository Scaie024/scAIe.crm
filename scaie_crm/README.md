# SCAIE - Sistema Agente Conversacional para Ventas con IA

<p align="center">
  <img src="docs/assets/scaie-logo.png" alt="SCAIE Logo" width="200"/>
</p>

SCAIE (Sistema Conversacional con Agente Inteligente Empresarial) es una plataforma avanzada de agentes conversacionales basada en inteligencia artificial que ayuda a las empresas a automatizar ventas, mejorar la atención al cliente y optimizar procesos mediante la automatización inteligente.

## Características Principales

### 🤖 Agente Conversacional Inteligente Especializado en Ventas de Workshops

El agente de SCAIE está especialmente entrenado para vender el workshop **"Sé más eficiente con IA"**, una solución práctica para que los equipos aprendan a usar inteligencia artificial en sus procesos diarios.

**Capacidades del Agente:**
- **Ventas Consultivas**: Técnicas avanzadas de descubrimiento, manejo de objeciones y cierre
- **Personalización**: Adaptación de mensajes según el perfil del cliente
- **Contexto**: Mantenimiento de conversaciones coherentes a través de múltiples interacciones
- **Multi-Canal**: Funciona en WhatsApp, Facebook Messenger, Web Chat y Telegram

### 📊 Panel de Administración Completo

- Dashboard con KPIs de ventas y métricas de agentes
- Gestión de contactos con niveles de interés (Nuevo, Contactado, Interesado, Confirmado, No Interesado)
- Visualización de conversaciones en tiempo real
- Gestión de tareas y seguimiento de leads
- Importación/Exportación de datos (CSV, JSON)

### 🔧 Tecnología de Vanguardia

- Backend en Python/FastAPI con SQLite
- Frontend en Vue 3 con Vite y TailwindCSS
- Integración con Qwen (Aliyun Dashscope) para procesamiento de lenguaje natural
- Arquitectura modular y escalable

## Workshop "Sé más eficiente con IA"

### ¿De qué trata?

Un workshop intensivo diseñado para equipos que quieren empezar a usar inteligencia artificial en su trabajo diario. A través de ejercicios prácticos, casos reales y herramientas específicas, los participantes aprenden a automatizar tareas, analizar información y generar contenido con IA, sin necesidad de conocimientos técnicos previos.

### Resultados Esperados

- Al menos 3 herramientas de IA activas y funcionando
- Un proceso de trabajo automatizado
- Plantillas y prompts personalizados para el equipo
- Plan de implementación de IA en la organización

### Modalidades

- **Básico** ($1,499 MXN): 2 horas, online en vivo, hasta 10 personas
- **Profesional** ($2,999 MXN): 4 horas, online o presencial, hasta 20 personas
- **Empresarial** (Precio personalizado): Implementación completa con múltiples sesiones

## Requisitos del Sistema

- Python 3.8+
- Node.js 14+
- npm 6+
- SQLite (incluido) o MySQL

## Instalación y Configuración

### Método 1: Ejecución Directa (Recomendado para desarrollo)

1. Clonar el repositorio:
```bash
git clone https://github.com/Scaie024/scAIe.crm.git
cd scAIe.crm
```

2. Ejecutar el script de configuración:
```bash
chmod +x setup.sh
./setup.sh
```

3. Configurar las variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales de API
```

4. Ejecutar la aplicación:
```bash
chmod +x run_app.sh
./run_app.sh
```

### Método 2: Ejecución Completa (Recomendado para producción)

```bash
chmod +x run_complete.sh
./run_complete.sh
```

Este script realiza todas las tareas necesarias:
- Configuración del entorno virtual
- Instalación de dependencias backend y frontend
- Construcción del frontend
- Inicio del servidor backend en el puerto 8003

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

## Uso

Una vez iniciado el servidor:

1. Accede a la interfaz web: http://localhost:8003
2. Usa la sección de chat para probar el agente
3. Explora el dashboard para ver métricas y contactos
4. Configura integraciones con WhatsApp/Facebook según necesites

## Endpoints de la API

- Documentación de la API: http://localhost:8003/docs
- Health check: http://localhost:8003/health
- Chat endpoint: http://localhost:8003/api/chat/
- Endpoint del agente omnipotente: http://localhost:8003/api/omnipotent-agent/

## Arquitectura del Sistema

```
scaie_crm/
├── backend/
│   ├── src/scaie/
│   │   ├── app/
│   │   │   ├── api/          # Endpoints de la API
│   │   │   ├── core/         # Configuración del núcleo
│   │   │   ├── models/       # Modelos de datos
│   │   │   ├── schemas/      # Esquemas de Pydantic
│   │   │   ├── services/     # Servicios de negocio
│   │   │   └── main.py       # Punto de entrada de la aplicación
│   │   └── static/           # Archivos estáticos (frontend compilado)
│   └── requirements.txt      # Dependencias de Python
├── frontend/
│   ├── src/
│   │   ├── assets/           # Recursos estáticos
│   │   ├── components/       # Componentes de Vue
│   │   ├── layouts/          # Diseños de página
│   │   ├── pages/            # Páginas de la aplicación
│   │   ├── router/           # Configuración de rutas
│   │   ├── services/         # Servicios de API
│   │   ├── stores/           # Stores de Pinia
│   │   └── utils/            # Utilidades
│   └── package.json          # Dependencias de Node.js
├── docs/                     # Documentación
├── scripts/                  # Scripts de utilidad
├── setup.sh                  # Script de configuración
├── run_app.sh                # Script de ejecución
└── run_complete.sh           # Script de ejecución completa
```

## Agentes y Funcionalidades

### Agente Especializado en Ventas del Workshop

El agente está entrenado específicamente para:
1. **Descubrir Necesidades**: Hacer preguntas abiertas para entender los desafíos del cliente
2. **Posicionar Valor**: Conectar los problemas del cliente con soluciones de IA
3. **Manejar Objeciones**: Responder con empatía a preocupaciones comunes
4. **Cerrar Ventas**: Guiar al cliente hacia agendar una sesión o solicitar información

### Integraciones

- WhatsApp Business API
- Facebook Messenger
- Telegram Bot
- Web Chat

## Desarrollo

### Estructura del Backend

El backend está construido con FastAPI y sigue una arquitectura limpia:
- **API Endpoints**: Rutas REST bien definidas
- **Modelos**: SQLAlchemy ORM para interacción con la base de datos
- **Servicios**: Lógica de negocio encapsulada
- **Esquemas**: Validación de datos con Pydantic

### Estructura del Frontend

El frontend utiliza Vue 3 con Composition API:
- **Componentes Reutilizables**: Diseño modular
- **Estado Global**: Gestión con Pinia
- **Enrutamiento**: Vue Router para navegación
- **Estilos**: TailwindCSS para diseño responsivo

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

## Contribución

1. Haz un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Realiza tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Haz push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Para más información, visita [www.scaie.com.mx](https://www.scaie.com.mx) o contacta con el equipo de desarrollo.

## Estado del Proyecto

Versión actual: v1.0.0 - Producción

El sistema está listo para ser usado en entornos de producción con todas las funcionalidades implementadas y probadas.

## 📞 Support

For support, please open an issue on the GitHub repository or contact the development team.